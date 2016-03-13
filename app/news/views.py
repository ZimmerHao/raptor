# -*- coding: UTF-8 -*-

import hashlib
from datetime import datetime
from urlparse import urlparse

from flask import request
from flask_restful import Resource
from thrift.packages.hbase.ttypes import TGet, TDelete, TPut, TColumnValue

from app import db, hbase_client
from app.news import api
from app.news.models import NewsSource, OrgNewsMap, OrgNewsCategory, NewsCategory
from app.common.error import ApiError
from app.common.constants import NEWS_SOURCE_PER_PAGE,DEFAULT_RANK, DEFAULT_HBASE_DATE_FORMAT, \
    DEFAULT_HBASE_NEWS_DATE_KEY_FORMAT, DEFAULT_DATA_LOADER, \
    NEWS_PER_PAGE,  NEWS_CATEGORY_SERACH_COUNT, NEWS_SOURCE_SEARCH_COUNT


class NewsMixin(object):
    ORG_KEY_LEN = 11
    NEWS_DATE_LEN = 8
    SOURCE_KEY_LEN = 9
    SEQ_LEN = 4
    HASH_KEY_LEN = 32

    def get_by_row_key(self, row_key):
        t_result = hbase_client.get('org_news', TGet(row=row_key))
        news_item = dict()
        for item in t_result.columnValues:
            news_item[item.qualifier] = item.value
        news_item['row_key'] = t_result.row
        category_models = OrgNewsCategory.query.filter(OrgNewsCategory.row_key == row_key)
        categorie_list = []
        for item in category_models:
            category_item = dict()
            category_item['id'] = item.news_category_key
            category_item['name'] = item.news_category.news_category_name
            categorie_list.append(category_item)
        news_item['categories'] = categorie_list
        return news_item

    def get_seq(self, org_key, news_date, source_key):
        seq_values = OrgNewsMap.query.filter_by(org_key=org_key, news_date=news_date, source_key=source_key)\
            .order_by(OrgNewsMap.seq.desc()).values('seq')
        seq_list = [x[0] for x in seq_values]
        if seq_list:
            return seq_list[0]
        else:
            return 0

    def _format_org_key(self, org_key):
        return str(org_key).zfill(self.__class__.ORG_KEY_LEN)

    def _format_source_key(self, source_key):
        return str(source_key).zfill(self.__class__.SOURCE_KEY_LEN)

    def _format_hash_key(self, org_key):
        m = hashlib.md5()
        m.update(str(org_key))
        return m.hexdigest()

    def _format_news_date(self, news_date):
        news_date = news_date.strftime(DEFAULT_HBASE_NEWS_DATE_KEY_FORMAT)
        return news_date

    def _format_seq_key(self, seq):
        return str(seq).zfill(self.__class__.SEQ_LEN)

    def format_row_key(self, org_key='', news_date=None, source_key='', seq=''):
        org_key_part = self._format_org_key(org_key)
        source_key_part = self._format_source_key(source_key)
        hash_key_part = self._format_hash_key(org_key)
        news_date_part = self._format_news_date(news_date)
        seq_part = self._format_seq_key(seq)

        return '{0}{1}{2}{3}{4}'.format(hash_key_part, org_key_part, news_date_part, source_key_part, seq_part)


class NewsHandler(Resource, NewsMixin):
    def get(self):
        org_key = request.args.get('org_key', '')
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        source_key = request.args.get('source_key', '')
        page = request.args.get('page', 1)

        if not org_key:
            return ApiError(40001).to_json()

        try:
            page = int(page)
        except:
            return ApiError(40001).to_json()

        map_models = OrgNewsMap.query.filter(OrgNewsMap.org_key == org_key)
        if source_key:
            map_models = map_models.filter(OrgNewsMap.source_key == source_key)
        if start_date and end_date:
            map_models = map_models.filter(OrgNewsMap.news_date.between(start_date, end_date))
        map_models = map_models.paginate(page, NEWS_PER_PAGE, False)

        news_list = [super(NewsHandler, self).get_by_row_key(x.row_key) for x in map_models.items]
        data = dict()
        data['news'] = news_list
        if map_models.has_next:
            data['next_num'] = map_models.next_num
        if map_models.has_prev:
            data['prev_num'] = map_models.prev_num
        data['total'] = map_models.total
        return data

    def delete(self, nid):
        org_news_map_model = OrgNewsMap.query.get(nid)
        if not org_news_map_model:
            return ApiError(40001).to_json()
        row_key = org_news_map_model.row_key
        hbase_client.delete('org_news', TDelete(row=row_key))
        db.session.delete(org_news_map_model)
        db.session.commit()
        return {'nid': nid}

    def post(self):
        org_key = request.form.get('org_key', '')
        source = request.form.get('source', '')
        news_title = request.form.get('news_title', '')
        news_link = request.form.get('news_link', '')
        news_date_str = request.form.get('news_date', '')
        news_summary = request.form.get('news_summary', '')

        if not (org_key and source and news_title and news_link \
                and news_date_str and news_summary):
            return ApiError(40001).to_json()

        try:
            org_key = int(org_key)
        except:
            return ApiError(40001).to_json()

        news_link = news_link.strip()
        source_site = 'http://{0}'.format(urlparse(news_link).netloc)
        source_model = NewsSource.query.filter_by(news_source_name=source).first()
        if not source_model:
            source_model = NewsSource()
            source_model.news_source_name = source
            source_model.official_web_site = source_site
            db.session.add(source_model)
            db.session.commit()

        org_key_col_val = TColumnValue('cf', 'org_key', str(org_key))
        source_key_col_val = TColumnValue('cf', 'source_key', str(source_model.news_source_key))
        news_source_col_val = TColumnValue('cf', 'news_source', str(source_model.news_source_name))
        news_title_col_val = TColumnValue('cf', 'news_title', str(news_title))
        news_link_col_val = TColumnValue('cf', 'news_link', str(news_link))
        news_date_col_val = TColumnValue('cf', 'news_date', str(news_date_str))
        news_summary_col_val = TColumnValue('cf', 'news_summary', str(news_summary))

        news_date = datetime.strptime(news_date_str, DEFAULT_HBASE_DATE_FORMAT)
        seq = super(NewsHandler, self).get_seq(org_key, news_date.date(), source_model.news_source_key)
        seq_col_val = TColumnValue('cf', 'seq', str(seq+1))

        column_values = [org_key_col_val, source_key_col_val, news_source_col_val, news_title_col_val,
                         news_link_col_val, news_date_col_val, news_summary_col_val, seq_col_val]

        row_key = super(NewsHandler, self).format_row_key(org_key=org_key,
                                                          news_date=news_date,
                                                          source_key=source_model.news_source_key,
                                                          seq=seq+1)

        t_put = TPut(row_key, column_values)
        try:
            hbase_client.put('org_news', t_put)
        except:
            return ApiError(40103).to_json()

        news_map = OrgNewsMap(row_key=row_key,
                              org_key=org_key,
                              source_key=source_model.news_source_key,
                              news_date=news_date.date(),
                              seq=seq+1,
                              data_loader=DEFAULT_DATA_LOADER)
        db.session.add(news_map)
        db.session.commit()

        return {
            'org_key': org_key,
            'source_key': source_model.news_source_key,
            'news_source': source_model.news_source_name,
            'news_title': news_title,
            'news_link': news_link,
            'news_date': news_date_str,
            'news_summary': news_summary
        }


class NewsSourceHandler(Resource):
    def get(self):
        source = request.args.get('q', '')
        page = request.args.get('page', 1)
        try:
            page = int(page)
        except:
            return ApiError(40001).to_json()

        news_source_models = NewsSource.query
        if source:
            news_source_models = news_source_models.filter(NewsSource.news_source_name.like('%'+source+'%'))
        news_source_models = news_source_models.paginate(page, NEWS_SOURCE_PER_PAGE, False)
        source_list = []
        for item in news_source_models.items:
            source_item = dict()
            source_item['id'] = item.news_source_key
            source_item['name'] = item.news_source_name
            source_item['website'] = item.official_web_site
            source_item['agent'] = item.news_agent_name
            source_item['rank'] = item.rank
            source_list.append(source_item)

        data = dict()
        data['new_sources'] = source_list
        if news_source_models.has_next:
            data['next_num'] = news_source_models.next_num
        if news_source_models.has_prev:
            data['prev_num'] = news_source_models.prev_num
        data['total'] = news_source_models.total
        return data

    def delete(self, id):
        news_source_model = NewsSource.query.get(id)
        if not news_source_model:
            return ApiError(40001).to_json()
        db.session.delete(news_source_model)
        db.session.commit()

        return {
            'id': news_source_model.news_source_key,
            'name': news_source_model.news_source_name,
            'website': news_source_model.official_web_site,
            'agent': news_source_model.news_agent_name,
            'rank': news_source_model.rank
        }

    def put(self, id):
        name = request.form.get('name', '')
        website = request.form.get('website', '')
        agent = request.form.get('agent', '')
        rank = request.form.get('rank', '')

        if not name:
            return ApiError(40001).to_json()
        if not rank:
            rank = DEFAULT_RANK

        news_source_model = NewsSource.query.get(id)
        if not news_source_model:
            return ApiError(40101)

        news_source_model.news_source_name = name
        news_source_model.official_web_site = website
        news_source_model.news_agent_name = agent
        news_source_model.rank = int(rank)
        db.session.commit()

        return {
            'id': news_source_model.news_source_key,
            'name': news_source_model.news_source_name,
            'website': news_source_model.official_web_site,
            'agent': news_source_model.news_agent_name,
            'rank': news_source_model.rank
        }

    def post(self):
        name = request.form.get('name', '')
        website = request.form.get('website', '')
        agent = request.form.get('agent', '')
        rank = request.form.get('rank', '')

        if not name:
            return ApiError(40001).to_json()
        if not rank:
            rank = DEFAULT_RANK

        news_source_model = NewsSource.query.filter(NewsSource.news_source_name == name).first()
        if news_source_model:
            return ApiError(40104).to_json()

        source = NewsSource(
            news_source_name=name,
            official_web_site=website,
            news_agent_name=agent,
            rank=int(rank)
        )
        db.session.add(source)
        db.session.commit()

        return {
            'id': source.news_source_key,
            'name': source.news_source_name,
            'website': source.official_web_site,
            'agent': source.news_agent_name,
            'rank': source.rank
        }


class NewsSourceSearchHandler(Resource):
    def get(self):
        source = request.args.get('q', '')
        news_source_models = NewsSource.query.filter(NewsSource.news_source_name.like('%'+source+'%')).\
            limit(NEWS_SOURCE_SEARCH_COUNT)
        source_list = []
        for item in news_source_models:
            source_item = dict()
            source_item['id'] = item.news_source_key
            source_item['name'] = item.news_source_name
            source_list.append(source_item)

        data = dict()
        data['new_sources'] = source_list
        data['total'] = len(source_list)
        return data


class NewsCategoryHandler(Resource):
    def get(self):
        news_category_models = NewsCategory.query.order_by(NewsCategory.news_category_key)[2:]
        news_category_list = []
        for item in news_category_models:
            category_item = dict()
            category_item['id'] = item.news_category_key
            category_item['name'] = item.news_category_name
            news_category_list.append(category_item)

        data = dict()
        data['categories'] = news_category_list
        data['total'] = len(news_category_list)
        return data


class OrgNewsCategoryHandler(Resource):
    def get(self, nid):
        category_models = OrgNewsCategory.query.filter(OrgNewsCategory.org_news_map_key == nid)
        categorie_list = []
        for item in category_models:
            category_item = dict()
            category_item['id'] = item.news_category_key
            category_item['name'] = item.news_category.news_category_name
            categorie_list.append(category_item)

        data = dict()
        data['categories'] = categorie_list
        data['total'] = len(categorie_list)
        return data

    def post(self, nid):
        category = request.form.get('category', '')
        if not category:
            return ApiError(40001).to_json()

        org_news_cats = OrgNewsCategory.query.filter(OrgNewsCategory.org_news_map_key == nid).values('news_category_key')
        org_news_cats = [x[0] for x in org_news_cats]
        if int(category) in org_news_cats:
            return ApiError(40001).to_json()

        org_news_cat_model = OrgNewsCategory(nid, int(category))
        db.session.add(org_news_cat_model)
        db.session.commit()

        return {
            'nid': nid,
            'category': int(category)
        }

    def delete(self, nid):
        category = request.args.get('category', '')
        if not category:
            return ApiError(40001).to_json()
        OrgNewsCategory.query.filter(OrgNewsCategory.org_news_map_key == nid,
                                     OrgNewsCategory.news_category_key == int(category)).delete()
        db.session.commit()

        return {
            'nid': nid,
            'category': int(category)
        }


class NewsCategorySearchHandler(Resource):
    def get(self):
        category_name = request.args.get('q', '')
        news_category_models = NewsCategory.query.filter(NewsCategory.news_category_name.like('%'+category_name+'%')).\
            limit(NEWS_CATEGORY_SERACH_COUNT)
        news_category_list = []
        for item in news_category_models:
            category_item = dict()
            category_item['id'] = item.news_category_key
            category_item['name'] = item.news_category_name
            news_category_list.append(category_item)

        data = dict()
        data['categories'] = news_category_list
        data['total'] = len(news_category_list)
        return data


api.add_resource(NewsHandler, '/news',
                              '/news/<int:nid>', endpoint='news')

api.add_resource(NewsSourceHandler, '/news_sources',
                                    '/news_sources/<int:id>', endpoint='news_source')
api.add_resource(NewsSourceSearchHandler, '/news_sources/search', endpoint='news_source_search')

api.add_resource(NewsCategoryHandler, '/news_categories', endpoint='news_category')
api.add_resource(OrgNewsCategoryHandler, '/news/<int:nid>/categories', endpoint='org_news_category')
api.add_resource(NewsCategorySearchHandler, '/news_categories/search', endpoint='org_news_category_search')


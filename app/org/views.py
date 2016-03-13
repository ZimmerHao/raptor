# -*- coding: UTF-8 -*-

from flask import request
from flask_restful import Resource

from app import db
from app.org import api
from app.common.models import Organization, IndustryClass
from app.org.models import OrgCommMediaFact, Tag, OrgTagFact, OrgKeyword, OrgWatched
from app.common.constants import ORG_PER_PAGE, ORG_SERACH_COUNT, COMM_MEDIA_TYPE, TAG_SERACH_COUNT, \
    ORG_KEYWORD_PER_PAGE, DEFAULT_RANK, ORG_WATCHED_SERACH_COUNT, ORG_WATCHED_PER_PAGE
from app.common.error import ApiError


class OrgHandler(Resource):
    def get(self, oid):
        org_model = Organization.query.get(oid)
        if not org_model:
            return ApiError(40201).to_json()

        wechat = OrgCommMediaFact.query.filter(OrgCommMediaFact.org_key == oid,
                                               OrgCommMediaFact.comm_media_key == COMM_MEDIA_TYPE.WECHAT).first()
        return {
            'id': org_model.org_key,
            'name': org_model.org_name,
            'desc': org_model.org_desc or '',
            'website': org_model.org_website or '',
            'phone': org_model.main_phone_num or '',
            'industry_key': org_model.industry_class_key or '',
            'industry': org_model.industry_class.industry_class_name or '',
            'status': org_model.org_status.org_status or '',
            'wechat': wechat.comm_media_number if wechat else ''
        }

    def put(self, oid):
        industry = request.form.get('industry', '')
        website = request.form.get('website', '')
        phone = request.form.get('phone', '')
        wechat = request.form.get('wechat', '')

        org_model = Organization.query.get(oid)
        if not org_model:
            return ApiError(40201)

        if wechat:
            wechat_model = OrgCommMediaFact.query.\
                filter(OrgCommMediaFact.org_key == oid,
                       OrgCommMediaFact.comm_media_key == COMM_MEDIA_TYPE.WECHAT).first()
            if wechat_model:
                wechat_model.comm_media_number = wechat
            else:
                wechat_model = OrgCommMediaFact(
                    org_key=oid,
                    comm_media_key=COMM_MEDIA_TYPE.WECHAT,
                    comm_media_number=wechat
                )
                db.session.add(wechat_model)

        if industry:
            org_model.industry_class_key = int(industry)
        if website:
            org_model.org_website = website
        if phone:
            org_model.main_phone_num = phone
        db.session.commit()

        return {
            'industry': int(industry),
            'website': website,
            'phone': phone,
            'wechat': wechat
        }


class OrgListHandler(Resource):
    def get(self):
        page = request.args.get('page', 1)
        try:
            page = int(page)
        except:
            return ApiError(40001).to_json()

        org_models = Organization.query.paginate(page, ORG_PER_PAGE, False)
        org_list = []
        for item in org_models.items:
            org_item = dict()
            org_item['id'] = item.org_key
            org_item['name'] = item.org_name
            org_item['website'] = item.org_website or ''
            org_item['desc'] = item.org_desc or ''
            org_item['phone'] = item.main_phone_num or ''
            org_item['industry'] = item.industry_class.industry_class_name
            org_item['industry_key'] = item.industry_class_key or ''
            org_item['status'] = item.org_status.org_status or ''

            wechat_model = OrgCommMediaFact.query.filter(OrgCommMediaFact.org_key == item.org_key,
                                                     OrgCommMediaFact.comm_media_key == COMM_MEDIA_TYPE.WECHAT).first()
            org_item['wechat'] = wechat_model.comm_media_number if wechat_model else ''
            org_list.append(org_item)

        data = dict()
        data['companies'] = org_list
        if org_models.has_next:
            data['next_num'] = org_models.next_num
        if org_models.has_prev:
            data['prev_num'] = org_models.prev_num
        data['total'] = org_models.total
        return data


class OrgSearchHandler(Resource):
    def get(self):
        org_name = request.args.get('q', '')
        org_models = Organization.query.filter(Organization.org_name.like('%'+org_name+'%')).limit(ORG_SERACH_COUNT)
        org_list = []
        for item in org_models:
            org_item = dict()
            org_item['id'] = item.org_key
            org_item['org_name'] = item.org_name
            org_list.append(org_item)

        data = dict()
        data['orgs'] = org_list
        data['total'] = len(org_list)
        return data


class IndustryClassHandler(Resource):
    def get(self):
        industry_class_name = request.args.get('q', '')
        industry_class_models = IndustryClass.query.\
            filter(IndustryClass.industry_class_name.like('%'+industry_class_name+'%'))
        industry_class_list = []
        for item in industry_class_models:
            industry_class_item = dict()
            industry_class_item['id'] = item.industry_class_key
            industry_class_item['industry_name'] = item.industry_class_name
            industry_class_list.append(industry_class_item)

        data = dict()
        data['industries'] = industry_class_list
        data['total'] = len(industry_class_list)
        return data


class OrgTagHandler(Resource):
    def get(self, oid):
        org_tag_fact_models = OrgTagFact.query.filter(OrgTagFact.org_key == oid)
        tag_list = []
        for item in org_tag_fact_models:
            tag_item = dict()
            tag_item['id'] = item.tag_key
            tag_item['tag_name'] = item.tag.tag_name
            tag_item['tag_category'] = item.tag.tag_category or ''
            tag_list.append(tag_item)
        data = dict()
        data['tags'] = tag_list
        data['total'] = len(tag_list)
        return data

    def post(self, oid):
        tag_id = request.form.get('tag_id', '')
        if not tag_id:
            return ApiError(40001).to_json()
        org_tag_model = OrgTagFact(id, int(tag_id))
        db.session.add(org_tag_model)
        db.session.commit()

        return {'tag_id': tag_id}

    def delete(self, oid, tid):
        OrgTagFact.query.filter(OrgTagFact.org_key == oid, OrgTagFact.tag_key == int(tid)).delete()
        db.session.commit()
        return {'tag_id': int(tid)}


class TagSearchHandler(Resource):
    def get(self):
        tag_name = request.args.get('q', '')
        tag_models = Tag.query.filter(Tag.tag_name.like('%'+tag_name+'%')).limit(TAG_SERACH_COUNT)
        tag_list = []
        for item in tag_models:
            tag_item = dict()
            tag_item['id'] = item.tag_key
            tag_item['tag_name'] = item.tag_name
            tag_item['tag_category'] = item.tag_category
            tag_list.append(tag_item)

        data = dict()
        data['tags'] = tag_list
        data['total'] = len(tag_list)
        return data


class TagHandler(Resource):
    def get(self):
        tag_models = Tag.query.all()
        tag_list = []
        for item in tag_models:
            tag_item = dict()
            tag_item['id'] = item.tag_key
            tag_item['tag_name'] = item.tag_name
            tag_item['tag_category'] = item.tag_category or ''
            tag_list.append(tag_item)

        data = dict()
        data['tags'] = tag_list
        data['total'] = len(tag_list)
        return data

    def post(self):
        tag_name = request.form.get('tag_name', '')
        tag_category = request.form.get('tag_category', '')
        if not tag_name:
            return ApiError(40001).to_json()

        tag_model = Tag(tag_name=tag_name)
        if tag_category:
            tag_model.tag_category = tag_category

        db.session.add(tag_model)
        db.session.commit()
        return {'id': tag_model.tag_key, 'tag_name': tag_model.tag_name, 'tag_category':tag_category}


class OrgKeywordHandler(Resource):
    def get(self):
        org_key = request.args.get('org_key', '')
        page = request.args.get('page', 1)
        if not org_key:
            return ApiError(40001).to_json()
        try:
            page = int(page)
        except:
            return ApiError(40001).to_json()
        org_keyword_models = OrgKeyword.query.filter_by(org_key=int(org_key)).paginate(page, ORG_KEYWORD_PER_PAGE, False)
        keyword_list = []
        for item in org_keyword_models.items:
            keyword_item = dict()
            keyword_item['id'] = item.org_keyword_key
            keyword_item['org_key'] = item.org_key
            keyword_item['keyword'] = item.keyword
            keyword_item['rank'] = item.rank
            keyword_list.append(keyword_item)

        data = dict()
        data['keywords'] = keyword_list
        if org_keyword_models.has_next:
            data['next_num'] = org_keyword_models.next_num
        if org_keyword_models.has_prev:
            data['prev_num'] = org_keyword_models.prev_num
        data['total'] = org_keyword_models.total
        return data

    def delete(self, kid):
        org_keyword_model = OrgKeyword.query.get(kid)
        if not org_keyword_model:
            return ApiError(40102).to_json()
        db.session.delete(org_keyword_model)
        db.session.commit()

        return {
            'id': org_keyword_model.org_keyword_key,
            'org_key': org_keyword_model.org_key,
            'keyword': org_keyword_model.keyword,
            'rank': org_keyword_model.rank
        }

    def put(self, kid):
        org_key = request.form.get('org_key', '')
        keyword = request.form.get('keyword', '')
        rank = request.form.get('rank', '')

        if not (org_key and keyword):
            return ApiError(40001).to_json()

        org_keyword_model = OrgKeyword.query.get(kid)
        if not org_keyword_model:
            return ApiError(40102).to_json()
        if not rank:
            rank = DEFAULT_RANK

        org_keyword_model.org_key = int(org_key)
        org_keyword_model.keyword = keyword
        org_keyword_model.rank = int(rank)
        db.session.commit()

        return {
            'id': org_keyword_model.org_keyword_key,
            'org_key': org_keyword_model.org_key,
            'keyword': org_keyword_model.keyword,
            'rank': org_keyword_model.rank
        }

    def post(self):
        org_key = request.form.get('org_key', '')
        keyword = request.form.get('keyword', '')
        rank = request.form.get('rank', '')

        if not (org_key and keyword):
            return ApiError(40001).to_json()
        if not rank:
            rank = DEFAULT_RANK

        keyword = OrgKeyword(
            org_key=int(org_key),
            keyword=keyword,
            rank=int(rank)
        )
        db.session.add(keyword)
        db.session.commit()

        return {
            'id': keyword.org_keyword_key,
            'keyword': keyword.keyword,
            'org_key': keyword.org_key,
            'rank': keyword.rank
        }


class OrgWatchedHandler(Resource):
    def get(self):
        page = request.args.get('page', 1)
        try:
            page = int(page)
        except:
            return ApiError(40001).to_json()
        org_watched_models = OrgWatched.query.order_by('org_watched_key').paginate(page, ORG_WATCHED_PER_PAGE, False)
        org_watched_list = []
        for item in org_watched_models.items:
            org_item = dict()
            org_item['id'] = item.org_watched_key
            org_item['org_key'] = item.org.org_key
            org_item['org_name'] = item.org.org_name
            keywords = OrgKeyword.query.filter_by(org_key=item.org.org_key).values('keyword')
            org_item['keywords'] = [x[0] for x in keywords]
            org_watched_list.append(org_item)

        data = dict()
        data['watched_list'] = org_watched_list
        if org_watched_models.has_next:
            data['next_num'] = org_watched_models.next_num
        if org_watched_models.has_prev:
            data['prev_num'] = org_watched_models.prev_num
        data['total'] = org_watched_models.total
        return data


class OrgWatchedSearchHandler(Resource):
    def get(self):
        org_name = request.args.get('q', '')
        org_watched_models = Organization.query.join(OrgWatched).\
            filter(Organization.org_name.like('%'+org_name+'%')).order_by('org_key').limit(ORG_WATCHED_SERACH_COUNT)
        org_watched_list = []
        for item in org_watched_models:
            org_item = dict()
            org_item['id'] = item.org_key
            org_item['org_name'] = item.org_name
            org_watched_list.append(org_item)

        data = dict()
        data['watched_list'] = org_watched_list
        data['total'] = len(org_watched_list)
        return data


api.add_resource(OrgListHandler, '/orgs', endpoint='org_list')
api.add_resource(OrgHandler, '/orgs/<int:oid>', endpoint='org')
api.add_resource(OrgSearchHandler, '/orgs/search', endpoint='org_search')

api.add_resource(IndustryClassHandler, '/industries/search', endpoint='industry_search')

api.add_resource(OrgTagHandler, '/orgs/<int:oid>/tags',
                                '/orgs/<int:oid>/tags/<int:tid>', endpoint='org_tag')
api.add_resource(TagSearchHandler, '/tags/search', endpoint='tag_search')
api.add_resource(TagHandler, '/tags', endpoint='tags')

api.add_resource(OrgKeywordHandler, '/org_keywords'
                                    '/org_keywords/<int:kid>', endpoint='org_keyword')

api.add_resource(OrgWatchedHandler, '/watched_orgs', endpoint='org_watched')
api.add_resource(OrgWatchedSearchHandler, '/watched_orgs/search', endpoint='org_watched_search')




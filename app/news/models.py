# -*- coding: UTF-8 -*-

import datetime

from app import db
from app.common.models import Organization
from app.common.constants import DEFAULT_RANK, DEFAULT_DATA_LOADER

class NewsSource(db.Model):
    __table_args__ = {'schema': 'warehouse'}
    __tablename__ = 'news_source'

    news_source_key = db.Column(db.Integer, primary_key=True)
    news_source_name = db.Column(db.String(250), unique=True, nullable=False)
    official_web_site = db.Column(db.Text, nullable=True)
    news_agent_name = db.Column(db.String(250), nullable=True)
    rank = db.Column(db.Integer, default=-1)
    data_loaded_date = db.Column(db.DateTime, nullable=True)
    data_loader = db.Column(db.String(50), nullable=True)

    def __init__(self, news_source_name=None, official_web_site=None, news_agent_name=None,
                 rank=DEFAULT_RANK, data_loaded_date=None, data_loader=DEFAULT_DATA_LOADER):
        self.news_source_name = news_source_name
        self.official_web_site = official_web_site
        self.news_agent_name = news_agent_name
        self.rank = rank
        if not data_loaded_date:
            data_loaded_date = datetime.datetime.now()
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader

    def __repr__(self):
        return '<NewsSource %r>' % self.news_source_name


class OrgNewsMap(db.Model):
    __table_args__ = {'schema': 'xboard'}
    __tablename__ = 'org_news_map'

    org_news_map_key = db.Column(db.Integer, primary_key=True)
    row_key = db.Column(db.String(200), unique=True, nullable=False)
    org_key = db.Column(db.Integer, db.ForeignKey(Organization.org_key), nullable=False)
    source_key = db.Column(db.Integer, db.ForeignKey(NewsSource.news_source_key), nullable=False)
    news_date = db.Column(db.Date, nullable=False)
    seq = db.Column(db.Integer, nullable=False)
    data_loaded_date = db.Column(db.DateTime, nullable=True)
    data_loader = db.Column(db.String(50), nullable=True)

    org = db.relationship('Organization')
    source = db.relationship('NewsSource')

    def __init__(self, row_key=None, org_key=None, source_key=None, news_date=None, seq=None,
                 data_loaded_date=None, data_loader=DEFAULT_DATA_LOADER):
        self.row_key = row_key
        self.org_key = org_key
        self.source_key = source_key
        self.news_date = news_date
        self.seq=seq
        if not data_loaded_date:
            data_loaded_date = datetime.datetime.now()
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader


class NewsCategory(db.Model):
    __table_args__ = {'schema': 'warehouse'}
    __tablename__ = 'news_category'

    news_category_key = db.Column(db.Integer, primary_key=True)
    news_category_name = db.Column(db.String(50), nullable=False)
    news_category_desc = db.Column(db.Text)
    data_loaded_date = db.Column(db.DateTime, nullable=True)
    data_loader = db.Column(db.String(50), nullable=True)

    def __init__(self, news_category_name, news_category_desc, data_loaded_date, data_loader):
        self.news_category_name = news_category_name
        self.news_category_desc = news_category_desc
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader


class OrgNewsCategory(db.Model):
    __table_args__ = {'schema': 'xboard'}
    __tablename__ = 'org_news_category'

    org_news_category_key = db.Column(db.Integer, primary_key=True)
    org_news_map_key = db.Column(db.Integer, db.ForeignKey(OrgNewsMap.org_news_map_key))
    news_category_key = db.Column(db.Integer, db.ForeignKey(NewsCategory.news_category_key))
    data_loaded_date = db.Column(db.DateTime, nullable=True)
    data_loader = db.Column(db.String(50), nullable=True)

    news_category = db.relationship('NewsCategory')
    news = db.relationship('OrgNewsMap')

    def __init__(self, org_news_map_key, news_category_key, data_loaded_date=None, data_loader=DEFAULT_DATA_LOADER):
        self.org_news_map_key = org_news_map_key
        self.news_category_key = news_category_key
        if not data_loaded_date:
            data_loaded_date = datetime.datetime.now()
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader





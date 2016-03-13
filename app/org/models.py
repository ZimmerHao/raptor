# -*- coding: UTF-8 -*-

import datetime

from app import db
from app.common.models import Organization
from app.common.constants import DEFAULT_DATA_LOADER, COMM_MEDIA_STATUS, DATA_SOURCE_TYPE


class OrgCommMediaFact(db.Model):
    __table_args__ = {"schema": "warehouse"}
    __tablename__ = 'org_comm_media_fact'

    org_comm_media_fact_key = db.Column(db.Integer, primary_key=True)
    org_key = db.Column(db.Integer, db.ForeignKey(Organization.org_key), nullable=False)
    comm_media_key = db.Column(db.Integer, nullable=False)
    comm_media_status_key = db.Column(db.Integer, nullable=False)
    comm_media_number = db.Column(db.String(250))
    comm_media_alias = db.Column(db.Text)
    data_source_key = db.Column(db.Integer, nullable=False)
    data_loaded_date = db.Column(db.DateTime, nullable=False)
    data_loader = db.Column(db.String(50), nullable=False)

    org = db.relationship("Organization", backref=db.backref('comm_medias'))

    def __init__(self, org_key=None, comm_media_key=None, comm_media_status_key=COMM_MEDIA_STATUS.EFFECTIVE,
                 comm_media_number=None, comm_media_alias=None, data_source_key=DATA_SOURCE_TYPE.MANUAL,
                 data_loaded_date=None, data_loader=DEFAULT_DATA_LOADER):
        self.org_key = org_key
        self.comm_media_key = comm_media_key
        self.comm_media_status_key = comm_media_status_key
        self.comm_media_number = comm_media_number
        self.comm_media_alias = comm_media_alias
        self.data_source_key = data_source_key
        if not data_loaded_date:
            data_loaded_date = datetime.datetime.now()
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader


class Tag(db.Model):
    __table_args__ = {"schema": "warehouse"}
    __tablename__ = 'tag'

    tag_key = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(250), nullable=False)
    tag_category = db.Column(db.String(50))
    data_loaded_date = db.Column(db.DateTime, nullable=False)
    data_loader = db.Column(db.String(50), nullable=False)

    def __init__(self, tag_name=None, tag_category=None, data_loaded_date=None, data_loader=DEFAULT_DATA_LOADER):
        self.tag_name = tag_name
        self.tag_category = tag_category
        if not data_loaded_date:
            data_loaded_date = datetime.datetime.now()
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader


class OrgTagFact(db.Model):
    __table_args__ = {"schema": "warehouse"}
    __tablename__ = 'org_tag_fact'

    org_tag_fact_id = db.Column(db.Integer, primary_key=True)
    org_key = db.Column(db.Integer, db.ForeignKey(Organization.org_key), nullable=False)
    tag_key = db.Column(db.Integer, db.ForeignKey(Tag.tag_key), nullable=False)
    data_loaded_date = db.Column(db.DateTime, nullable=False)
    data_loader = db.Column(db.String(50), nullable=False)

    org = db.relationship("Organization")
    tag = db.relationship("Tag")

    def __init__(self, org_key=None, tag_key=None, data_loaded_date=None, data_loader=DEFAULT_DATA_LOADER):
        self.org_key = org_key
        self.tag_key = tag_key
        if not data_loaded_date:
            data_loaded_date = datetime.datetime.now()
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader


class OrgKeyword(db.Model):
    __table_args__ = {'schema': 'xboard'}
    __tablename__ = 'org_keyword'

    org_keyword_key = db.Column(db.Integer, primary_key=True)
    org_key = db.Column(db.Integer, db.ForeignKey(Organization.org_key), nullable=False)
    keyword = db.Column(db.String(250), unique=True, nullable=False)
    rank = db.Column(db.Integer, default=-1)
    data_loaded_date = db.Column(db.DateTime, nullable=True)
    data_loader = db.Column(db.String(50), nullable=True)

    org = db.relationship("Organization", backref=db.backref('keywords'))

    def __init__(self, org_key=None, keyword=None, rank=None, data_loaded_date=None, data_loader=DEFAULT_DATA_LOADER):
        self.org_key = org_key
        self.keyword = keyword
        self.rank = rank
        if not data_loaded_date:
            data_loaded_date = datetime.datetime.now()
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader

    def __repr__(self):
        return '<OrgKeyword %r>' % self.org_key

class OrgWatched(db.Model):
    __table_args__ = {'schema': 'xboard'}
    __tablename__ = 'org_watched'

    org_watched_key = db.Column(db.Integer, primary_key=True)
    org_key = db.Column(db.Integer, db.ForeignKey(Organization.org_key), nullable=False)
    data_loaded_date = db.Column(db.DateTime, nullable=True)
    data_loader = db.Column(db.String(50), nullable=True)

    org = db.relationship('Organization')

    def __init__(self, org_key, data_loaded_date=None, data_loader=DEFAULT_DATA_LOADER):
        self.org_key = org_key
        if not data_loaded_date:
            data_loaded_date = datetime.datetime.now()
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader

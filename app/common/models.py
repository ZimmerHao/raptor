# -*- coding: UTF-8 -*-
import datetime

from app import db
from app.common.constants import DEFAULT_RANK, DEFAULT_DATA_LOADER


class Currency(db.Model):
    __table_args__ = {"schema": "warehouse"}
    __tablename__ = 'currency'

    currency_key = db.Column(db.Integer, primary_key=True)
    currency_name = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(256))
    currency_sign = db.Column(db.String(10), nullable=False)
    exchange_rate = db.Column(db.Numeric(5, 2))
    data_loaded_date = db.Column(db.DateTime, nullable=True)
    data_loader = db.Column(db.String(50), nullable=False)

    def __init__(self, currency_name, description, currency_sign, exchange_rate, data_loaded_date, data_loader):
        self.currency_name = currency_name
        self.description = description
        self.currency_sign = currency_sign
        self.exchange_rate = exchange_rate
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader


class IndustryClass(db.Model):
    __table_args__ = {"schema": "warehouse"}
    __tablename__ = 'industry_class'

    industry_class_key = db.Column(db.Integer, primary_key=True)
    industry_class_name = db.Column(db.String(50), nullable=False)
    industry_class_desc = db.Column(db.String(256))
    industry_class_type = db.Column(db.String(50), nullable=False)
    data_loaded_date = db.Column(db.DateTime, nullable=False)
    data_loader = db.Column(db.String(50), nullable=False)

    def __init__(self, industry_class_name, industry_class_desc, industry_class_type, data_loaded_date, data_loader):
        self.industry_class_name = industry_class_name
        self.industry_class_desc = industry_class_desc
        self.industry_class_type = industry_class_type
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader


class NationalIndustryClass(db.Model):
    __table_args__ = {"schema": "warehouse"}
    __tablename__ = 'national_industry_class'

    nic_key = db.Column(db.Integer, primary_key=True)
    nic_code = db.Column(db.String(20), nullable=False)
    nic_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    parent_code = db.Column(db.String(20))
    level1_code = db.Column(db.String(20))
    level2_code = db.Column(db.String(20))
    level3_code = db.Column(db.String(20))
    level4_code = db.Column(db.String(20))
    data_loaded_date = db.Column(db.DateTime, nullable=False)
    data_loader = db.Column(db.String(50), nullable=False)

    def __init__(self, nic_code, nic_name, description, parent_code, level1_code, level2_code,
                 level3_code, level4_code, data_loaded_date, data_loader):
        self.nic_code = nic_code
        self.nic_name = nic_name
        self.description = description
        self.parent_code = parent_code
        self.level1_code = level1_code
        self.level2_code = level2_code
        self.level3_code = level3_code
        self.level4_code = level4_code
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader


class Address(db.Model):
    __table_args__ = {"schema": "warehouse"}
    __tablename__ = 'address'

    address_key = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(25), nullable=False)
    province = db.Column(db.String(25))
    city = db.Column(db.String(25))
    county = db.Column(db.String(50))
    district = db.Column(db.String(50))
    mail_address = db.Column(db.String(500))
    zipcode = db.Column(db.String(10))
    post_office_box = db.Column(db.String(10))
    latitude = db.Column(db.String(30))
    longitude = db.Column(db.String(30))
    search_criteria = db.Column(db.String)
    org_license_number = db.Column(db.String(30))
    org_name = db.Column(db.String(250))
    registered_address_seq = db.Column(db.Integer)
    office_address_seq = db.Column(db.Integer)
    data_loaded_date = db.Column(db.DateTime, nullable=True)
    data_loader = db.Column(db.String(50), nullable=False)

    def __init__(self, country=None, province=None, city=None, county=None,
                 district=None, mail_address=None, zipcode=None, post_office_box=None,
                 latitude=None, longitude=None, search_criteria=None, org_license_number=None,
                 registered_address_seq=None, office_address_seq=None,
                 data_loaded_date=None, data_loader=DEFAULT_DATA_LOADER):
        self.country = country
        self.province = province
        self.city = city
        self.county = county
        self.district = district
        self.mail_address = mail_address
        self.zipcode = zipcode
        self.post_office_box = post_office_box
        self.latitude = latitude
        self.longitude = longitude
        self.search_criteria = search_criteria
        self.org_license_number = org_license_number
        self.registered_address_seq = registered_address_seq
        self.office_address_seq = office_address_seq
        if not data_loaded_date:
            data_loaded_date = datetime.datetime.now()
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader


class OrgRegisterationType(db.Model):
    __table_args__ = {"schema": "warehouse"}
    __tablename__ = 'org_registration_type'

    org_reg_type_key = db.Column(db.Integer, primary_key=True)
    org_reg_type = db.Column(db.String(250), nullable=False)
    org_reg_type_category = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(256))
    data_loaded_date = db.Column(db.DateTime, nullable=False)
    data_loader = db.Column(db.String(50), nullable=True)

    def __init__(self, org_reg_type, org_reg_type_category, description, data_loaded_date, data_loader):
        self.org_reg_type = org_reg_type
        self.org_reg_type_category = org_reg_type_category
        self.description = description
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader


class CalendarDate(db.Model):
    __table_args__ = {"schema": "warehouse"}
    __tablename__ = 'calendar_date'

    calendar_date_key = db.Column(db.Numeric(8), primary_key=True)
    year_date = db.Column(db.Date, nullable=False)
    year = db.Column(db.Numeric(4))
    quarter_date = db.Column(db.Date, nullable=False)
    quarter = db.Column(db.Numeric(1), nullable=False)
    month_date = db.Column(db.Date, nullable=False)
    month = db.Column(db.Numeric(2), nullable=False)
    month_name = db.Column(db.String(10), nullable=False)
    sunday_week_date = db.Column(db.Date, nullable=False)
    sunday_week = db.Column(db.Numeric(2), nullable=False)
    monday_week_date = db.Column(db.Date, nullable=False)
    monday_week = db.Column(db.Numeric(2), nullable=False)
    week_in_month = db.Column(db.Numeric(1), nullable=False)
    julian_week_numeric = db.Column(db.Numeric(2), nullable=False)
    julian_day = db.Column(db.Numeric(3), nullable=False)
    day_date = db.Column(db.Date, nullable=False)
    day_name = db.Column(db.String(10), nullable=False)
    holiday_flag = db.Column(db.String(1))
    holiday_name = db.Column(db.String(25))

    def __init__(self, year_date=None, quarter_date=None, quarter=None, month_date=None,
                 month=None, month_name=None, sunday_week_date=None, sunday_week=None,
                 week_in_month=None, julian_week_numeric=None, julian_day=None, day_date=None,
                 day_name=None, holiday_flag=None, holiday_name=None):
        self.year_date = year_date
        self.quarter_date = quarter_date
        self.quarter = quarter
        self.month_date = month_date
        self.month = month
        self.month_name = month_name
        self.sunday_week_date = sunday_week_date
        self.sunday_week = sunday_week
        self.week_in_month = week_in_month
        self.julian_week_numeric = julian_week_numeric
        self.julian_day = julian_day
        self.day_date = day_date
        self.day_name = day_name
        self.holiday_flag = holiday_flag
        self.holiday_name = holiday_name


class OrgStatus(db.Model):
    __table_args__ = {"schema": "warehouse"}
    __tablename__ = 'org_status'

    org_status_key = db.Column(db.Integer, primary_key=True)
    org_status = db.Column(db.String(25), unique=True, nullable=False)
    description = db.Column(db.String(256))
    org_status_type = db.Column(db.String(25), nullable=False)
    data_loaded_date = db.Column(db.DateTime, nullable=False)
    data_loader = db.Column(db.String(50), nullable=True)

    def __init__(self, org_status=None, description=None, org_status_type=None,
                 data_loaded_date=None, data_loader=DEFAULT_DATA_LOADER):
        self.org_status = org_status
        self.description = description
        self.org_status_type = org_status_type
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader


class HighTechZone(db.Model):
    __table_args__ = {"schema": "warehouse"}
    __tablename__ = 'high_tech_zone'

    high_tech_zone_key = db.Column(db.Integer, primary_key=True)
    zone_name = db.Column(db.String(250), nullable=False)
    zone_rank = db.Column(db.String(50))
    zone_desc = db.Column(db.Text)
    zone_feature = db.Column(db.Text)
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    district = db.Column(db.String(50))
    data_loaded_date = db.Column(db.DateTime, nullable=False)
    data_loader = db.Column(db.String(50), nullable=False)

    def __init__(self, zone_name, zone_rank, zone_desc, zone_feature, province, city, district,
                 data_loaded_date, data_loader):
        self.zone_name = zone_name
        self.zone_rank = zone_rank
        self.zone_desc = zone_desc
        self.zone_feature = zone_feature
        self.province = province
        self.city = city
        self.district = district
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader


class CommMedia(db.Model):
    __table_args__ = {"schema": "warehouse"}
    __tablename__ = 'comm_media'

    comm_media_key = db.Column(db.Integer, primary_key=True)
    comm_media_name = db.Column(db.String(50), nullable=False)
    comm_media_category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    comm_media_alias = db.Column(db.String(50))
    data_loaded_date = db.Column(db.DateTime, nullable=False)
    data_loader = db.Column(db.String(50), nullable=False)

    def __init__(self, comm_media_name, comm_media_category, description, comm_media_alias,
                 data_loaded_date, data_loader):
        self.comm_media_name = comm_media_name
        self.comm_media_category = comm_media_category
        self.description = description
        self.comm_media_alias = comm_media_alias
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader


class CommMediaStatus(db.Model):
    __table_args__ = {"schema": "warehouse"}
    __tablename__ = 'comm_media_status'

    comm_media_status_key = db.Column(db.Integer, primary_key=True)
    comm_media_status = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    data_loaded_date = db.Column(db.DateTime, nullable=False)
    data_loader = db.Column(db.String(50), nullable=False)

    def __init__(self, comm_media_status, description, data_loaded_date, data_loader):
        self.comm_media_status = comm_media_status
        self.description = description
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader



class Organization(db.Model):
    __table_args__ = {"schema": "warehouse"}
    __tablename__ = 'organization'

    org_key = db.Column(db.Integer, primary_key=True)
    effective_start_date = db.Column(db.Date, nullable=False)
    org_name = db.Column(db.String(250), nullable=False)
    org_desc = db.Column(db.Text)
    org_short_name = db.Column(db.String(50))
    org_english_name = db.Column(db.String(250))
    org_english_name_abbr = db.Column(db.String(50))
    org_start_date_key = db.Column(db.Integer, nullable=False)
    org_start_date_src = db.Column(db.String(50))
    industry_class_key = db.Column(db.Integer, db.ForeignKey(IndustryClass.industry_class_key), nullable=False)
    nic_key = db.Column(db.Integer, nullable=False)
    org_website = db.Column(db.String(250))
    in_charge_person_key = db.Column(db.Integer, nullable=False)
    main_phone_num = db.Column(db.String(20))
    registered_capital = db.Column(db.BigInteger)
    capital_currency_key = db.Column(db.Integer, nullable=False)
    registered_address_key = db.Column(db.Integer, nullable=False)
    office_address_key = db.Column(db.Integer, nullable=False)
    core_business = db.Column(db.Text)
    org_status_key = db.Column(db.Integer, db.ForeignKey(OrgStatus.org_status_key), nullable=False)
    license_number = db.Column(db.String(30))
    org_code = db.Column(db.String(30))
    revenue = db.Column(db.Numeric(12,2))
    org_size = db.Column(db.Integer)
    data_source_key = db.Column(db.Integer, nullable=False)
    org_reg_type_key = db.Column(db.Integer, nullable=False)
    business_scope = db.Column(db.Text)
    business_term = db.Column(db.String(250))
    org_seq = db.Column(db.Integer)
    shareholder_org_seq = db.Column(db.Integer)
    org_size_src = db.Column(db.String(250))
    affiliated_org_seq = db.Column(db.Integer)
    duplicated = db.Column(db.Boolean, nullable=False)
    high_tech_zone_key = db.Column(db.Integer, nullable=False)
    company_value = db.Column(db.String(250))
    src_data_add_date_key = db.Column(db.Integer, nullable=False)
    data_loaded_date = db.Column(db.DateTime, nullable=True)
    data_loader = db.Column(db.String(50), nullable=True)

    industry_class = db.relationship('IndustryClass')
    org_status = db.relationship('OrgStatus')

    def __init__(self, effective_start_date, org_name, org_desc, org_short_name, org_english_name,
                 org_english_name_abbr, org_start_date_key, org_start_date_src, industry_class_key, nic_key,
                 org_website, in_charge_person_key, main_phone_num, registered_capital, capital_currency_key,
                 registered_address_key, core_business, org_status_key, license_number, org_code, revenue, org_size,
                 data_source_key, org_reg_type_key, business_scope, business_term, org_seq, shareholder_org_seq,
                 org_size_src, affiliated_org_seq, duplicated, high_tech_zone_key, company_value,
                 src_data_add_date_key, data_loaded_date, data_loader):
        self.effective_start_date = effective_start_date
        self.org_name = org_name
        self.org_desc = org_desc
        self.org_short_name = org_short_name
        self.org_english_name = org_english_name
        self.org_english_name_abbr = org_english_name_abbr
        self.org_start_date_key = org_start_date_key
        self.org_start_date_src = org_start_date_src
        self.industry_class_key = industry_class_key
        self.nic_key = nic_key
        self.org_website = org_website
        self.in_charge_person_key = in_charge_person_key
        self.main_phone_num = main_phone_num
        self.registered_capital = registered_capital
        self.capital_currency_key = capital_currency_key
        self.registered_address_key = registered_address_key
        self.core_business = core_business
        self.org_status_key = org_status_key
        self.license_number = license_number
        self.org_code = org_code
        self.revenue = revenue
        self.org_size = org_size
        self.data_source_key = data_source_key
        self.org_reg_type_key = org_reg_type_key
        self.business_scope = business_scope
        self.business_term = business_term
        self.org_seq = org_seq
        self.shareholder_org_seq = shareholder_org_seq
        self.org_size_src = org_size_src
        self.affiliated_org_seq = affiliated_org_seq
        self.duplicated = duplicated
        self.high_tech_zone_key = high_tech_zone_key
        self.company_value = company_value
        self.src_data_add_date_key = src_data_add_date_key
        if not data_loaded_date:
            data_loaded_date = datetime.datetime.now()
        self.data_loaded_date = data_loaded_date
        self.data_loader = data_loader

    def __repr__(self):
        return '<Organization %r>' % self.org_name

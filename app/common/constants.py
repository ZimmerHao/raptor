# -*- coding: UTF-8 -*-

class Enum(object):
    def __init__(self, *args, **kwargs):
        self.__dict__.update(
            dict(zip(args, range(len(args))), **kwargs)
        )

    def inv_dict(self):
        d = self.__dict__.values()
        if len(d) != len(set(d)):
            raise "Cannot reverse key-value because the Enum obj has duplicated values."
        return {v: k for k, v in self.__dict__.iteritems()}

    def sorted_names(self):
        return sorted(self.names(),
                      lambda a, b: cmp(self.__dict__[a], self.__dict__[b]))

    def sorted_values(self):
        return sorted(self.values())

    def names(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def __contains__(self, key):
        return key in self.values()



NEWS_SOURCE_PER_PAGE = 10
ORG_KEYWORD_PER_PAGE = 10
ORG_WATCHED_PER_PAGE = 10
ORG_PER_PAGE = 10
NEWS_PER_PAGE = 10
ORG_WATCHED_SERACH_COUNT = 20
ORG_SERACH_COUNT = 20
TAG_SERACH_COUNT = 10
NEWS_CATEGORY_SERACH_COUNT = 10
NEWS_SOURCE_SEARCH_COUNT = 20

DEFAULT_RANK = -1
DEFAULT_DATA_LOADER = u'system'

DEFAULT_HBASE_DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
DEFAULT_HBASE_NEWS_DATE_KEY_FORMAT = '%Y%m%d'


COMM_MEDIA_TYPE = Enum()
COMM_MEDIA_TYPE.TELEPHOME = 1
COMM_MEDIA_TYPE.MOBILE = 2
COMM_MEDIA_TYPE.FAX = 4
COMM_MEDIA_TYPE.WEIBO = 5
COMM_MEDIA_TYPE.WECHAT = 7
COMM_MEDIA_TYPE.EMAIL = 8

COMM_MEDIA_STATUS = Enum()
COMM_MEDIA_STATUS.NONEFFECTIVE = 0
COMM_MEDIA_STATUS.EFFECTIVE = 1

DATA_SOURCE_TYPE = Enum()
DATA_SOURCE_TYPE.MANUAL = 3


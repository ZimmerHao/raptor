# -*- coding: UTF-8 -*-

class UnicodeDict(dict):
    def __getitem__(self, key):
        value = super(UnicodeDict, self).__getitem__(key)
        try:
            value = unicode(value)
        except:
            pass
        return value

ERRORS = UnicodeDict({
    40001: u"参数错误",
    # 401新闻相关
    40101: u"未找到该新闻来源",
    40102: u"未找到该企业关键词",
    40103: u"插入新闻失败",
    40104: u"该新闻来源已存在",

    # 402企业相关
    40201: u"未找到该企业",
})


class ApiError(Exception):
    def __init__(self, code, status=400):
        self.code = code
        self.status = status
        self.msg = unicode(ERRORS[code])
        Exception.__init__(self, str(self))

    def __str__(self):
        return "<ApiError %s:(%s)>" % (self.status, self.code)

    def __repr__(self):
        return str(self)

    def to_json(self):
        return {
            'error': self.code,
            'message': self.msg
        }










if __name__ == "__main__":
    print ApiError(40001)






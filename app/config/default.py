import os

class Config(object):
    DEBUG = True
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    HBASE_HOST = '192.168.30.47'
    HBASE_PORT = 9090
    SQLALCHEMY_DATABASE_URI = 'postgresql://haojm:ytdb.2013@192.168.31.103/yunti'
    SQLALCHEMY_BINDS = {

    }

    SESSION_OPTS = {
        'session.type': 'redis',
        'session.url': '127.0.0.1:6379',
    }






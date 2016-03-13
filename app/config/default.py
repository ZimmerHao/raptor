import os

class Config(object):
    DEBUG = True
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    HBASE_HOST = '192.168.30.47'
    HBASE_PORT = 9090
    SQLALCHEMY_DATABASE_URI = 'postgresql://ws_dblayer:progress*2013@192.168.31.103/yunti'
    SQLALCHEMY_BINDS = {

    }






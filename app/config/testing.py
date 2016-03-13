import os
from app.config.default import Config


class TestingConfig(Config):
    DEBUG = False
    LOG_DIR = os.path.join(Config.BASE_DIR, 'logs')
    LOGGING = {
        'version': 1,    # Configuration schema in use; must be 1 for now
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s'
            },
            'simple': {
                'format': '%(asctime)s - %(levelname)s - %(message)s'
            }
        },
        'handlers': {
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'flask.log'),
                'formatter': 'standard'

            },
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            }
        },
        # Specify all the subordinate loggers
        'loggers': {
            'root': {
                'handlers': ['console']
            },
            'flask': {
                'handlers': ['console']
            },
            'flask.request': {
                'handlers': ['file']
            }
        }
    }




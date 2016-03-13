import os
from app.config.default import Config


class DevelopmentConfig(Config):
    DEBUG = True
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
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            }
        },
        # Specify all the subordinate loggers
        'loggers': {
            'root': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False
            },
            'flask': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False
            },
            'flask.request': {
                'level': 'INFO',
                'handlers': ['file'],
                'propagate': False
            }
        }
    }




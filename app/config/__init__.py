import os


def load_config():
    mode = os.environ.get('MODE')
    try:
        if mode == 'PRODUCTION':
            from prod import ProductionConfig
            return ProductionConfig
        elif mode == 'TESTING':
            from testing import TestingConfig
            return TestingConfig
        else:
            from local import DevelopmentConfig
            return DevelopmentConfig
    except ImportError:
        from default import Config
        return Config
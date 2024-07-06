import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
PG_DRIVER = os.environ.get('PG_DRIVER')
PG_HOST = os.environ.get('PG_HOST')
PG_USERNAME = os.environ.get('PG_USERNAME')
PG_PASSWORD = os.environ.get('PG_PASSWORD')
PG_DB = os.environ.get('PG_DB')

class Config():
    """Contains common configuration for every environemnt"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=60)


    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Development server"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DB') or \
                              f'{PG_DRIVER}://{PG_USERNAME}:{PG_PASSWORD}@{PG_HOST}/{PG_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DB') or \
                              f'{PG_DRIVER}://{PG_USERNAME}:{PG_PASSWORD}@{PG_HOST}/{PG_DB}'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB') or \
                            'sqlite://'
    
config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}
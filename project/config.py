import os

class BaseConfig:
    """Base Confilguration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY ='K1m3tsuN0Ya1ba'

class DevelopmentConfig(BaseConfig):
    """Development Configuration"""
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/books_gallery'
    CORS_HEADERS = 'Content-Type'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(BaseConfig):
    """Production Configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
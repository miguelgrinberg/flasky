import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'omnia kurssi'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DB_NAME = 'flasky'
    DB_USERNAME = 'root'
    DB_PASSWORD = ''
    DB_URL = 'mysql+pymysql://' + DB_USERNAME + ':' + \
        DB_PASSWORD + '@localhost:3306/' + DB_NAME
    SQLALCHEMY_DATABASE_URI = DB_URL
    # os.environ.get('DEV_DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    DB_NAME = 'flasky'
    DB_USERNAME = 'root'
    DB_PASSWORD = ''
    DB_URL = 'mysql+pymysql://' + DB_USERNAME + ':' + \
        DB_PASSWORD + '@localhost:3306/' + DB_NAME
    SQLALCHEMY_DATABASE_URI = DB_URL
    # SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    #     'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

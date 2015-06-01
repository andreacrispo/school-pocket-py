import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '%\xee\xda;\xdemo\x03\xee~\x1eV\xbb\xaf5\xa6\xfa\xfdPY\xff\xf3\x03h'
    SSL_DISABLE = True

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SCHOOL_POCKET_MAIL_SUBJECT_PREFIX = '[School Pocket]'
    SCHOOL_POCKET_MAIL_SENDER = 'School Pocket Admin'
    SCHOOL_POCKET_ADMIN = os.environ.get('SCHOOL_POCKET_ADMIN')

    UPLOAD_FOLDER =  os.path.join(basedir, 'app/static/uploads')
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    @staticmethod
    def init_app(app):
        pass



class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
   

class HerokuConfig(ProductionConfig):
    """ Deployment on Heroku """
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
    ProductionConfig.init_app(app)
    # log to stderr
    import logging
    from logging import StreamHandler
    file_handler = StreamHandler()
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

config = {
    'development': DevelopmentConfig,
    'testing'    : TestingConfig,
    'production' : ProductionConfig,
    'heroku'     : HerokuConfig,
    
    'default'    : DevelopmentConfig
}


LANGUAGES = {
    'en': 'English',
    'it': 'Italiano'
}
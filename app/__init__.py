from flask import Flask, request, g
from flask.ext.bootstrap  import Bootstrap
from flask.ext.mail       import Mail
from flask.ext.moment     import Moment
from flask.ext.login      import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babel      import Babel
from config import config, LANGUAGES

bootstrap     = Bootstrap()
mail          = Mail()
moment        = Moment()
db            = SQLAlchemy()
babel         = Babel()
login_manager = LoginManager()

login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)


    @babel.localeselector
    def get_locale():
        g.locale = request.accept_languages.best_match(LANGUAGES.keys())
        return g.locale


    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        sslify = SSLify(app)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app



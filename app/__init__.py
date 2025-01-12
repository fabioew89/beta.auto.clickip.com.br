from flask_admin import Admin
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for
from sqlalchemy.orm import DeclarativeBase
# from livereload import Server


# Declarativa base para o SQLAlchemy
class Base(DeclarativeBase):
    pass


# Inicializando extensões
db = SQLAlchemy(model_class=Base)
lm = LoginManager()
admin = Admin()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # Inicializando extensões com o app
    db.init_app(app)
    lm.init_app(app)
    admin.init_app(app)
    migrate.init_app(app, db)

    lm.login_view = 'auth.login'
    lm.login_message = 'Please log in to access this page.'
    lm.login_message_category = 'info'
    lm.session_protection = "strong"

    lm.refresh_view = "auth.login"
    lm.needs_refresh_message = (
        u"To protect your account, please reauthenticate to access this page."
    )
    lm.needs_refresh_message_category = "info"

    # Registrando blueprints
    from app.controllers.blueprints.auth_routes import auth_bp
    from app.controllers.blueprints.network_routes import network_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(network_bp, url_prefix='/network')

    with app.app_context():
        db.create_all()

    # Rota básica para home
    @app.route('/')
    def page_home():
        return redirect(url_for('network.interface_summary'))

    # config livereload only for development frontend
    # server = Server(app.wsgi_app)
    # server.watch('app/templates/**/*')
    # server.watch('app/static/**/*')
    # server.serve(port=5000)

    return app

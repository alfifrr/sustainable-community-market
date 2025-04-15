from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import DeclarativeBase
from os import environ
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
bcrypt = Bcrypt()
mail = Mail()
jwt = JWTManager()
migrate = Migrate()


def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
    app.config['JWT_SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['MAIL_SERVER'] = environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = environ.get('MAIL_SENDER')

    if config:
        app.config.update(config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()
        from app.models.seeder import seed_product_categories
        seed_product_categories()

    return app

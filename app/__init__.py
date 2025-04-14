from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import DeclarativeBase
from os import environ


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
bcrypt = Bcrypt()


def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
    app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')

    if config:
        app.config.update(config)

    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()
        from app.models.seeder import seed_product_categories
        seed_product_categories()

    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import DeclarativeBase
from os import environ
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv

load_dotenv(override=True)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
bcrypt = Bcrypt()
mail = Mail()
jwt = JWTManager()
migrate = Migrate()


def create_app(config=None):
    app = Flask(__name__)

    url = environ.get("POSTGRESQL_URL")
    if not url:
        raise ValueError("POSTGRESQL_URL environment variable is not set")

    try:
        if not database_exists(url):
            create_database(url)
            print(f"Database created successfully at {url}")
        else:
            print("Database already exists")
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        raise

    app.config.update(
        SQLALCHEMY_DATABASE_URI=url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=environ.get("SECRET_KEY"),
        SECRET_KEY=environ.get("SECRET_KEY"),
        WTF_CSRF_ENABLED=False,
        MAIL_SERVER=environ.get("MAIL_SERVER"),
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME=environ.get("MAIL_USERNAME"),
        MAIL_PASSWORD=environ.get("MAIL_PASSWORD"),
        MAIL_DEFAULT_SENDER=environ.get("MAIL_SENDER"),
    )

    if config:
        app.config.update(config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        try:
            db.create_all()
            from app.models.seeder import seed_product_categories, seed_roles

            seed_product_categories()
            seed_roles()
            print("Database tables created and seeded successfully")
        except Exception as e:
            print(f"Error creating tables: {str(e)}")
            raise

    return app

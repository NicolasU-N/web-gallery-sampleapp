from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, current_user

# globals
# DB_NAME = "database.db"

db = SQLAlchemy()
UPLOAD_FOLDER = "App/static/img/"


def create_app():
    # configure app
    app = Flask(__name__)

    server = "nikos-server.database.windows.net"
    database = "nikos-db"
    username = "nikosdb"
    password = "Admin1234"
    driver = "ODBC+Driver+17+for+SQL+Server"

    app.config["SECRET_KEY"] = "this is the SECRET_KEY"
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}"

    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    # app.config["SECRET_KEY"] = "this is the key"
    # app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    # app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    # register the blueprints
    from . import auth
    from . import views

    app.register_blueprint(auth.auth, url_prefix="/")
    app.register_blueprint(views.views, url_prefix="/")

    # Configure database
    db.init_app(app)
    db.create_all(app=app)
    # create_database(app)
    print("Database Created!")

    # Configure login manager

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    return app


# def create_database(app):
#     if not os.path.exists(f"App/{DB_NAME}"):
#         db.create_all(app=app)
#         print("Database Created!")

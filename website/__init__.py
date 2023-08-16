from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import sqlite3
import mysql

db = SQLAlchemy()
DB_NAME = "myth-db"

PASSWORD = databasePW
PUBLIC_IP_ADDRESS = "34.106.7.90"
DBNAME ="myth-db"
PROJECT_ID ="wowmythicgroups"
INSTANCE_NAME ="wowmythicgroups:us-west3:myth-db"

def create_app():
    app = Flask(__name__,template_folder='Templates',static_folder='Static')
    app.config["SECRET_KEY"] = "notAsecret"
    # app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    # app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://databaseUser:databasePW@34.106.7.90/{DB_NAME}"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql + mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    from .models import Users, Players, Characters, Role_Entries, Keys 
    # clear_database()

    create_database(app)

    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")

    else:
        try:
            conn = sqlite3.connect("website/database.db")
            cursor = conn.cursor()
            print("DB Connected")
            query = f"SELECT name FROM sqlite_master WHERE type='table'"
            cursor.execute(query)
            results = cursor.fetchall()
            print(results)
            cursor.close()
        except sqlite3.Error as error:
            print("Error occurred - ", error)
        finally:
            if conn:
                conn.close()
                print("Connection closed")

        if len(results) < 1:
            print(f"No '{DB_NAME}' tables exists")
            db.create_all(app=app)
            print("Created Database!")

        else:
            print(f"Table {DB_NAME} exists, new db not created!")



def clear_database():
    if path.exists("website/" + DB_NAME):
        try:

            conn = sqlite3.connect("website/database.db")
            conn.execute("DROP TABLE user")

        except sqlite3.Error as error:
            print("Error occurred - ", error)

        finally:
            if conn:
                conn.close()
                print("Connection closed")
                print("Database Cleared")
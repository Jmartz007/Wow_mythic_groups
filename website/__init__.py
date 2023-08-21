
from __future__ import annotations
import logging
import os
from flask import Flask, Response
import sqlalchemy
from sqlalchemy import exc

from .connect_connector import connect_with_connector
from .connect_connector_auto_iam_authn import connect_with_connector_auto_iam_authn
from .connect_tcp import connect_tcp_socket
from .connect_unix import connect_unix_socket

# environment variables when testing

#

app = Flask(__name__, template_folder='Templates',static_folder='Static')
app.secret_key = "123123123"

logger = logging.getLogger()


def init_connection_pool() -> sqlalchemy.engine.base.Engine:
    """Sets up connection pool for the app."""
    # use a TCP socket when INSTANCE_HOST (e.g. 127.0.0.1) is defined
    if os.environ.get("INSTANCE_HOST"):
        return connect_tcp_socket()

    # use a Unix socket when INSTANCE_UNIX_SOCKET (e.g. /cloudsql/project:region:instance) is defined
    if os.environ.get("INSTANCE_UNIX_SOCKET"):
        return connect_unix_socket()

    # use the connector when INSTANCE_CONNECTION_NAME (e.g. project:region:instance) is defined
    if os.environ.get("INSTANCE_CONNECTION_NAME"):
        # Either a DB_USER or a DB_IAM_USER should be defined. If both are
        # defined, DB_IAM_USER takes precedence.
        return (
            connect_with_connector_auto_iam_authn()
            if os.environ.get("DB_IAM_USER")
            else connect_with_connector()
        )

    raise ValueError(
        "Missing database connection type. Please define one of INSTANCE_HOST, INSTANCE_UNIX_SOCKET, or INSTANCE_CONNECTION_NAME"
    )

# This global variable is declared with a value of `None`, instead of calling
# `init_db()` immediately, to simplify testing. In general, it
# is safe to initialize your database connection pool when your script starts
# -- there is no need to wait for the first request.
db = init_connection_pool()


# init_db lazily instantiates a database connection pool. Users of Cloud Run or
# App Engine may wish to skip this lazy instantiation and connect as soon
# as the function is loaded. This is primarily to help testing.
# @app.before_first_request
# def init_db() -> sqlalchemy.engine.base.Engine:
#     """Initiates connection to database and its' structure."""
#     global db
#     db = init_connection_pool()
#     # migrate_db(db)

def player_entry(playerName, characterName, className, role):
    try:
        # Using a with statement ensures that the connection is always released
        # back into the pool at the end of statement (even if an error occurs)
        with db.connect() as conn:
            user = conn.execute(sqlalchemy.text(
                f"SELECT PlayerName FROM players WHERE PlayerName='{playerName}'"
            )).first()

            if not user:
                conn.execute(sqlalchemy.text(f"INSERT INTO players (PlayerName) VALUES ('{playerName}') "))
            
            
            stmt = sqlalchemy.text(
                "INSERT INTO characters (CharacterName, PlayerName, Class) VALUES (:characterName, :PlayerName, :className)"
                )
            conn.execute(stmt, parameters={"characterName": characterName, "PlayerName": playerName, "className": className})

            for i in role:
                conn.execute(sqlalchemy.text(
                    f"INSERT INTO role_entries (CharacterName, Role) VALUES ('{characterName}', '{i}')")
                    )
            conn.commit()
    except exc.SQLAlchemyError as error:
        logger.exception(error)
    except Exception as e:
            # If something goes wrong, handle the error in this section. This might
            # involve retrying or adjusting parameters depending on the situation.
            # [START_EXCLUDE]
            logger.exception(e)
            return Response(
                status=500,
                response="Unable to successfully sign up player! Please check the "
                "application logs for more details.",
        )
        # [END_EXCLUDE]
    # [END cloud_sql_mysql_sqlalchemy_connection]

    return Response(status=200, response=f"Entry successful for '{playerName}'")


def clear_database():
    try:
        with db.connect() as conn:
            conn.execute(sqlalchemy.text("DELETE FROM role_entries"))
            conn.execute(sqlalchemy.text("DELETE FROM characters"))
            conn.execute(sqlalchemy.text("DELETE FROM players"))
            
            conn.commit()
            logger.info("Database Cleared")
    except Exception as error:
        print("Error occurred - ", error)
        logger.exception(error)


from .views import views
app.register_blueprint(views, url_prefix="/")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
    db = init_connection_pool()



























"""
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


 """
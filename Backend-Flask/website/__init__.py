import os
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from utils.customexceptions import DatabaseError
import LoggingUtility
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

logger = logging.getLogger("main")

logger.info("---------------------------------")
logger.info("---------- STARTED APP ----------")
logger.info("---------------------------------")
# db = db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="Templates",
        static_folder="Static",
    )

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    app.config.from_mapping(
        SECRET_KEY="123123123",
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    @app.errorhandler(DatabaseError)
    def handle_database_error(error):
        response = {"error": str(error)}
        return response, 500

    from .views import views

    app.register_blueprint(views)

    from .auth import bp

    app.register_blueprint(bp)

    from .apiviews import api_bp

    app.register_blueprint(api_bp)

    return app


if __name__ == "__main__":
    create_app(host="0.0.0.0", port=5000, debug=True)
    # db = db

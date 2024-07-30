import os
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from dotenv import load_dotenv
import LoggingUtility

load_dotenv()

logger = logging.getLogger("main")

logger.info("---------------------------------")
logger.info("---------- STARTED APP ----------")
logger.info("---------------------------------")
# db = db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, template_folder='Templates',static_folder='Static')
    app.config.from_mapping(
        SECRET_KEY='123123123',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from .views import views
    app.register_blueprint(views, url_prefix="/")

    from .auth import bp
    app.register_blueprint(bp)

    return app


if __name__ == "__main__":
    create_app(host="127.0.0.1", port=8080, debug=True)
    # db = db
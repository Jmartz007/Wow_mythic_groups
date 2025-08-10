import logging
import os
from math import log

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from utils.customexceptions import DatabaseError, DataNotFoundError, ServiceException
import LoggingUtility
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

__version__ = "v4.2.1"

logger = logging.getLogger("main")

logger.info("---------- Starting App ----------")
logger.info("App Version: %s", __version__)
logger.info("---------------------------------")
logger.info("---------- STARTED APP ----------")
logger.info("---------------------------------")
# db = db


def create_app(test_config=None):
    """create and configure the app"""
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

    CORS(
        app,
        resources={
            r"/*": {
                "origins": ["http://localhost:5173", "https://jmartz.servegame.com"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            }
        },
    )

    # Register blueprints
    from .auth import bp as auth_bp
    from .playersview import bp as players_bp
    from .Oauth import oauth as oauth_bp
    from .dungeonsviews import api_bp as dungeons_bp
    from .wow_profile import wow_profile as wow_profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(oauth_bp)
    app.register_blueprint(dungeons_bp)
    app.register_blueprint(wow_profile_bp)

    # Register error handlers
    @app.errorhandler(DatabaseError)
    def handle_database_error(error):
        logger.exception(error)
        response = {"error": str(error)}
        return response, 500

    @app.errorhandler(DataNotFoundError)
    def handle_no_data_error(error):
        # logger.exception(error)
        response = {"error": str(error)}
        return response, 404

    @app.errorhandler(ServiceException)
    def handle_service_error(e):
        return {"error": str(e)}, 500

    @app.errorhandler(404)
    def not_found_error(error):
        logger.error("404 Error: %s - %s", error, request.url)
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error("500 Error: %s", error)
        return jsonify({"error": "Internal server error"}), 500

    # Log all requests
    @app.before_request
    def log_request_info():
        logger.debug("Request URL: %s", request.url)
        logger.debug("Request method: %s", request.method)
        logger.debug("Request headers: %s", dict(request.headers))

    return app

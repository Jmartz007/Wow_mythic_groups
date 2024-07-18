import logging

from flask import Flask
import graypy
from dotenv import load_dotenv

from sqlconnector.connection_pool import db

load_dotenv()

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)-5s] [%(module)s]-%(funcName)s: %(message)s', datefmt='%b/%d/%y %I:%M:%S %p')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

socket_handler = graypy.GELFTCPHandler(host="localhost", port=5555)
socket_handler.setLevel(logging.DEBUG)
socket_handler.setFormatter(formatter)
logger.addHandler(socket_handler)

logger.info("STARTED APP ----------")
db = db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, template_folder='Templates',static_folder='Static')
    app.config.from_mapping(
        SECRET_KEY='123123123',
        # DATABASE=os.path.join(app.instance_path, 'website.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)


    # a simple page that says hello
    from .views import views
    app.register_blueprint(views, url_prefix="/")

    return app


if __name__ == "__main__":
    create_app(host="127.0.0.1", port=8080, debug=True)
    # db = db
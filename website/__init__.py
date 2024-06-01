import logging

from __future__ import annotations
from flask import Flask

from sqlconnector.connection_pool import db

app = Flask(__name__, template_folder='Templates',static_folder='Static')
app.secret_key = "123123123"

logger = logging.getLogger()


# This global variable is declared with a value of `None`, instead of calling
# `init_db()` immediately, to simplify testing. In general, it
# is safe to initialize your database connection pool when your script starts
# -- there is no need to wait for the first request.
db = db


from .views import views
app.register_blueprint(views, url_prefix="/")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
    db = db
import logging
import functools
from flask import (
    Blueprint,
    g,
    jsonify,
    request,
    session,
)
from werkzeug.security import check_password_hash, generate_password_hash
import sqlalchemy

from sqlconnector.sqlReader import db
from utils.helpers import build_error_response, build_success_response

logger = logging.getLogger(f"main.{__name__}")


bp = Blueprint("auth", __name__, url_prefix="/groups/auth")


@bp.route("/login", methods=["POST"])
def login():
    form_data = request.json
    logger.debug(form_data)
    username = form_data.get("username")
    password = form_data.get("password")

    try:

        error = None
        with db.connect() as conn:
            user = conn.execute(
                sqlalchemy.text("""SELECT * FROM user where username = :username"""),
                {"username": username},
            ).first()
            logger.debug("user results: %s", user)

        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user[2], password):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session["username"] = user[1]
            return build_success_response("Logged in", 200)
    except Exception as error:
        logger.exception(error)
        return build_error_response("server error", 500)

    return build_error_response(f"An error occurred: {error}", 400)


@bp.route("/create", methods=["POST"])
def create_user():
    form_data = request.json
    logger.debug(form_data)
    username = form_data.get("username")
    password = form_data.get("password")

    hashed_password = generate_password_hash(password=password)
    with db.connect() as conn:
        conn.execute(
            sqlalchemy.text(
                """INSERT INTO user (username, password)
                            VALUES (:username, :password)"""
            ),
            {"username": username, "password": hashed_password},
        )
        conn.commit()

    return build_success_response("User created", 201)


@bp.route("/reset-password", methods=["POST"])
def reset_password():
    form_data = request.json
    logger.debug(form_data)
    username = form_data.get("username")
    password = form_data.get("password")

    hashed_password = generate_password_hash(password=password)
    with db.connect() as conn:
        conn.execute(
            sqlalchemy.text(
                """UPDATE user 
                            SET password = :password
                            WHERE username = :username"""
            ),
            {"username": username, "password": hashed_password},
        )
        conn.commit()

    return build_success_response("password updated", 201)


@bp.route("/status")
def auth_status():
    if "username" in session:
        logger.info("username in session: %s", session["username"])
        return jsonify({"authenticated": True}), 200
    logger.info("user not logged in")
    return jsonify({"authenticated": False}), 200


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return build_success_response("Logged out", 200)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.username is None:
            return build_error_response("Unauthorized", 401)
            # return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    username = session.get("username")

    if username is None:
        g.username = None
        logger.info("username is: %s", g.username)

    else:
        with db.connect() as conn:
            result = conn.execute(
                sqlalchemy.text(
                    """SELECT username FROM user WHERE username = :username"""
                ),
                {"username": username},
            ).first()
            g.username = result[0]
            logger.info("user found in database: %s", g.username)

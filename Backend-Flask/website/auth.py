import logging
import functools
import jwt
import os
from flask import Blueprint, request, g
from werkzeug.security import generate_password_hash
import sqlalchemy

from sqlconnector.sqlReader import db
from utils.helpers import build_error_response, build_success_response

# Load and check JWT_SECRET_KEY for auth
logger = logging.getLogger(f"main.{__name__}")
try:
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
except KeyError as e:
    logger.error("Environment variable not set: %s", e)
    raise RuntimeError(f"Missing environment variable: {e}")

bp = Blueprint("auth", __name__, url_prefix="/groups/auth")


@bp.route("/create", methods=["POST"])
def create_user():
    form_data = request.json
    if form_data:
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
    return build_error_response("No data provided or missing data", 400)


@bp.route("/reset-password", methods=["POST"])
def reset_password():
    form_data = request.json
    if form_data:
        logger.debug(form_data)
        username = form_data.get("username")
        new_password = form_data.get("password")

        hashed_password = generate_password_hash(password=new_password)
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
    return build_error_response("No data provided or missing data", 400)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("No bearer token found in request")
            return build_error_response("No authorization token provided", 401)

        try:
            # Extract the token (remove 'Bearer ' prefix)
            token = auth_header.split(" ")[1]

            # Verify and decode the token
            decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])

            # Store decoded user info in Flask's g object for use in the rest of the request
            g.user_id = decoded.get("sub")
            g.battletag = decoded.get("battletag")

            return view(**kwargs)

        except jwt.ExpiredSignatureError:
            logger.warning("Expired token received")
            return build_error_response("Token has expired", 401)
        except jwt.InvalidTokenError as e:
            logger.warning("Invalid token received: %s", str(e))
            return build_error_response("Invalid token", 401)
        except Exception as e:
            logger.error("Unexpected error in auth: %s", str(e))
            return build_error_response("Authentication error", 500)

    return wrapped_view

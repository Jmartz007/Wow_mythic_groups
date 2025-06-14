import logging
import functools
import os
import jwt
from flask import Blueprint, jsonify, request, g
from werkzeug.security import check_password_hash, generate_password_hash
import sqlalchemy
from dotenv import load_dotenv

from sqlconnector.sqlReader import db
from utils.helpers import build_error_response, build_success_response

load_dotenv()
logger = logging.getLogger(f"main.{__name__}")


bp = Blueprint("auth", __name__, url_prefix="/groups/auth")


# @bp.route("/login", methods=["POST"])
# def login():
#     form_data = request.json
#     logger.debug(form_data)
#     username = form_data.get("username")
#     password = form_data.get("password")

#     try:

#         error = None
#         with db.connect() as conn:
#             user = conn.execute(
#                 sqlalchemy.text("""SELECT * FROM user where username = :username"""),
#                 {"username": username},
#             ).first()
#             logger.debug("user results: %s", user)

#         if user is None:
#             error = "Incorrect username"
#         elif not check_password_hash(user[2], password):
#             error = "Incorrect password"

#         if error is None:
#             session.clear()
#             session["username"] = user[1]
#             return build_success_response("Logged in", 200)
#     except Exception as error:
#         logger.exception(error)
#         return build_error_response("server error", 500)

#     return build_error_response(f"An error occurred: {error}", 400)


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


# @bp.route("/status")
# def auth_status():
#     if "username" in session:
#         logger.info("username in session: %s", session["username"])
#         return jsonify({"authenticated": True}), 200
#     logger.info("user not logged in")
#     return jsonify({"authenticated": False}), 200


# @bp.route("/logout", methods=["POST"])
# def logout():
#     try:
#         # Clear session
#         session.clear()

#         # Get the token from Authorization header
#         auth_header = request.headers.get("Authorization")
#         if auth_header and auth_header.startswith("Bearer "):
#             token = auth_header.split(" ")[1]
#             # Here you could add the token to a blacklist if you want to invalidate it
#             # For now, we'll just clear the session

#         return build_success_response("Logged out successfully", 200)
#     except Exception as e:
#         logger.error(f"Error during logout: {str(e)}")
#         return build_error_response("Logout failed", 500)


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
            decoded = jwt.decode(
                token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"]
            )

            # Store user info in Flask's g object for use in the route
            g.user_id = decoded.get("sub")
            g.battletag = decoded.get("battletag")

            return view(**kwargs)

        except jwt.ExpiredSignatureError:
            logger.warning("Expired token received")
            return build_error_response("Token has expired", 401)
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token received: {str(e)}")
            return build_error_response("Invalid token", 401)
        except Exception as e:
            logger.error(f"Unexpected error in auth: {str(e)}")
            return build_error_response("Authentication error", 500)

    return wrapped_view


# @bp.before_app_request
# def load_logged_in_user():
#     username = session.get("username")

#     if username is None:
#         g.username = None
#         logger.info("username is: %s", g.username)

#     else:
#         with db.connect() as conn:
#             result = conn.execute(
#                 sqlalchemy.text(
#                     """SELECT username FROM user WHERE username = :username"""
#                 ),
#                 {"username": username},
#             ).first()
#             g.username = result[0]
#             logger.info("user found in database: %s", g.username)

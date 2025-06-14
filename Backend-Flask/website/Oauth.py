"""OAuth2.0 integration for Blizzard Battle.net using Flask"""

from math import log
import requests
import os
import logging
from datetime import datetime, timedelta

# from functools import wraps
import jwt

from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(f"main.{__name__}")

oauth = Blueprint("oauth", __name__, url_prefix="/groups")

try:
    BLIZZARD_TOKEN_URL = "https://oauth.battle.net/token"
    BLIZZARD_REDIRECT_URI = os.environ["BLIZZARD_REDIRECT_URI"]
    BLIZZARD_CLIENT_ID = os.environ["BLIZZARD_CLIENT_ID"]
    BLIZZARD_CLIENT_SECRET = os.environ["BLIZZARD_CLIENT_SECRET"]
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
except KeyError as e:
    logger.error("Environment variable not set: %s", e)
    raise RuntimeError(f"Missing environment variable: {e}")


@oauth.route("/auth/oauth/blizzard/callback", methods=["GET"])
def blizzard_callback():
    "Get the authorization code from the URL parameters"
    logger.debug("Received OAuth callback request")
    logger.debug("Request URL: %s", request.url)
    logger.debug("Request args: %s", request.args)

    auth_code = request.args.get("code")
    if not auth_code:
        logger.error("No authorization code found in request")
        return jsonify({"error": "Authorization code not found"}), 400

    try:
        # Ensure client ID and secret are set
        if not BLIZZARD_CLIENT_ID or not BLIZZARD_CLIENT_SECRET:
            raise KeyError("Blizzard client credentials are not set")

        # Exchange the authorization code for an access token
        logger.debug("Exchanging authorization code for access token")
        logger.debug("Authorization code: %s", auth_code)
        token_response = requests.post(
            BLIZZARD_TOKEN_URL,
            auth=(BLIZZARD_CLIENT_ID, BLIZZARD_CLIENT_SECRET),
            data={
                "grant_type": "authorization_code",
                "code": auth_code,
                "redirect_uri": BLIZZARD_REDIRECT_URI,
            },
            timeout=10,
        )

        # Check if the token request was successful
        if token_response.status_code != 200:
            logger.error(
                "status code %s: message: %s",
                token_response.status_code,
                token_response.text,
            )
            return jsonify({"error": "Failed to exchange authorization code"}), 400

        token_data = token_response.json()

        # Get the access token and other relevant data
        access_token = token_data.get("access_token")
        token_type = token_data.get("token_type")
        expires_in = token_data.get("expires_in")
        logger.debug(
            "Access token: %s, Token type: %s, Expires in: %s seconds",
            access_token,
            token_type,
            expires_in,
        )

        # Get the user's Battle.net information
        user_info_response = requests.get(
            "https://oauth.battle.net/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )

        if user_info_response.status_code != 200:
            logger.error("Failed to get user information: %s", user_info_response.text)
            return jsonify({"error": "Failed to get user information"}), 400

        user_info = user_info_response.json()
        logger.debug("User info: %s", user_info)

        # Create a JWT token for the user
        if JWT_SECRET_KEY is not None:
            jwt_token = jwt.encode(
                {
                    "sub": user_info.get("sub"),
                    "battletag": user_info.get("battletag"),
                    "exp": datetime.now() + timedelta(days=1),
                },
                JWT_SECRET_KEY,
                algorithm="HS256",
            )

            # Return the JWT token and user info
            return jsonify(
                {
                    "token": jwt_token,
                    "user": {
                        "id": user_info.get("sub"),
                        "battletag": user_info.get("battletag"),
                    },
                }
            )

        # If JWT_SECRET_KEY is None, raise an error
        raise KeyError("JWT secret key is not set")

    except requests.exceptions.RequestException as e:
        logger.error("Request exception during OAuth callback: %s", e)
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.exception("An unexpected error occurred during OAuth callback: %s", e)
        return jsonify({"error": "An unexpected error occurred"}), 500

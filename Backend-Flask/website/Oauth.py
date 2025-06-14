"""OAuth2.0 integration for Blizzard Battle.net using Flask"""

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

oauth = Blueprint("oauth", __name__)

BLIZZARD_TOKEN_URL = "https://oauth.battle.net/token"
BLIZZARD_REDIRECT_URI = os.getenv("BLIZZARD_REDIRECT_URI")
BLIZZARD_CLIENT_ID = os.getenv("BLIZZARD_CLIENT_ID")
BLIZZARD_CLIENT_SECRET = os.getenv("BLIZZARD_CLIENT_SECRET")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


@oauth.route("/api/oauth/blizzard/callback")
def blizzard_callback():
    "Get the authorization code from the URL parameters"
    auth_code = request.args.get("code")
    if not auth_code:
        return jsonify({"error": "Authorization code not found"}), 400

    try:
        # Ensure client ID and secret are set
        if not BLIZZARD_CLIENT_ID or not BLIZZARD_CLIENT_SECRET:
            raise KeyError("Blizzard client credentials are not set")

        # Exchange the authorization code for an access token
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
            return jsonify({"error": "Failed to exchange authorization code"}), 400

        token_data = token_response.json()

        # Get the access token and other relevant data
        access_token = token_data.get("access_token")
        token_type = token_data.get("token_type")
        expires_in = token_data.get("expires_in")

        # Get the user's Battle.net information
        user_info_response = requests.get(
            "https://oauth.battle.net/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )

        if user_info_response.status_code != 200:
            return jsonify({"error": "Failed to get user information"}), 400

        user_info = user_info_response.json()

        # Create a JWT token for the user
        if JWT_SECRET_KEY is not None:
            jwt_token = jwt.encode(
                {
                    "sub": user_info.get("sub"),
                    "battletag": user_info.get("battletag"),
                    "exp": datetime.utcnow() + timedelta(days=1),
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
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.exception("An unexpected error occurred during OAuth callback: %s", e)
        return jsonify({"error": "An unexpected error occurred"}), 500

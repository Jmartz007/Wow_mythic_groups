import os
import logging
import requests
from flask import Blueprint, request, jsonify, g

from website.auth import login_required

logger = logging.getLogger(f"main.{__name__}")

# You may want to set this dynamically based on region
BLIZZARD_API_BASE = "https://us.api.blizzard.com"
PROFILE_ENDPOINT = "/profile/user/wow"

wow_profile = Blueprint("wow_profile", __name__, url_prefix="/groups")


@wow_profile.route("api/profile/import-characters", methods=["GET"])
@login_required
def get_wow_characters():
    """
    Fetch the user's WoW account and character list from Battle.net Profile API.
    Requires a valid Bearer access token in the Authorization header.
    """
    auth_token = request.headers.get("Authorization")
    if not auth_token or not auth_token.startswith("Bearer "):
        logger.error("Missing or invalid Authorization header")
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    logger.debug("g properties: %s", g.__dict__)
    access_token = g.get("access_token")
    if not access_token:
        logger.error("No access token found in g object")
        return jsonify({"error": "No access token found"}), 401

    logger.debug("Fetching WoW profile with access token: %s", access_token)
    try:
        response = requests.get(
            f"{BLIZZARD_API_BASE}{PROFILE_ENDPOINT}",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"namespace": "profile-us", "locale": "en_US"},
            timeout=10,
        )
        if response.status_code != 200:
            try:
                error_data = response.json()
                logger.error("Failed to fetch WoW profile: %s", error_data)
            except ValueError:
                # If the response is not JSON, log the raw text
                logger.error("Failed to fetch WoW profile: %s", response.text)
            finally:
                return (
                    jsonify({"error": "Failed to fetch WoW profile"}),
                    response.status_code,
                )

        profile_data = response.json()
        return jsonify(profile_data)

    except requests.exceptions.RequestException as e:
        logger.error("Request exception while fetching WoW profile: %s", e)
        return jsonify({"error": str(e)}), 500

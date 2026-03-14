"""Service to fetch character data from Blizzard OAuth API"""

import logging
import os

import requests
from utils.customexceptions import (
    ServiceException,
    DataNotFoundError,
)

logger = logging.getLogger(f"main.{__name__}")

# Blizzard API endpoints
US_USER_PROFILE_URL = "https://us.api.blizzard.com/profile/user/wow"
EU_CHARACTER_API_URL = "https://eu.api.blizzard.com/profile/wow/character/"
US_CHARACTER_API_URL = "https://us.api.blizzard.com/profile/wow/character/"
REGION_URL = os.environ.get("BLIZZARD_API_REGION", "us").lower()

# Default Blizzard OAuth scope for character data
CHARACTER_OAUTH_SCOPE = "wow.profile"


def get_character_api_url():
    """Returns the appropriate character API URL based on region."""
    return EU_CHARACTER_API_URL if REGION_URL == "eu" else US_CHARACTER_API_URL


def get_user_profile(access_token: str) -> list[dict]:
    try:
        response = requests.get(
            US_USER_PROFILE_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            params={
                "region": "us",
                "namespace": "profile-us",
                "locale": "en_US",
            },  # Adjust namespace based on region
            timeout=10,
        )
        if response.status_code != 200:
            logger.error("Failed to fetch user profile: %s", response.text)
            raise ServiceException(f"Failed to fetch user profile: {response.text}")

        character_data = (
            response.json().get("wow_accounts", [])[0].get("characters", [])
        )
        # logger.debug("Character data:\n %s", character_data)
        character_list = []
        for i in character_data:
            character_list.append(i.get("name"))

        logger.debug("Character names: %s", character_list)
        return character_data

    except requests.RequestException as e:
        logger.error("Error fetching user profile: %s", e)
        raise ServiceException(f"Error fetching user profile: {e}")


def get_character_list_from_blizzard(
    character_data: list[dict], battletag: str, access_token: str
) -> list[dict]:
    """
    Fetches the list of characters for a player from Blizzard API.

    Args:
        character_data (list[dict]): The list of character data fetched from the user profile
        battletag (str): The Blizzard BattleTag of the player (e.g., #1234)
        access_token (str): The OAuth access token from Blizzard

    Returns:
        list[dict]: List of character dictionaries containing character info

    Raises:
        customexceptions.ServiceException: If API request fails
        customexceptions.DataNotFoundError: If no characters found for player
    """
    logger.info("Fetching character list from Blizzard API")
    logger.info("Battletag: %s", battletag)

    url = get_character_api_url()
    character_list = []

    for c in character_data:
        realmSlug = c.get("realm", {}).get("slug")
        characterName = c.get("name", "").lower()
        logger.debug("Processing character: %s on realm: %s", characterName, realmSlug)

        try:
            # Make the API request to get character list
            response = requests.get(
                f"{url}/{realmSlug}/{characterName}",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                },
                params={
                    "region": "us",
                    "namespace": "profile-us",
                    "locale": "en_US",
                },
                timeout=15,
            )

            # Log the response status and details
            logger.debug("Blizzard API response status: %s", response.status_code)

            if response.status_code != 200:
                logger.error(
                    "Blizzard API request failed with status: %s", response.status_code
                )
                logger.error("Blizzard API response: %s", response.text)
                raise ServiceException(f"Blizzard API request failed: {response.text}")

            # Parse the response data
            characters = response.json()
            logger.debug("Blizzard API response data: %s", characters)

            # Transform the API response into a usable format
            transformed_char = {
                "character_id": characters.get("id"),
                "character_name": characters.get("name"),
                "realm": characters.get("realm", {}).get("name"),
                "realm_id": characters.get("realm", {}).get("id"),
                "realm_slug": characters.get("realm", {}).get("slug"),
                "level": characters.get("level"),
                "item_level": characters.get("average_item_level"),
                "faction": characters.get("faction", {}).get("name"),
                "class": characters.get("character_class", {}).get("name"),
                "specialization": characters.get("active_spec", {}).get("name"),
                "guild": characters.get("guild", {}).get("name"),
            }
            character_list.append(transformed_char)

            logger.info(
                "Transformed character: %s", transformed_char.get("character_name")
            )

        except requests.exceptions.Timeout:
            logger.error("Request to Blizzard API timed out")
            # raise ServiceException("Request to Blizzard timed out")

        except requests.exceptions.ConnectionError as e:
            logger.error("Connection error: %s", e)
            # raise ServiceException("Could not connect to Blizzard API")

        except requests.exceptions.RequestException as e:
            logger.error("Request exception: %s", e)
            # raise ServiceException(f"Failed to fetch characters: {e}")

        except Exception as e:
            logger.exception("Unexpected error fetching characters: %s", e)
            # raise ServiceException(f"An unexpected error occurred: {e}")

    return character_list


def get_character_by_id(access_token: str, character_id: str) -> dict | None:
    """
    Fetches a single character by ID from Blizzard API.

    Args:
        access_token (str): The OAuth access token from Blizzard
        character_id (str): The Blizzard character ID

    Returns:
        dict | None: Character data or None if not found

    Raises:
        customexceptions.ServiceException: If API request fails
    """
    logger.info("Fetching character details from Blizzard API")
    logger.info("Character ID: %s", character_id)

    url = get_character_api_url()

    try:
        response = requests.get(
            f"{url}/{character_id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            timeout=15,
        )

        logger.debug("Blizzard API response status: %s", response.status_code)

        if response.status_code == 404:
            logger.info("Character not found for ID: %s", character_id)
            return None

        if response.status_code != 200:
            logger.error("Blizzard API request failed: %s", response.text)
            raise ServiceException(f"Failed to fetch character: {response.text}")

        return response.json()

    except requests.exceptions.RequestException as e:
        logger.error("Request exception: %s", e)
        raise ServiceException(f"Failed to fetch character: {e}")

    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        raise


def get_player_battletag(access_token: str) -> str:
    """
    Extracts the player's BattleTag from the Blizzard API.

    Args:
        access_token (str): The OAuth access token from Blizzard

    Returns:
        str: The player's BattleTag (e.g., #1234)
    """
    try:
        response = requests.get(
            get_character_api_url(),
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )

        if response.status_code != 200:
            raise ServiceException(f"Failed to fetch player info: {response.text}")

        data = response.json()
        battletag = (
            data.get("account", {}).get("name", "") if data.get("account") else ""
        )

        logger.info("Retrieved BattleTag from Blizzard: %s", battletag)
        return battletag

    except ServiceException:
        raise
    except Exception as e:
        logger.exception("Error getting BattleTag: %s", e)
        raise ServiceException(f"Failed to get BattleTag: {e}")


def delete_character_from_blizzard(access_token: str, character_id: str) -> bool:
    """
    Deletes a character from the user's Blizzard profile.
    Note: This typically just removes from roster, doesn't delete the actual character.

    Args:
        access_token (str): The OAuth access token from Blizzard
        character_id (str): The Blizzard character ID

    Returns:
        bool: True if character was removed, False otherwise

    Raises:
        customexceptions.ServiceException: If API request fails
    """
    logger.info("Removing character from Blizzard profile")
    logger.info("Character ID: %s", character_id)

    try:
        response = requests.delete(
            f"{get_character_api_url()}/{character_id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            timeout=15,
        )

        logger.debug("Blizzard DELETE response status: %s", response.status_code)

        if response.status_code in [200, 202]:  # 200 OK, 202 Accepted
            logger.info("Successfully removed character from profile: %s", character_id)
            return True

        logger.error("Failed to remove character: %s", response.text)
        return False

    except requests.exceptions.RequestException as e:
        logger.error("Request exception: %s", e)
        raise ServiceException(f"Failed to remove character: {e}")

    except Exception as e:
        logger.exception("Unexpected error removing character: %s", e)
        raise ServiceException(f"Failed to remove character: {e}")


def refresh_access_token(client_id: str, client_secret: str, auth_code: str) -> str:
    """
    Refreshes the Blizzard access token using authorization code.

    Args:
        client_id (str): Blizzard OAuth client ID
        client_secret (str): Blizzard OAuth client secret
        auth_code (str): The authorization code from the redirect

    Returns:
        str: The new access token

    Raises:
        customexceptions.ServiceException: If token refresh fails
    """
    logger.info("Refreshing Blizzard access token")

    token_url = "https://oauth.battle.net/token"

    try:
        response = requests.post(
            token_url,
            auth=(client_id, client_secret),
            data={
                "grant_type": "authorization_code",
                "code": auth_code,
                "redirect_uri": os.environ.get("BLIZZARD_REDIRECT_URI", ""),
                "scope": CHARACTER_OAUTH_SCOPE,
            },
            timeout=15,
        )

        if response.status_code != 200:
            logger.error("Token refresh failed: %s", response.text)
            raise ServiceException(f"Token refresh failed: {response.text}")

        token_data = response.json()
        new_token = token_data.get("access_token")

        logger.info("Successfully refreshed access token")
        return new_token

    except requests.exceptions.RequestException as e:
        logger.error("Token refresh exception: %s", e)
        raise ServiceException(f"Token refresh failed: {e}")

    except Exception as e:
        logger.exception("Unexpected error refreshing token: %s", e)
        raise ServiceException(f"Token refresh failed: {e}")

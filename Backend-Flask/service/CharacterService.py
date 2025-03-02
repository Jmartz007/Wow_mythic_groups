from ast import Dict
from collections import defaultdict
from email.policy import default
import logging
from typing import DefaultDict

from sqlalchemy import exc


from utils.customexceptions import (
    CharacterNotFoundError,
    DataNotFoundError,
    DatabaseError,
    ServiceException,
)

from datagatherer.playerdata import (
    db_get_all_info_for_character,
    db_find_character_by_name,
    delete_char_from_db,
)
from datagatherer.mythickeydata import db_get_key_info_by_id, db_udpate_key_data


logger = logging.getLogger(f"main.{__name__}")


def get_character_data(character_name: str):
    """
    Get all character data for a given character name

    Args:
        character_name (str): The name of the character

    Returns:
        dict: A dictionary containing all character data
    """
    try:
        character = db_find_character_by_name(character_name)
        if not character:
            raise CharacterNotFoundError(f"Character not found: {character_name}")

        char_info_list = db_get_all_info_for_character(character[1])

        data = []
        for char_info in char_info_list:
            char_data = {
                "character_name": char_info[1],
                "class_name": char_info[2],
                "party_role": char_info[4],
                "role_range_name": char_info[5],
                "role_skill": char_info[6],
                "dungeon_name": char_info[7],
                "level": char_info[8],
            }
            data.append(char_data)

        return data
    except CharacterNotFoundError:
        raise
    except exc.SQLAlchemyError as e:
        logger.exception("A sql error occurred: %s", e)
        raise DatabaseError("An error occurred in the database")
    except Exception as e:
        logger.exception("An error occurred: %s", e)
        raise ServiceException("An error occurred")


def delete_character_service(character_name: str):
    try:
        num_deleted = delete_char_from_db(character_name)
        if num_deleted > 0:
            return True
        else:
            return False
    except Exception as e:
        logger.error(e)
        raise e


def update_character_key(character_name: str, data: Dict):
    """Updates the given characters key info"""

    try:
        new_dungeon = data.get("Dungeon", None)
        new_level = data.get("Key Level", None)
        if new_dungeon is None and new_level is None:
            raise ServiceException("No data to update")

        new_level = int(new_level)

        if new_level < 0:
            raise ServiceException("Invalid Key number. Must be integer greater than 0")

        result = db_udpate_key_data(character_name, new_dungeon, new_level)

        if result < 1:
            raise DataNotFoundError("Character or dungeon not found")

        return result
    except KeyError as e:
        logger.error("key error: %s", e)
        raise ServiceException("Invalid or missing data")
    except ValueError as e:
        logger.error("ValueError: %s", e)
        raise ServiceException("Invalid Key Number. Must be integer")
    except Exception as e:
        logger.exception(e)
        raise

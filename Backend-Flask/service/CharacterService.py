from collections import defaultdict
from email.policy import default
import logging
from typing import DefaultDict

from sqlalchemy import exc


from utils.customexceptions import *

from datagatherer.playerdata import (
    db_find_player_by_name,
    db_find_player_id,
    db_get_all_info_for_character,
    db_get_character_for_player,
    db_find_character_by_name,
    get_all_players,
    delete_player_from_db,
    delete_char_from_db,
)
from datagatherer.mythickeydata import db_get_key_info_by_id


logger = logging.getLogger(f"main.{__name__}")


# TODO: #47 implement logic for getting all character data including mythic key info
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

        char_info = db_get_all_info_for_character(character[1])

        data = {
            "character_name": char_info[1],
            "class_name": char_info[2],
            "party_role": char_info[4],
            "role_range_name": char_info[5],
            "role_skill": char_info[6],
            "dungeon_name": char_info[7],
            "level": char_info[8],
        }
        return data
    except CharacterNotFoundError:
        raise
    except exc.SQLAlchemyError as e:
        logger.exception(f"A sql error occurred: {e}")
        raise DatabaseError("An error occurred in the database")
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        raise ServiceException("An error occurred")

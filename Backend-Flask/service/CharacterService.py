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
        logger.exception(f"A sql error occurred: {e}")
        raise DatabaseError("An error occurred in the database")
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
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

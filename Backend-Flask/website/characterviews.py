import logging
import functools

from flask import Blueprint, Response, request, session, jsonify
import sqlalchemy
from service.PlayersService import (
    get_all_chars_from_player,
    process_player_data,
    process_data_to_frontend,
    del_char,
)
from service.CharacterService import *

from utils.customexceptions import DataNotFoundError, DatabaseError
from utils.helpers import build_success_response, build_error_response


logger = logging.getLogger(f"main.{__name__}")

# api_bp = Blueprint("characters", __name__, url_prefix="/groups/api")
char_bp = Blueprint("characters", __name__, url_prefix="/players/<player_name>/")


@char_bp.route("/characters", methods=["GET"])
def get_characters_for_player(player_name):
    logger.debug(f"player_name is: {player_name}")
    data = get_all_chars_from_player(player_name)
    logger.debug(data)
    return jsonify(data)


@char_bp.route("/characters/<character_name>", methods=["GET"])
def get_characters_by_name(player_name, character_name):
    logger.debug(f"character_name is: {character_name}")
    data = get_character_data(character_name)
    logger.debug(data)
    return jsonify(data)


@char_bp.route("/characters/<character_name>", methods=["DELETE"])
def delete_character_request(player_name, character_name):
    logger.debug(
        f"Attempting to delete character name: {character_name}, from player name: {player_name}"
    )
    deleted = delete_character_service(character_name)
    if deleted:
        return build_success_response("Character deleted", 200)
    else:
        return build_error_response("Character not found", 404)

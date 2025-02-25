import logging

from flask import Blueprint, jsonify, request
from service.PlayersService import get_all_chars_from_player
from service.CharacterService import delete_character_service, get_character_data

from utils.helpers import build_success_response, build_error_response


logger = logging.getLogger(f"main.{__name__}")

char_bp = Blueprint("characters", __name__, url_prefix="/players/<player_name>/")


@char_bp.route("/characters", methods=["GET"])
def get_characters_for_player(player_name):
    """Gets all the characters' data for the player_name in the url paramter"""
    logger.debug("player_name is: %s", player_name)
    data = get_all_chars_from_player(player_name)
    logger.debug(data)
    return jsonify(data)


@char_bp.route("/characters/<character_name>", methods=["GET"])
def get_characters_by_name(player_name, character_name):
    """Gets character information based on the character_name url parameter"""
    logger.debug("character_name is: %s", character_name)
    data = get_character_data(character_name)
    logger.debug(data)
    return jsonify(data)


@char_bp.route("/characters/<character_name>", methods=["DELETE"])
def delete_character_request(player_name, character_name):
    """Deletes a character based on the character_name url paramter"""
    logger.debug(
        "Attempting to delete character name: %s{}, from player name: %s",
        character_name,
        player_name,
    )
    deleted = delete_character_service(character_name)
    if deleted:
        return build_success_response("Character deleted", 200)

    return build_error_response("Character not found", 404)


@char_bp.route("/characters/<character_name>", methods=["PATCH"])
def update_character_info(player_name, character_name):
    """Updates the character information based on the body of the request"""
    logger.debug("character_name is: %s", character_name)
    data = request.json
    logger.debug("request body is: %s", data)
    return jsonify(data)

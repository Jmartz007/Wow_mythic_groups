import logging
from os import access
from urllib import response

from flask import Blueprint, request, jsonify, g
import jwt

from service.PlayersService import (
    delete_player_by_id_or_name,
    get_player_by_name,
    process_player_data,
    process_data_to_frontend,
)

from utils.customexceptions import DataNotFoundError, DatabaseError
from utils.helpers import (
    build_data_response,
    build_success_response,
    build_error_response,
)
from .auth import login_required
from .characterviews import char_bp
from .Oauth import JWT_SECRET_KEY


logger = logging.getLogger(f"main.{__name__}")

bp = Blueprint("players", __name__, url_prefix="/groups/api")


@bp.route("/players", methods=["POST"])
def add_new_player():
    """Endpoint that accepts a post request with form data to enter a new player
    into the database"""
    try:
        data = request.get_json()
        logger.debug("Form data from request: %s", data)
        character_name = data["characterName"]
        result = process_player_data(data)
        if result:
            logger.info("Character %s added successfully", character_name)
            return build_success_response(f"Character {character_name} added", 201)
        return build_error_response("could not add character", 500)
    except DatabaseError as sqlerror:
        return build_error_response("a database error occurred", 500, sqlerror)
    except Exception as e:
        return build_error_response("a server error occurred", 500, e)


@bp.route("/players/characters", methods=["POST"])
@login_required
def import_characters():
    """Endpoint that accepts a post request with json data to import characters"""

    player_name = g.get("battletag")
    logger.info("Importing characters for player name : %s", player_name)
    try:
        if not player_name:
            logger.error("Player name not found in token")
            return jsonify({"message": "Player name not found in token"}), 401

        # Get the character data from the request body
        character_data = request.json
        logger.debug("Character data from request: %s", character_data)

        if not character_data or not isinstance(character_data, list):
            return build_error_response("Invalid data format", 400)
        character_response = []
        for char in character_data:
            character_info = {}
            character_info["name"] = char.get("name")
            character_info["level"] = char.get("level")
            character_info["class"] = char.get("playable_class").get("name")
            character_info["realm"] = char.get("realm").get("name")
            character_response.append(character_info)

        response_data = {"player_name": player_name, "characters": character_response}
        return build_data_response(response_data, 200)

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

    # TODO: Create logic to insert characters into the database
    try:
        character_name = character_data["characterName"]
        result = process_player_data(character_data)
        if result:
            logger.info("Character %s added successfully", character_name)
            return build_success_response(f"Character {character_name} added", 201)
        return build_error_response("could not add character", 500)
    except DatabaseError as sqlerror:
        return build_error_response("a database error occurred", 500, sqlerror)
    except Exception as e:
        return build_error_response("a server error occurred", 500, e)


@bp.route("/players", methods=["GET"])
@login_required
def players():
    try:
        data = process_data_to_frontend()
        return jsonify(data), 200
    except DatabaseError as e:
        logger.error(e)
        raise DatabaseError  # DatabaseErrors are handled by global error handlers
    except Exception as e:
        logger.exception(e)
        return build_error_response("error occurred getting player data", 500)


@bp.route("/players-flat", methods=["GET"])
@login_required
def players_flat():
    try:
        data = process_data_to_frontend(flattened=True)
        return jsonify(data), 200
    except DatabaseError as e:
        logger.error(e)
        raise DatabaseError
    except Exception as e:
        logger.exception(e)
        return build_error_response("error occurred getting player data", 500)


@bp.route("/players/<player_name>", methods=["GET"])
def get_player_request(player_name):
    try:
        data = get_player_by_name(player_name)
        return jsonify(data), 200
    except DatabaseError as e:
        logger.error(e)
        raise DatabaseError  # DatabaseErrors are handled by global error handlers
    except Exception as e:
        logger.exception(e)
        return build_error_response("error occurred getting player data", 500)


@bp.route("/players/<id>", methods=["DELETE"])
def del_player(id):
    try:
        result = delete_player_by_id_or_name(id)
        return build_success_response(f"removed player: {id}", 200)
    except DataNotFoundError as e:
        logger.warning(e)
        raise
    except Exception as e:
        logger.error(e)
        return build_error_response("could not delete player", exception=e)


bp.register_blueprint(char_bp)

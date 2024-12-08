import logging

from flask import Blueprint, request, jsonify
from service.PlayersService import (
    delete_player_by_id_or_name,
    get_all_chars_from_player,
    get_player_by_name,
    process_player_data,
    process_data_to_frontend,
)

from utils.customexceptions import DataNotFoundError, DatabaseError
from utils.helpers import build_success_response, build_error_response


logger = logging.getLogger(f"main.{__name__}")

bp = Blueprint("players", __name__, url_prefix="/groups/api")


@bp.route("/addplayer", methods=["POST"])
def add_new_player():
    try:
        data = request.get_json()
        logger.debug(f"Form data from request: {data}")
        characterName = data["characterName"]
        result = process_player_data(data)
        if result == True:
            logger.info(f"Character {characterName} added successfully")
            return build_success_response(f"Character {characterName} added", 201)
    except DatabaseError as sqlerror:
        build_error_response("a database error occurred", 500, sqlerror)
    except Exception as e:
        build_error_response("a server error occurred", 500)


@bp.route("/players", methods=["GET"])
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


char_bp = Blueprint("characters", __name__, url_prefix="/players/<player_name>/")


@char_bp.route("/characters", methods=["GET"])
def get_characters_for_player(player_name):
    logger.debug(f"player_name is: {player_name}")
    data = get_all_chars_from_player(player_name)
    logger.debug(data)
    return jsonify(data)


bp.register_blueprint(char_bp)

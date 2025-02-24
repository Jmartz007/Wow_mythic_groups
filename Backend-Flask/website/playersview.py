import logging

from flask import Blueprint, request, jsonify
from service.PlayersService import (
    delete_player_by_id_or_name,
    get_player_by_name,
    process_player_data,
    process_data_to_frontend,
)

from utils.customexceptions import DataNotFoundError, DatabaseError
from utils.helpers import build_success_response, build_error_response
from .auth import login_required
from .characterviews import char_bp


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


# TODO: need to find a good spot for this
# @bp.route("/characters", methods=["GET"])
# def get_all_characters():
#     try:
#         result = process_data_to_frontend(flattened=True)
#         if not result:
#             raise DataNotFoundError()
#         else:
#             return jsonify(result), 200
#     except Exception as e:
#         return build_error_response("an error occurred", exception=e)


bp.register_blueprint(char_bp)

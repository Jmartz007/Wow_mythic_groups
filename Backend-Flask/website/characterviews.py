import logging
import functools

from flask import Blueprint, Response, request, session, jsonify
import sqlalchemy
from service.PlayersService import (
    process_player_data,
    process_data_to_frontend,
    del_char,
)

from utils.customexceptions import DataNotFoundError, DatabaseError
from utils.helpers import build_success_response, build_error_response


logger = logging.getLogger(f"main.{__name__}")

api_bp = Blueprint("characters", __name__, url_prefix="/groups/api")


@api_bp.route("/characters", methods=["GET"])
def get_all_characters():
    try:
        result = process_data_to_frontend(flattened=True)
        if not result:
            raise DataNotFoundError()
        else:
            return jsonify(result), 200
    except Exception as e:
        return build_error_response("an error occurred", exception=e)


@api_bp.route("/characters", methods=["DELETE"])
def delete_character_request():
    try:
        data = request.json
        logger.debug(f"form data from request: {data}")
        character_name = data["Character"]
        result = del_char(character_name)
        if result > 0:
            logger.info(f"Num of rows deleted: {result} for {character_name}")
            return build_success_response(
                f"successfully deleted character {character_name}", 200
            )
        else:
            logger.warning(f"character {character_name} not found")
            return build_error_response(f"character {character_name} not found", 404)
    except Exception as e:
        build_error_response("an error occurred")

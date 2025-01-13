import logging

from flask import Blueprint, request, jsonify

from service.DungeonService import (
    add_dungeon,
    del_dungeon_by_id_or_name,
    get_dungeon_by_id_or_name,
    get_dungeons_all,
)

from utils.customexceptions import DataNotFoundError, DatabaseError
from utils.helpers import build_success_response, build_error_response


logger = logging.getLogger(f"main.{__name__}")

api_bp = Blueprint("dungeons", __name__, url_prefix="/groups/api")


@api_bp.route("/dungeons", methods=["GET"])
def get_dungeons_request():
    try:
        data = get_dungeons_all()
        return jsonify(data), 200
    except Exception as e:
        return build_error_response()


@api_bp.route("/dungeons/<id>", methods=["GET"])
def get_dungeon_by_id_request(id):
    try:
        data = get_dungeon_by_id_or_name(id)
        return jsonify(data), 200
    except Exception as e:
        logger.exception(e)
        return build_error_response(exception=e)


@api_bp.route("/dungeons/<id>", methods=["DELETE"])
def del_dungeon_request(id):
    try:
        result = del_dungeon_by_id_or_name(id)
        if result:
            return build_success_response(f"removed dungeon: {id}", 200)
        else:
            return build_error_response("could not delete dungeon")
    except Exception as e:
        logger.error(e)
        return build_error_response("could not delete dungeon", exception=e)


@api_bp.route("/dungeons", methods=["POST"])
def add_dungeon_request():
    try:
        data = request.form.to_dict()
        logger.debug(f"form data from request: {data}")
        dungeon_name = data["Dungeon"]
        result = add_dungeon(dungeon_name)
        return build_success_response(f"new dungeon added: {result}", status_code=201)
    except Exception as e:
        return build_error_response(f"Could not add dungeon, {e}", exception=e)

import logging
import functools

from flask import Blueprint, Response, request, session, jsonify
import sqlalchemy
from service.PlayersService import (
    process_player_data,
    process_data_to_frontend,
    delete_player,
    del_char,
)
from service.DungeonService import (
    add_dungeon,
    del_dungeon_by_id_or_name,
    get_dungeon_by_id,
    get_dungeons_all,
)

from utils.customexceptions import DataNotFoundError, DatabaseError
from utils.helpers import build_success_response, build_error_response


logger = logging.getLogger(f"main.{__name__}")

api_bp = Blueprint("api", __name__, url_prefix="/groups/api")


@api_bp.route("/players", methods=["GET", "POST"])
def players():
    if request.method == "POST":
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

    if request.method == "GET":
        try:
            data = process_data_to_frontend()
            return jsonify(data), 200
        except DatabaseError as e:
            logger.error(e)
            raise DatabaseError  # DatabaseErrors are handled by global error handlers
        except Exception as e:
            logger.exception(e)
            return build_error_response("error occurred getting player data", 500)


@api_bp.route("/players-flat", methods=["GET"])
def players_flat():
    if request.method == "GET":
        try:
            data = process_data_to_frontend(flattened=True)
            return jsonify(data), 200
        except DatabaseError as e:
            logger.error(e)
            raise DatabaseError
        except Exception as e:
            logger.exception(e)
            return build_error_response("error occurred getting player data", 500)
            # return Response(
            #     status=500,
            #     response="An error occurred processing your request.",
            # )


@api_bp.route("/players", methods=["DELETE"])
def del_player():
    if request.method == "DELETE":
        try:
            data = request.json
            logger.debug(f"form data from request: {data}")
            player_name = data["playerName"]
            result = delete_player(player_name)
            if result > 0:
                logger.info(
                    f"Num of rows deleted: {result} for {player_name} deleted succesfully"
                )
                return build_success_response(f"Player {player_name} deleted", 200)
                # return (jsonify("Player deleted"), 204)
            else:
                logger.warning(f"player not found")
                return build_error_response(f"Player {player_name} not found", 404)
                # return (f"Player {player_name} not found", 404)
        except DatabaseError as e:
            logger.error(e)
            raise DatabaseError


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
            # return jsonify(f"Character {character_name} not found"), 404
    except Exception as e:
        build_error_response("an error occurred")


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
        data = get_dungeon_by_id(id)
        return jsonify(data), 200
    except DataNotFoundError as e:
        logger.warning(e)
        return build_error_response("Dungeon id not found", 404)
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
        data = request.json
        logger.debug(f"form data from request: {data}")
        dungeon_name = data["Dungeon"]
        result = add_dungeon(dungeon_name)
        return build_success_response(f"new dungeon added: {result}", status_code=201)
    except Exception as e:
        return build_error_response("an error occurred", exception=e)

import logging
import functools

from flask import Blueprint, Response, request, session, jsonify
from service.PlayersService import (
    process_player_data,
    process_data_to_frontend,
    delete_player,
    del_char
)

from utils.customexceptions import DatabaseError
from utils.helpers import build_success_message, build_error_message

logger = logging.getLogger(f"main.{__name__}")

api_bp = Blueprint("api", __name__, url_prefix="/groups/api")


@api_bp.route("/players", methods=["GET", "POST"])
def players():
    if request.method == "POST":
        data = request.get_json()
        logger.debug(f"Form data from request: {data}")
        characterName = data["characterName"]
        result = process_player_data(data)
        if result == True:
            logger.info(f"Character {characterName} added successfully")
            return build_success_message(f"Character {characterName} added", 201)
            return ("Character added", 200)
        elif result == False:
            return build_error_message()
            return Response(
                status=500,
                response="Unable to successfully sign up player! Please check the application logs for more details.",
            )
    if request.method == "GET":
        try:
            data = process_data_to_frontend()
            return jsonify(data), 200
        except DatabaseError as e:
            logger.error(e)
            raise DatabaseError
        except Exception as e:
            logger.exception(e)
            return Response(
                status=500,
                response="An error occurred processing your request.",
            )
        
@api_bp.route("/players", methods=["DELETE"])
def del_player():
    if request.method == "DELETE":
        try:
            data = request.json
            logger.debug(f"form data from request: {data}")
            player_name = data["playerName"]
            result = delete_player(player_name)
            if result > 0:
                logger.info(f"No of rows deleted: {result} for {player_name} deleted succesfully")
                return (jsonify("Player deleted"), 204)
            else:
                logger.warning(f"player not found")
                return (f"Player {player_name} not found", 404)
        except DatabaseError as e:
            return (jsonify("An error occurred processing your request."), 500)


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
            return Response(
                status=500,
                response="An error occurred processing your request.",
            )

@api_bp.route("/characters", methods=["DELETE"])
def delete_character_request():
    try:
        data = request.json
        logger.debug(f"form data from request: {data}")
        character_name = data["characterName"]
        result = del_char(character_name)
        if result >0:
            logger.info(f"Num of rows deleted: {result} for {character_name}")
            return build_success_message("successfully deleted character", 200)
        else:
            logger.warning(f"character {character_name} not found")
            return build_error_message(e, 404)
            # return jsonify(f"Character {character_name} not found"), 404

    except DatabaseError as e:
        return jsonify("A database error occurred processing your request."), 500
    
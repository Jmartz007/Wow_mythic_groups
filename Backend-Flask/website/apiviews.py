import logging
import functools

from flask import Blueprint, Response, request, session, jsonify
from service.PlayersService import (
    process_player_data,
    process_data_to_frontend,
)

from utils.customexceptions import DatabaseError

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
            return ("Character added", 200)
        elif result == False:
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

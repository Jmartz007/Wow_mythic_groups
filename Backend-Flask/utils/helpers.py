from flask import jsonify
from typing import Optional

import logging

logger = logging.getLogger(f"main")


def build_success_response(message: str, status_code: int):
    return jsonify({"message": message}), status_code


def build_data_response(data: dict, status_code: int = 200):
    return jsonify(data), status_code


def build_error_response(
    message: str = "an error occurred",
    status_code: int = 500,
    exception: Optional[Exception] = None,
) -> tuple:
    """
    Helper function to build an error response.

    Args:
        message (str): Custom error message to include in the response.
        status_code (int): HTTP status code for the error.
        exception (Optional[Exception]): Optional exception to include in the error response.

    Returns:
        tuple: Flask JSON response and status code tuple
    """
    error_response = {
        "error": {
            "message": message,
            "status_code": status_code,
        }
    }

    if exception:
        logger.error(f"{message}: {exception}")
        error_response["error"]["details"] = str(exception)

    return jsonify(error_response), status_code

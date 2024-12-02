from flask import jsonify

def build_success_message(message: str, status_code: int):
    return jsonify({"message": message}), status_code

def build_error_message(error_msg, status_code: int=500, error=None ):
    return jsonify({"error": error_msg}), status_code
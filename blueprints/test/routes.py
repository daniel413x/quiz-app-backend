import os
from flask import Blueprint, jsonify
from consts.routes import TEST_ROUTE

test_bp = Blueprint(f"{TEST_ROUTE}", __name__)

@test_bp.route("", methods=["GET"])
def index():
    return jsonify({"messsage": "The server is running"})

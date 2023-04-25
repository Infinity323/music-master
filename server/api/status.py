from flask import Blueprint, jsonify
import platform

# Check status route
status_blueprint = Blueprint("status", __name__)
@status_blueprint.route("/status", methods=["GET"])
def get_status():
    return jsonify({ "status": "ready" })

# Get platform
@status_blueprint.route("/status/platform", methods=["GET"])
def get_platform():
    return jsonify({ "platform": platform.platform() })
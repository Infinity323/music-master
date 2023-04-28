from flask import Blueprint, jsonify
import platform

status_blueprint = Blueprint("status", __name__)

@status_blueprint.route("/status", methods=["GET"])
def get_status():
    """Get the status of the backend.

    Returns:
        dict: A dict of the status
    """
    return jsonify({ "status": "ready" })

@status_blueprint.route("/status/platform", methods=["GET"])
def get_platform():
    """Get the platform of the machine.

    Returns:
        dict: A dict of the platform information
    """
    return jsonify({ "platform": platform.platform() })
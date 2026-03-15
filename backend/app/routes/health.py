from flask import Blueprint, jsonify
from app.utils.logger import get_logger

logger = get_logger(__name__)

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health():
    logger.info("Health check requested")
    return jsonify({"status": "ok"})

from flask import Blueprint, jsonify, request
from dataclasses import asdict
from app.database.transcriptions import search_transcriptions
from app.utils.logger import get_logger

logger = get_logger(__name__)

search_bp = Blueprint("search", __name__)


@search_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "")
    logger.info(f"Search request for query: '{query}'")

    if not query:
        logger.warning("Search request without query parameter")
        return jsonify({"error": "Query parameter is required"}), 400

    try:
        results = search_transcriptions(query)
        logger.info(f"Search found {len(results)} results for query: '{query}'")
        return jsonify([asdict(r) for r in results])
    except Exception as e:
        logger.error(f"Search failed for query '{query}': {str(e)}")
        return jsonify({"error": str(e)}), 500

from app.database.transcriptions import insert_transcription, get_transcriptions
from flask import Blueprint, request, jsonify
import os
from dataclasses import asdict
from app.services.whisper_service import transcribe_audio
from app.database.transcriptions import get_unique_filename
from app.utils.logger import get_logger
from app.utils.file import save_temporary_file, delete_temporary_file

logger = get_logger(__name__)

transcriptions_bp = Blueprint("transcriptions", __name__)


@transcriptions_bp.route("/transcribe", methods=["POST"])
def transcribe():
    logger.info("Transcription request received")

    if "file" not in request.files:
        logger.warning("No file uploaded in request")
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    original_filename = os.path.basename(file.filename)
    unique_filename = get_unique_filename(original_filename)

    # Create temp file path
    tmp_path = save_temporary_file(file, unique_filename)

    try:
        # Transcribe using Whisper
        text = transcribe_audio(tmp_path)

        # Save to SQLite
        insert_transcription(unique_filename, text)
        logger.info(f"Transcription saved for {unique_filename}")
    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        # Ensure the temporary file is removed
        is_deleted = delete_temporary_file(tmp_path)
        if is_deleted:
            logger.info(f"Temporary file removed: {tmp_path}")
        else:
            logger.warning(f"Temporary file not found for deletion: {tmp_path}")

    return jsonify({"filename": unique_filename, "transcription": text})


@transcriptions_bp.route("/transcriptions", methods=["GET"])
def retrieve_transcriptions():
    logger.info("Retrieving all transcriptions")
    transcriptions = get_transcriptions()
    logger.info(f"Retrieved {len(transcriptions)} transcriptions")
    return jsonify([asdict(t) for t in transcriptions])

from app.database.transcriptions import insert_transcription, get_transcriptions
from flask import Blueprint, request, jsonify
import uuid, os, tempfile
from dataclasses import asdict
from app.services.whisper_service import transcribe_audio
from app.utils.logger import get_logger

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
    unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
    logger.info(f"Processing file: {original_filename} -> {unique_filename}")

    # Create temp file path
    tmp_dir = tempfile.gettempdir()
    tmp_path = os.path.join(tmp_dir, unique_filename)
    file.save(tmp_path)

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
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
            logger.info(f"Temporary file removed: {tmp_path}")

    return jsonify({"filename": unique_filename, "transcription": text})


@transcriptions_bp.route("/transcriptions", methods=["GET"])
def retrieve_transcriptions():
    logger.info("Retrieving all transcriptions")
    transcriptions = get_transcriptions()
    logger.info(f"Retrieved {len(transcriptions)} transcriptions")
    return jsonify([asdict(t) for t in transcriptions])

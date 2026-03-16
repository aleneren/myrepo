import os
from uuid import uuid4
from app.database.transcriptions import insert_transcription, get_transcriptions
from flask import Blueprint, request, jsonify
from dataclasses import asdict
from app.services.whisper_service import transcribe_audio
from app.utils.logger import get_logger

logger = get_logger(__name__)

transcriptions_bp = Blueprint("transcriptions", __name__)


@transcriptions_bp.route("/transcribe", methods=["POST"])
def transcribe():
    logger.info("Transcription request received")

    files = request.files.getlist("file")

    if not files:
        logger.warning("No file uploaded in request")
        return jsonify({"error": "No file uploaded"}), 400

    results = []
    for file in files:
        try:
            filename = os.path.basename(file.filename)
            if not filename:
                logger.error("Uploaded file has no filename")
                raise ValueError("Uploaded file must have a filename")

            # Read audio bytes
            audio_bytes = file.read()

            # Transcribe using Whisper
            text = transcribe_audio(audio_bytes)

            # Save to SQLite
            uuid = uuid4().hex
            insert_transcription(uuid, filename, text)
            logger.info(f"Transcription saved for {uuid}")
            results.append({"id": uuid, "filename": filename, "transcription": text})
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            results.append({"error": str(e)})

    return jsonify(results)


@transcriptions_bp.route("/transcriptions", methods=["GET"])
def retrieve_transcriptions():
    logger.info("Retrieving all transcriptions")
    transcriptions = get_transcriptions()
    logger.info(f"Retrieved {len(transcriptions)} transcriptions")
    return jsonify([asdict(t) for t in transcriptions])

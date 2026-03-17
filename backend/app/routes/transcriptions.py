import os
from uuid import uuid4
from app.database.transcriptions import insert_transcription, get_transcriptions
from flask import Blueprint, request, jsonify
from dataclasses import asdict
from app.services.whisper_service import transcribe_audio
from app.utils.logger import get_logger
from app.utils.file import save_temporary_file, delete_temporary_file

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
        audio_path = None
        try:
            filename = os.path.basename(file.filename)
            if not filename:
                logger.error("Uploaded file has no filename")
                raise ValueError("Uploaded file must have a filename")

            # Save to SQLite
            uuid = uuid4().hex
            audio_path = save_temporary_file(file, f"{uuid}_{filename}")
            logger.info(f"Original audio saved to temporary path: {audio_path}")

            # Transcribe using Whisper
            text = transcribe_audio(audio_path)

            # Insert into DB
            insert_transcription(uuid, filename, text)
            logger.info(f"Transcription saved for {uuid}")
            results.append({"id": uuid, "filename": filename, "transcription": text})
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            results.append({"error": str(e)})
        finally:
            is_deleted = delete_temporary_file(audio_path)
            if is_deleted:
                logger.info(f"Temporary file deleted for original audio: {audio_path}")
            else:
                logger.warning(
                    f"Failed to delete temporary file for original audio: {audio_path}"
                )

    return jsonify(results)


@transcriptions_bp.route("/transcriptions", methods=["GET"])
def retrieve_transcriptions():
    logger.info("Retrieving all transcriptions")
    transcriptions = get_transcriptions()
    logger.info(f"Retrieved {len(transcriptions)} transcriptions")
    return jsonify([asdict(t) for t in transcriptions])

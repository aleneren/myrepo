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

MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 25))
MAX_FILES = int(os.getenv("MAX_FILES", 5))


@transcriptions_bp.route("/transcribe", methods=["POST"])
def transcribe():
    logger.info("Transcription request received")

    files = request.files.getlist("file")

    if not files:
        logger.warning("No file uploaded in request")
        return jsonify({"error": "No file uploaded"}), 400

    if len(files) > MAX_FILES:
        logger.warning(
            f"Too many files uploaded: {len(files)}. Max allowed is {MAX_FILES}"
        )
        return (
            jsonify({"error": f"Too many files uploaded. Max allowed is {MAX_FILES}"}),
            400,
        )

    results = []
    for file in files:
        audio_path = None
        filename = os.path.basename(file.filename)
        try:
            if not filename:
                logger.error("Uploaded file has no filename")
                raise ValueError("Uploaded file must have a filename")

            # Save as temporary file for processing
            uuid = uuid4().hex
            audio_path = save_temporary_file(file, f"{uuid}_{filename}")
            file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
            logger.info(
                f"Original audio ({file_size_mb:.2f} MB) saved to temporary path: {audio_path}"
            )

            if file_size_mb > MAX_FILE_SIZE_MB:
                logger.warning(
                    f"File {filename} ({file_size_mb:.2f} MB) exceeds max size of {MAX_FILE_SIZE_MB} MB"
                )
                raise ValueError(
                    f"File {filename} ({file_size_mb:.2f} MB) exceeds max size of {MAX_FILE_SIZE_MB} MB"
                )

            # Transcribe using Whisper
            text = transcribe_audio(audio_path)

            # Insert into DB
            insert_transcription(uuid, filename, text)
            logger.info(f"Transcription saved for {uuid}")
            results.append({"id": uuid, "filename": filename, "transcription": text})
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            results.append({"filename": filename, "error": str(e)})
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

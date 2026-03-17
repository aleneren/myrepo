import subprocess
import numpy as np
import tempfile
import os
from transformers import pipeline
from app.utils.logger import get_logger
from app.utils.file import delete_temporary_file

logger = get_logger(__name__)

STANDARD_SAMPLING_RATE = 16000

pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-tiny",
    chunk_length_s=30,
    stride_length_s=5,
    device="cpu",  # Use CPU to miminise memory usage
)


def resample_audio_ffmpeg(audio_path: str) -> str:
    """
    Converts and resamples audio to 16kHz mono WAV using ffmpeg.
    Works with any format ffmpeg supports (mp3, ogg, webm, m4a, etc.)

    Args:
        audio_path (str): Path to the input audio file (any format).

    Returns:
        str: Path to the converted WAV temp file.
    """
    fd, tmp_wav = tempfile.mkstemp(suffix=".wav")
    os.close(fd)  # close fd before ffmpeg writes to the path
    command = [
        "ffmpeg",
        "-i",
        audio_path,  # input (any format)
        "-ac",
        "1",  # mono
        "-ar",
        str(STANDARD_SAMPLING_RATE),  # resample to 16kHz
        "-f",
        "wav",
        tmp_wav,  # separate output path
        "-loglevel",
        "error",
        "-y",
    ]
    result = subprocess.run(command, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {result.stderr.decode()}")

    return tmp_wav  # caller is responsible for cleanup


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes audio data using huggingface openai/whisper-tiny.

    Args:
        audio_path (str): Path to the original audio file.

    Returns:
        str: The transcription text.
    """
    logger.info("Starting transcription")

    try:
        resampled_audio_path = resample_audio_ffmpeg(audio_path)

        resampled_size = os.path.getsize(resampled_audio_path)
        logger.info(f"Audio converted, size: {resampled_size} bytes")

        result = pipe(resampled_audio_path)

        transcription = result["text"].strip()
        logger.info(f"Transcription completed: {len(transcription)} characters")
        return transcription

    except Exception as e:
        logger.error(f"Error during transcription: {e}")
        raise

    finally:
        is_deleted = delete_temporary_file(resampled_audio_path)
        if is_deleted:
            logger.info(
                f"Temporary file deleted for resampled audio: {resampled_audio_path}"
            )
        else:
            logger.warning(
                f"Failed to delete temporary file for resampled audio: {resampled_audio_path}"
            )

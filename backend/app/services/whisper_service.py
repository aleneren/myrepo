# Ref: https://huggingface.co/openai/whisper-tiny#transcription
from io import BytesIO
import librosa
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from app.utils.logger import get_logger

logger = get_logger(__name__)

STANDARD_SAMPLING_RATE = 16000

processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
model.to(
    "cpu"
)  # Move model to CPU to reduce memory issues, as whisper-tiny is small and can run on CPU
model.config.forced_decoder_ids = (
    None  # Disable forced language token to allow auto-detection of language
)


def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Transcribes audio data using huggingface openai/whisper-tiny.

    Args:
        audio_bytes (bytes): Audio data as bytes.

    Returns:
        str: The transcription text.
    """
    logger.info("Starting transcription")

    try:
        # Pre-process the audio file to ensure it is in the correct format and sampling rate
        # Ref: https://learnopencv.com/fine-tuning-whisper-on-custom-dataset/#:~:text=Preprocessing%20f%20the%20dataset%20to,map%20the%20datasets%20for%20this.
        audio_array, sampling_rate = librosa.load(
            BytesIO(audio_bytes), sr=STANDARD_SAMPLING_RATE
        )
        duration = len(audio_array) / sampling_rate

        # Assumption: Small audio files (<=30s) are expected due to synchronous batch processing
        if duration > 30:
            logger.error(f"Audio duration {duration:.2f}s exceeds 30s, rejecting file")
            raise ValueError(
                "Audio duration exceeds 30 seconds, please upload a shorter file"
            )

        logger.info(f"Audio loaded, duration: {duration:.2f}s")

        # Process the audio and generate transcription
        input_features = processor(
            audio_array, sampling_rate=sampling_rate, return_tensors="pt"
        ).input_features
        predicted_ids = model.generate(input_features)

        # Post-process the predicted token ids to get the transcription text
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
        logger.info(f"Transcription completed: {len(transcription[0])} characters")
        return transcription[0].strip()
    except Exception as e:
        logger.error(f"Error during transcription: {e}")
        raise

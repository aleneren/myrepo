# Ref: https://huggingface.co/openai/whisper-tiny#long-form-transcription
import librosa
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from app.utils.logger import get_logger

logger = get_logger(__name__)

processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
model.config.forced_decoder_ids = None


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes an audio file using huggingface openai/whisper-tiny.

    Args:
        audio_path (str): Path to the audio file.

    Returns:
        str: The transcription text.
    """
    logger.info(f"Starting transcription for {audio_path}")

    # Ref: https://learnopencv.com/fine-tuning-whisper-on-custom-dataset/#:~:text=Preprocessing%20f%20the%20dataset%20to,map%20the%20datasets%20for%20this.
    audio_array, sampling_rate = librosa.load(audio_path, sr=16000)
    logger.info(f"Audio loaded, duration: {len(audio_array)/sampling_rate:.2f}s")

    input_features = processor(
        audio_array, sampling_rate=sampling_rate, return_tensors="pt"
    ).input_features
    predicted_ids = model.generate(input_features)

    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    logger.info(f"Transcription completed: {len(transcription[0])} characters")
    return transcription[0]

"""Transcribe downloaded audio files with a cached Whisper model."""

from functools import lru_cache
import whisper

@lru_cache(maxsize=1)
def load_whisper_model():
    """Load and cache the Whisper base model."""
    return whisper.load_model("base")

def transcribe_audio(audio_path):
    """Return cleaned transcript text for an audio file."""
    result = load_whisper_model().transcribe(str(audio_path))
    return result["text"].strip()

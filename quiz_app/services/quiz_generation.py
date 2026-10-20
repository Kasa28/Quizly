"""Coordinate the complete YouTube-to-quiz generation process."""

from tempfile import TemporaryDirectory
from .gemini import generate_quiz_data
from .transcription import transcribe_audio
from .youtube import download_audio, validate_youtube_url

def generate_quiz_from_youtube(url):
    """Download, transcribe, and convert a YouTube video into a quiz."""
    youtube_url = validate_youtube_url(url)
    with TemporaryDirectory(prefix="quizly_") as temp_folder:
        audio_file = download_audio(youtube_url, temp_folder)
        transcript = transcribe_audio(audio_file)
        return generate_quiz_data(transcript)

from functools import lru_cache
import whisper

@lru_cache(maxsize=1)
def load_whisper_model():
    return whisper.load_model("base")

def transcribe_audio(audio_path):
    result = load_whisper_model().transcribe(str(audio_path))
    return result["text"].strip()

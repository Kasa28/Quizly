import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import yt_dlp
from rest_framework.exceptions import ValidationError

YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}
VIDEO_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{11}$")

def get_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path.strip("/").split("/")[0]
    if parsed_url.path == "/watch":
        return parse_qs(parsed_url.query).get("v", [None])[0]
    if parsed_url.path.startswith(("/shorts/", "/embed/")):
        return parsed_url.path.strip("/").split("/")[1]
    return None


def validate_youtube_url(url):
    if not isinstance(url, str) or not url.strip():
        raise ValidationError({"url": "YouTube URL is required."})
    url = url.strip()
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ("http", "https"):
        raise ValidationError({"url": "Invalid URL format."})
    if parsed_url.hostname not in YOUTUBE_HOSTS:
        raise ValidationError({"url": "Only YouTube links are allowed."})
    video_id = get_video_id(url)
    if not video_id or not VIDEO_ID_PATTERN.fullmatch(video_id):
        raise ValidationError({"url": "Invalid YouTube video ID."})
    return url


def get_download_options(folder):
    return {
        "format": "bestaudio/best",
        "outtmpl": str(Path(folder) / "%(id)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }],
    }


def download_audio(url, folder):
    valid_url = validate_youtube_url(url)
    options = get_download_options(folder)
    with yt_dlp.YoutubeDL(options) as downloader:
        video = downloader.extract_info(valid_url, download=True)
    audio_file = Path(folder) / f"{video['id']}.mp3"
    if not audio_file.exists():
        raise RuntimeError("Audio file could not be created.")
    return audio_file

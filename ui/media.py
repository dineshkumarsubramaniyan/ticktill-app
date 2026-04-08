from pathlib import Path
import base64
import mimetypes


BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "audio"
SUPPORTED_FILES = [
    "background.mp3",
    "background.wav",
    "background.ogg",
    "background.m4a",
]


def get_audio_source():
    for filename in SUPPORTED_FILES:
        audio_path = AUDIO_DIR / filename
        if audio_path.exists():
            mime_type, _ = mimetypes.guess_type(audio_path.name)
            mime_type = mime_type or "audio/mpeg"
            audio_base64 = base64.b64encode(audio_path.read_bytes()).decode()
            return f"data:{mime_type};base64,{audio_base64}", True

    return "", False

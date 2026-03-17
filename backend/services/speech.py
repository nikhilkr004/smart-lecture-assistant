"""
speech.py — Downloads audio and converts it to text using OpenAI Whisper API.

Flow:
  1. download_audio()  → saves a remote audio file locally
  2. speech_to_text()  → sends the file to Whisper and returns the transcript
"""

import os
import requests
from openai import OpenAI
from config import OPENAI_API_KEY

# Initialize the OpenAI client once
client = OpenAI(api_key=OPENAI_API_KEY)


def download_audio(url: str, save_path: str = "temp_audio.mp3") -> str:
    """
    Download an audio file from a URL and save it locally.

    Args:
        url:       Public URL of the audio file (e.g. Firebase Storage link).
        save_path: Local filename to save the downloaded audio.

    Returns:
        The local file path of the saved audio.

    Raises:
        Exception: If the download fails (non-200 status code).
    """
    response = requests.get(url, timeout=120)

    if response.status_code != 200:
        raise Exception(f"Failed to download audio. HTTP {response.status_code}")

    with open(save_path, "wb") as f:
        f.write(response.content)

    return save_path


def speech_to_text(file_path: str) -> str:
    """
    Transcribe an audio file to text using OpenAI Whisper.

    Args:
        file_path: Path to the local audio file (.mp3, .wav, .m4a, etc.).

    Returns:
        The full transcript as a string.
    """
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )

    # Clean up the temporary audio file
    if os.path.exists(file_path):
        os.remove(file_path)

    return transcript.text

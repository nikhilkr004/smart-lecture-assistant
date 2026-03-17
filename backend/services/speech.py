"""
speech.py — Downloads audio and converts it to text using OpenAI Whisper API.
"""

import os
import requests
from openai import OpenAI, APIError
from fastapi import HTTPException
from config import OPENAI_API_KEY

# Initialize the OpenAI client once
client = OpenAI(api_key=OPENAI_API_KEY)


def download_audio(url: str, save_path: str = "temp_audio.mp3") -> str:
    """
    Download an audio file from a URL and save it locally.
    """
    try:
        response = requests.get(url, timeout=120)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        with open(save_path, "wb") as f:
            f.write(response.content)

        return save_path
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to download audio: {e}")


def speech_to_text(file_path: str) -> str:
    """
    Transcribe an audio file to text using OpenAI Whisper.
    """
    try:
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Audio file not found.")

        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
            )
        
        # Clean up the temporary audio file
        os.remove(file_path)

        return transcript.text
    except APIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error during transcription: {e.body.get('message', 'Unknown error')}")
    except Exception as e:
        # Clean up even if there's an error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to transcribe audio: {e}")
"""
config.py — Loads environment variables from .env file.

This is the single source of truth for all API keys and configuration.
Other files import from here instead of reading .env directly.
"""

import os
from dotenv import load_dotenv

# Load variables from .env file into the environment
load_dotenv()

# OpenAI key for Whisper (speech-to-text) and GPT (note generation)
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

# Firebase Storage bucket name (e.g. "my-app.appspot.com")
FIREBASE_STORAGE_BUCKET: str = os.getenv("FIREBASE_STORAGE_BUCKET", "")

# Path to the Firebase service-account JSON credential file
FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json")

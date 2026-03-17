"""
firebase_service.py — Uploads files to Firebase Cloud Storage.
"""

import firebase_admin
from firebase_admin import credentials, storage
from fastapi import HTTPException
from config import FIREBASE_CREDENTIALS_PATH, FIREBASE_STORAGE_BUCKET

# Initialise Firebase Admin SDK
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred, {
            "storageBucket": FIREBASE_STORAGE_BUCKET,
        })
except Exception as e:
    # This will crash the app on startup if Firebase isn't configured correctly,
    # which is intentional. A missing Firebase config is a fatal error.
    raise RuntimeError(f"Failed to initialize Firebase Admin SDK: {e}") from e

def upload_pdf(file_path: str, destination_name: str = "lecture_notes.pdf") -> str:
    """
    Upload a PDF to Firebase Storage and return its public URL.
    """
    try:
        bucket = storage.bucket()
        blob = bucket.blob(f"notes/{destination_name}")
        blob.upload_from_filename(file_path)
        blob.make_public()
        return blob.public_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload to Firebase: {e}")

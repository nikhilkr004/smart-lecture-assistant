"""
firebase_service.py — Uploads files to Firebase Cloud Storage.

On first import the Firebase Admin SDK is initialised using the
service-account JSON whose path is set in .env.
"""

import firebase_admin
from firebase_admin import credentials, storage
from config import FIREBASE_CREDENTIALS_PATH, FIREBASE_STORAGE_BUCKET

# Initialise Firebase Admin SDK (runs once when the module is first imported)
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred, {
        "storageBucket": FIREBASE_STORAGE_BUCKET,
    })


def upload_pdf(file_path: str, destination_name: str = "lecture_notes.pdf") -> str:
    """
    Upload a PDF to Firebase Storage and return its public URL.

    Args:
        file_path:        Local path of the PDF file.
        destination_name: The filename to use inside the storage bucket.

    Returns:
        A public URL string for the uploaded file.
    """
    bucket = storage.bucket()
    blob = bucket.blob(f"notes/{destination_name}")
    blob.upload_from_filename(file_path)
    blob.make_public()
    return blob.public_url

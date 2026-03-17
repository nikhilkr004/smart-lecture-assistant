"""
main.py — FastAPI entry point for the Smart Classroom Assistant backend.

Run with:
    uvicorn main:app --reload --host 0.0.0.0 --port 8000

Endpoints:
    GET  /            → Health check
    POST /process     → Full pipeline: audio → transcript → notes → PDF → URL
"""

import os
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.speech import download_audio, speech_to_text
from services.summary import generate_notes
from services.pdf import create_pdf
from services.firebase_service import upload_pdf

# ── App Setup ───────────────────────────────────────────────
app = FastAPI(
    title="Smart Classroom Assistant API",
    description="Converts lecture audio into structured PDF notes using AI.",
    version="1.0.0",
)


# ── Request / Response Models ───────────────────────────────
class LectureRequest(BaseModel):
    """The Android app sends this JSON body."""
    audio_url: str          # Public URL of the recorded lecture audio


class LectureResponse(BaseModel):
    """What we send back to the Android app."""
    transcript: str         # Raw speech-to-text output
    notes: str              # Markdown-formatted study notes
    pdf_url: str            # Public Firebase Storage URL of the PDF


# ── Endpoints ───────────────────────────────────────────────
@app.get("/")
def health_check():
    """Simple health check so you can verify the server is alive."""
    return {"status": "ok", "message": "Smart Classroom Assistant API is running 🚀"}


@app.post("/process", response_model=LectureResponse)
def process_lecture(data: LectureRequest):
    """
    Full processing pipeline:
      1. Download the audio file from the provided URL
      2. Transcribe it to text using OpenAI Whisper
      3. Generate structured notes using GPT
      4. Convert the notes to a styled PDF
      5. Upload the PDF to Firebase Storage
      6. Return the transcript, notes, and PDF URL
    """
    try:
        # ── Step 1: Download audio ──────────────────────────
        audio_path = download_audio(data.audio_url)

        # ── Step 2: Transcribe ──────────────────────────────
        transcript = speech_to_text(audio_path)

        if not transcript.strip():
            raise HTTPException(status_code=400, detail="Transcript is empty. Check audio quality.")

        # ── Step 3: Generate notes ──────────────────────────
        notes = generate_notes(transcript)

        # ── Step 4: Create PDF ──────────────────────────────
        unique_name = f"notes_{uuid.uuid4().hex[:8]}.pdf"
        pdf_path = create_pdf(notes, output_path=unique_name)

        # ── Step 5: Upload to Firebase ──────────────────────
        pdf_url = upload_pdf(pdf_path, destination_name=unique_name)

        # Clean up local PDF
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        # ── Step 6: Respond ─────────────────────────────────
        return LectureResponse(
            transcript=transcript,
            notes=notes,
            pdf_url=pdf_url,
        )

    except HTTPException:
        raise  # Re-raise known HTTP errors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

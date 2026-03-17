# Smart Classroom Assistant — Backend

AI-powered backend that converts lecture audio into structured PDF notes.

## Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # Then edit with your real keys
```

Place your `firebase-credentials.json` in this folder.

## Run

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/process` | Process lecture audio → returns transcript, notes, PDF URL |

### POST /process

```json
{ "audio_url": "https://example.com/lecture.mp3" }
```

**Response:**
```json
{
  "transcript": "Today we discussed...",
  "notes": "# Lecture Notes\n## Topic 1\n- ...",
  "pdf_url": "https://storage.googleapis.com/.../notes.pdf"
}
```

## Deploy on Render

1. Push to GitHub
2. Render → New Web Service → connect repo
3. Build: `pip install -r requirements.txt`
4. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add env vars: `OPENAI_API_KEY`, `FIREBASE_STORAGE_BUCKET`

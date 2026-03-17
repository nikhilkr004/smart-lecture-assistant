"""
summary.py — Generates structured lecture notes from a transcript using GPT.
"""

from openai import OpenAI, APIError
from fastapi import HTTPException
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """You are an expert academic note-taker.
Given a lecture transcript, produce well-structured study notes in Markdown with:
1. A clear **Title**
2. **Section Headings** (##) for each major topic
3. **Bullet points** summarising key ideas
4. A **Key Concepts** section at the end listing important terms and definitions
Keep the language clear and beginner-friendly."""


def generate_notes(transcript: str) -> str:
    """
    Send the transcript to GPT and return formatted Markdown notes.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Here is the lecture transcript:\n\n{transcript}"},
            ],
            temperature=0.3,
            max_tokens=4096,
        )
        return response.choices[0].message.content
    except APIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error during note generation: {e.body.get('message', 'Unknown error')}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate notes: {e}")

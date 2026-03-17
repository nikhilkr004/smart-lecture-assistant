"""
pdf.py — Converts Markdown-formatted notes into a styled PDF using ReportLab.
"""

import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from fastapi import HTTPException

def create_pdf(notes: str, output_path: str = "lecture_notes.pdf") -> str:
    """
    Convert Markdown notes into a PDF file.
    """
    try:
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=2 * cm,
            rightMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("NoteTitle", parent=styles["Title"], fontSize=22, textColor=HexColor("#2563EB"), spaceAfter=16)
        heading_style = ParagraphStyle("NoteHeading", parent=styles["Heading2"], fontSize=15, textColor=HexColor("#1E293B"), spaceBefore=14, spaceAfter=6)
        body_style = ParagraphStyle("NoteBody", parent=styles["BodyText"], fontSize=11, leading=16, textColor=HexColor("#1E293B"))
        bullet_style = ParagraphStyle("NoteBullet", parent=body_style, leftIndent=20, bulletIndent=10, spaceBefore=2, spaceAfter=2)

        content = []
        for line in notes.split("\n"):
            stripped = line.strip()
            if not stripped:
                content.append(Spacer(1, 6))
            elif stripped.startswith("# "):
                text = re.sub(r"[#*]+", "", stripped).strip()
                content.append(Paragraph(text, title_style))
            elif stripped.startswith("## "):
                text = re.sub(r"[#*]+", "", stripped).strip()
                content.append(Paragraph(text, heading_style))
            elif stripped.startswith("- ") or stripped.startswith("* "):
                text = stripped[2:]
                text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
                content.append(Paragraph(f"• {text}", bullet_style))
            else:
                text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", stripped)
                content.append(Paragraph(text, body_style))

        doc.build(content)
        return output_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create PDF: {e}")

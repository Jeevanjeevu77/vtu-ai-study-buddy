import os, io
from dotenv import load_dotenv
from groq import Groq
from PyPDF2 import PdfReader
from ai_engine import groq_chat_completion

def analyze_pdf(file_input):
    if isinstance(file_input, (bytes, bytearray)):
        reader = PdfReader(io.BytesIO(file_input))
    elif hasattr(file_input, 'read'):
        reader = PdfReader(file_input)
    else:
        reader = PdfReader(file_input)

    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "")

    prompt = f"""
    Summarize this study material in simple bullet points for students.

    {text[:8000]}
    """

    response = groq_chat_completion(
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
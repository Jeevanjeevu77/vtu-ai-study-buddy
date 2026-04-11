import os
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader

load_dotenv(override=True)

# Get API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def analyze_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""
    for page in reader.pages:
        text += page.extract_text()

    prompt = f"""
    Summarize this study material in simple bullet points for students.

    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
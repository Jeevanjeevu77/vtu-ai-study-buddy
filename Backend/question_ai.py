import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(override=True)

# Get API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def generate_exam_questions(subject):

    prompt = f"""
    Generate 5 VTU style exam questions for the subject {subject}.
    Include both theory and long answer questions.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
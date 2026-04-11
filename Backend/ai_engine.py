import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(override=True)

# Get API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# Ask AI
def generate_answer(question: str):
    """Generates a general answer for a given question."""
    if not GROQ_API_KEY:
        return "⚠️ GROQ_API_KEY not found in .env file."

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an AI tutor for VTU engineering students. Answer concisely and use bullet points."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

def generate_aptitude_questions(company: str):
    """Generates company-specific aptitude and logical reasoning questions."""
    if not GROQ_API_KEY:
        return "⚠️ GROQ_API_KEY not found in .env file."

    prompt = f"""
Analyze the past year question (PYQ) patterns for the company: {company}.
Generate 5 high-quality aptitude and logical reasoning questions that strictly follow the difficulty and style of {company}'s actual placement papers.

Include a mix of:
1. Quantitative Aptitude (Time & Work, Percentages, Profit/Loss, etc.)
2. Logical Reasoning (Coding-Decoding, Series, Blood Relations, Syllogisms, etc.)

Format for each question:
Category: (Quant/Logical)
Question: [The question]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
Answer: [A/B/C/D]
Explanation: [Detailed explanation as to why this is the answer]
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a placement preparation expert who has analyzed thousands of company PYQs. Provide accurate and challenging questions."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

def generate_mock_interview_questions(company: str, role: str):
    """Generates technical and HR interview questions for a specific role and company."""
    if not GROQ_API_KEY:
        return "⚠️ GROQ_API_KEY not found in .env file."

    prompt = f"""
Generate 8-10 interview questions for a candidate applying for the role of '{role}' at '{company}'.

The questions should be a mix of:
- Technical Questions (Data Structures, Algorithms, Core CS concepts relevant to the role)
- Behavioral/HR Questions (Situational questions frequent at {company})
- Company-specific questions (Culture, recent news, or why {company})

Provide the questions in a clear, numbered list.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a senior hiring manager at a top tech company. Provide insightful and relevant interview questions."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# Generate exam questions
def generate_exam_questions(subject: str):
    """Generates VTU style exam questions for a subject."""
    if not GROQ_API_KEY:
        return "⚠️ GROQ_API_KEY not found in .env file."

    prompt = f"""
Generate 5 VTU exam questions for the subject: {subject}

Include:
- 2 questions for 2 marks
- 2 questions for 5 marks
- 1 question for 10 marks
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You generate VTU engineering exam questions."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
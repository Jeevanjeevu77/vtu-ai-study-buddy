import os, json
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
Generate exactly 30 high-quality aptitude and logical reasoning questions that strictly follow the difficulty and style of {company}'s actual placement papers.

Include a mix of:
1. Quantitative Aptitude (Time & Work, Percentages, Profit/Loss, etc.)
2. Logical Reasoning (Coding-Decoding, Series, Blood Relations, Syllogisms, etc.)

Provide the response EXCLUSIVELY as a valid JSON object with a single key "questions" containing a list of 30 question objects. Do not include markdown blocks or any other text.
JSON Structure:
{{
  "questions": [
    {{
      "category": "Quantitative Aptitude",
      "question": "Sample question text?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "A",
      "explanation": "Explanation here."
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a placement preparation expert who outputs strictly valid JSON objects."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    try:
        content = response.choices[0].message.content
        # Remove markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        parsed = json.loads(content.strip())
        questions = parsed.get("questions", [])
        
        # Validation: ensure 4 options and explanation
        valid_qs = []
        for q in questions:
            if all(k in q for k in ["question", "options", "answer", "explanation"]) and len(q["options"]) == 4:
                valid_qs.append(q)
        return valid_qs
    except:
        return []

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


# Generate VTU Exam Questions - 5 per module (Total 25)
def generate_vtu_questions(subject: str, scheme: str, semester: str, q_type: str = "important"):
    """Generates 25 VTU exam questions (5 per module) for a subject."""
    if not GROQ_API_KEY:
        return []

    prompt = f"""
Analyze the syllabus for the VTU subject: '{subject}' (Scheme: {scheme}, Semester: {semester}).
Generate exactly 25 '{q_type}' questions. 
The syllabus strictly contains 5 modules. Generate exactly 5 distinct and high-quality questions for EACH module.

Provide the response EXCLUSIVELY as a valid JSON object with a single key "questions" containing a list of 25 question objects. 
Each object MUST have "module" (integer 1-5) and "text" (string).

JSON Structure:
{{
  "questions": [
    {{ "module": 1, "text": "Question text here?" }},
    ...
  ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a VTU academic expert who outputs strictly valid JSON formatting."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    import json
    try:
        content = response.choices[0].message.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        parsed = json.loads(content.strip())
        return parsed.get("questions", [])
    except:
        return []

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

def generate_interview_response(history: list, company: str, role: str):
    """Generates interactive interview responses with feedback and the next question."""
    if not GROQ_API_KEY:
        return "⚠️ GROQ_API_KEY not found in .env file."

    system_prompt = f"""
You are a senior hiring manager at {company} interviewing a candidate for the role of '{role}'.

Your goal is to conduct a realistic, high-quality technical and HR interview.

RULES:
1. Conduct the interview one question at a time.
2. After the candidate answers, analyze their response:
   - Provide a section called **FEEDBACK**: This should include a brief analysis of the answer. If the answer is wrong, provide the correct information. If it's good, suggest how it could be even better.
   - Provide a section called **NEXT QUESTION**: Ask the next relevant question for the role and company.
3. If the interview is starting (no history), greet the candidate and ask the first question (omit the FEEDBACK section).
4. If the interview is ending (after ~6 questions), provide an **OVERALL SUMMARY** and performance score out of 10.

FORMAT YOUR RESPONSE AS:
**FEEDBACK:** [Your analysis/correction]
**NEXT QUESTION:** [The next question]
"""

    messages = [{"role": "system", "content": system_prompt}]
    # Add history (last few messages to keep context)
    messages.extend(history[-10:]) 

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    return response.choices[0].message.content
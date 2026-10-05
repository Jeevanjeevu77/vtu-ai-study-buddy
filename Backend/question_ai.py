import os
from ai_engine import groq_chat_completion

def generate_exam_questions(subject):

    prompt = f"""
    Generate 5 VTU style exam questions for the subject {subject}.
    Include both theory and long answer questions.
    """

    response = groq_chat_completion(
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
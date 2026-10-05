import os, json
from dotenv import load_dotenv
from groq import Groq
import concurrent.futures

# Search for .env in current file directory, parent directory, and cwd
current_dir = os.path.dirname(os.path.abspath(__file__))
for path in [
    os.path.join(current_dir, ".env"),
    os.path.join(current_dir, "..", ".env"),
    os.path.join(os.getcwd(), ".env")
]:
    if os.path.exists(path):
        load_dotenv(path, override=True)
        break

# Get API key and preferred models from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")
AVAILABLE_MODELS = [
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-120b"
]

def get_groq_client():
    key = os.getenv("GROQ_API_KEY") or GROQ_API_KEY
    if not key:
        return None
    try:
        return Groq(api_key=key)
    except Exception:
        return None

client = get_groq_client()

def groq_chat_completion(messages, model=None, response_format=None, max_tokens=None):
    cli = get_groq_client()
    if not cli:
        raise ValueError("GROQ_API_KEY not configured or invalid")
    
    preferred_models = [model] if model else []
    preferred_models.extend(AVAILABLE_MODELS)
    # Deduplicate while preserving order
    models_to_try = list(dict.fromkeys([m for m in preferred_models if m]))
    
    last_err = None
    for m in models_to_try:
        try:
            kwargs = {
                "model": m,
                "messages": messages,
            }
            if response_format:
                kwargs["response_format"] = response_format
            if max_tokens:
                kwargs["max_tokens"] = max_tokens
            return cli.chat.completions.create(**kwargs)
        except Exception as e:
            last_err = e
            continue
    raise last_err

# Ask AI
def generate_answer(question: str):
    """Generates a general answer for a given question."""
    key = os.getenv("GROQ_API_KEY") or GROQ_API_KEY
    if not key:
        return "⚠️ GROQ_API_KEY not found in .env file."

    try:
        response = groq_chat_completion(
            messages=[
                {"role": "system", "content": "You are an AI tutor for VTU engineering students. Answer concisely and use bullet points."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI service error: {str(e)}"

def generate_aptitude_questions(company: str):
    """Generates company-specific aptitude and logical reasoning questions."""
    key = os.getenv("GROQ_API_KEY") or GROQ_API_KEY
    if not key:
        return []

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

    try:
        response = groq_chat_completion(
            messages=[
                {"role": "system", "content": "You are a placement preparation expert who outputs strictly valid JSON objects."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
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
    except Exception as e:
        print(f"Error in generate_aptitude_questions: {e}")
        return []

def generate_mock_interview_questions(company: str, role: str):
    """Generates technical and HR interview questions for a specific role and company."""
    key = os.getenv("GROQ_API_KEY") or GROQ_API_KEY
    if not key:
        return f"⚠️ Interview generation error: GROQ_API_KEY not configured"

    prompt = f"""
You are a senior technical interviewer at {company} conducting a comprehensive campus recruitment interview for the role of {role}.

Generate an initial warm greeting followed by the first technical question.
Focus on core engineering competencies, data structures, algorithms, system design, or problem solving relevant to {company}.
Keep the tone professional, encouraging, and authentic.
"""

    try:
        response = groq_chat_completion(
            messages=[
                {"role": "system", "content": f"You are an expert technical interviewer at {company}."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Interview generation error: {str(e)}"

# Generate VTU Exam Questions (Fast single-prompt generation for all 5 modules)
def generate_vtu_questions(subject: str, scheme: str, semester: str, branch: str = "CSE", q_type: str = "important"):
    """Generates 50 VTU exam questions (10 per module) for a subject quickly in valid JSON."""
    key = os.getenv("GROQ_API_KEY") or GROQ_API_KEY
    if not key:
        return []

    prompt = f"""
You are a senior VTU university examination paper setter. 
Your task is to generate {q_type.upper()} questions for the official VTU subject '{subject}' (Branch: {branch}, Scheme: {scheme}, Semester: {semester}).

INSTRUCTION: Rely on your extensive knowledge of engineering curricula. Formulate the questions based on the standard topics taught for '{subject}' under the VTU syllabus. If you don't have the exact syllabus verbatim, generate highly accurate, standard topics that perfectly align with a typical 5-module VTU engineering syllabus for this branch.
You MUST NOT refuse to answer or state that you don't have the syllabus. ALWAYS generate the questions.

Generate 50 realistic VTU examination {q_type.upper()} questions (exactly 10 questions per Module for all 5 Modules: Module 1, Module 2, Module 3, Module 4, and Module 5).

STRICT RULES:
1. Questions must follow standard VTU phrasing ("Explain with neat diagram", "Derive", "Differentiate between", "Write an algorithm for", "With examples explain").
2. Include marks e.g. "(5 marks)", "(6 marks)", "(8 marks)", "(10 marks)".
3. Each question object must specify "module" (1, 2, 3, 4, or 5) and "text".

Return EXCLUSIVELY a JSON object in this exact format:
{{
  "questions": [
    {{ "module": 1, "text": "Question 1 for Module 1 (8 marks)" }},
    {{ "module": 1, "text": "Question 2 for Module 1 (6 marks)" }},
    ...
    {{ "module": 5, "text": "Question 10 for Module 5 (10 marks)" }}
  ]
}}
"""

    try:
        response = groq_chat_completion(
            messages=[
                {"role": "system", "content": "You are a senior VTU professor who sets question papers. Return strictly valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        parsed = json.loads(content.strip())
        return parsed.get("questions", [])
    except Exception as e:
        print(f"Error in fast generate_vtu_questions: {e}")
        return []

def generate_exam_questions(subject: str):
    """Generates VTU style exam questions for a subject."""
    key = os.getenv("GROQ_API_KEY") or GROQ_API_KEY
    if not key:
        return "⚠️ GROQ_API_KEY not found in .env file."

    prompt = f"""
Generate 5 VTU exam questions for the subject: {subject}

Include:
- 2 questions for 2 marks
- 2 questions for 5 marks
- 1 question for 10 marks
"""

    try:
        response = groq_chat_completion(
            messages=[
                {"role": "system", "content": "You generate VTU engineering exam questions."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Exam questions generation error: {str(e)}"

def generate_interview_response(history: list, company: str, role: str):
    """Generates interactive interview responses with feedback and the next question."""
    key = os.getenv("GROQ_API_KEY") or GROQ_API_KEY
    if not key:
        return "⚠️ GROQ_API_KEY not found in environment or .env file."

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

    try:
        response = groq_chat_completion(
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Mock Interview error: {str(e)}"

def generate_vtu_notes(subject: str, scheme: str, semester: str, branch: str = "CSE"):
    """Generates exhaustive VTU-syllabus-aligned study notes for all 5 modules concurrently."""
    key = os.getenv("GROQ_API_KEY") or GROQ_API_KEY
    if not key:
        return []

    def fetch_notes(mod_num):
        print(f"DEBUG: Generating detailed notes for Module {mod_num} of {subject}...")
        prompt = f"""
You are writing official VTU study notes for '{subject}' (Branch: {branch}, Scheme: {scheme}, Semester: {semester}), MODULE {mod_num}.

STRICT REQUIREMENTS:
1. INSTRUCTION: Generate the absolute best, highly accurate educational content for Module {mod_num} of '{subject}'. If you do not have the exact VTU syllabus verbatim in your memory, construct a highly realistic and standard curriculum for this module. NEVER refuse to answer or say you lack access to the syllabus.
2. Structure the notes as a proper study guide with:
   - Module title and list of topics covered
   - Detailed explanations with definitions, theorems, and proofs where applicable
   - Key formulas and derivations
   - Diagrams described in text (e.g., "[Diagram: Binary Search Tree with nodes 10, 5, 15, 3, 7]")
   - Worked examples and numerical problems with step-by-step solutions
   - Comparison tables where applicable (e.g., "TCP vs UDP", "Paging vs Segmentation")
   - Important points to remember (exam tips)
   - Previous year question patterns for this module
3. Content MUST be 1500-2000 words minimum — comprehensive enough to study for exams
4. Use proper headings with === and --- separators for readability
5. Include mnemonics or memory aids where helpful
6. End with "Key Questions from this Module" section listing 5 frequently asked VTU questions

Do NOT output JSON. Output purely the Markdown content for the notes. Start your response directly with the title of the module.
"""
        try:
            response = groq_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a senior VTU professor writing comprehensive study material. You know the exact VTU syllabus inside-out. Your notes help students score 90+ in VTU exams."},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content
            return {
                "module": mod_num,
                "title": f"Module {mod_num}",
                "content": content.strip()
            }
        except Exception as e:
            err_str = str(e).encode('ascii', 'replace').decode('ascii')
            print(f"Error generating notes for module {mod_num}: {err_str}")
            return {"module": mod_num, "title": f"Module {mod_num}", "content": f"Detailed notes for Module {mod_num} could not be generated at this time."}

    modules_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_notes, range(1, 6))
        for res in results:
            modules_data.append(res)

    return modules_data

def generate_vtu_model_paper(subject: str, scheme: str, semester: str, branch: str = "CSE", course_code: str = None):
    """Generates an official 100-mark VTU Model Question Paper conforming to university guidelines in 2-3 seconds."""
    key = os.getenv("GROQ_API_KEY") or GROQ_API_KEY
    code_str = course_code or f"{scheme[-2:] if len(scheme)>=2 else '22'}{branch[:2].upper()}{semester}1"

    prompt = f"""
You are the Chief Examiner and Board of Examiners Chairperson for Visvesvaraya Technological University (VTU), Belagavi.
Set an official 100-Mark VTU Model Question Paper for:
- Course Title: {subject}
- Course Code: {code_str}
- Scheme: {scheme} Scheme
- Semester: {semester}th Semester B.E. / B.Tech.
- Department: {branch}

INSTRUCTION: Rely on your extensive knowledge of engineering curricula. Formulate the Model Paper based on the standard topics taught for '{subject}' under the VTU syllabus. If you don't have the exact syllabus verbatim, generate highly accurate, standard topics that perfectly align with a typical 5-module VTU engineering syllabus for this branch. You MUST NOT refuse to answer or state that you don't have the syllabus. ALWAYS generate the complete JSON object.

OFFICIAL VTU EXAMINATION BLUEPRINT:
Set all 5 Modules (Module 1, 2, 3, 4, 5).
For each module:
1. "module_num": 1 to 5, "co": "CO1" to "CO5"
2. "question_odd": Q.1, Q.3, Q.5, Q.7, Q.9 with sub-questions (a, b, c) totaling 20 marks.
3. "question_even": Q.2, Q.4, Q.6, Q.8, Q.10 with sub-questions (a, b, c) totaling 20 marks.
4. Each sub-question part MUST have:
   - "sub_q": "a", "b", or "c"
   - "text": Authentic VTU phrasing ("With a neat sketch explain...", "Derive the mathematical formula...", "Differentiate between...", "Write an algorithm for...", "Explain with block diagram...")
   - "marks": integer e.g. 8, 6, 6, 10
   - "level": "L1", "L2", "L3", or "L4"
   - "co": e.g. "CO1"

Output EXCLUSIVELY a JSON object:
{{
  "modules": [
    {{
      "module_num": 1,
      "co": "CO1",
      "question_odd": {{
        "q_num": 1,
        "parts": [
          {{ "sub_q": "a", "text": "Question text here (8 marks)", "marks": 8, "level": "L2", "co": "CO1" }},
          {{ "sub_q": "b", "text": "Question text here (6 marks)", "marks": 6, "level": "L3", "co": "CO1" }},
          {{ "sub_q": "c", "text": "Question text here (6 marks)", "marks": 6, "level": "L2", "co": "CO1" }}
        ]
      }},
      "question_even": {{
        "q_num": 2,
        "parts": [
          {{ "sub_q": "a", "text": "Question text here (10 marks)", "marks": 10, "level": "L2", "co": "CO1" }},
          {{ "sub_q": "b", "text": "Question text here (10 marks)", "marks": 10, "level": "L3", "co": "CO1" }}
        ]
      }}
    }}
  ]
}}
"""

    modules = []
    if key:
        try:
            response = groq_chat_completion(
                messages=[
                    {"role": "system", "content": "You are the senior VTU examination board member. Output strictly valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            parsed = json.loads(content.strip())
            modules = parsed.get("modules", [])
        except Exception as e:
            print(f"Error in single-shot model paper generation: {e}")

    # If AI returned fewer than 5 modules, fill remaining with syllabus questions
    if len(modules) < 5:
        existing_nums = {m.get("module_num") for m in modules}
        for mod_num in range(1, 6):
            if mod_num not in existing_nums:
                co_tag = f"CO{mod_num}"
                q_odd = (mod_num - 1) * 2 + 1
                q_even = q_odd + 1
                modules.append({
                    "module_num": mod_num,
                    "co": co_tag,
                    "question_odd": {
                        "q_num": q_odd,
                        "parts": [
                            {"sub_q": "a", "text": f"Explain the fundamental architecture and principles of {subject} in Module {mod_num} with a neat diagram.", "marks": 10, "level": "L2", "co": co_tag},
                            {"sub_q": "b", "text": f"Derive and explain the key algorithms/equations used in {subject} Module {mod_num}.", "marks": 10, "level": "L3", "co": co_tag}
                        ]
                    },
                    "question_even": {
                        "q_num": q_even,
                        "parts": [
                            {"sub_q": "a", "text": f"Differentiate between key methodologies and design paradigms in Module {mod_num} with practical examples.", "marks": 10, "level": "L3", "co": co_tag},
                            {"sub_q": "b", "text": f"Write detailed technical notes on application scenarios and performance analysis for Module {mod_num}.", "marks": 10, "level": "L2", "co": co_tag}
                        ]
                    }
                })
        modules.sort(key=lambda m: m.get("module_num", 0))

    return {
        "university": "VISVESVARAYA TECHNOLOGICAL UNIVERSITY, BELAGAVI",
        "title": "B.E. / B.Tech. Degree Examination — Model Question Paper",
        "scheme": scheme,
        "semester": semester,
        "branch": branch,
        "subject": subject,
        "course_code": code_str,
        "time_allowed": "3 Hours",
        "max_marks": 100,
        "instructions": [
            "Answer any FIVE full questions, choosing ONE full question from each module.",
            "M: Marks, L: Revised Bloom's Taxonomy Level (L1: Remember, L2: Understand, L3: Apply, L4: Analyze), CO: Course Outcome.",
            "Draw neat sketches / circuit diagrams / flowcharts wherever necessary."
        ],
        "modules": modules
    }
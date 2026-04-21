"""
main.py — VTU Genius AI  (FastAPI backend)
Features: SQLite DB, Groq LLaMA3, RAG for /ask, PDF upload & read
"""
import os, shutil, random
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from PyPDF2 import PdfReader
from groq import Groq

from database import engine, get_db, Base
from models import Subject, Note, Question, User, AptitudeQuestion
from auth import get_current_user, get_password_hash, verify_password, create_access_token
from pydantic import BaseModel
from fpdf import FPDF
import io

# ── Boot ───────────────────────────────────────────────────────────────────────
load_dotenv(override=True)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Database setup skipped or failed: {e}")

app = FastAPI(title="VTU Genius AI")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
client = Groq(api_key=GROQ_API_KEY)

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static / Frontend ──────────────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
def home():
    return FileResponse("../frontend/index.html")

# ── Helpers ────────────────────────────────────────────────────────────────────
ALIAS = {
    "operating systems": "OS",
    "operating system":  "OS",
    "data structures":   "DSA",
    "database management system": "DBMS",
    "computer networks": "CN",
    "theory of computation": "TOC",
    "design & analysis of algorithms": "ADA",
    "algorithms": "ADA",
    "discrete maths": "DM",
    "discrete mathematics": "DM",
}

def resolve_code(name: str) -> str:
    return ALIAS.get(name.strip().lower(), name.strip())

def get_subject(db: Session, name: str, scheme: str = None, sem: str = None) -> Subject | None:
    code = resolve_code(name)
    query = db.query(Subject).filter((Subject.code == code) | (Subject.name == name))
    if scheme:
        query = query.filter(Subject.scheme == scheme)
    if sem:
        sem_num = sem.replace("Sem ", "").strip()
        query = query.filter(Subject.semester == sem_num)
    return query.first()

# ── SCHEMAS ────────────────────────────────────────────────────────────────────
class UserCreate(BaseModel):
    username: str
    password: str

# ── ROUTES ─────────────────────────────────────────────────────────────────────

# ✅ REGISTER
@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        return {"error": "Username already taken"}
    new_user = User(username=user.username, password_hash=get_password_hash(user.password))
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

# ✅ LOGIN / TOKEN
@app.post("/token")
def login(data: dict, db: Session = Depends(get_db)):
    username = data.get("username")
    password = data.get("password")
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return {"error": "Incorrect username or password"}
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "username": user.username}

# ✅ SUBJECTS — list all subjects for a scheme + sem from DB
@app.get("/subjects")
def subjects_route(scheme: str, sem: str, db: Session = Depends(get_db)):
    rows = db.query(Subject).filter_by(scheme=scheme, semester=sem).all()
    return {"subjects": [r.name for r in rows]}


# ✅ ASK AI — RAG: inject subject notes as context before calling Groq
@app.post("/ask")
def ask_ai(data: dict, db: Session = Depends(get_db)):
    q       = data.get("question", "").strip()
    subname = data.get("subject", "").strip()

    # Build context from DB notes
    context = ""
    if subname and subname not in ("Select Subject", ""):
        sub = get_subject(db, subname, data.get("scheme"), data.get("sem"))
        if sub:
            # Fetch general notes AND user-specific notes if token passed
            token = data.get("token")
            user_id = None
            if token:
                user = get_current_user(token, db)
                if user:
                    user_id = user.id
            
            notes = db.query(Note).filter(
                (Note.subject_id == sub.id) & 
                ((Note.user_id == None) | (Note.user_id == user_id))
            ).all()
            context = "\n\n".join(n.content for n in notes)[:20000]

    if context:
        system_prompt = (
            "You are VTU Genius AI, an expert exam tutor for Visvesvaraya Technological University (VTU) students. "
            "Answer the student's question using ONLY the following syllabus notes. "
            "Be concise, use bullet points, and always relate your answer to VTU exam patterns.\n\n"
            f"---NOTES---\n{context}\n---END NOTES---"
        )
    else:
        system_prompt = (
            "You are VTU Genius AI, an expert exam tutor for VTU students. "
            "Answer concisely with bullet points, always relevant to VTU exams."
        )

    try:
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": q}
            ]
        )
        return {"answer": res.choices[0].message.content}
    except Exception as e:
        error_msg = str(e)
        print(f"DEBUG: AI Error - {error_msg}")
        if "AuthenticationError" in str(type(e)) or "401" in error_msg or "Invalid API Key" in error_msg:
            # Fallback mock response so the UI still functions without an API Key
            mock_ans = (
                f"**[MOCK AI MODE]** I noticed you don't have a valid Groq API Key set!\n\n"
                f"But if I were LLaMA 3.1, here is how I would answer your question about **'{q}'**:\n"
                f"• I would scan through the syllabus database.\n"
                f"• I would extract relevant topics.\n"
                f"• I'd generate bullet points summarizing the most important concepts for your exams!\n\n"
                f"*(To enable real AI, add a valid `GROQ_API_KEY` to the `/backend/.env` file)*"
            )
            return {"answer": mock_ans}
        return {"answer": f"⚠️ AI service unavailable right now. Error: {error_msg}"}


# ✅ GENERATE QUESTIONS — PYQ from DB
@app.post("/generate")
def generate_q(data: dict, db: Session = Depends(get_db)):
    sub = get_subject(db, data.get("subject", ""), data.get("scheme"), data.get("sem"))
    if not sub:
        return {"questions": []}
    
    subject_query = data.get("subject", "").replace(" ", "+")
    search_link = f"https://www.google.com/search?q=VTU+{subject_query}+previous+year+question+papers+all+schemes+PDF"
    vtu_boss_link = f"https://vtuboss.com/vtu-question-papers/"
    vtu_resource_link = f"https://www.vturesource.com/vtu-question-papers/"
    vtu_connect_link = f"https://vtuconnect.in/vtu-question-papers"

    msg = (f"Access the Previous Year Question Papers for **{sub.name}**\n\n"
           f"Here are the direct links to download official VTU question papers (applicable for all 3 Schemes & 8 Semesters):\n\n"
           f"🔗 VTU Boss Question Papers: {vtu_boss_link}\n"
           f"🔗 VTU Resource Question Papers: {vtu_resource_link}\n"
           f"🔗 VTU Connect Question Papers: {vtu_connect_link}\n\n"
           f"🔍 Search for specific Question Papers directly: {search_link}")

    return {"message": msg, "questions": []}


# ✅ IMPORTANT QUESTIONS
@app.post("/important-questions")
def important_q(data: dict, db: Session = Depends(get_db)):
    sub = get_subject(db, data.get("subject", ""), data.get("scheme"), data.get("sem"))
    if not sub:
        return {"questions": []}
    
    qs = db.query(Question).filter_by(subject_id=sub.id, q_type="important").all()
    
    # Check if we have at least 5 per module (25 total)
    if len(qs) < 25:
        from ai_engine import generate_vtu_questions
        ai_qs = generate_vtu_questions(sub.name, sub.scheme, sub.semester, "important")
        if ai_qs:
            for q_data in ai_qs:
                # Basic duplicate check
                text = q_data.get("text")
                module = q_data.get("module", 1)
                existing = db.query(Question).filter_by(subject_id=sub.id, text=text, q_type="important").first()
                if not existing:
                    db.add(Question(subject_id=sub.id, text=text, q_type="important", unit=module))
            db.commit()
            qs = db.query(Question).filter_by(subject_id=sub.id, q_type="important").all()

    return {"questions": list(dict.fromkeys(q.text for q in qs))}


# ✅ EXPECTED QUESTIONS
@app.post("/expected-questions")
def expected_q(data: dict, db: Session = Depends(get_db)):
    sub = get_subject(db, data.get("subject", ""), data.get("scheme"), data.get("sem"))
    if not sub:
        return {"questions": []}
    
    qs = db.query(Question).filter_by(subject_id=sub.id, q_type="expected").all()
    
    if len(qs) < 25:
        from ai_engine import generate_vtu_questions
        ai_qs = generate_vtu_questions(sub.name, sub.scheme, sub.semester, "expected")
        if ai_qs:
            for q_data in ai_qs:
                text = q_data.get("text")
                module = q_data.get("module", 1)
                existing = db.query(Question).filter_by(subject_id=sub.id, text=text, q_type="expected").first()
                if not existing:
                    db.add(Question(subject_id=sub.id, text=text, q_type="expected", unit=module))
            db.commit()
            qs = db.query(Question).filter_by(subject_id=sub.id, q_type="expected").all()

    return {"questions": list(dict.fromkeys(q.text for q in qs))}


# ✅ GET CONTENT / NOTES
@app.post("/get-content")
def get_content(data: dict, db: Session = Depends(get_db)):
    sub = get_subject(db, data.get("subject", ""), data.get("scheme"), data.get("sem"))
    if not sub:
        return {"notes": "No data found for this subject.", "important": [], "questions": []}

    imp_qs = db.query(Question).filter_by(subject_id=sub.id, q_type="important").all()
    pyq    = db.query(Question).filter_by(subject_id=sub.id, q_type="pyq").all()

    subject_query = data.get("subject", "").replace(" ", "+")
    search_link = f"https://www.google.com/search?q=VTU+{subject_query}+notes+all+5+modules+all+schemes+PDF"
    vtu_boss_link = f"https://vtuboss.com/vtu-notes/"
    vtu_resource_link = f"https://www.vturesource.com/vtu-notes/"

    msg = (f"Access the complete notes (All 5 Modules) for {sub.name}\n\n"
           f"Here are the direct links to download full notes (applicable for all 3 Schemes & 8 Semesters):\n\n"
           f"🔗 VTU Boss Notes Portal: {vtu_boss_link}\n"
           f"🔗 VTU Resource Portal: {vtu_resource_link}\n\n"
           f"🔍 Search for specific PDFs directly: {search_link}")

    return {
        "notes":     msg,
        "important": list(dict.fromkeys(q.text for q in imp_qs)),
        "questions": list(dict.fromkeys(q.text for q in pyq)),
    }


# ✅ MOCK EXAM
@app.post("/exam/start")
def start_exam(data: dict, db: Session = Depends(get_db)):
    sub = get_subject(db, data.get("subject", ""), data.get("scheme"), data.get("sem"))
    if not sub:
        return {"questions": []}
    qs = db.query(Question).filter_by(subject_id=sub.id, q_type="pyq").all()
    unique_qs = list(dict.fromkeys(q.text for q in qs))
    selected = random.sample(unique_qs, min(5, len(unique_qs)))
    return {"questions": selected}


@app.post("/exam/submit")
def submit_exam(data: dict):
    answers = data.get("answers", [])
    score   = sum(1 for a in answers if len(a.split()) > 5)
    return {"score": score, "total": len(answers)}


# ✅ FILE UPLOAD
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...), 
    subject: str = Form(""), 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    os.makedirs("uploads", exist_ok=True)
    path = f"uploads/{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if subject and subject != "Select Subject":
        try:
            reader = PdfReader(path)
            text = "".join(page.extract_text() or "" for page in reader.pages)
            sub = get_subject(db, subject)
            if sub and text:
                uploader_name = user.username if user else "Guest"
                uploader_id = user.id if user else None
                db.add(Note(
                    subject_id=sub.id, 
                    user_id=uploader_id, 
                    module=99, 
                    content=f"[{uploader_name} UPLOADED PDF CONTENT: {file.filename}]\n{text}"
                ))
                db.commit()
                return {"message": "PDF uploaded & indexed for RAG."}
        except Exception as e:
            return {"message": "Stored in uploads. Could not extract text.", "error": str(e)}

    return {"message": "Uploaded successfully. Not indexed."}



# ✅ APTITUDE PREP
@app.post("/aptitude")
def aptitude_prep(data: dict, db: Session = Depends(get_db)):
    company = data.get("company", "General")
    # Try fetching from DB first
    qs = db.query(AptitudeQuestion).filter(AptitudeQuestion.company.ilike(f"%{company}%")).all()
    
    if len(qs) < 30:
        # Fallback to AI generation if fewer than 30 in DB
        from ai_engine import generate_aptitude_questions
        try:
            ai_res = generate_aptitude_questions(company)
            if isinstance(ai_res, list) and len(ai_res) > 0:
                # Successfully generated questions; save to DB for persistence
                new_qs = []
                for item in ai_res:
                    # Duplicate check based on question text
                    existing = db.query(AptitudeQuestion).filter_by(question=item["question"]).first()
                    if not existing:
                        opts = item.get("options", ["", "", "", ""])
                        # Standardize options to exactly 4
                        while len(opts) < 4: opts.append("")
                        q = AptitudeQuestion(
                            company=company,
                            category=item.get("category", "General"),
                            question=item["question"],
                            option_a=opts[0],
                            option_b=opts[1],
                            option_c=opts[2],
                            option_d=opts[3],
                            answer=item.get("answer", "A"),
                            explanation=item.get("explanation", "")
                        )
                        db.add(q)
                        new_qs.append(q)
                db.commit()
                # Refund updated list from DB
                qs = db.query(AptitudeQuestion).filter(AptitudeQuestion.company.ilike(f"%{company}%")).all()
        except Exception as ai_err:
            error_str = str(ai_err)
            if "RateLimitError" in error_str or "429" in error_str:
                return {"questions": [], "ai_suggestion": "⚠️ AI Rate limit reached. The database will use previously saved questions if available. Please try again in a few minutes."}
            return {"questions": [], "ai_suggestion": f"Failed to generate questions. Error: {error_str}. Please check your API key or connection."}
    
    return {
        "questions": [
            {
                "id": q.id,
                "category": q.category,
                "question": q.question,
                "options": [q.option_a, q.option_b, q.option_c, q.option_d],
                "answer": q.answer,
                "explanation": q.explanation
            } for q in qs
        ]
    }


# ✅ MOCK INTERVIEW
@app.post("/mock-interview")
def mock_interview(data: dict):
    company = data.get("company", "General")
    role    = data.get("role", "Software Engineer")
    
    from ai_engine import generate_mock_interview_questions
    ai_res = generate_mock_interview_questions(company, role)
    return {"questions": ai_res}


@app.post("/interview/next")
def interview_next(data: dict):
    history = data.get("history", [])
    company = data.get("company", "General")
    role    = data.get("role", "Software Engineer")
    
    from ai_engine import generate_interview_response
    res = generate_interview_response(history, company, role)
    return {"answer": res}


@app.post("/interview/voice")
async def interview_voice(file: UploadFile = File(...)):
    import tempfile
    
    # Create a persistent temp dir inside backend/scratch to be safe but manageable
    # or just use system temp. Let's use system temp to avoid uvicorn monitoring.
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name
    
    try:
        from voice_ai import speech_to_text
        text = speech_to_text(temp_path)
        return {"text": text}
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass


# ✅ PDF DOWNLOAD HELPER
def create_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, title, ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    # Sanitize content for FPDF (handles multi-line)
    pdf.multi_cell(0, 10, content.encode('latin-1', 'replace').decode('latin-1'))
    
    # Save to byte stream
    pdf_bytes = pdf.output()
    return io.BytesIO(pdf_bytes)


@app.get("/download/notes")
def download_notes(subject: str, db: Session = Depends(get_db)):
    sub = get_subject(db, subject)
    if not sub:
        return {"error": "Subject not found"}
    
    notes = db.query(Note).filter_by(subject_id=sub.id).all()
    content = "\n\n".join([f"Module {n.module}:\n{n.content}" for n in notes])
    
    file_stream = create_pdf(f"Study Notes: {sub.name}", content)
    
    headers = {'Content-Disposition': f'attachment; filename="{sub.code}_Notes.pdf"'}
    return Response(content=file_stream.getvalue(), media_type='application/pdf', headers=headers)

# Helper for Response
from fastapi.responses import Response

@app.get("/download/questions")
def download_questions(subject: str, type: str = "pyq", db: Session = Depends(get_db)):
    sub = get_subject(db, subject)
    if not sub:
        return {"error": "Subject not found"}
    
    qs = db.query(Question).filter_by(subject_id=sub.id, q_type=type).all()
    content = "\n\n".join([f"{i+1}. {q.text}" for i, q in enumerate(qs)])
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, f"{type.upper()} Questions: {sub.name}", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, content.encode('latin-1', 'replace').decode('latin-1'))
    
    pdf_output = pdf.output()
    return Response(content=pdf_output, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename={sub.code}_{type}.pdf"
    })
# ✅ ACADEMIC INFO
import requests
from bs4 import BeautifulSoup
def resilient_scrape(url):
    default = {"url": url, "title": "Access Official VTU Portal"}
    try:
        h = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=h, timeout=4)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                text = a.get_text(strip=True)
                href = a['href']
                # VTU links usually have substantial text, and we want pdfs or specific updates
                if len(text) > 15 and ('pdf' in href.lower() or 'circular' in href.lower() or 'notification' in href.lower() or 'time-table' in href.lower() or 'revised' in href.lower()):
                    # Avoid generic side navigation texts
                    if "download" not in text.lower() and "read more" not in text.lower():
                        return {"url": href, "title": text[:60] + "..." if len(text) > 60 else text}
    except Exception as e:
        print("Scrape error:", e)
    return default

@app.get("/academic-info")
def get_academic_info():
    cal = resilient_scrape("https://vtu.ac.in/en/academic-calendar/")
    tt = resilient_scrape("https://vtu.ac.in/en/category/examination/time-table/")
    circ = resilient_scrape("https://vtu.ac.in/en/circulars/")
    return {
        "calendar": cal,
        "timetable": tt,
        "circulars": circ
    }


# ── Run directly ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
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
Base.metadata.create_all(bind=engine)

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

def get_subject(db: Session, name: str) -> Subject | None:
    code = resolve_code(name)
    return db.query(Subject).filter(Subject.code == code).first()

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
        sub = get_subject(db, subname)
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
    sub = get_subject(db, data.get("subject", ""))
    if not sub:
        return {"questions": []}
    qs = db.query(Question).filter_by(subject_id=sub.id, q_type="pyq").all()
    return {"questions": [q.text for q in qs]}


# ✅ IMPORTANT QUESTIONS
@app.post("/important-questions")
def important_q(data: dict, db: Session = Depends(get_db)):
    sub = get_subject(db, data.get("subject", ""))
    if not sub:
        return {"questions": []}
    qs = db.query(Question).filter_by(subject_id=sub.id, q_type="important").all()
    return {"questions": [q.text for q in qs]}


# ✅ EXPECTED QUESTIONS
@app.post("/expected-questions")
def expected_q(data: dict, db: Session = Depends(get_db)):
    sub = get_subject(db, data.get("subject", ""))
    if not sub:
        return {"questions": []}
    qs = db.query(Question).filter_by(subject_id=sub.id, q_type="expected").all()
    return {"questions": [q.text for q in qs]}


# ✅ GET CONTENT / NOTES
@app.post("/get-content")
def get_content(data: dict, db: Session = Depends(get_db)):
    sub = get_subject(db, data.get("subject", ""))
    if not sub:
        return {"notes": "No data found for this subject.", "important": [], "questions": []}

    notes  = db.query(Note).filter_by(subject_id=sub.id, module=0).first()
    imp_qs = db.query(Question).filter_by(subject_id=sub.id, q_type="important").all()
    pyq    = db.query(Question).filter_by(subject_id=sub.id, q_type="pyq").all()

    return {
        "notes":     notes.content if notes else "No notes available.",
        "important": [q.text for q in imp_qs],
        "questions": [q.text for q in pyq],
    }


# ✅ MOCK EXAM
@app.post("/exam/start")
def start_exam(data: dict, db: Session = Depends(get_db)):
    sub = get_subject(db, data.get("subject", ""))
    if not sub:
        return {"questions": []}
    qs = db.query(Question).filter_by(subject_id=sub.id, q_type="pyq").all()
    selected = random.sample(qs, min(5, len(qs)))
    return {"questions": [q.text for q in selected]}


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
    if not user:
        return {"message": "Authentication required to upload.", "error": "Unauthorized"}

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
                db.add(Note(
                    subject_id=sub.id, 
                    user_id=user.id, 
                    module=99, 
                    content=f"[USER ({user.username}) UPLOADED PDF CONTENT: {file.filename}]\n{text}"
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
    
    if not qs:
        # Fallback to AI generation if none in DB
        from ai_engine import generate_aptitude_questions
        ai_res = generate_aptitude_questions(company)
        return {"questions": [], "ai_suggestion": ai_res}
    
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


# ── Run directly ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
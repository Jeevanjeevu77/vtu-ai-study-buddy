"""
main.py — VTU Genius AI  (FastAPI backend)
Features: SQLite DB, Groq LLaMA3, RAG for /ask, PDF upload & read
"""
import os, shutil, random
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Depends, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
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

from ai_engine import groq_chat_completion, get_groq_client

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
client = get_groq_client()

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static / Frontend ──────────────────────────────────────────────────────────
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def home():
    if os.path.exists(frontend_dir):
        return FileResponse(os.path.join(frontend_dir, "index.html"))
    return {"message": "VTU Genius AI Backend API is running."}

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
    if not name or name in ("Select Subject", ""):
        return None
    code = resolve_code(name)
    query = db.query(Subject).filter((Subject.code == code) | (Subject.name == name))
    if scheme:
        query = query.filter(Subject.scheme == scheme)
    if sem:
        sem_num = str(sem).replace("Sem ", "").strip()
        query = query.filter(Subject.semester == sem_num)
    sub = query.first()
    if not sub:
        try:
            sem_num = str(sem).replace("Sem ", "").strip() if sem else "3"
            scheme_val = scheme or "2022"
            sub = Subject(name=name, code=code or f"VTU_{name[:6].upper()}", scheme=scheme_val, semester=sem_num)
            db.add(sub)
            db.commit()
            db.refresh(sub)
        except Exception:
            db.rollback()
            sub = db.query(Subject).filter(Subject.name == name).first()
    return sub

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

# ✅ DEPARTMENTS
@app.get("/departments")
def departments_route():
    from syllabus import DEPARTMENTS
    return {"departments": DEPARTMENTS}

# ✅ SUBJECTS — list all subjects for a scheme + branch + sem
@app.get("/subjects")
def subjects_route(scheme: str = "2022", sem: str = "3", branch: str = "CSE", db: Session = Depends(get_db)):
    from syllabus import get_department_subjects
    dept_subs = get_department_subjects(branch, scheme, sem)
    if dept_subs:
        return {
            "subjects": [s["name"] for s in dept_subs],
            "details": dept_subs
        }
    
    # Fallback to DB
    sem_num = sem.replace("Sem ", "").strip()
    rows = db.query(Subject).filter_by(scheme=scheme, semester=sem_num).all()
    if rows:
        return {
            "subjects": [r.name for r in rows],
            "details": [{"name": r.name, "code": r.code} for r in rows]
        }
    return {"subjects": [], "details": []}



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
        res = groq_chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": q}
            ]
        )
        return {"answer": res.choices[0].message.content}
    except Exception as e:
        error_msg = str(e)
        print(f"DEBUG: AI Error - {error_msg}")
        if "AuthenticationError" in str(type(e)) or "401" in error_msg or "Invalid API Key" in error_msg or "not configured" in error_msg:
            # Fallback mock response so the UI still functions without an API Key
            mock_ans = (
                f"**[MOCK AI MODE]** I noticed you don't have a valid Groq API Key set!\n\n"
                f"But if I were AI, here is how I would answer your question about **'{q}'**:\n"
                f"• I would scan through the syllabus database.\n"
                f"• I would extract relevant topics.\n"
                f"• I'd generate bullet points summarizing the most important concepts for your exams!\n\n"
                f"*(To enable real AI, add a valid `GROQ_API_KEY` to the `/backend/.env` file)*"
            )
            return {"answer": mock_ans}
        return {"answer": f"⚠️ AI service unavailable right now. Error: {error_msg}"}



# ✅ GENERATE QUESTIONS — PYQ from DB + AI
@app.post("/generate")
def generate_q(data: dict, db: Session = Depends(get_db)):
    sub = get_subject(db, data.get("subject", ""), data.get("scheme"), data.get("sem"))
    if not sub:
        return {"questions": [], "modules": {}}
    
    qs = db.query(Question).filter_by(subject_id=sub.id, q_type="pyq").order_by(Question.unit).all()
    
    # If fewer than 50 PYQs, generate more with AI
    if len(qs) < 50:
        from ai_engine import generate_vtu_questions
        branch = data.get("branch", "CSE")
        ai_qs = generate_vtu_questions(sub.name, sub.scheme, sub.semester, branch, "pyq")
        if ai_qs:
            for q_data in ai_qs:
                text = q_data.get("text")
                module = q_data.get("module", 1)
                existing = db.query(Question).filter_by(subject_id=sub.id, text=text, q_type="pyq").first()
                if not existing:
                    db.add(Question(subject_id=sub.id, text=text, q_type="pyq", unit=module))
            db.commit()
            qs = db.query(Question).filter_by(subject_id=sub.id, q_type="pyq").order_by(Question.unit).all()
    
    # Organize by module
    modules = {}
    for q in qs:
        mod = q.unit if q.unit and 1 <= q.unit <= 5 else 1
        if mod not in modules:
            modules[mod] = []
        if q.text not in modules[mod]:
            modules[mod].append(q.text)
    
    total = sum(len(v) for v in modules.values())

    return {
        "modules": modules,
        "total": total,
        "subject": sub.name,
        "download_url": f"/download/questions?subject={sub.name}&type=pyq&scheme={sub.scheme}&sem={sub.semester}"
    }


# ✅ IMPORTANT QUESTIONS
@app.post("/important-questions")
def important_q(data: dict, db: Session = Depends(get_db)):
    sub = get_subject(db, data.get("subject", ""), data.get("scheme"), data.get("sem"))
    if not sub:
        return {"questions": [], "modules": {}}
    
    qs = db.query(Question).filter_by(subject_id=sub.id, q_type="important").order_by(Question.unit).all()
    
    # Need at least 50 (10 per module)
    if len(qs) < 50:
        from ai_engine import generate_vtu_questions
        branch = data.get("branch", "CSE")
        ai_qs = generate_vtu_questions(sub.name, sub.scheme, sub.semester, branch, "important")
        if ai_qs:
            for q_data in ai_qs:
                text = q_data.get("text")
                module = q_data.get("module", 1)
                existing = db.query(Question).filter_by(subject_id=sub.id, text=text, q_type="important").first()
                if not existing:
                    db.add(Question(subject_id=sub.id, text=text, q_type="important", unit=module))
            db.commit()
            qs = db.query(Question).filter_by(subject_id=sub.id, q_type="important").order_by(Question.unit).all()

    # Organize by module
    modules = {}
    for q in qs:
        mod = q.unit if q.unit and 1 <= q.unit <= 5 else 1
        if mod not in modules:
            modules[mod] = []
        if q.text not in modules[mod]:
            modules[mod].append(q.text)

    return {"modules": modules, "questions": list(dict.fromkeys(q.text for q in qs))}


# ✅ EXPECTED QUESTIONS
@app.post("/expected-questions")
def expected_q(data: dict, db: Session = Depends(get_db)):
    sub = get_subject(db, data.get("subject", ""), data.get("scheme"), data.get("sem"))
    if not sub:
        return {"questions": [], "modules": {}}
    
    qs = db.query(Question).filter_by(subject_id=sub.id, q_type="expected").order_by(Question.unit).all()
    
    if len(qs) < 50:
        from ai_engine import generate_vtu_questions
        branch = data.get("branch", "CSE")
        ai_qs = generate_vtu_questions(sub.name, sub.scheme, sub.semester, branch, "expected")
        if ai_qs:
            for q_data in ai_qs:
                text = q_data.get("text")
                module = q_data.get("module", 1)
                existing = db.query(Question).filter_by(subject_id=sub.id, text=text, q_type="expected").first()
                if not existing:
                    db.add(Question(subject_id=sub.id, text=text, q_type="expected", unit=module))
            db.commit()
            qs = db.query(Question).filter_by(subject_id=sub.id, q_type="expected").order_by(Question.unit).all()

    # Organize by module
    modules = {}
    for q in qs:
        mod = q.unit if q.unit and 1 <= q.unit <= 5 else 1
        if mod not in modules:
            modules[mod] = []
        if q.text not in modules[mod]:
            modules[mod].append(q.text)

    return {"modules": modules, "questions": list(dict.fromkeys(q.text for q in qs))}


# ✅ GET CONTENT / NOTES — Returns module-wise structured notes
@app.post("/get-content")
def get_content(data: dict, db: Session = Depends(get_db)):
    sub = get_subject(db, data.get("subject", ""), data.get("scheme"), data.get("sem"))
    if not sub:
        return {"notes": "No data found for this subject.", "modules": {}, "important": [], "questions": []}

    notes = db.query(Note).filter_by(subject_id=sub.id).order_by(Note.module).all()
    
    # Check if we have substantial notes for all 5 modules
    module_notes = {n.module: n.content for n in notes if 1 <= n.module <= 5}
    total_len = sum(len(c) for c in module_notes.values())
    
    # If notes are missing or too short, generate comprehensive ones via AI
    if len(module_notes) < 5 or total_len < 2500:
        from ai_engine import generate_vtu_notes
        branch = data.get("branch", "CSE")
        ai_notes = generate_vtu_notes(sub.name, sub.scheme, sub.semester, branch)
        if ai_notes:
            for item in ai_notes:
                mod_num = item.get("module")
                content = item.get("content", "")
                title = item.get("title", f"Module {mod_num}")
                if mod_num not in module_notes or len(module_notes.get(mod_num, "")) < 500:
                    module_notes[mod_num] = f"{title}\n\n{content}"
                    # Save to DB for persistence
                    existing = db.query(Note).filter_by(subject_id=sub.id, module=mod_num).first()
                    if existing:
                        existing.content = module_notes[mod_num]
                    else:
                        db.add(Note(subject_id=sub.id, module=mod_num, content=module_notes[mod_num]))
            db.commit()
    
    # Build structured response
    modules_response = {}
    for mod in range(1, 6):
        if mod in module_notes:
            modules_response[str(mod)] = module_notes[mod]
        else:
            modules_response[str(mod)] = f"Module {mod} notes are being generated. Please try again."

    return {
        "subject": sub.name,
        "modules": modules_response,
        "download_url": f"/download/notes?subject={sub.name}&scheme={sub.scheme}&sem={sub.semester}"
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
    try:
        content_bytes = await file.read()
        if not content_bytes:
            return {"error": "Empty file received."}

        # Attempt to save to disk if possible (ignored if read-only filesystem like Vercel)
        try:
            os.makedirs("uploads", exist_ok=True)
            with open(f"uploads/{file.filename}", "wb") as buffer:
                buffer.write(content_bytes)
        except Exception:
            pass

        # Extract text in-memory
        reader = PdfReader(io.BytesIO(content_bytes))
        text = "".join(page.extract_text() or "" for page in reader.pages)

        target_subject = subject.strip() if subject and subject != "Select Subject" else "General"
        sub = get_subject(db, target_subject)
        if not sub:
            code = resolve_code(target_subject)
            sub = Subject(name=target_subject, code=code, scheme="2022", semester="3", branch="CS")
            db.add(sub)
            db.commit()
            db.refresh(sub)

        uploader_name = user.username if user else "Guest"
        uploader_id = user.id if user else None

        if text.strip():
            db.add(Note(
                subject_id=sub.id, 
                user_id=uploader_id, 
                module=99, 
                content=f"[{uploader_name} UPLOADED PDF CONTENT: {file.filename}]\n{text.strip()}"
            ))
            db.commit()
            return {"message": f"PDF '{file.filename}' processed & indexed for {target_subject}."}
        else:
            return {"message": f"PDF '{file.filename}' uploaded, but no extractable text found (it may contain scanned images)."}
    except Exception as e:
        print(f"DEBUG: PDF Upload Error: {e}")
        return {"error": f"Could not process PDF: {str(e)}"}




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


@app.post("/interview/start")
def interview_start(data: dict):
    company = data.get("company", "General")
    role    = data.get("role", "Software Engineer")
    from ai_engine import generate_mock_interview_questions
    ai_res = generate_mock_interview_questions(company, role)
    return {"question": ai_res, "questions": ai_res}

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
    try:
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
    except Exception:
        pdf_bytes = pdf.output()
    return io.BytesIO(pdf_bytes)


# ✅ OFFICIAL VTU MODEL QUESTION PAPER
@app.post("/vtu/model-paper")
def vtu_model_paper(data: dict):
    subject = data.get("subject", "Data Structures and Applications")
    scheme  = str(data.get("scheme", "2022"))
    sem     = str(data.get("sem", "3"))
    branch  = data.get("branch", "CSE")
    code    = data.get("code")
    
    from ai_engine import generate_vtu_model_paper
    paper = generate_vtu_model_paper(subject, scheme, sem, branch, code)
    if not paper:
        return {"error": "Failed to generate VTU model question paper"}
    return paper


@app.post("/vtu/model-paper/pdf")
def vtu_model_paper_pdf_post(data: dict):
    from vtu_paper_pdf import generate_vtu_paper_pdf
    pdf_bytes = generate_vtu_paper_pdf(data)
    
    code = data.get("course_code", "VTU_Paper")
    filename = f"{code}_Model_Question_Paper.pdf"
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.get("/download/model-paper-pdf")
def download_model_paper_pdf(
    subject: str, 
    scheme: str = "2022", 
    sem: str = "3", 
    branch: str = "CSE",
    code: str = None
):
    from ai_engine import generate_vtu_model_paper
    from vtu_paper_pdf import generate_vtu_paper_pdf
    
    paper = generate_vtu_model_paper(subject, scheme, sem, branch, code)
    pdf_bytes = generate_vtu_paper_pdf(paper)
    
    code_str = code or f"{scheme[-2:] if len(scheme)>=2 else '22'}{branch[:2].upper()}{sem}1"
    clean_sub = "".join(c for c in subject if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
    filename = f"{code_str}_{clean_sub}_Model_Paper.pdf"
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )



@app.get("/download/notes")
def download_notes(subject: str, scheme: str = "2022", sem: str = "3", db: Session = Depends(get_db)):
    sub = get_subject(db, subject, scheme, sem)
    
    notes = []
    sub_name = subject or "Subject"
    sub_code = "SUB"
    if sub:
        notes = db.query(Note).filter_by(subject_id=sub.id).order_by(Note.module).all()
        sub_name = sub.name
        sub_code = sub.code
    
    # Calculate total length of module 1-5 notes
    total_len = sum(len(n.content) for n in notes if 1 <= n.module <= 5)
    
    # If fewer than 5 modules OR total content is too short (less than 2500 chars total), trigger AI
    if len([n for n in notes if 1 <= n.module <= 5]) < 5 or total_len < 2500:
        print(f"DEBUG: Notes for {sub_name} are insufficient ({total_len} chars). Triggering AI Exhaustive Notes...")
        from ai_engine import generate_vtu_notes
        ai_notes = generate_vtu_notes(sub_name, scheme, sem)
        if ai_notes:
            # Create a combined view: prefer DB notes if they exist for a module, otherwise use AI
            db_module_map = {n.module: n.content for n in notes}
            combined_content = []
            for item in ai_notes:
                mod_num = item.get("module")
                ai_content = item.get("content")
                content = db_module_map.get(mod_num, ai_content)
                combined_content.append((mod_num, content))
            
            # Reconstruct notes list for PDF generation
            notes_data = []
            for mod_num, content in combined_content:
                notes_data.append(type('Note', (), {'module': mod_num, 'content': content}))
            notes = notes_data

    # Unique modules check to ensure we say "All 5 Modules" if they exist
    content = ""
    for n in notes:
        mod_label = f"Module {n.module}" if n.module > 0 else "Introduction"
        if n.module == 99: mod_label = "Supplemental Material"
        content += f"--- {mod_label} ---\n{n.content}\n\n"
    
    if not content:
        content = f"Comprehensive 5-module notes for {sub_name} are currently being indexed. Please try again in 5 minutes."

    file_stream = create_pdf(f"VTU Study Buddy - {sub_name} Notes", content)
    
    filename = f"{sub_code}_Complete_Notes.pdf".replace(" ", "_")
    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"',
        'Access-Control-Expose-Headers': 'Content-Disposition'
    }
    return Response(content=file_stream.getvalue(), media_type='application/pdf', headers=headers)

# Helper for Response
# (Imported at top)

@app.get("/download/questions")
def download_questions(subject: str, q_type: str = Query("pyq", alias="type"), scheme: str = "2022", sem: str = "3", db: Session = Depends(get_db)):
    sub = get_subject(db, subject, scheme, sem)
    
    qs = []
    sub_name = subject or "Subject"
    sub_code = "SUB"
    if sub:
        qs = db.query(Question).filter_by(subject_id=sub.id, q_type=q_type).order_by(Question.unit).all()
        sub_name = sub.name
        sub_code = sub.code

    # If no questions in DB, try generating them with AI
    if not qs:
        from ai_engine import generate_vtu_questions
        ai_qs = generate_vtu_questions(sub_name, scheme, sem, q_type)
        if ai_qs:
            qs = [type('Question', (), {'unit': q['module'], 'text': q['text']}) for q in ai_qs]

    content = ""
    current_unit = -1
    for q in qs:
        if q.unit != current_unit:
            current_unit = q.unit
            content += f"\n--- Unit/Module {current_unit} ---\n"
        content += f"• {q.text}\n"
    
    if not content:
        content = f"Official VTU {q_type.upper()} questions for {sub_name} are being synthesized."

    file_stream = create_pdf(f"VTU {q_type.upper()} Questions: {sub_name}", content)
    
    filename = f"{sub_code}_{q_type}_Questions.pdf".replace(" ", "_")
    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "Access-Control-Expose-Headers": "Content-Disposition"
    }
    return Response(content=file_stream.getvalue(), media_type="application/pdf", headers=headers)
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


# ✅ COMMUNITY NOTES
@app.get("/community-notes")
def get_community_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).filter(Note.is_public == 1).order_by(Note.id.desc()).limit(50).all()
    res = []
    for n in notes:
        sub_name = n.subject.name if n.subject else "General"
        user_name = n.user.username if n.user else "Anonymous"
        res.append({
            "id": n.id,
            "subject": sub_name,
            "module": n.module,
            "content": n.content[:200] + "..." if len(n.content) > 200 else n.content,
            "author": user_name
        })
    return {"notes": res}

@app.post("/community-notes/publish")
def publish_note(data: dict, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    note_id = data.get("note_id")
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user.id).first()
    if note:
        note.is_public = 1
        db.commit()
        return {"message": "Note published to community"}
    return {"error": "Note not found or unauthorized"}

# ✅ AI FLASHCARDS
@app.post("/generate-flashcards")
def generate_flashcards(data: dict, db: Session = Depends(get_db)):
    subject_name = data.get("subject", "General")
    sub = get_subject(db, subject_name)
    if not sub:
        return {"flashcards": []}
        
    from models import Flashcard
    existing = db.query(Flashcard).filter(Flashcard.subject_id == sub.id).all()
    if existing and len(existing) >= 5:
        return {"flashcards": [{"q": f.question, "a": f.answer} for f in existing]}
        
    system_prompt = "You are a VTU exam tutor. Generate 5 short Q&A flashcards for the subject. Return exactly in format: Q: [question] | A: [answer]"
    prompt = f"Subject: {subject_name}. Generate 5 flashcards."
    try:
        from ai_engine import groq_chat_completion
        res = groq_chat_completion([{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}])
        text = res.choices[0].message.content
        cards = []
        for line in text.split('\n'):
            if "Q:" in line and "A:" in line:
                parts = line.split("| A:")
                q = parts[0].replace("Q:", "").strip()
                a = parts[1].strip()
                cards.append({"q": q, "a": a})
                db.add(Flashcard(subject_id=sub.id, question=q, answer=a))
        db.commit()
        if cards: return {"flashcards": cards}
    except Exception as e:
        print("Flashcard generation error:", e)
    
    # Fallback mock cards
    return {"flashcards": [
        {"q": f"What is a key concept in {subject_name}?", "a": "It involves studying the fundamental principles of the subject."},
        {"q": f"Define the primary goal of {subject_name}.", "a": "To optimize and understand the underlying mechanisms."},
    ]}

# ✅ BUILT-IN COMPILER (PISTON API)
@app.post("/compile")
def compile_code(data: dict):
    code = data.get("code", "")
    language = data.get("language", "python")
    
    if language != "python":
        return {"output": "Currently, the built-in compiler only supports Python natively. Please select Python to run code!"}
        
    import subprocess
    import tempfile
    import os
    import sys
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name
            
        try:
            # Run the python code with a 5 second timeout
            res = subprocess.run([sys.executable, temp_path], capture_output=True, text=True, timeout=5)
            output = res.stdout + res.stderr
            return {"output": output or "Program finished with no output."}
        finally:
            os.remove(temp_path)
    except subprocess.TimeoutExpired:
        return {"output": "Execution timed out (5 seconds)."}
    except Exception as e:
        return {"output": f"Execution failed: {e}"}

# ✅ YOUTUBE SUMMARIZER
@app.post("/youtube-summary")
def youtube_summary(data: dict):
    url = data.get("url", "")
    if "v=" not in url and "youtu.be/" not in url:
        return {"summary": "Invalid YouTube URL"}
        
    try:
        # Extract video ID
        vid = url.split("v=")[-1].split("&")[0] if "v=" in url else url.split("youtu.be/")[-1].split("?")[0]
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            transcript_list = YouTubeTranscriptApi().fetch(vid, languages=['en', 'en-US', 'en-GB', 'en-IN', 'hi', 'bn'])
            text = " ".join([t.text for t in transcript_list])[:5000] # get first 5000 chars
        except Exception as e:
            return {"summary": f"Could not fetch transcript (maybe it doesn't have subtitles): {e}"}
            
        system_prompt = "Summarize the following YouTube video transcript in bullet points for a student."
        from ai_engine import groq_chat_completion
        res = groq_chat_completion([{"role": "system", "content": system_prompt}, {"role": "user", "content": text}])
        return {"summary": res.choices[0].message.content}
    except Exception as e:
        return {"summary": f"Summary failed: {e}"}

# ✅ USER PROGRESS TRACKING
@app.get("/progress")
def get_progress(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user: return {'detail': 'Not authenticated'}
    from models import UserProgress
    prog = db.query(UserProgress).filter(UserProgress.user_id == user.id).first()
    if not prog:
        prog = UserProgress(user_id=user.id)
        db.add(prog)
        db.commit()
        db.refresh(prog)
    return {
        "streak": prog.study_streak,
        "mock_score": prog.mock_score,
        "modules_read": prog.modules_read
    }

# ── Run directly ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)

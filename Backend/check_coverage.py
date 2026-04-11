"""check_coverage.py — Report on DB coverage across all schemes/semesters"""
from database import SessionLocal
from models import Subject, Note, Question

db = SessionLocal()

total_subjects = 0
total_notes = 0
total_questions = 0

for s in ["2018", "2021", "2022"]:
    print(f"\n{'='*50}")
    print(f"  SCHEME {s}")
    print(f"{'='*50}")
    for sem in ["1","2","3","4","5","6","7","8"]:
        subs = db.query(Subject).filter_by(scheme=s, semester=sem).all()
        n = sum(db.query(Note).filter(Note.subject_id==sub.id).count() for sub in subs)
        q = sum(db.query(Question).filter(Question.subject_id==sub.id).count() for sub in subs)
        names = ", ".join(sub.name for sub in subs)
        status = "✅" if subs else "❌"
        print(f"  {status} Sem {sem}: {len(subs)} subjects, {n} notes, {q} questions")
        if names:
            print(f"     → {names}")
        total_subjects += len(subs)
        total_notes += n
        total_questions += q

print(f"\n{'='*50}")
print(f"  GRAND TOTAL: {total_subjects} subjects, {total_notes} notes, {total_questions} questions")
print(f"{'='*50}")

db.close()

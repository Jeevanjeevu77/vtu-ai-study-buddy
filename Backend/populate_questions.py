"""
populate_questions.py — Pre-populate VTU subjects with 5 questions per module.
Run: python populate_questions.py
"""
import sys
import os
# Ensure we can import from current directory
sys.path.append(os.getcwd())

from database import SessionLocal
from models import Subject, Question
from ai_engine import generate_vtu_questions

def deep_seed():
    db = SessionLocal()
    subjects = db.query(Subject).all()
    print(f"Checking {len(subjects)} subjects for question density...")

    for sub in subjects:
        for q_type in ["important", "expected"]:
            existing_count = db.query(Question).filter_by(subject_id=sub.id, q_type=q_type).count()
            
            if existing_count < 25:
                print(f"   -> Seeding {q_type} questions for {sub.name} ({sub.code}) [Scheme: {sub.scheme}, Sem: {sub.semester}]...")
                ai_qs = generate_vtu_questions(sub.name, sub.scheme, sub.semester, q_type)
                
                if ai_qs:
                    added = 0
                    for q_data in ai_qs:
                        text = q_data.get("text")
                        module = q_data.get("module", 1)
                        # Avoid duplicates
                        existing = db.query(Question).filter_by(subject_id=sub.id, text=text, q_type=q_type).first()
                        if not existing:
                            db.add(Question(subject_id=sub.id, text=text, q_type=q_type, unit=module))
                            added += 1
                    db.commit()
                    print(f"      Success: Added {added} questions.")
                else:
                    print(f"      Failed: AI returned no questions for {sub.name}.")
            else:
                print(f"   -> {sub.name} already has {existing_count} {q_type} questions.")

    db.close()
    print("\nAll subjects processed!")

if __name__ == "__main__":
    deep_seed()

"""
models.py — SQLAlchemy ORM models for VTU Genius AI
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id       = Column(Integer, primary_key=True, index=True)
    name     = Column(String, nullable=False)          # e.g. "Data Structures"
    code     = Column(String, nullable=False)          # e.g. "DSA"
    scheme   = Column(String, nullable=False)          # e.g. "2022"
    semester = Column(String, nullable=False)          # e.g. "3"
    branch   = Column(String, default="CS")            # e.g. "CS" / "EC" / "ME"

    notes     = relationship("Note",     back_populates="subject", cascade="all, delete")
    questions = relationship("Question", back_populates="subject", cascade="all, delete")


class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    username      = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    notes         = relationship("Note", back_populates="user", cascade="all, delete")

class Note(Base):
    __tablename__ = "notes"

    id         = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=True)
    module     = Column(Integer, default=0)            # 0 = general, 1–5 = unit numbers
    content    = Column(Text, nullable=False)
    pdf_path   = Column(String, nullable=True)         # path to uploaded PDF if any

    subject = relationship("Subject", back_populates="notes")
    user    = relationship("User", back_populates="notes")


class Question(Base):
    __tablename__ = "questions"

    id         = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    text       = Column(Text, nullable=False)
    q_type     = Column(String, nullable=False)        # "pyq" | "important" | "expected"
    unit       = Column(Integer, default=1)

    subject = relationship("Subject", back_populates="questions")

class AptitudeQuestion(Base):
    __tablename__ = "aptitude_questions"

    id          = Column(Integer, primary_key=True, index=True)
    company     = Column(String, index=True)            # e.g. "TCS", "Infosys"
    category    = Column(String)                        # e.g. "Quantitative", "Logical", "Verbal"
    question    = Column(Text, nullable=False)
    option_a    = Column(String)
    option_b    = Column(String)
    option_c    = Column(String)
    option_d    = Column(String)
    answer      = Column(String)                        # e.g. "A"
    explanation = Column(Text, nullable=True)
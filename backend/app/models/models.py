from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, Enum, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

# Association table for many-to-many relationship between users and courses
course_enrollment = Table(
    "course_enrollment",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("course.id"), primary_key=True),
    Column("enrolled_at", DateTime, default=datetime.utcnow),
    Column("progress", Float, default=0.0),  # 0-100
)

class RoleEnum(str, enum.Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"

class PaymentStatusEnum(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class QuestionTypeEnum(str, enum.Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"
    TRUE_FALSE = "true_false"

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(255))
    phone = Column(String(20), nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.STUDENT)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    courses_enrolled = relationship("Course", secondary=course_enrollment, backref="students")
    courses_created = relationship("Course", backref="instructor", foreign_keys="Course.instructor_id")
    payments = relationship("Payment", backref="user")
    certificates = relationship("Certificate", backref="user")
    quiz_attempts = relationship("QuizAttempt", backref="user")
    lessons_progress = relationship("LessonProgress", backref="user")

class Course(Base):
    __tablename__ = "course"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(Text)
    slug = Column(String(255), unique=True, index=True)
    thumbnail_url = Column(String(500), nullable=True)
    price = Column(Float, default=0.0)
    currency = Column(String(3), default="USD")
    is_free = Column(Boolean, default=False)
    duration_hours = Column(Float, nullable=True)
    duration_weeks = Column(Integer, nullable=True)
    level = Column(String(50), default="beginner")  # beginner, intermediate, advanced
    category = Column(String(100), index=True)
    is_published = Column(Boolean, default=False)
    instructor_id = Column(Integer, ForeignKey("user.id"))
    learning_objectives = Column(Text, nullable=True)  # Store as JSON string
    requirements = Column(Text, nullable=True)  # Store as JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lessons = relationship("Lesson", backref="course", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", backref="course", cascade="all, delete-orphan")
    payments = relationship("Payment", backref="course")

class Lesson(Base):
    __tablename__ = "lesson"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("course.id"))
    title = Column(String(255))
    description = Column(Text, nullable=True)
    order = Column(Integer)
    content_type = Column(String(50))  # video, document, text
    content_url = Column(String(500))
    duration_minutes = Column(Integer, nullable=True)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    progress = relationship("LessonProgress", backref="lesson", cascade="all, delete-orphan")

class LessonProgress(Base):
    __tablename__ = "lesson_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    lesson_id = Column(Integer, ForeignKey("lesson.id"))
    completed = Column(Boolean, default=False)
    progress_percent = Column(Float, default=0.0)
    last_accessed = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class Quiz(Base):
    __tablename__ = "quiz"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("course.id"))
    title = Column(String(255))
    description = Column(Text, nullable=True)
    passing_score = Column(Float, default=60.0)
    time_limit_minutes = Column(Integer, nullable=True)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    questions = relationship("Question", backref="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", backref="quiz", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "question"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quiz.id"))
    question_text = Column(Text)
    question_type = Column(Enum(QuestionTypeEnum))
    correct_answer = Column(Text)  # JSON for multiple choice
    explanation = Column(Text, nullable=True)
    order = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    answers = relationship("Answer", backref="question", cascade="all, delete-orphan")

class Answer(Base):
    __tablename__ = "answer"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("question.id"))
    answer_text = Column(Text)
    is_correct = Column(Boolean, default=False)
    order = Column(Integer)

class QuizAttempt(Base):
    __tablename__ = "quiz_attempt"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quiz.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    score = Column(Float, nullable=True)
    passed = Column(Boolean, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    responses = relationship("QuestionResponse", backref="attempt", cascade="all, delete-orphan")

class QuestionResponse(Base):
    __tablename__ = "question_response"
    
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempt.id"))
    question_id = Column(Integer, ForeignKey("question.id"))
    student_answer = Column(Text)
    is_correct = Column(Boolean, nullable=True)
    points_earned = Column(Float, default=0.0)

class Payment(Base):
    __tablename__ = "payment"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    course_id = Column(Integer, ForeignKey("course.id"))
    amount = Column(Float)
    currency = Column(String(3), default="USD")
    payment_method = Column(String(50))  # paystack, flutterwave
    transaction_id = Column(String(255), unique=True, index=True)
    reference = Column(String(255), unique=True)
    status = Column(Enum(PaymentStatusEnum), default=PaymentStatusEnum.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Certificate(Base):
    __tablename__ = "certificate"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    course_id = Column(Integer, ForeignKey("course.id"))
    certificate_number = Column(String(100), unique=True, index=True)
    issue_date = Column(DateTime, default=datetime.utcnow)
    pdf_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notification"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    title = Column(String(255))
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

"""
Database models for EduLearn Platform
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Float,
    ForeignKey, Table, Enum, LargeBinary, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum
from app.core.database import Base


# Association tables for many-to-many relationships
course_prerequisites = Table(
    'course_prerequisites',
    Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True),
    Column('prerequisite_id', Integer, ForeignKey('courses.id'), primary_key=True)
)

student_courses = Table(
    'student_courses',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True),
    Column('enrolled_at', DateTime, default=func.now()),
)


class UserRole(str, enum.Enum):
    """User roles in the platform"""
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"


class User(Base):
    """User model for students, instructors, and admins"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255), nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime, nullable=True)
    
    # Relationships
    courses_created = relationship("Course", back_populates="instructor", foreign_keys="Course.instructor_id")
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="student", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="student", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User {self.username}>"


class Course(Base):
    """Course model"""
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    thumbnail_url = Column(String(500), nullable=True)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    level = Column(String(50), default="beginner")  # beginner, intermediate, advanced
    price = Column(Float, default=0.0)
    currency = Column(String(10), default="NGN")
    is_published = Column(Boolean, default=False, index=True)
    is_free = Column(Boolean, default=False)
    
    # Course details
    learning_objectives = Column(JSON, nullable=True)  # List of learning objectives
    requirements = Column(JSON, nullable=True)  # List of requirements
    duration_hours = Column(Float, nullable=True)
    
    # Relationships
    instructor = relationship("User", back_populates="courses_created", foreign_keys=[instructor_id])
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="course", cascade="all, delete-orphan")
    prerequisites = relationship(
        "Course",
        secondary=course_prerequisites,
        primaryjoin=id == course_prerequisites.c.course_id,
        secondaryjoin=id == course_prerequisites.c.prerequisite_id,
    )
    certificates = relationship("Certificate", back_populates="course", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Course {self.title}>"


class Lesson(Base):
    """Lesson model for course content"""
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, nullable=False)
    
    # Content types: video, document, text
    content_type = Column(String(50), nullable=False)  # video, document, text
    content_url = Column(String(500), nullable=True)  # URL for video or document
    content_text = Column(Text, nullable=True)  # For text content
    
    duration_seconds = Column(Integer, nullable=True)
    is_free = Column(Boolean, default=False)
    
    # Relationships
    course = relationship("Course", back_populates="lessons")
    progress = relationship("LessonProgress", back_populates="lesson", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Lesson {self.title}>"


class Enrollment(Base):
    """Enrollment model for student-course relationship"""
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    
    enrollment_date = Column(DateTime, default=func.now())
    is_completed = Column(Boolean, default=False)
    completion_date = Column(DateTime, nullable=True)
    progress_percentage = Column(Float, default=0.0)
    
    # Relationships
    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    progress = relationship("LessonProgress", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Enrollment {self.student_id}-{self.course_id}>"


class LessonProgress(Base):
    """Track student progress through lessons"""
    __tablename__ = "lesson_progress"

    id = Column(Integer, primary_key=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False, index=True)
    
    is_completed = Column(Boolean, default=False)
    progress_percentage = Column(Float, default=0.0)
    time_spent_seconds = Column(Integer, default=0)
    last_position_seconds = Column(Integer, default=0)  # For video lessons
    
    # Relationships
    lesson = relationship("Lesson", back_populates="progress")
    
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<LessonProgress {self.enrollment_id}-{self.lesson_id}>"


class Quiz(Base):
    """Quiz model"""
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, nullable=False)
    
    passing_score = Column(Float, default=60.0)
    max_attempts = Column(Integer, default=3)
    time_limit_minutes = Column(Integer, nullable=True)
    shuffle_questions = Column(Boolean, default=False)
    
    # Relationships
    course = relationship("Course", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Quiz {self.title}>"


class Question(Base):
    """Question model for quizzes"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)  # multiple_choice, true_false, short_answer
    order = Column(Integer, nullable=False)
    points = Column(Float, default=1.0)
    
    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan")
    answers = relationship("StudentAnswer", back_populates="question", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Question {self.question_text[:50]}>"


class QuestionOption(Base):
    """Options for multiple choice questions"""
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    option_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    order = Column(Integer, nullable=False)
    
    # Relationships
    question = relationship("Question", back_populates="options")
    
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<QuestionOption {self.option_text[:50]}>"


class QuizAttempt(Base):
    """Track student quiz attempts"""
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False, index=True)
    
    score = Column(Float, default=0.0)
    max_score = Column(Float, nullable=False)
    is_passed = Column(Boolean, default=False)
    attempt_number = Column(Integer, nullable=False)
    time_taken_seconds = Column(Integer, nullable=True)
    
    # Relationships
    student = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")
    answers = relationship("StudentAnswer", back_populates="attempt", cascade="all, delete-orphan")
    
    completed_at = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<QuizAttempt {self.student_id}-{self.quiz_id}>"


class StudentAnswer(Base):
    """Student answers to quiz questions"""
    __tablename__ = "student_answers"

    id = Column(Integer, primary_key=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    selected_option_id = Column(Integer, ForeignKey("question_options.id"), nullable=True)
    answer_text = Column(Text, nullable=True)  # For short answer questions
    
    points_earned = Column(Float, default=0.0)
    
    # Relationships
    attempt = relationship("QuizAttempt", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<StudentAnswer {self.attempt_id}-{self.question_id}>"


class Payment(Base):
    """Payment model for course enrollments"""
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True, index=True)
    
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="NGN")
    payment_method = Column(String(50), nullable=False)  # paystack, flutterwave
    
    # Payment tracking
    reference = Column(String(255), unique=True, nullable=False, index=True)
    transaction_id = Column(String(255), unique=True, nullable=True)
    status = Column(String(50), default="pending", index=True)  # pending, completed, failed, cancelled
    
    payment_date = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="payments")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Payment {self.reference}>"


class Certificate(Base):
    """Certificate model"""
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    
    certificate_number = Column(String(255), unique=True, nullable=False, index=True)
    certificate_url = Column(String(500), nullable=False)
    
    issued_date = Column(DateTime, default=func.now())
    expiry_date = Column(DateTime, nullable=True)
    
    # Relationships
    student = relationship("User", back_populates="certificates")
    course = relationship("Course", back_populates="certificates")
    
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Certificate {self.certificate_number}>"


class Revenue(Base):
    """Revenue tracking for courses and instructors"""
    __tablename__ = "revenues"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    total_revenue = Column(Float, default=0.0)
    total_enrollments = Column(Integer, default=0)
    total_students = Column(Integer, default=0)
    
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Revenue {self.course_id}-{self.year}-{self.month}>"

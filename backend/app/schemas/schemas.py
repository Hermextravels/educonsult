from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ==================== User Schemas ====================
class UserRole(str, Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"


class UserRegister(BaseModel):
    """User registration schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: UserRole = UserRole.STUDENT


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response schema"""
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """User update schema"""
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenRefresh(BaseModel):
    """Token refresh schema"""
    refresh_token: str


# ==================== Course Schemas ====================
class CourseCreate(BaseModel):
    """Create course schema"""
    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=10)
    category: str
    level: str = "beginner"
    price: float = 0.0
    currency: str = "NGN"
    is_free: bool = False
    thumbnail_url: Optional[str] = None
    learning_objectives: Optional[List[str]] = None
    requirements: Optional[List[str]] = None
    duration_hours: Optional[float] = None


class CourseUpdate(BaseModel):
    """Update course schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    level: Optional[str] = None
    price: Optional[float] = None
    is_free: Optional[bool] = None
    is_published: Optional[bool] = None
    learning_objectives: Optional[List[str]] = None
    requirements: Optional[List[str]] = None
    duration_hours: Optional[float] = None


class CourseResponse(BaseModel):
    """Course response schema"""
    id: int
    title: str
    description: str
    slug: str
    category: str
    level: str
    price: float
    currency: str
    is_published: bool
    is_free: bool
    instructor_id: int
    thumbnail_url: Optional[str] = None
    duration_hours: Optional[float] = None
    learning_objectives: Optional[List[str]] = None
    requirements: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    @validator('learning_objectives', 'requirements', pre=True)
    def parse_json_fields(cls, v):
        """Convert JSON strings to lists"""
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except:
                return []
        return v

    class Config:
        from_attributes = True


# ==================== Lesson Schemas ====================
class LessonCreate(BaseModel):
    """Create lesson schema"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    order: int
    content_type: str  # video, document, text
    content_url: Optional[str] = None
    content_text: Optional[str] = None
    duration_seconds: Optional[int] = None
    is_free: bool = False


class LessonUpdate(BaseModel):
    """Update lesson schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    content_url: Optional[str] = None
    content_text: Optional[str] = None
    duration_seconds: Optional[int] = None
    is_free: Optional[bool] = None


class LessonResponse(BaseModel):
    """Lesson response schema"""
    id: int
    course_id: int
    title: str
    description: Optional[str]
    order: int
    content_type: str
    content_url: Optional[str]
    duration_seconds: Optional[int]
    is_free: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Enrollment Schemas ====================
class EnrollmentResponse(BaseModel):
    """Enrollment response schema"""
    id: int
    student_id: int
    course_id: int
    enrollment_date: datetime
    is_completed: bool
    progress_percentage: float
    completion_date: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== Quiz Schemas ====================
class QuizCreate(BaseModel):
    """Create quiz schema"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    order: int
    passing_score: float = 60.0
    max_attempts: int = 3
    time_limit_minutes: Optional[int] = None
    shuffle_questions: bool = False


class QuizUpdate(BaseModel):
    """Update quiz schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    passing_score: Optional[float] = None
    max_attempts: Optional[int] = None
    time_limit_minutes: Optional[int] = None
    shuffle_questions: Optional[bool] = None


class QuizResponse(BaseModel):
    """Quiz response schema"""
    id: int
    course_id: int
    title: str
    description: Optional[str]
    order: int
    passing_score: float
    max_attempts: int
    time_limit_minutes: Optional[int]
    shuffle_questions: bool
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionOptionResponse(BaseModel):
    """Question option response schema"""
    id: int
    option_text: str
    order: int

    class Config:
        from_attributes = True


class QuestionOptionCreate(BaseModel):
    """Question option create schema"""
    option_text: str
    is_correct: bool
    order: int


class QuestionCreate(BaseModel):
    """Create question schema"""
    question_text: str = Field(..., min_length=1)
    question_type: str  # multiple_choice, true_false, short_answer
    order: int
    points: float = 1.0
    options: Optional[List[QuestionOptionCreate]] = None


class QuestionResponse(BaseModel):
    """Question response schema"""
    id: int
    quiz_id: int
    question_text: str
    question_type: str
    order: int
    points: float
    options: Optional[List[QuestionOptionResponse]] = None

    class Config:
        from_attributes = True


class StudentAnswerCreate(BaseModel):
    """Student answer submission"""
    question_id: int
    selected_option_id: Optional[int] = None
    answer_text: Optional[str] = None


class QuizAttemptResponse(BaseModel):
    """Quiz attempt response schema"""
    id: int
    student_id: int
    quiz_id: int
    score: float
    max_score: float
    is_passed: bool
    attempt_number: int
    time_taken_seconds: Optional[int]
    completed_at: datetime

    class Config:
        from_attributes = True


# ==================== Payment Schemas ====================
class PaymentCreate(BaseModel):
    """Create payment schema"""
    course_id: int
    amount: float
    currency: str = "NGN"
    payment_method: str  # paystack, flutterwave


class PaymentResponse(BaseModel):
    """Payment response schema"""
    id: int
    user_id: int
    course_id: Optional[int]
    amount: float
    currency: str
    reference: str
    transaction_id: Optional[str]
    status: str
    payment_date: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PaymentWebhookPaystack(BaseModel):
    """Paystack webhook payload"""
    event: str
    data: dict


class PaymentWebhookFlutterwave(BaseModel):
    """Flutterwave webhook payload"""
    event: str
    data: dict


# ==================== Certificate Schemas ====================
class CertificateResponse(BaseModel):
    """Certificate response schema"""
    id: int
    student_id: int
    course_id: int
    certificate_number: str
    certificate_url: str
    issued_date: datetime
    expiry_date: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== Pagination Schemas ====================
class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)


class PaginatedResponse(BaseModel):
    """Paginated response schema"""
    total: int
    page: int
    page_size: int
    total_pages: int
    data: list


# ==================== Dashboard Schemas ====================
class StudentDashboardStats(BaseModel):
    """Student dashboard statistics"""
    total_courses: int
    courses_completed: int
    courses_in_progress: int
    total_certificates: int
    total_spent: float


class InstructorDashboardStats(BaseModel):
    """Instructor dashboard statistics"""
    total_courses: int
    total_students: int
    total_revenue: float
    average_rating: Optional[float] = None


class AdminDashboardStats(BaseModel):
    """Admin dashboard statistics"""
    total_users: int
    total_courses: int
    total_revenue: float
    total_payments: int
    pending_payments: int
    is_published: Optional[bool] = None


class LessonProgressResponse(BaseModel):
    id: int
    lesson_id: int
    completed: bool
    progress_percent: float
    last_accessed: datetime
    
    class Config:
        from_attributes = True

# Quiz Schemas
class AnswerCreate(BaseModel):
    answer_text: str
    is_correct: bool
    order: int

class QuestionBase(BaseModel):
    question_text: str
    question_type: str
    correct_answer: str
    explanation: Optional[str] = None
    order: int

class QuestionCreate(QuestionBase):
    answers: Optional[List[AnswerCreate]] = None

class QuestionResponse(QuestionBase):
    id: int
    quiz_id: int
    
    class Config:
        from_attributes = True

class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    passing_score: float = 60.0
    time_limit_minutes: Optional[int] = None

class QuizCreate(QuizBase):
    questions: Optional[List[QuestionCreate]] = None

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    passing_score: Optional[float] = None
    is_published: Optional[bool] = None

class QuizResponse(QuizBase):
    id: int
    course_id: int
    is_published: bool
    question_count: int = 0
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuestionResponseSubmit(BaseModel):
    question_id: int
    student_answer: str

class QuizSubmissionRequest(BaseModel):
    responses: List[QuestionResponseSubmit]

class QuizAttemptResponse(BaseModel):
    id: int
    quiz_id: int
    user_id: int
    score: Optional[float]
    passed: Optional[bool]
    started_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Payment Schemas
class PaymentInitiate(BaseModel):
    course_id: int
    payment_method: str  # paystack, flutterwave

class PaymentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    amount: float
    currency: str
    status: str
    transaction_id: str
    reference: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class PaymentWebhook(BaseModel):
    event: str
    data: dict

# Certificate Schemas
class CertificateResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    certificate_number: str
    issue_date: datetime
    pdf_url: str
    
    class Config:
        from_attributes = True

# Dashboard Schemas
class StudentDashboardStats(BaseModel):
    total_courses_enrolled: int
    completed_courses: int
    in_progress_courses: int
    total_certificates: int
    average_grade: float

class InstructorDashboardStats(BaseModel):
    total_courses: int
    total_students: int
    total_revenue: float
    avg_course_rating: float
    recent_enrollments: int

class AdminDashboardStats(BaseModel):
    total_users: int
    total_courses: int
    total_revenue: float
    pending_payments: int
    monthly_revenue: List[dict]
    top_courses: List[dict]

# Enrollment Schemas
class EnrollmentRequest(BaseModel):
    course_id: int

class EnrollmentResponse(BaseModel):
    user_id: int
    course_id: int
    enrolled_at: datetime
    progress: float
    
    class Config:
        from_attributes = True

# Notification Schemas
class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

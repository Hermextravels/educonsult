from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User, Course, Certificate, Payment, Quiz, Lesson, QuizAttempt, LessonProgress, PaymentStatusEnum
from app.schemas.schemas import CertificateResponse, StudentDashboardStats, InstructorDashboardStats, AdminDashboardStats
from app.services.quiz_service import CertificateService
from app.services.certificate_service import CertificateGenerator
from app.tasks.celery_app import send_certificate_email
from app.api.endpoints.auth import get_current_user_id
from datetime import datetime
import uuid
import os

router = APIRouter(prefix="/certificates", tags=["certificates"])

@router.get("/student/{course_id}", response_model=CertificateResponse)
def get_certificate(
    course_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get certificate for completed course"""
    certificate = db.query(Certificate).filter(
        Certificate.course_id == course_id,
        Certificate.user_id == current_user_id
    ).first()
    
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )
    
    return certificate

@router.post("/generate/{course_id}", response_model=CertificateResponse, status_code=status.HTTP_201_CREATED)
def generate_certificate(
    course_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Generate certificate after course completion"""
    user = db.query(User).filter(User.id == current_user_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not user or not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or course not found"
        )
    
    # Check if user is enrolled
    if course not in user.courses_enrolled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enrolled in this course"
        )
    
    # Check if already has certificate
    existing = db.query(Certificate).filter(
        Certificate.user_id == current_user_id,
        Certificate.course_id == course_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Certificate already generated"
        )
    
    # Check if course is completed
    if not CertificateService.check_completion(db, current_user_id, course_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Course not completed. All lessons and quizzes must be completed."
        )
    
    # Generate certificate
    certificate_number = f"CERT-{course_id}-{current_user_id}-{uuid.uuid4().hex[:8].upper()}"
    instructor = db.query(User).filter(User.id == course.instructor_id).first()
    
    pdf_content = CertificateGenerator.generate_certificate(
        student_name=user.full_name,
        course_name=course.title,
        certificate_number=certificate_number,
        instructor_name=instructor.full_name if instructor else "Course Instructor"
    )
    
    # Save PDF (in production, use cloud storage like S3)
    os.makedirs("certificates", exist_ok=True)
    pdf_filename = f"certificates/{certificate_number}.pdf"
    with open(pdf_filename, "wb") as f:
        f.write(pdf_content)
    
    # Create certificate record
    certificate = Certificate(
        user_id=current_user_id,
        course_id=course_id,
        certificate_number=certificate_number,
        pdf_url=f"/api/v1/certificates/download/{certificate_number}"
    )
    
    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    
    # Send email
    send_certificate_email.delay(
        user_email=user.email,
        certificate_number=certificate_number,
        course_name=course.title,
        pdf_content=pdf_content
    )
    
    return certificate

# Dashboard endpoints
@router.get("/dashboard/student")
def student_dashboard(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> StudentDashboardStats:
    """Get student dashboard statistics"""
    user = db.query(User).filter(User.id == current_user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    total_courses = len(user.courses_enrolled)
    total_certificates = db.query(Certificate).filter(Certificate.user_id == current_user_id).count()
    
    # Calculate completed vs in progress
    completed = 0
    in_progress = 0
    
    for course in user.courses_enrolled:
        if CertificateService.check_completion(db, current_user_id, course.id):
            completed += 1
        else:
            in_progress += 1
    
    # Calculate average grade
    attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == current_user_id).all()
    avg_grade = sum([a.score for a in attempts if a.score]) / len(attempts) if attempts else 0
    
    return StudentDashboardStats(
        total_courses_enrolled=total_courses,
        completed_courses=completed,
        in_progress_courses=in_progress,
        total_certificates=total_certificates,
        average_grade=round(avg_grade, 2)
    )

@router.get("/dashboard/instructor")
def instructor_dashboard(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> InstructorDashboardStats:
    """Get instructor dashboard statistics"""
    user = db.query(User).filter(User.id == current_user_id).first()
    
    if not user or user.role.value != "instructor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors can view this"
        )
    
    courses = db.query(Course).filter(Course.instructor_id == current_user_id).all()
    total_courses = len(courses)
    
    total_students = 0
    total_revenue = 0.0
    
    for course in courses:
        total_students += len(course.students)
        payments = db.query(Payment).filter(
            Payment.course_id == course.id,
            Payment.status == PaymentStatusEnum.COMPLETED
        ).all()
        total_revenue += sum([p.amount for p in payments])
    
    return InstructorDashboardStats(
        total_courses=total_courses,
        total_students=total_students,
        total_revenue=round(total_revenue, 2),
        avg_course_rating=0.0,  # Placeholder
        recent_enrollments=10  # Placeholder
    )

@router.get("/dashboard/admin")
def admin_dashboard(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> AdminDashboardStats:
    """Get admin dashboard statistics"""
    user = db.query(User).filter(User.id == current_user_id).first()
    
    if not user or user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view this"
        )
    
    total_users = db.query(User).count()
    total_courses = db.query(Course).count()
    
    completed_payments = db.query(Payment).filter(
        Payment.status == PaymentStatusEnum.COMPLETED
    ).all()
    total_revenue = sum([p.amount for p in completed_payments])
    
    pending_payments = db.query(Payment).filter(
        Payment.status == PaymentStatusEnum.PENDING
    ).count()
    
    return AdminDashboardStats(
        total_users=total_users,
        total_courses=total_courses,
        total_revenue=round(total_revenue, 2),
        pending_payments=pending_payments,
        monthly_revenue=[],  # Placeholder
        top_courses=[]  # Placeholder
    )

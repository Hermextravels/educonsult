from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.models import Course, Lesson, Quiz, Question, User
from app.schemas.schemas import CourseCreate, CourseResponse, CourseUpdate, LessonCreate, LessonResponse, LessonUpdate
from typing import List, Optional
from app.api.endpoints.auth import get_current_user_id, get_current_user_id_optional
import json

router = APIRouter(prefix="/courses", tags=["courses"])

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course_data: CourseCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a new course (admin and instructors)"""
    user = db.query(User).filter(User.id == current_user_id).first()
    
    if not user or user.role.value not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors and admins can create courses"
        )
    
    # Check if slug already exists
    existing = db.query(Course).filter(Course.slug == course_data.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course slug already exists"
        )
    
    # Convert lists to JSON strings for storage
    course_dict = course_data.dict()
    if course_dict.get('learning_objectives'):
        course_dict['learning_objectives'] = json.dumps(course_dict['learning_objectives'])
    if course_dict.get('requirements'):
        course_dict['requirements'] = json.dumps(course_dict['requirements'])
    
    db_course = Course(
        **course_dict,
        instructor_id=current_user_id
    )
    
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    
    return db_course

@router.get("/", response_model=List[CourseResponse])
def list_courses(
    skip: int = 0,
    limit: int = 20,
    category: str = None,
    level: str = None,
    current_user_id: Optional[int] = Depends(get_current_user_id_optional),
    db: Session = Depends(get_db)
):
    """List courses - all courses for admins/instructors, only published for others"""
    # Try to get the current user if authenticated
    user = None
    if current_user_id:
        user = db.query(User).filter(User.id == current_user_id).first()
    
    # Show all courses to admins and instructors, only published to others
    query = db.query(Course)
    if not user or user.role.value not in ["admin", "instructor"]:
        query = query.filter(Course.is_published == True)
    
    if category:
        query = query.filter(Course.category == category)
    if level:
        query = query.filter(Course.level == level)
    
    courses = query.offset(skip).limit(limit).all()
    
    # Add students count
    for course in courses:
        course.students_count = len(course.students)
    
    return courses

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Get course details"""
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    course.students_count = len(course.students)
    return course

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course_update: CourseUpdate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update course (instructor only)"""
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if course.instructor_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own courses"
        )
    
    update_data = course_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)
    
    db.commit()
    db.refresh(course)
    
    return course

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Delete course (instructor only)"""
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if course.instructor_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own courses"
        )
    
    db.delete(course)
    db.commit()

# Lesson endpoints
@router.post("/{course_id}/lessons", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
def create_lesson(
    course_id: int,
    lesson_data: LessonCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a lesson in a course"""
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if course.instructor_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only add lessons to your own courses"
        )
    
    db_lesson = Lesson(
        **lesson_data.dict(),
        course_id=course_id
    )
    
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    
    return db_lesson

@router.get("/{course_id}/lessons", response_model=List[LessonResponse])
def list_lessons(course_id: int, db: Session = Depends(get_db)):
    """List lessons in a course"""
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    lessons = db.query(Lesson).filter(Lesson.course_id == course_id).order_by(Lesson.order).all()
    return lessons

@router.put("/{course_id}/lessons/{lesson_id}", response_model=LessonResponse)
def update_lesson(
    course_id: int,
    lesson_id: int,
    lesson_update: LessonUpdate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update a lesson"""
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course or course.instructor_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update lessons in your own courses"
        )
    
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id, Lesson.course_id == course_id).first()
    
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    update_data = lesson_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lesson, field, value)
    
    db.commit()
    db.refresh(lesson)
    
    return lesson

# Enrollment endpoint
@router.post("/{course_id}/enroll", status_code=status.HTTP_200_OK)
def enroll_in_course(
    course_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Enroll in a course (free courses only - paid courses require payment)"""
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if not course.is_published:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course is not published yet"
        )
    
    user = db.query(User).filter(User.id == current_user_id).first()
    
    # Check if already enrolled
    if course in user.courses_enrolled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already enrolled in this course"
        )
    
    # Check if course is free
    if not course.is_free and course.price > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This course requires payment. Please use the payment endpoint."
        )
    
    # Enroll the user
    user.courses_enrolled.append(course)
    db.commit()
    
    return {
        "message": "Successfully enrolled in course",
        "course_id": course_id,
        "course_title": course.title
    }

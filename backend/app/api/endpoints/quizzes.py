from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Quiz, Question, QuizAttempt, Course, User
from app.schemas.schemas import QuizCreate, QuizResponse, QuizUpdate, QuizSubmissionRequest, QuizAttemptResponse
from app.services.quiz_service import QuizService
from typing import List
from app.api.endpoints.auth import get_current_user_id

router = APIRouter(prefix="/quizzes", tags=["quizzes"])

@router.post("/{course_id}/quizzes", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
def create_quiz(
    course_id: int,
    quiz_data: QuizCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a quiz for a course"""
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if course.instructor_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create quizzes for your own courses"
        )
    
    db_quiz = Quiz(
        **quiz_data.dict(exclude={"questions"}),
        course_id=course_id
    )
    
    if quiz_data.questions:
        for q_data in quiz_data.questions:
            question = Question(
                **q_data.dict(exclude={"answers"}),
                quiz_id=None  # Will be set after quiz is created
            )
            db_quiz.questions.append(question)
    
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    
    return db_quiz

@router.get("/{course_id}/quizzes", response_model=List[QuizResponse])
def list_quizzes(course_id: int, db: Session = Depends(get_db)):
    """List quizzes for a course"""
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    quizzes = db.query(Quiz).filter(Quiz.course_id == course_id).all()
    return quizzes

@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """Get quiz details"""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    return quiz

@router.post("/{quiz_id}/submit", response_model=QuizAttemptResponse)
def submit_quiz(
    quiz_id: int,
    submission: QuizSubmissionRequest,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Submit quiz answers"""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    attempt, score, passed = QuizService.submit_quiz(
        db=db,
        quiz_id=quiz_id,
        user_id=current_user_id,
        responses=submission.responses
    )
    
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to process quiz submission"
        )
    
    return attempt

@router.get("/{quiz_id}/attempts/{attempt_id}", response_model=QuizAttemptResponse)
def get_quiz_attempt(
    quiz_id: int,
    attempt_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get quiz attempt details"""
    attempt = db.query(QuizAttempt).filter(
        QuizAttempt.id == attempt_id,
        QuizAttempt.quiz_id == quiz_id,
        QuizAttempt.user_id == current_user_id
    ).first()
    
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz attempt not found"
        )
    
    return attempt

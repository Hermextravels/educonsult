from sqlalchemy.orm import Session
from app.models.models import User, Course, Lesson, Quiz, Question, Answer, LessonProgress, QuizAttempt, QuestionResponse
from app.schemas.schemas import QuestionResponseSubmit
from typing import List, Optional

class QuizService:
    @staticmethod
    def submit_quiz(db: Session, quiz_id: int, user_id: int, responses: List[QuestionResponseSubmit]) -> tuple:
        """
        Process quiz submission and return score and pass status
        """
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            return None, None, None
        
        # Create quiz attempt
        attempt = QuizAttempt(quiz_id=quiz_id, user_id=user_id)
        
        total_questions = len(quiz.questions)
        correct_answers = 0
        total_points = 0
        max_points = total_questions * 1.0
        
        for response in responses:
            question = db.query(Question).filter(Question.id == response.question_id).first()
            if not question:
                continue
            
            is_correct = False
            if question.question_type == "multiple_choice":
                is_correct = response.student_answer == question.correct_answer
            elif question.question_type == "true_false":
                is_correct = response.student_answer.lower() == question.correct_answer.lower()
            # Short answer and essay require manual grading
            
            if is_correct:
                correct_answers += 1
                total_points += 1.0
            
            q_response = QuestionResponse(
                attempt_id=attempt.id,
                question_id=question.id,
                student_answer=response.student_answer,
                is_correct=is_correct,
                points_earned=1.0 if is_correct else 0.0
            )
            db.add(q_response)
        
        score = (total_points / max_points * 100) if max_points > 0 else 0
        passed = score >= quiz.passing_score
        
        attempt.score = score
        attempt.passed = passed
        
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        
        return attempt, score, passed

class EnrollmentService:
    @staticmethod
    def enroll_student(db: Session, user_id: int, course_id: int) -> bool:
        """Enroll a student in a course"""
        user = db.query(User).filter(User.id == user_id).first()
        course = db.query(Course).filter(Course.id == course_id).first()
        
        if not user or not course:
            return False
        
        # Check if already enrolled
        if course in user.courses_enrolled:
            return False
        
        user.courses_enrolled.append(course)
        db.commit()
        return True

class ProgressService:
    @staticmethod
    def update_lesson_progress(db: Session, user_id: int, lesson_id: int, completed: bool = False, progress: float = 0.0) -> bool:
        """Update lesson progress for a student"""
        lesson_progress = db.query(LessonProgress).filter(
            LessonProgress.user_id == user_id,
            LessonProgress.lesson_id == lesson_id
        ).first()
        
        if not lesson_progress:
            lesson_progress = LessonProgress(
                user_id=user_id,
                lesson_id=lesson_id,
                completed=completed,
                progress_percent=progress
            )
            db.add(lesson_progress)
        else:
            lesson_progress.completed = completed
            lesson_progress.progress_percent = progress
        
        db.commit()
        return True
    
    @staticmethod
    def get_course_progress(db: Session, user_id: int, course_id: int) -> float:
        """Calculate overall course progress"""
        lessons = db.query(Lesson).filter(Lesson.course_id == course_id).all()
        if not lessons:
            return 0.0
        
        total_progress = 0.0
        for lesson in lessons:
            progress = db.query(LessonProgress).filter(
                LessonProgress.user_id == user_id,
                LessonProgress.lesson_id == lesson.id
            ).first()
            
            if progress:
                total_progress += progress.progress_percent
        
        return (total_progress / len(lessons)) if lessons else 0.0

class CertificateService:
    @staticmethod
    def check_completion(db: Session, user_id: int, course_id: int) -> bool:
        """Check if student has completed all course requirements"""
        # Check if all lessons completed
        lessons = db.query(Lesson).filter(Lesson.course_id == course_id).all()
        
        for lesson in lessons:
            progress = db.query(LessonProgress).filter(
                LessonProgress.user_id == user_id,
                LessonProgress.lesson_id == lesson.id,
                LessonProgress.completed == True
            ).first()
            
            if not progress:
                return False
        
        # Check if all quizzes passed
        quizzes = db.query(Quiz).filter(Quiz.course_id == course_id).all()
        
        for quiz in quizzes:
            attempt = db.query(QuizAttempt).filter(
                QuizAttempt.quiz_id == quiz.id,
                QuizAttempt.user_id == user_id,
                QuizAttempt.passed == True
            ).first()
            
            if not attempt:
                return False
        
        return True

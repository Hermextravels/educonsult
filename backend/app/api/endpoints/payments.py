from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Payment, Course, User, PaymentStatusEnum, Certificate
from app.schemas.schemas import PaymentInitiate, PaymentResponse, PaymentWebhook
from app.services.payment_service import PaymentService
from app.services.quiz_service import EnrollmentService, CertificateService
from app.services.certificate_service import CertificateGenerator
from app.tasks.celery_app import send_certificate_email, send_enrollment_notification
from app.api.endpoints.auth import get_current_user_id
from datetime import datetime
import uuid

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/initiate", response_model=dict, status_code=status.HTTP_201_CREATED)
def initiate_payment(
    payment_data: PaymentInitiate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Initiate payment for course enrollment"""
    course = db.query(Course).filter(Course.id == payment_data.course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    user = db.query(User).filter(User.id == current_user_id).first()
    
    # Check if already enrolled
    if course in user.courses_enrolled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already enrolled in this course"
        )
    
    # Create payment record
    reference = PaymentService.create_payment_reference()
    transaction_id = str(uuid.uuid4())
    
    payment = Payment(
        user_id=current_user_id,
        course_id=payment_data.course_id,
        amount=course.price,
        currency=course.currency,
        payment_method=payment_data.payment_method,
        transaction_id=transaction_id,
        reference=reference,
        status=PaymentStatusEnum.PENDING
    )
    
    db.add(payment)
    db.commit()
    db.refresh(payment)
    
    return {
        "reference": reference,
        "transaction_id": transaction_id,
        "amount": payment.amount,
        "currency": payment.currency,
        "payment_method": payment.payment_method
    }

@router.post("/webhook/paystack")
def paystack_webhook(payload: PaymentWebhook, db: Session = Depends(get_db)):
    """Handle Paystack webhook"""
    if payload.event == "charge.success":
        data = payload.data
        reference = data.get("reference")
        
        payment = db.query(Payment).filter(Payment.reference == reference).first()
        
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
        
        # Verify with Paystack
        verified_data = PaymentService.verify_paystack_payment(reference)
        
        if verified_data and verified_data.get("data", {}).get("status") == "success":
            payment.status = PaymentStatusEnum.COMPLETED
            payment.updated_at = datetime.utcnow()
            
            # Enroll user in course
            EnrollmentService.enroll_student(db, payment.user_id, payment.course_id)
            
            # Send confirmation email
            user = db.query(User).filter(User.id == payment.user_id).first()
            course = db.query(Course).filter(Course.id == payment.course_id).first()
            
            send_enrollment_notification.delay(
                user_email=user.email,
                course_name=course.title,
                access_url=f"http://localhost:3000/courses/{course.id}"
            )
            
            db.commit()
            
            return {"status": "success"}
    
    return {"status": "processed"}

@router.post("/webhook/flutterwave")
def flutterwave_webhook(payload: PaymentWebhook, db: Session = Depends(get_db)):
    """Handle Flutterwave webhook"""
    if payload.event == "charge.completed":
        data = payload.data
        transaction_id = data.get("id")
        
        payment = db.query(Payment).filter(Payment.transaction_id == str(transaction_id)).first()
        
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
        
        # Verify with Flutterwave
        verified_data = PaymentService.verify_flutterwave_payment(transaction_id)
        
        if verified_data and verified_data.get("data", {}).get("status") == "successful":
            payment.status = PaymentStatusEnum.COMPLETED
            payment.updated_at = datetime.utcnow()
            
            # Enroll user in course
            EnrollmentService.enroll_student(db, payment.user_id, payment.course_id)
            
            # Send confirmation email
            user = db.query(User).filter(User.id == payment.user_id).first()
            course = db.query(Course).filter(Course.id == payment.course_id).first()
            
            send_enrollment_notification.delay(
                user_email=user.email,
                course_name=course.title,
                access_url=f"http://localhost:3000/courses/{course.id}"
            )
            
            db.commit()
            
            return {"status": "success"}
    
    return {"status": "processed"}

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get payment details"""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    
    if not payment or payment.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    return payment

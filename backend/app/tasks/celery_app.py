from celery import Celery, Task
from app.core.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

celery_app = Celery(
    "edulearn",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

class CallbackTask(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 3}
    retry_backoff = True

celery_app.Task = CallbackTask

@celery_app.task
def send_email(subject: str, email_to: str, body: str, html: str = None):
    """Send email using SMTP"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_FROM
        msg['To'] = email_to
        
        if html:
            msg.attach(MIMEText(body, 'plain'))
            msg.attach(MIMEText(html, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        return {"status": "success", "message": f"Email sent to {email_to}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@celery_app.task
def send_certificate_email(user_email: str, certificate_number: str, course_name: str, pdf_content: bytes):
    """Send certificate email to student"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Your {course_name} Certificate"
        msg['From'] = settings.EMAIL_FROM
        msg['To'] = user_email
        
        body = f"""
        Congratulations! You have completed {course_name}.
        
        Your certificate has been generated and is attached to this email.
        Certificate Number: {certificate_number}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDF
        from email.mime.base import MIMEBase
        from email import encoders
        
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(pdf_content)
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename= certificate_{certificate_number}.pdf')
        msg.attach(attachment)
        
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        return {"status": "success", "message": f"Certificate email sent to {user_email}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@celery_app.task
def send_enrollment_notification(user_email: str, course_name: str, access_url: str):
    """Send enrollment confirmation email"""
    html = f"""
    <html>
        <body>
            <h2>Enrollment Confirmation</h2>
            <p>You have been successfully enrolled in <strong>{course_name}</strong>.</p>
            <p>You can now access the course at: <a href="{access_url}">Start Learning</a></p>
            <p>Best regards,<br/>EduLearn Team</p>
        </body>
    </html>
    """
    
    return send_email.delay(
        subject=f"Welcome to {course_name}",
        email_to=user_email,
        body=f"You have been enrolled in {course_name}. Visit {access_url} to start learning.",
        html=html
    )

@celery_app.task
def send_quiz_result_notification(user_email: str, quiz_name: str, score: float, passed: bool):
    """Send quiz result notification"""
    status = "PASSED" if passed else "FAILED"
    html = f"""
    <html>
        <body>
            <h2>Quiz Result</h2>
            <p>Quiz: <strong>{quiz_name}</strong></p>
            <p>Status: <strong style="color: {'green' if passed else 'red'}">{status}</strong></p>
            <p>Score: {score:.2f}%</p>
            <p>Best regards,<br/>EduLearn Team</p>
        </body>
    </html>
    """
    
    return send_email.delay(
        subject=f"Quiz Result: {quiz_name}",
        email_to=user_email,
        body=f"You scored {score:.2f}% on {quiz_name}",
        html=html
    )

@celery_app.task
def generate_monthly_report(month: int, year: int):
    """Generate monthly revenue and enrollment report"""
    # This would typically connect to database and generate reports
    # For now, it's a placeholder
    return {"status": "success", "message": f"Report generated for {month}/{year}"}

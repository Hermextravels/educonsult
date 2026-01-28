import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Course, User
from app.api.endpoints.auth import get_current_user_id
from datetime import datetime
import uuid

router = APIRouter(prefix="/uploads", tags=["uploads"])

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
VIDEOS_DIR = os.path.join(UPLOAD_DIR, "videos")
THUMBNAILS_DIR = os.path.join(UPLOAD_DIR, "thumbnails")
MATERIALS_DIR = os.path.join(UPLOAD_DIR, "materials")

for directory in [VIDEOS_DIR, THUMBNAILS_DIR, MATERIALS_DIR]:
    os.makedirs(directory, exist_ok=True)

# File size limits (in bytes)
MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500 MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024    # 5 MB
MAX_MATERIAL_SIZE = 50 * 1024 * 1024  # 50 MB

# Allowed file types
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/quicktime", "video/x-msvideo", "video/x-matroska"}
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_MATERIAL_TYPES = {"application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "text/plain"}


def validate_file(file: UploadFile, max_size: int, allowed_types: set) -> None:
    """Validate file size and type"""
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {allowed_types}"
        )
    
    # Check file size by reading content
    content = file.file.read()
    file.file.seek(0)  # Reset file pointer
    
    if len(content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum limit of {max_size / (1024*1024):.0f}MB"
        )


@router.post("/video/{course_id}")
async def upload_video(
    course_id: int,
    file: UploadFile = File(...),
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Upload a video for a course"""
    # Validate course exists and user has permission
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if user is the instructor or an admin
    user = db.query(User).filter(User.id == current_user_id).first()
    if course.instructor_id != current_user_id and (not user or user.role.value != "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the course instructor or admin can upload videos"
        )
    
    # Validate file
    validate_file(file, MAX_VIDEO_SIZE, ALLOWED_VIDEO_TYPES)
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(VIDEOS_DIR, unique_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save video file"
        )
    
    return {
        "filename": unique_filename,
        "url": f"/uploads/videos/{unique_filename}",
        "original_name": file.filename,
        "size": os.path.getsize(file_path)
    }


@router.post("/thumbnail/{course_id}")
async def upload_thumbnail(
    course_id: int,
    file: UploadFile = File(...),
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Upload a thumbnail for a course"""
    # Validate course exists and user has permission
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if user is the instructor or an admin
    user = db.query(User).filter(User.id == current_user_id).first()
    if course.instructor_id != current_user_id and (not user or user.role.value != "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the course instructor or admin can upload thumbnails"
        )
    
    # Validate file
    validate_file(file, MAX_IMAGE_SIZE, ALLOWED_IMAGE_TYPES)
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(THUMBNAILS_DIR, unique_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save thumbnail file"
        )
    
    # Update course thumbnail URL
    course.thumbnail_url = f"/uploads/thumbnails/{unique_filename}"
    db.commit()
    
    return {
        "filename": unique_filename,
        "url": f"/uploads/thumbnails/{unique_filename}",
        "original_name": file.filename,
        "size": os.path.getsize(file_path)
    }


@router.post("/material/{course_id}")
async def upload_material(
    course_id: int,
    file: UploadFile = File(...),
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Upload course materials (PDFs, documents, etc.)"""
    # Validate course exists and user has permission
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if user is the instructor or an admin
    user = db.query(User).filter(User.id == current_user_id).first()
    if course.instructor_id != current_user_id and (not user or user.role.value != "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the course instructor or admin can upload materials"
        )
    
    # Validate file
    validate_file(file, MAX_MATERIAL_SIZE, ALLOWED_MATERIAL_TYPES)
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(MATERIALS_DIR, unique_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save material file"
        )
    
    return {
        "filename": unique_filename,
        "url": f"/uploads/materials/{unique_filename}",
        "original_name": file.filename,
        "size": os.path.getsize(file_path)
    }

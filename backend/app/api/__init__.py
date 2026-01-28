from fastapi import APIRouter
from app.api.endpoints import auth, courses, quizzes, payments, dashboards, uploads

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(courses.router)
api_router.include_router(quizzes.router)
api_router.include_router(payments.router)
api_router.include_router(dashboards.router)
api_router.include_router(uploads.router)

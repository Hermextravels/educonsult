from app.core.database import SessionLocal, engine
from app.core.security import get_password_hash
from app.models.models import User, RoleEnum, Base

DEFAULT_EMAIL = "admin@educonsult.com"
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "Admin@12345"
DEFAULT_FULL_NAME = "Admin User"


def seed_admin() -> None:
    # Create all tables first
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        existing = (
            db.query(User)
            .filter((User.email == DEFAULT_EMAIL) | (User.username == DEFAULT_USERNAME))
            .first()
        )
        if existing:
            print("Admin user already exists. No changes made.")
            return

        admin_user = User(
            email=DEFAULT_EMAIL,
            username=DEFAULT_USERNAME,
            full_name=DEFAULT_FULL_NAME,
            hashed_password=get_password_hash(DEFAULT_PASSWORD),
            role=RoleEnum.ADMIN,
            is_active=True,
            is_verified=True,
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created:")
        print(f"  email: {DEFAULT_EMAIL}")
        print(f"  username: {DEFAULT_USERNAME}")
        print(f"  password: {DEFAULT_PASSWORD}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()

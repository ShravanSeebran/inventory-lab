from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.models.user import User


class UserRepository:
    """Generic user repository using SQLAlchemy ORM"""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user(self, user_data: dict) -> User:
        """Create a new user"""
        try:
            db_user = User(**user_data)
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError(f"User creation failed: {str(e)}")

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get a list of users with pagination"""
        return self.db.query(User).offset(skip).limit(limit).all()

    def update_user(self, user_id: int, user_data: dict) -> Optional[User]:
        """Update user"""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return None

        for key, value in user_data.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)

        try:
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError(f"User update failed: {str(e)}")

    def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return False

        self.db.delete(db_user)
        self.db.commit()
        return True

    def get_active_users(self) -> List[User]:
        """Get only active users"""
        return self.db.query(User).filter(User.is_active).all()

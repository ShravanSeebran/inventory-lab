from sqlalchemy.orm import Session

from app.db.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self):
        """Create a new user"""
        pass

    def authenticate_user(self):
        """Authenticate user credentials"""
        pass

    def update_user(self, user_id: int, user_data: UserUpdate):
        """Update user information"""
        upate_dict = user_data.model_dump(exclude_unset=True)
        db_user = self.repo.update_user(user_id, upate_dict)
        if db_user:
            return UserResponse.model_validate(db_user)
        return None

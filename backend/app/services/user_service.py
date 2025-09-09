from passlib.context import CryptContext
from app.db.repositories.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self):
        """Create a new user"""
        pass

    def authenticate_user(self, username: str, password: str):
        """Authenticate user credentials"""
        user = self.repo.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def update_user(self):
        """Update user information"""
        pass

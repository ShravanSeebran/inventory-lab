from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.db.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password for storing"""
    return pwd_context.hash(password)

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user with validation and password hashing"""
        # Check if user already exists
        if self.repo.get_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        if self.repo.get_user_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Hash the password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user using repository
        try:
            db_user = self.repo.create_user(
                username=user_data.username,
                email=user_data.email,
                hashed_password=hashed_password,
                full_name=f"{user_data.first_name} {user_data.last_name}",
                is_active=user_data.is_active,
                is_admin=getattr(user_data, 'is_admin', False)  # Default to False if not provided
            )
            return UserResponse.model_validate(db_user)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User creation failed due to database constraints"
            )

    def authenticate_user(self, username: str, password: str):
        """Authenticate user credentials"""
        user = self.repo.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def update_user(self, user_id: int, user_data: UserUpdate):
        """Update user information"""
        # Prepare update data, excluding unset values
        update_dict = user_data.model_dump(exclude_unset=True)
        
        # If password is being updated, hash it
        if 'password' in update_dict:
            update_dict['hashed_password'] = get_password_hash(update_dict.pop('password'))
        
        # Update user using repository
        db_user = self.repo.update_user(user_id, update_dict)
        if db_user:
            return UserResponse.model_validate(db_user)
        return None

    def get_user_by_id(self, user_id: int):
        """Get user by ID"""
        return self.repo.get_user_by_id(user_id)

    def get_all_users(self):
        """Get all users"""
        return self.repo.get_all_users()

    def delete_user(self, user_id: int):
        """Delete a user"""
        return self.repo.delete_user(user_id)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.db.repositories.user_repository import UserRepository
from app.schemas.user import UserLogin, UserResponse, UserCreate
from app.services.user_service import UserService


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    return user_service


router = APIRouter(prefix="/users", tags=["users"])



@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate, 
    user_service: UserService = Depends(get_user_service)
):
    try:
        new_user = user_service.create_user(user_data)
        return new_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user account"
        )


@router.post("/login", response_model=UserResponse)
def login(user: UserLogin, user_service: UserService = Depends(get_user_service)):
    db_user = user_service.authenticate_user(user.username, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return db_user
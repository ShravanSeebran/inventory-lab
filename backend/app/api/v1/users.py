import os

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.db.repositories.user_repository import UserRepository
from app.schemas.user import UserLogin, UserResponse, UserCreate, UserUpdate
from app.services.user_service import UserService
from app.api.auth import SESSION_COOKIE, get_current_user, require_same_origin
from app.services.session_service import SESSION_SECONDS, SessionService


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


@router.post("/login", response_model=UserResponse, dependencies=[Depends(require_same_origin)])
def login(user: UserLogin, request: Request, response: Response, user_service: UserService = Depends(get_user_service), db: Session = Depends(get_db)):
    db_user = user_service.authenticate_user(user.username, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = SessionService(db).create(db_user.id, request.cookies.get(SESSION_COOKIE))
    response.set_cookie(
        SESSION_COOKIE, token, max_age=SESSION_SECONDS, httponly=True,
        secure=os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true",
        samesite="lax", path="/",
    )
    response.headers["Cache-Control"] = "no-store"
    return db_user


@router.get("/me", response_model=UserResponse)
def current_user(response: Response, user=Depends(get_current_user)):
    response.headers["Cache-Control"] = "no-store"
    return user


@router.patch("/me", response_model=UserResponse, dependencies=[Depends(require_same_origin)])
def update_profile(user_data: UserUpdate, response: Response, user=Depends(get_current_user), user_service: UserService = Depends(get_user_service)):
    updated = user_service.update_user(user.id, user_data)
    if updated is None:
        raise HTTPException(status_code=404, detail="User not found")
    response.headers["Cache-Control"] = "no-store"
    return updated


@router.post("/logout", status_code=204, dependencies=[Depends(require_same_origin)])
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    SessionService(db).revoke(request.cookies.get(SESSION_COOKIE))
    response.delete_cookie(SESSION_COOKIE, path="/", httponly=True, samesite="lax")
    response.headers["Cache-Control"] = "no-store"

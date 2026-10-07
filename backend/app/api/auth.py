from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.session_service import SessionService


SESSION_COOKIE = "inventory_session"


def require_same_origin(request: Request):
    origin = request.headers.get("origin")
    if (origin and origin != str(request.base_url).rstrip("/")) or request.headers.get("sec-fetch-site") == "cross-site":
        raise HTTPException(status_code=403, detail="Cross-origin request rejected")


def get_current_user(request: Request, db: Session = Depends(get_db)):
    user = SessionService(db).get_user(request.cookies.get(SESSION_COOKIE))
    if user is None:
        raise HTTPException(status_code=401, detail="Sign in to continue")
    return user

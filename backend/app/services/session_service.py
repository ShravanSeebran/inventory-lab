from datetime import datetime, timedelta, UTC
from hashlib import sha256
import secrets

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.models.session import UserSession
from app.db.models.user import User


SESSION_SECONDS = 8 * 60 * 60


def token_hash(token: str) -> str:
    return sha256(token.encode()).hexdigest()


class SessionService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, previous_token: str | None = None) -> str:
        now = datetime.now(UTC).replace(tzinfo=None)
        self.db.execute(delete(UserSession).where(UserSession.expires_at <= now))
        if previous_token:
            self.db.execute(delete(UserSession).where(UserSession.token_hash == token_hash(previous_token)))
        token = secrets.token_urlsafe(32)
        self.db.add(UserSession(token_hash=token_hash(token), user_id=user_id, expires_at=now + timedelta(seconds=SESSION_SECONDS)))
        self.db.commit()
        return token

    def get_user(self, token: str | None) -> User | None:
        if not token:
            return None
        return self.db.scalar(
            select(User).join(UserSession, UserSession.user_id == User.id).where(
                UserSession.token_hash == token_hash(token),
                UserSession.expires_at > datetime.now(UTC).replace(tzinfo=None),
                User.is_active.is_(True),
            )
        )

    def revoke(self, token: str | None):
        if token:
            self.db.execute(delete(UserSession).where(UserSession.token_hash == token_hash(token)))
            self.db.commit()

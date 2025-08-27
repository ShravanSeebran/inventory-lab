from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common fields"""

    email: EmailStr
    username: str
    first_name: str
    last_name: str
    is_active: bool = True


class UserInDB(UserBase):
    """Schema representing user in database"""

    id: int
    hashed_password: str
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models


class UserResponse(UserBase):
    """Schema for user responses (public data only)"""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

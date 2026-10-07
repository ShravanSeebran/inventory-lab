from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints, field_validator
from typing import Annotated, Optional
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

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str = Field(min_length=1, max_length=72)

    @field_validator("password")
    @classmethod
    def validate_password_bytes(cls, value):
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 UTF-8 bytes")
        return value


Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
Username = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=50)]


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: Username
    email: EmailStr
    first_name: Name
    last_name: Name
    password: str = Field(min_length=8, max_length=72)

    @field_validator("password")
    @classmethod
    def validate_password_bytes(cls, value):
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 UTF-8 bytes")
        return value


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None

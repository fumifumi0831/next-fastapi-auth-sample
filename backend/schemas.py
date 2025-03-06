from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional

from security import SecurityManager

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

    @validator('password')
    def validate_password(cls, password):
        """
        パスワードの複雑性チェック
        """
        if not SecurityManager.validate_password(password):
            raise ValueError(
                "パスワードは最低8文字で、大文字、小文字、数字、特殊文字を含む必要があります"
            )
        return password

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    sub: Optional[int] = None
    email: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

    @validator('new_password')
    def validate_password(cls, password):
        """
        パスワードの複雑性チェック
        """
        if not SecurityManager.validate_password(password):
            raise ValueError(
                "パスワードは最低8文字で、大文字、小文字、数字、特殊文字を含む必要があります"
            )
        return password

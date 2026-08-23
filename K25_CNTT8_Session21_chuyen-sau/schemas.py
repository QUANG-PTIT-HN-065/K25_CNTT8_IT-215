import re

from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Mật khẩu phải có ít nhất một chữ hoa"
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Mật khẩu phải có ít nhất một chữ thường"
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "Mật khẩu phải có ít nhất một chữ số"
            )

        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    is_active: bool


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
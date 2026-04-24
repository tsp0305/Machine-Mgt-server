from pydantic import EmailStr,field_validator,BaseModel
from src.validator.base_validator import BaseValidator


class SignupValidator(BaseValidator, BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class LoginValidator(BaseValidator, BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseValidator, BaseModel):
    refresh_token: str


class LogoutRequest(BaseValidator, BaseModel):
    refresh_token: str
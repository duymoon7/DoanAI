"""
Authentication Schemas
=====================
Pydantic models cho authentication endpoints.
"""
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from .nguoi_dung import NguoiDungResponse
import re


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    mat_khau: str


class RegisterRequest(BaseModel):
    """Register request schema"""
    email: EmailStr
    mat_khau: str
    ho_ten: str
    so_dien_thoai: Optional[str] = None
    
    @field_validator('mat_khau')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """
        Validate password strength:
        - At least 8 characters
        - Contains at least one uppercase letter
        - Contains at least one number
        """
        if len(v) < 8:
            raise ValueError('Mật khẩu phải có ít nhất 8 ký tự')
        
        if not re.search(r'[A-Z]', v):
            raise ValueError('Mật khẩu phải có ít nhất 1 chữ hoa')
        
        if not re.search(r'\d', v):
            raise ValueError('Mật khẩu phải có ít nhất 1 số')
        
        return v


class Token(BaseModel):
    """JWT Token response"""
    access_token: str
    token_type: str
    user: NguoiDungResponse


class TokenData(BaseModel):
    """Token payload data"""
    email: Optional[str] = None
    user_id: Optional[int] = None


class ResetPasswordRequest(BaseModel):
    """Reset password request schema"""
    email: EmailStr
    new_password: str
    
    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """
        Validate password strength:
        - At least 8 characters
        - Contains at least one uppercase letter
        - Contains at least one number
        """
        if len(v) < 8:
            raise ValueError('Mật khẩu phải có ít nhất 8 ký tự')
        
        if not re.search(r'[A-Z]', v):
            raise ValueError('Mật khẩu phải có ít nhất 1 chữ hoa')
        
        if not re.search(r'\d', v):
            raise ValueError('Mật khẩu phải có ít nhất 1 số')
        
        return v

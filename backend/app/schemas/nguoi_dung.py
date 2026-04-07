from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class NguoiDungBase(BaseModel):
    email: EmailStr
    ho_ten: Optional[str] = None
    so_dien_thoai: Optional[str] = None
    vai_tro: Optional[str] = "user"

class NguoiDungCreate(NguoiDungBase):
    mat_khau: str

class NguoiDungUpdate(BaseModel):
    email: Optional[EmailStr] = None
    mat_khau: Optional[str] = None
    ho_ten: Optional[str] = None
    so_dien_thoai: Optional[str] = None
    vai_tro: Optional[str] = None

class NguoiDungResponse(NguoiDungBase):
    id: int
    ngay_tao: datetime
    
    class Config:
        from_attributes = True

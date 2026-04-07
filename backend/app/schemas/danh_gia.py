from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal

class DanhGiaBase(BaseModel):
    san_pham_id: int
    diem_so: float = Field(..., ge=1, le=5, description="Điểm đánh giá từ 1-5 sao")
    binh_luan: Optional[str] = None

class DanhGiaCreate(DanhGiaBase):
    pass

class DanhGiaUpdate(BaseModel):
    diem_so: Optional[float] = Field(None, ge=1, le=5)
    binh_luan: Optional[str] = None

class NguoiDungInReview(BaseModel):
    id: int
    ho_ten: str
    email: str
    
    class Config:
        from_attributes = True

class SanPhamInReview(BaseModel):
    id: int
    ten: str
    hinh_anh: Optional[str] = None
    
    class Config:
        from_attributes = True

class DanhGiaResponse(DanhGiaBase):
    id: int
    nguoi_dung_id: int
    ngay_tao: datetime
    nguoi_dung: Optional[NguoiDungInReview] = None
    san_pham: Optional[SanPhamInReview] = None
    
    class Config:
        from_attributes = True

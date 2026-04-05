from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class DonHangBase(BaseModel):
    nguoi_dung_id: int
    tong_tien: Decimal
    trang_thai: Optional[str] = "pending"

class DonHangCreate(DonHangBase):
    pass

class DonHangUpdate(BaseModel):
    tong_tien: Optional[Decimal] = None
    trang_thai: Optional[str] = None

class DonHangResponse(DonHangBase):
    id: int
    ngay_tao: datetime
    
    class Config:
        from_attributes = True

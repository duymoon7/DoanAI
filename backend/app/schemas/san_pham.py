from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class SanPhamBase(BaseModel):
    ten: str
    gia: Decimal
    mo_ta: Optional[str] = None
    hinh_anh: Optional[str] = None
    danh_muc_id: int

class SanPhamCreate(SanPhamBase):
    pass

class SanPhamUpdate(BaseModel):
    ten: Optional[str] = None
    gia: Optional[Decimal] = None
    mo_ta: Optional[str] = None
    hinh_anh: Optional[str] = None
    danh_muc_id: Optional[int] = None

class DanhMucInProduct(BaseModel):
    id: int
    ten: str
    
    class Config:
        from_attributes = True

class SanPhamResponse(SanPhamBase):
    id: int
    ngay_tao: datetime
    danh_muc: Optional[DanhMucInProduct] = None
    
    class Config:
        from_attributes = True

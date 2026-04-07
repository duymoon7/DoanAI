from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class ChiTietDonHangBase(BaseModel):
    don_hang_id: int
    san_pham_id: int
    so_luong: int

class ChiTietDonHangCreate(ChiTietDonHangBase):
    pass

# Nested schema for product info in order detail
class SanPhamInOrderDetail(BaseModel):
    id: int
    ten: str
    gia: Decimal
    hinh_anh: Optional[str] = None
    
    class Config:
        from_attributes = True

class ChiTietDonHangResponse(ChiTietDonHangBase):
    id: int
    san_pham: Optional[SanPhamInOrderDetail] = None
    
    class Config:
        from_attributes = True

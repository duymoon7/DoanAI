from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal

class MaGiamGiaBase(BaseModel):
    ma_code: str = Field(..., min_length=3, max_length=50)
    mo_ta: Optional[str] = None
    loai_giam: str = Field(..., pattern="^(percent|fixed)$")
    gia_tri_giam: Decimal = Field(..., gt=0)
    gia_tri_don_toi_thieu: Decimal = Field(default=0, ge=0)
    so_luong: int = Field(default=1, ge=1)
    ngay_bat_dau: Optional[datetime] = None
    ngay_ket_thuc: Optional[datetime] = None
    hoat_dong: bool = True

class MaGiamGiaCreate(MaGiamGiaBase):
    pass

class MaGiamGiaUpdate(BaseModel):
    ma_code: Optional[str] = Field(None, min_length=3, max_length=50)
    mo_ta: Optional[str] = None
    loai_giam: Optional[str] = Field(None, pattern="^(percent|fixed)$")
    gia_tri_giam: Optional[Decimal] = Field(None, gt=0)
    gia_tri_don_toi_thieu: Optional[Decimal] = Field(None, ge=0)
    so_luong: Optional[int] = Field(None, ge=0)
    ngay_bat_dau: Optional[datetime] = None
    ngay_ket_thuc: Optional[datetime] = None
    hoat_dong: Optional[bool] = None

class MaGiamGiaResponse(MaGiamGiaBase):
    id: int
    da_su_dung: int
    ngay_tao: datetime
    
    class Config:
        from_attributes = True

class MaGiamGiaValidate(BaseModel):
    """Response khi validate mã giảm giá"""
    valid: bool
    message: str
    discount_amount: Decimal = Decimal(0)
    coupon_id: Optional[int] = None
    ma_giam_gia: Optional[MaGiamGiaResponse] = None

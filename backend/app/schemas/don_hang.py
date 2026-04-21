from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

class DonHangBase(BaseModel):
    nguoi_dung_id: int
    tong_tien: Decimal
    trang_thai: Optional[str] = "pending"
    phuong_thuc_thanh_toan: Optional[str] = "cod"
    
    # Thông tin giao hàng
    ten_nguoi_nhan: Optional[str] = None
    so_dien_thoai_nguoi_nhan: Optional[str] = None
    dia_chi_giao_hang: Optional[str] = None
    ghi_chu: Optional[str] = None
    
    # Mã giảm giá
    ma_giam_gia_id: Optional[int] = None
    so_tien_giam: Optional[Decimal] = 0

class DonHangCreate(DonHangBase):
    pass

class DonHangUpdate(BaseModel):
    tong_tien: Optional[Decimal] = None
    trang_thai: Optional[str] = None
    phuong_thuc_thanh_toan: Optional[str] = None
    ten_nguoi_nhan: Optional[str] = None
    so_dien_thoai_nguoi_nhan: Optional[str] = None
    dia_chi_giao_hang: Optional[str] = None
    ghi_chu: Optional[str] = None
    ma_giam_gia_id: Optional[int] = None
    so_tien_giam: Optional[Decimal] = None

# Nested schema for user info in order response
class NguoiDungInOrder(BaseModel):
    id: int
    email: str
    ho_ten: str
    so_dien_thoai: Optional[str] = None
    
    class Config:
        from_attributes = True

# Nested schema for product in order detail
class SanPhamInOrderDetail(BaseModel):
    id: int
    ten: str
    gia: Decimal
    hinh_anh: Optional[str] = None
    
    class Config:
        from_attributes = True

# Nested schema for order detail
class ChiTietDonHangInOrder(BaseModel):
    id: int
    san_pham_id: int
    so_luong: int
    san_pham: Optional[SanPhamInOrderDetail] = None
    
    class Config:
        from_attributes = True

class DonHangResponse(DonHangBase):
    id: int
    ngay_tao: datetime
    ngay_cap_nhat: Optional[datetime] = None
    nguoi_dung: Optional[NguoiDungInOrder] = None
    chi_tiet_don_hang: Optional[List[ChiTietDonHangInOrder]] = []
    
    class Config:
        from_attributes = True

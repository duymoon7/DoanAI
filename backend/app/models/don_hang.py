from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .base import BaseModel


class TrangThai(str, enum.Enum):
    """Enum cho trang thai don hang"""
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PhuongThucThanhToan(str, enum.Enum):
    """Enum cho phuong thuc thanh toan"""
    COD = "cod"
    BANK = "bank"


class DonHang(BaseModel):
    """Model cho bang don_hang"""
    __tablename__ = "don_hang"
    
    nguoi_dung_id = Column(Integer, ForeignKey("nguoi_dung.id"), nullable=False)
    tong_tien = Column(Numeric(10, 2), nullable=False)
    trang_thai = Column(String(20), default="pending", nullable=False)
    phuong_thuc_thanh_toan = Column(String(20), default="cod", nullable=False)
    
    # Thông tin giao hàng
    ten_nguoi_nhan = Column(String(255), nullable=True)
    so_dien_thoai_nguoi_nhan = Column(String(20), nullable=True)
    dia_chi_giao_hang = Column(Text, nullable=True)
    ghi_chu = Column(Text, nullable=True)
    
    # Mã giảm giá
    ma_giam_gia_id = Column(Integer, ForeignKey("ma_giam_gia.id"), nullable=True)
    so_tien_giam = Column(Numeric(10, 2), default=0, nullable=False)
    
    ngay_tao = Column(DateTime, default=datetime.utcnow, nullable=False)
    ngay_cap_nhat = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    nguoi_dung = relationship("NguoiDung", back_populates="don_hang")
    chi_tiet_don_hang = relationship("ChiTietDonHang", back_populates="don_hang", cascade="all, delete-orphan")
    ma_giam_gia = relationship("MaGiamGia", back_populates="don_hang")
    
    def __repr__(self):
        return f"<DonHang(id={self.id}, nguoi_dung_id={self.nguoi_dung_id}, tong_tien={self.tong_tien}, trang_thai={self.trang_thai})>"

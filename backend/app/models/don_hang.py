from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .base import BaseModel


class TrangThai(str, enum.Enum):
    """Enum cho trang thai don hang"""
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class DonHang(BaseModel):
    """Model cho bang don_hang"""
    __tablename__ = "don_hang"
    
    nguoi_dung_id = Column(Integer, ForeignKey("nguoi_dung.id"), nullable=False)
    tong_tien = Column(Numeric(10, 2), nullable=False)
    trang_thai = Column(Enum(TrangThai), default=TrangThai.PENDING, nullable=False)
    ngay_tao = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    nguoi_dung = relationship("NguoiDung", back_populates="don_hang")
    chi_tiet_don_hang = relationship("ChiTietDonHang", back_populates="don_hang", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<DonHang(id={self.id}, nguoi_dung_id={self.nguoi_dung_id}, tong_tien={self.tong_tien}, trang_thai={self.trang_thai})>"

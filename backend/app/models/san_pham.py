from sqlalchemy import Column, String, Numeric, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import BaseModel


class SanPham(BaseModel):
    """Model cho bang san_pham"""
    __tablename__ = "san_pham"
    
    ten = Column(String(255), nullable=False)
    gia = Column(Numeric(10, 2), nullable=False)
    mo_ta = Column(Text, nullable=True)
    hinh_anh = Column(String(500), nullable=True)
    danh_muc_id = Column(Integer, ForeignKey("danh_muc.id"), nullable=False)
    ngay_tao = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    danh_muc = relationship("DanhMuc", back_populates="san_pham")
    chi_tiet_don_hang = relationship("ChiTietDonHang", back_populates="san_pham")
    
    def __repr__(self):
        return f"<SanPham(id={self.id}, ten={self.ten}, gia={self.gia})>"

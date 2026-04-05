from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class ChiTietDonHang(BaseModel):
    """Model cho bang chi_tiet_don_hang"""
    __tablename__ = "chi_tiet_don_hang"
    
    don_hang_id = Column(Integer, ForeignKey("don_hang.id"), nullable=False)
    san_pham_id = Column(Integer, ForeignKey("san_pham.id"), nullable=False)
    so_luong = Column(Integer, nullable=False)
    
    # Relationships
    don_hang = relationship("DonHang", back_populates="chi_tiet_don_hang")
    san_pham = relationship("SanPham", back_populates="chi_tiet_don_hang")
    
    def __repr__(self):
        return f"<ChiTietDonHang(id={self.id}, don_hang_id={self.don_hang_id}, san_pham_id={self.san_pham_id}, so_luong={self.so_luong})>"

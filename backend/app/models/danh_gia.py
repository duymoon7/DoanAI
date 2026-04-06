from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class DanhGia(Base):
    __tablename__ = "danh_gia"
    
    id = Column(Integer, primary_key=True, index=True)
    nguoi_dung_id = Column(Integer, ForeignKey("nguoi_dung.id"), nullable=False)
    san_pham_id = Column(Integer, ForeignKey("san_pham.id"), nullable=False)
    diem_so = Column(Float, nullable=False)  # 1-5 sao
    binh_luan = Column(Text, nullable=True)
    ngay_tao = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    nguoi_dung = relationship("NguoiDung", back_populates="danh_gia")
    san_pham = relationship("SanPham", back_populates="danh_gia")

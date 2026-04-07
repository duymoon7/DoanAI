from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from datetime import datetime

from .base import BaseModel


class MaGiamGia(BaseModel):
    """Model cho bang ma_giam_gia"""
    __tablename__ = "ma_giam_gia"
    
    ma_code = Column(String(50), unique=True, nullable=False, index=True)
    mo_ta = Column(String(255))
    loai_giam = Column(String(20), nullable=False, default="percent")  # percent hoặc fixed
    gia_tri_giam = Column(Numeric(10, 2), nullable=False)
    gia_tri_don_toi_thieu = Column(Numeric(10, 2), default=0)
    so_luong = Column(Integer, default=1)
    da_su_dung = Column(Integer, default=0)
    ngay_bat_dau = Column(DateTime, default=datetime.utcnow)
    ngay_ket_thuc = Column(DateTime)
    hoat_dong = Column(Boolean, default=True)
    ngay_tao = Column(DateTime, default=datetime.utcnow, nullable=False)
    ngay_cap_nhat = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<MaGiamGia(id={self.id}, ma_code={self.ma_code}, gia_tri_giam={self.gia_tri_giam})>"

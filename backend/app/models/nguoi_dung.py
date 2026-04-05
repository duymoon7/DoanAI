from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .base import BaseModel


class VaiTro(str, enum.Enum):
    """Enum cho vai tro nguoi dung"""
    ADMIN = "admin"
    USER = "user"


class NguoiDung(BaseModel):
    """Model cho bang nguoi_dung"""
    __tablename__ = "nguoi_dung"
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    mat_khau = Column(String(255), nullable=False)
    vai_tro = Column(Enum(VaiTro), default=VaiTro.USER, nullable=False)
    ngay_tao = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    don_hang = relationship("DonHang", back_populates="nguoi_dung", cascade="all, delete-orphan")
    lich_su_chat = relationship("LichSuChat", back_populates="nguoi_dung", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<NguoiDung(id={self.id}, email={self.email}, vai_tro={self.vai_tro})>"

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class DanhMuc(BaseModel):
    """Model cho bang danh_muc"""
    __tablename__ = "danh_muc"
    
    ten = Column(String(255), nullable=False, unique=True)
    
    # Relationships
    san_pham = relationship("SanPham", back_populates="danh_muc")
    
    def __repr__(self):
        return f"<DanhMuc(id={self.id}, ten={self.ten})>"

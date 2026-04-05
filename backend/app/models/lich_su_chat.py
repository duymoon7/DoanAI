from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import BaseModel


class LichSuChat(BaseModel):
    """Model cho bang lich_su_chat"""
    __tablename__ = "lich_su_chat"
    
    nguoi_dung_id = Column(Integer, ForeignKey("nguoi_dung.id"), nullable=False)
    cau_hoi = Column(Text, nullable=False)
    cau_tra_loi = Column(Text, nullable=False)
    ngay_tao = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    nguoi_dung = relationship("NguoiDung", back_populates="lich_su_chat")
    
    def __repr__(self):
        return f"<LichSuChat(id={self.id}, nguoi_dung_id={self.nguoi_dung_id}, ngay_tao={self.ngay_tao})>"

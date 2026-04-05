from pydantic import BaseModel
from datetime import datetime

class LichSuChatBase(BaseModel):
    nguoi_dung_id: int
    cau_hoi: str
    cau_tra_loi: str

class LichSuChatCreate(LichSuChatBase):
    pass

class LichSuChatResponse(LichSuChatBase):
    id: int
    ngay_tao: datetime
    
    class Config:
        from_attributes = True

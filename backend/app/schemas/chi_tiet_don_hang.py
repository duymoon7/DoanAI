from pydantic import BaseModel

class ChiTietDonHangBase(BaseModel):
    don_hang_id: int
    san_pham_id: int
    so_luong: int

class ChiTietDonHangCreate(ChiTietDonHangBase):
    pass

class ChiTietDonHangResponse(ChiTietDonHangBase):
    id: int
    
    class Config:
        from_attributes = True

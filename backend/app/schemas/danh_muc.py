from pydantic import BaseModel
from typing import Optional

class DanhMucBase(BaseModel):
    ten: str

class DanhMucCreate(DanhMucBase):
    pass

class DanhMucUpdate(BaseModel):
    ten: Optional[str] = None

class DanhMucResponse(DanhMucBase):
    id: int
    
    class Config:
        from_attributes = True

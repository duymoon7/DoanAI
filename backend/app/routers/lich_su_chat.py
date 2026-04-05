from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import LichSuChat, NguoiDung
from app.schemas import LichSuChatCreate, LichSuChatResponse

router = APIRouter(prefix="/api/lich-su-chat", tags=["Lịch sử chat"])

@router.get("/", response_model=List[LichSuChatResponse])
def get_all_chat_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lấy danh sách tất cả lịch sử chat"""
    chats = db.query(LichSuChat).offset(skip).limit(limit).all()
    return chats

@router.get("/{chat_id}", response_model=LichSuChatResponse)
def get_chat(chat_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin lịch sử chat theo ID"""
    chat = db.query(LichSuChat).filter(LichSuChat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Lịch sử chat không tồn tại")
    return chat

@router.post("/", response_model=LichSuChatResponse, status_code=201)
def create_chat(chat: LichSuChatCreate, db: Session = Depends(get_db)):
    """Tạo lịch sử chat mới"""
    # Verify user exists
    user = db.query(NguoiDung).filter(NguoiDung.id == chat.nguoi_dung_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại")
    
    db_chat = LichSuChat(**chat.model_dump())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

@router.delete("/{chat_id}")
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    """Xóa lịch sử chat"""
    db_chat = db.query(LichSuChat).filter(LichSuChat.id == chat_id).first()
    if not db_chat:
        raise HTTPException(status_code=404, detail="Lịch sử chat không tồn tại")
    
    db.delete(db_chat)
    db.commit()
    return {"message": "Đã xóa lịch sử chat thành công"}

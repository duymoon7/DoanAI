from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import NguoiDung
from app.schemas import NguoiDungCreate, NguoiDungUpdate, NguoiDungResponse

router = APIRouter(prefix="/api/nguoi-dung", tags=["Người dùng"])

@router.get("/", response_model=List[NguoiDungResponse])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lấy danh sách tất cả người dùng"""
    users = db.query(NguoiDung).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=NguoiDungResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin người dùng theo ID"""
    user = db.query(NguoiDung).filter(NguoiDung.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại")
    return user

@router.post("/", response_model=NguoiDungResponse, status_code=201)
def create_user(user: NguoiDungCreate, db: Session = Depends(get_db)):
    """Tạo người dùng mới"""
    # Check if email exists
    existing = db.query(NguoiDung).filter(NguoiDung.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")
    
    db_user = NguoiDung(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/{user_id}", response_model=NguoiDungResponse)
def update_user(user_id: int, user: NguoiDungUpdate, db: Session = Depends(get_db)):
    """Cập nhật thông tin người dùng"""
    db_user = db.query(NguoiDung).filter(NguoiDung.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại")
    
    update_data = user.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Xóa người dùng"""
    db_user = db.query(NguoiDung).filter(NguoiDung.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại")
    
    db.delete(db_user)
    db.commit()
    return {"message": "Đã xóa người dùng thành công"}

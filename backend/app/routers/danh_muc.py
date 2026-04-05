from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import DanhMuc
from app.schemas import DanhMucCreate, DanhMucUpdate, DanhMucResponse

router = APIRouter(prefix="/api/danh-muc", tags=["Danh mục"])

@router.get("/", response_model=List[DanhMucResponse])
def get_all_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lấy danh sách tất cả danh mục"""
    categories = db.query(DanhMuc).offset(skip).limit(limit).all()
    return categories

@router.get("/{category_id}", response_model=DanhMucResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin danh mục theo ID"""
    category = db.query(DanhMuc).filter(DanhMuc.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Danh mục không tồn tại")
    return category

@router.post("/", response_model=DanhMucResponse, status_code=201)
def create_category(category: DanhMucCreate, db: Session = Depends(get_db)):
    """Tạo danh mục mới"""
    # Check if name exists
    existing = db.query(DanhMuc).filter(DanhMuc.ten == category.ten).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tên danh mục đã tồn tại")
    
    db_category = DanhMuc(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.put("/{category_id}", response_model=DanhMucResponse)
def update_category(category_id: int, category: DanhMucUpdate, db: Session = Depends(get_db)):
    """Cập nhật thông tin danh mục"""
    db_category = db.query(DanhMuc).filter(DanhMuc.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Danh mục không tồn tại")
    
    update_data = category.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Xóa danh mục"""
    db_category = db.query(DanhMuc).filter(DanhMuc.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Danh mục không tồn tại")
    
    db.delete(db_category)
    db.commit()
    return {"message": "Đã xóa danh mục thành công"}

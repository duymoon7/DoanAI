from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import SanPham, DanhMuc
from app.schemas import SanPhamCreate, SanPhamUpdate, SanPhamResponse

router = APIRouter(prefix="/api/san-pham", tags=["Sản phẩm"])

@router.get("/", response_model=List[SanPhamResponse])
def get_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lấy danh sách tất cả sản phẩm"""
    products = db.query(SanPham).offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=SanPhamResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin sản phẩm theo ID"""
    product = db.query(SanPham).filter(SanPham.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
    return product

@router.post("/", response_model=SanPhamResponse, status_code=201)
def create_product(product: SanPhamCreate, db: Session = Depends(get_db)):
    """Tạo sản phẩm mới"""
    # Verify category exists
    category = db.query(DanhMuc).filter(DanhMuc.id == product.danh_muc_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Danh mục không tồn tại")
    
    db_product = SanPham(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{product_id}", response_model=SanPhamResponse)
def update_product(product_id: int, product: SanPhamUpdate, db: Session = Depends(get_db)):
    """Cập nhật thông tin sản phẩm"""
    db_product = db.query(SanPham).filter(SanPham.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
    
    update_data = product.model_dump(exclude_unset=True)
    
    # Verify category if being updated
    if "danh_muc_id" in update_data:
        category = db.query(DanhMuc).filter(DanhMuc.id == update_data["danh_muc_id"]).first()
        if not category:
            raise HTTPException(status_code=404, detail="Danh mục không tồn tại")
    
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Xóa sản phẩm"""
    db_product = db.query(SanPham).filter(SanPham.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Đã xóa sản phẩm thành công"}

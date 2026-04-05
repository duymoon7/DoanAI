from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import ChiTietDonHang, DonHang, SanPham
from app.schemas import ChiTietDonHangCreate, ChiTietDonHangResponse

router = APIRouter(prefix="/api/chi-tiet-don-hang", tags=["Chi tiết đơn hàng"])

@router.get("/", response_model=List[ChiTietDonHangResponse])
def get_all_order_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lấy danh sách tất cả chi tiết đơn hàng"""
    items = db.query(ChiTietDonHang).offset(skip).limit(limit).all()
    return items

@router.get("/{item_id}", response_model=ChiTietDonHangResponse)
def get_order_item(item_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin chi tiết đơn hàng theo ID"""
    item = db.query(ChiTietDonHang).filter(ChiTietDonHang.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Chi tiết đơn hàng không tồn tại")
    return item

@router.post("/", response_model=ChiTietDonHangResponse, status_code=201)
def create_order_item(item: ChiTietDonHangCreate, db: Session = Depends(get_db)):
    """Tạo chi tiết đơn hàng mới"""
    # Verify order exists
    order = db.query(DonHang).filter(DonHang.id == item.don_hang_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Đơn hàng không tồn tại")
    
    # Verify product exists
    product = db.query(SanPham).filter(SanPham.id == item.san_pham_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
    
    db_item = ChiTietDonHang(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def delete_order_item(item_id: int, db: Session = Depends(get_db)):
    """Xóa chi tiết đơn hàng"""
    db_item = db.query(ChiTietDonHang).filter(ChiTietDonHang.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Chi tiết đơn hàng không tồn tại")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Đã xóa chi tiết đơn hàng thành công"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import DonHang, NguoiDung
from app.schemas import DonHangCreate, DonHangUpdate, DonHangResponse

router = APIRouter(prefix="/api/don-hang", tags=["Đơn hàng"])

@router.get("/", response_model=List[DonHangResponse])
def get_all_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lấy danh sách tất cả đơn hàng"""
    orders = db.query(DonHang).offset(skip).limit(limit).all()
    return orders

@router.get("/{order_id}", response_model=DonHangResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin đơn hàng theo ID"""
    order = db.query(DonHang).filter(DonHang.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Đơn hàng không tồn tại")
    return order

@router.post("/", response_model=DonHangResponse, status_code=201)
def create_order(order: DonHangCreate, db: Session = Depends(get_db)):
    """Tạo đơn hàng mới"""
    # Verify user exists
    user = db.query(NguoiDung).filter(NguoiDung.id == order.nguoi_dung_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại")
    
    # Validate payment method
    valid_methods = ['cod', 'bank']
    if order.phuong_thuc_thanh_toan and order.phuong_thuc_thanh_toan not in valid_methods:
        raise HTTPException(status_code=400, detail="Phương thức thanh toán không hợp lệ")
    
    db_order = DonHang(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.put("/{order_id}", response_model=DonHangResponse)
def update_order(order_id: int, order: DonHangUpdate, db: Session = Depends(get_db)):
    """Cập nhật thông tin đơn hàng"""
    db_order = db.query(DonHang).filter(DonHang.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Đơn hàng không tồn tại")
    
    update_data = order.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_order, field, value)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Xóa đơn hàng"""
    db_order = db.query(DonHang).filter(DonHang.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Đơn hàng không tồn tại")
    
    db.delete(db_order)
    db.commit()
    return {"message": "Đã xóa đơn hàng thành công"}

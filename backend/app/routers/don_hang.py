from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app.models import DonHang, NguoiDung, ChiTietDonHang
from app.schemas import DonHangCreate, DonHangUpdate, DonHangResponse

router = APIRouter(prefix="/api/don-hang", tags=["Đơn hàng"])

@router.get("/", response_model=List[DonHangResponse])
def get_all_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lấy danh sách tất cả đơn hàng với thông tin người đặt và chi tiết đơn hàng"""
    orders = db.query(DonHang).options(
        joinedload(DonHang.nguoi_dung),
        joinedload(DonHang.chi_tiet_don_hang).joinedload(ChiTietDonHang.san_pham)
    ).offset(skip).limit(limit).all()
    return orders

@router.get("/{order_id}", response_model=DonHangResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin đơn hàng theo ID với thông tin người đặt và chi tiết đơn hàng"""
    order = db.query(DonHang).options(
        joinedload(DonHang.nguoi_dung),
        joinedload(DonHang.chi_tiet_don_hang).joinedload(ChiTietDonHang.san_pham)
    ).filter(DonHang.id == order_id).first()
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
    
    # Validate shipping info
    if not order.ten_nguoi_nhan or not order.ten_nguoi_nhan.strip():
        raise HTTPException(status_code=400, detail="Vui lòng nhập tên người nhận")
    if not order.so_dien_thoai_nguoi_nhan or not order.so_dien_thoai_nguoi_nhan.strip():
        raise HTTPException(status_code=400, detail="Vui lòng nhập số điện thoại người nhận")
    if not order.dia_chi_giao_hang or not order.dia_chi_giao_hang.strip():
        raise HTTPException(status_code=400, detail="Vui lòng nhập địa chỉ giao hàng")
    
    # Validate coupon if provided
    if order.ma_giam_gia_id:
        from app.models import MaGiamGia
        from datetime import datetime
        
        coupon = db.query(MaGiamGia).filter(MaGiamGia.id == order.ma_giam_gia_id).first()
        if not coupon:
            raise HTTPException(status_code=404, detail="Mã giảm giá không tồn tại")
        
        # Check if coupon is active
        if not coupon.hoat_dong:
            raise HTTPException(status_code=400, detail="Mã giảm giá đã hết hạn hoặc không còn hiệu lực")
        
        # Check date range
        now = datetime.utcnow()
        if coupon.ngay_bat_dau and now < coupon.ngay_bat_dau:
            raise HTTPException(status_code=400, detail="Mã giảm giá chưa có hiệu lực")
        if coupon.ngay_ket_thuc and now > coupon.ngay_ket_thuc:
            raise HTTPException(status_code=400, detail="Mã giảm giá đã hết hạn")
        
        # Check usage limit
        if coupon.so_luong and coupon.da_su_dung >= coupon.so_luong:
            raise HTTPException(status_code=400, detail="Mã giảm giá đã hết lượt sử dụng")
        
        # Check minimum order value
        if coupon.gia_tri_don_toi_thieu and order.tong_tien < coupon.gia_tri_don_toi_thieu:
            raise HTTPException(
                status_code=400, 
                detail=f"Đơn hàng tối thiểu {coupon.gia_tri_don_toi_thieu:,.0f}đ để sử dụng mã này"
            )
        
        # Update usage count
        coupon.da_su_dung += 1
    
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

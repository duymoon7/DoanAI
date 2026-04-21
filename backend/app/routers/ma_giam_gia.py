from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from decimal import Decimal

from ..database import get_db
from ..models import MaGiamGia, NguoiDung
from ..schemas.ma_giam_gia import (
    MaGiamGiaCreate,
    MaGiamGiaUpdate,
    MaGiamGiaResponse,
    MaGiamGiaValidate
)
from ..auth import get_current_user

router = APIRouter(prefix="/api/ma-giam-gia", tags=["Mã giảm giá"])


@router.get("", response_model=List[MaGiamGiaResponse])
def get_all_coupons(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lấy danh sách tất cả mã giảm giá"""
    coupons = db.query(MaGiamGia).order_by(MaGiamGia.ngay_tao.desc()).offset(skip).limit(limit).all()
    return coupons


@router.get("/{coupon_id}", response_model=MaGiamGiaResponse)
def get_coupon(coupon_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin mã giảm giá theo ID"""
    coupon = db.query(MaGiamGia).filter(MaGiamGia.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Mã giảm giá không tồn tại")
    return coupon


@router.post("/validate", response_model=MaGiamGiaValidate)
def validate_coupon(
    ma_code: str,
    order_total: Decimal,
    db: Session = Depends(get_db)
):
    """Kiểm tra mã giảm giá có hợp lệ không"""
    coupon = db.query(MaGiamGia).filter(MaGiamGia.ma_code == ma_code.upper()).first()
    
    if not coupon:
        return MaGiamGiaValidate(
            valid=False,
            message="Mã giảm giá không tồn tại",
            coupon_id=None,
            discount_amount=Decimal(0)
        )
    
    if not coupon.hoat_dong:
        return MaGiamGiaValidate(
            valid=False,
            message="Mã giảm giá đã bị vô hiệu hóa",
            coupon_id=None,
            discount_amount=Decimal(0)
        )
    
    # Kiểm tra số lượng
    if coupon.da_su_dung >= coupon.so_luong:
        return MaGiamGiaValidate(
            valid=False,
            message="Mã giảm giá đã hết lượt sử dụng",
            coupon_id=None,
            discount_amount=Decimal(0)
        )
    
    # Kiểm tra thời gian
    now = datetime.utcnow()
    if coupon.ngay_bat_dau and now < coupon.ngay_bat_dau:
        return MaGiamGiaValidate(
            valid=False,
            message="Mã giảm giá chưa đến thời gian sử dụng",
            coupon_id=None,
            discount_amount=Decimal(0)
        )
    
    if coupon.ngay_ket_thuc and now > coupon.ngay_ket_thuc:
        return MaGiamGiaValidate(
            valid=False,
            message="Mã giảm giá đã hết hạn",
            coupon_id=None,
            discount_amount=Decimal(0)
        )
    
    # Kiểm tra giá trị đơn hàng tối thiểu
    if order_total < coupon.gia_tri_don_toi_thieu:
        return MaGiamGiaValidate(
            valid=False,
            message=f"Đơn hàng tối thiểu {coupon.gia_tri_don_toi_thieu:,.0f}đ để sử dụng mã này",
            coupon_id=None,
            discount_amount=Decimal(0)
        )
    
    # Tính giá trị giảm
    if coupon.loai_giam == "percent":
        discount_amount = order_total * (coupon.gia_tri_giam / 100)
    else:  # fixed
        discount_amount = coupon.gia_tri_giam
    
    return MaGiamGiaValidate(
        valid=True,
        message="Mã giảm giá hợp lệ",
        discount_amount=discount_amount,
        coupon_id=coupon.id,
        ma_giam_gia=coupon
    )


@router.post("", response_model=MaGiamGiaResponse, status_code=status.HTTP_201_CREATED)
def create_coupon(
    coupon: MaGiamGiaCreate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Tạo mã giảm giá mới (Admin/Manager only)"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Creating coupon - User: {current_user.email}, Role: {current_user.vai_tro}")
    
    # Kiểm tra quyền
    if current_user.vai_tro not in ["admin", "manager"]:
        logger.warning(f"User {current_user.email} with role {current_user.vai_tro} tried to create coupon")
        raise HTTPException(status_code=403, detail="Không có quyền tạo mã giảm giá")
    
    # Kiểm tra mã code đã tồn tại chưa
    existing = db.query(MaGiamGia).filter(MaGiamGia.ma_code == coupon.ma_code.upper()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Mã code đã tồn tại")
    
    # Tạo mã giảm giá mới
    db_coupon = MaGiamGia(**coupon.model_dump())
    db_coupon.ma_code = db_coupon.ma_code.upper()  # Chuyển thành chữ hoa
    db.add(db_coupon)
    db.commit()
    db.refresh(db_coupon)
    
    logger.info(f"Coupon created successfully: {db_coupon.ma_code}")
    return db_coupon


@router.put("/{coupon_id}", response_model=MaGiamGiaResponse)
def update_coupon(
    coupon_id: int,
    coupon_update: MaGiamGiaUpdate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Cập nhật mã giảm giá (Admin/Manager only)"""
    # Kiểm tra quyền
    if current_user.vai_tro not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Không có quyền cập nhật mã giảm giá")
    
    coupon = db.query(MaGiamGia).filter(MaGiamGia.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Mã giảm giá không tồn tại")
    
    # Cập nhật
    update_data = coupon_update.model_dump(exclude_unset=True)
    if "ma_code" in update_data:
        update_data["ma_code"] = update_data["ma_code"].upper()
    
    for field, value in update_data.items():
        setattr(coupon, field, value)
    
    db.commit()
    db.refresh(coupon)
    
    return coupon


@router.delete("/{coupon_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coupon(
    coupon_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Xóa mã giảm giá (Admin only)"""
    # Chỉ admin mới được xóa
    if current_user.vai_tro != "admin":
        raise HTTPException(status_code=403, detail="Chỉ Admin mới có quyền xóa mã giảm giá")
    
    coupon = db.query(MaGiamGia).filter(MaGiamGia.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Mã giảm giá không tồn tại")
    
    db.delete(coupon)
    db.commit()
    
    return None


@router.post("/{coupon_id}/use")
def use_coupon(
    coupon_id: int,
    db: Session = Depends(get_db)
):
    """Đánh dấu mã giảm giá đã được sử dụng"""
    coupon = db.query(MaGiamGia).filter(MaGiamGia.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Mã giảm giá không tồn tại")
    
    if coupon.da_su_dung >= coupon.so_luong:
        raise HTTPException(status_code=400, detail="Mã giảm giá đã hết lượt sử dụng")
    
    coupon.da_su_dung += 1
    db.commit()
    
    return {"message": "Đã sử dụng mã giảm giá", "remaining": coupon.so_luong - coupon.da_su_dung}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List
from ..database import get_db
from ..models import DanhGia, NguoiDung, SanPham
from ..schemas.danh_gia import DanhGiaCreate, DanhGiaUpdate, DanhGiaResponse
from ..auth import get_current_user

router = APIRouter(prefix="/api/danh-gia", tags=["Đánh giá"])

@router.post("", response_model=DanhGiaResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    review: DanhGiaCreate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Tạo đánh giá mới cho sản phẩm"""
    # Kiểm tra sản phẩm tồn tại
    product = db.query(SanPham).filter(SanPham.id == review.san_pham_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
    
    # Kiểm tra user đã đánh giá sản phẩm này chưa
    existing = db.query(DanhGia).filter(
        DanhGia.nguoi_dung_id == current_user.id,
        DanhGia.san_pham_id == review.san_pham_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Bạn đã đánh giá sản phẩm này rồi")
    
    # Tạo đánh giá mới
    db_review = DanhGia(
        nguoi_dung_id=current_user.id,
        **review.model_dump()
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    
    return db_review

@router.get("", response_model=List[DanhGiaResponse])
def get_reviews(
    san_pham_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lấy danh sách đánh giá"""
    query = db.query(DanhGia).options(joinedload(DanhGia.nguoi_dung))
    
    if san_pham_id:
        query = query.filter(DanhGia.san_pham_id == san_pham_id)
    
    query = query.order_by(DanhGia.ngay_tao.desc())
    reviews = query.offset(skip).limit(limit).all()
    
    return reviews


@router.get("/all", response_model=List[DanhGiaResponse])
def get_all_reviews(
    skip: int = 0,
    limit: int = 1000,
    db: Session = Depends(get_db)
):
    """Lấy tất cả đánh giá với thông tin sản phẩm và người dùng (cho admin)"""
    reviews = db.query(DanhGia).options(
        joinedload(DanhGia.nguoi_dung),
        joinedload(DanhGia.san_pham)
    ).order_by(DanhGia.ngay_tao.desc()).offset(skip).limit(limit).all()
    
    return reviews


@router.get("/stats/{san_pham_id}")
def get_review_stats(san_pham_id: int, db: Session = Depends(get_db)):
    """Lấy thống kê đánh giá của sản phẩm"""
    # Kiểm tra sản phẩm tồn tại
    product = db.query(SanPham).filter(SanPham.id == san_pham_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
    
    # Tổng số đánh giá
    total_reviews = db.query(func.count(DanhGia.id)).filter(
        DanhGia.san_pham_id == san_pham_id
    ).scalar()
    
    # Điểm trung bình
    avg_rating = db.query(func.avg(DanhGia.diem_so)).filter(
        DanhGia.san_pham_id == san_pham_id
    ).scalar()
    
    # Phân bố theo số sao
    rating_distribution = {}
    for star in range(1, 6):
        count = db.query(func.count(DanhGia.id)).filter(
            DanhGia.san_pham_id == san_pham_id,
            DanhGia.diem_so >= star,
            DanhGia.diem_so < star + 1
        ).scalar()
        rating_distribution[star] = count
    
    return {
        "total_reviews": total_reviews or 0,
        "average_rating": round(float(avg_rating), 1) if avg_rating else 0,
        "rating_distribution": rating_distribution
    }

@router.get("/{review_id}", response_model=DanhGiaResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin một đánh giá"""
    review = db.query(DanhGia).filter(DanhGia.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Đánh giá không tồn tại")
    
    review.nguoi_dung = {
        "id": review.nguoi_dung.id,
        "ho_ten": review.nguoi_dung.ho_ten,
        "email": review.nguoi_dung.email
    }
    
    return review

@router.put("/{review_id}", response_model=DanhGiaResponse)
def update_review(
    review_id: int,
    review_update: DanhGiaUpdate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Cập nhật đánh giá"""
    review = db.query(DanhGia).filter(DanhGia.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Đánh giá không tồn tại")
    
    # Chỉ cho phép user sở hữu hoặc admin sửa
    if review.nguoi_dung_id != current_user.id and current_user.vai_tro != "admin":
        raise HTTPException(status_code=403, detail="Không có quyền sửa đánh giá này")
    
    # Cập nhật
    for key, value in review_update.model_dump(exclude_unset=True).items():
        setattr(review, key, value)
    
    db.commit()
    db.refresh(review)
    
    return review

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Xóa đánh giá"""
    review = db.query(DanhGia).filter(DanhGia.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Đánh giá không tồn tại")
    
    # Chỉ cho phép user sở hữu hoặc admin xóa
    if review.nguoi_dung_id != current_user.id and current_user.vai_tro != "admin":
        raise HTTPException(status_code=403, detail="Không có quyền xóa đánh giá này")
    
    db.delete(review)
    db.commit()
    
    return None

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import SanPham, DanhMuc
from app.schemas import SanPhamCreate, SanPhamUpdate, SanPhamResponse

router = APIRouter(prefix="/api/san-pham", tags=["Sản phẩm"])

@router.get("/", response_model=List[SanPhamResponse])
def get_all_products(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    danh_muc_id: int = None,
    min_price: float = None,
    max_price: float = None,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách sản phẩm với filter và search
    
    - search: Tìm kiếm theo tên sản phẩm
    - danh_muc_id: Lọc theo danh mục
    - min_price, max_price: Lọc theo khoảng giá
    - sort_by: Sắp xếp theo (id, ten, gia, ngay_tao)
    - order: Thứ tự (asc, desc)
    """
    query = db.query(SanPham)
    
    # Search by name
    if search:
        query = query.filter(SanPham.ten.like(f"%{search}%"))
    
    # Filter by category
    if danh_muc_id:
        query = query.filter(SanPham.danh_muc_id == danh_muc_id)
    
    # Filter by price range
    if min_price is not None:
        query = query.filter(SanPham.gia >= min_price)
    if max_price is not None:
        query = query.filter(SanPham.gia <= max_price)
    
    # Sorting
    if sort_by == "ten":
        query = query.order_by(SanPham.ten.desc() if order == "desc" else SanPham.ten.asc())
    elif sort_by == "gia":
        query = query.order_by(SanPham.gia.desc() if order == "desc" else SanPham.gia.asc())
    elif sort_by == "ngay_tao":
        query = query.order_by(SanPham.ngay_tao.desc() if order == "desc" else SanPham.ngay_tao.asc())
    else:
        query = query.order_by(SanPham.id.desc() if order == "desc" else SanPham.id.asc())
    
    products = query.offset(skip).limit(limit).all()
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


@router.get("/search", response_model=List[SanPhamResponse])
def search_products(q: str, limit: int = 10, db: Session = Depends(get_db)):
    """
    Tìm kiếm nhanh sản phẩm
    
    - q: Từ khóa tìm kiếm
    """
    products = db.query(SanPham).filter(
        SanPham.ten.like(f"%{q}%")
    ).limit(limit).all()
    return products


@router.get("/category/{category_id}", response_model=List[SanPhamResponse])
def get_products_by_category(
    category_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lấy sản phẩm theo danh mục"""
    products = db.query(SanPham).filter(
        SanPham.danh_muc_id == category_id
    ).offset(skip).limit(limit).all()
    return products


@router.get("/featured", response_model=List[SanPhamResponse])
def get_featured_products(limit: int = 6, db: Session = Depends(get_db)):
    """Lấy sản phẩm nổi bật (mới nhất)"""
    products = db.query(SanPham).order_by(
        SanPham.ngay_tao.desc()
    ).limit(limit).all()
    return products

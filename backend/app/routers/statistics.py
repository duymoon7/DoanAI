"""
Statistics Router
=================
Endpoints cho thống kê và báo cáo.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import SanPham, DanhMuc, DonHang, NguoiDung, ChiTietDonHang
from app.auth import get_current_admin_user

router = APIRouter(prefix="/api/statistics", tags=["Statistics"])


@router.get("/dashboard")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """
    Lấy thống kê tổng quan cho dashboard admin
    
    Requires: Admin role
    """
    # Count totals
    total_products = db.query(SanPham).count()
    total_categories = db.query(DanhMuc).count()
    total_users = db.query(NguoiDung).count()
    total_orders = db.query(DonHang).count()
    
    # Revenue statistics
    total_revenue = db.query(func.sum(DonHang.tong_tien)).scalar() or 0
    
    # Order status breakdown
    order_status = db.query(
        DonHang.trang_thai,
        func.count(DonHang.id)
    ).group_by(DonHang.trang_thai).all()
    
    # Top selling products
    top_products = db.query(
        SanPham.ten,
        func.sum(ChiTietDonHang.so_luong).label('total_sold')
    ).join(
        ChiTietDonHang, SanPham.id == ChiTietDonHang.san_pham_id
    ).group_by(
        SanPham.id, SanPham.ten
    ).order_by(
        func.sum(ChiTietDonHang.so_luong).desc()
    ).limit(5).all()
    
    # Recent orders
    recent_orders = db.query(DonHang).order_by(
        DonHang.ngay_tao.desc()
    ).limit(5).all()
    
    return {
        "totals": {
            "products": total_products,
            "categories": total_categories,
            "users": total_users,
            "orders": total_orders,
            "revenue": float(total_revenue)
        },
        "order_status": [
            {"status": status, "count": count}
            for status, count in order_status
        ],
        "top_products": [
            {"name": name, "sold": int(sold)}
            for name, sold in top_products
        ],
        "recent_orders": [
            {
                "id": order.id,
                "user_id": order.nguoi_dung_id,
                "total": float(order.tong_tien),
                "status": order.trang_thai,
                "created_at": order.ngay_tao.isoformat()
            }
            for order in recent_orders
        ]
    }


@router.get("/revenue")
async def get_revenue_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """
    Thống kê doanh thu
    
    Requires: Admin role
    """
    # Total revenue
    total_revenue = db.query(func.sum(DonHang.tong_tien)).scalar() or 0
    
    # Revenue by status
    revenue_by_status = db.query(
        DonHang.trang_thai,
        func.sum(DonHang.tong_tien).label('revenue'),
        func.count(DonHang.id).label('count')
    ).group_by(DonHang.trang_thai).all()
    
    # Average order value
    avg_order_value = db.query(func.avg(DonHang.tong_tien)).scalar() or 0
    
    return {
        "total_revenue": float(total_revenue),
        "average_order_value": float(avg_order_value),
        "by_status": [
            {
                "status": status,
                "revenue": float(revenue),
                "order_count": count
            }
            for status, revenue, count in revenue_by_status
        ]
    }


@router.get("/products")
async def get_product_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """
    Thống kê sản phẩm
    
    Requires: Admin role
    """
    # Products by category
    products_by_category = db.query(
        DanhMuc.ten,
        func.count(SanPham.id).label('count')
    ).join(
        SanPham, DanhMuc.id == SanPham.danh_muc_id
    ).group_by(
        DanhMuc.id, DanhMuc.ten
    ).all()
    
    # Price statistics
    price_stats = db.query(
        func.min(SanPham.gia).label('min_price'),
        func.max(SanPham.gia).label('max_price'),
        func.avg(SanPham.gia).label('avg_price')
    ).first()
    
    return {
        "by_category": [
            {"category": name, "count": count}
            for name, count in products_by_category
        ],
        "price_range": {
            "min": float(price_stats.min_price or 0),
            "max": float(price_stats.max_price or 0),
            "average": float(price_stats.avg_price or 0)
        }
    }

"""
Statistics Router
=================
Endpoints cho thống kê và báo cáo theo PB31.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_, case
from app.database import get_db
from app.models import SanPham, DanhMuc, DonHang, NguoiDung, ChiTietDonHang, MaGiamGia
from app.auth import get_current_admin_user
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter(prefix="/api/statistics", tags=["Statistics"])


@router.get("/dashboard")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """
    PB31 - Báo cáo thống kê Dashboard
    
    Trả về:
    - Card doanh thu tháng hiện tại với % biến động so với tháng trước
    - Số lượng đơn hàng (chỉ tính completed)
    - Pie Chart trạng thái đơn hàng (pending, completed, cancelled)
    - Top 10 sản phẩm bán chạy nhất
    
    Requires: Admin/Manager role
    """
    now = datetime.utcnow()
    current_month = now.month
    current_year = now.year
    
    # Tính tháng trước
    if current_month == 1:
        previous_month = 12
        previous_year = current_year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year
    
    # 1. Doanh thu tháng hiện tại (chỉ tính completed)
    current_month_revenue = db.query(func.sum(DonHang.tong_tien)).filter(
        and_(
            extract('month', DonHang.ngay_tao) == current_month,
            extract('year', DonHang.ngay_tao) == current_year,
            DonHang.trang_thai == 'completed'
        )
    ).scalar() or 0
    
    # 2. Doanh thu tháng trước
    previous_month_revenue = db.query(func.sum(DonHang.tong_tien)).filter(
        and_(
            extract('month', DonHang.ngay_tao) == previous_month,
            extract('year', DonHang.ngay_tao) == previous_year,
            DonHang.trang_thai == 'completed'
        )
    ).scalar() or 0
    
    # 3. Tính % biến động
    if previous_month_revenue > 0:
        revenue_change_percent = ((current_month_revenue - previous_month_revenue) / previous_month_revenue) * 100
    else:
        revenue_change_percent = 100 if current_month_revenue > 0 else 0
    
    # 4. Số lượng đơn hàng completed
    completed_orders_count = db.query(func.count(DonHang.id)).filter(
        DonHang.trang_thai == 'completed'
    ).scalar() or 0
    
    # 5. Pie Chart - Trạng thái đơn hàng
    order_status_breakdown = db.query(
        DonHang.trang_thai,
        func.count(DonHang.id).label('count')
    ).group_by(DonHang.trang_thai).all()
    
    # 6. Top 10 sản phẩm bán chạy nhất (chỉ tính completed orders)
    top_selling_products = db.query(
        SanPham.id,
        SanPham.ten,
        SanPham.gia,
        SanPham.hinh_anh,
        func.sum(ChiTietDonHang.so_luong).label('total_sold'),
        func.sum(ChiTietDonHang.so_luong * SanPham.gia).label('total_revenue')
    ).join(
        ChiTietDonHang, SanPham.id == ChiTietDonHang.san_pham_id
    ).join(
        DonHang, ChiTietDonHang.don_hang_id == DonHang.id
    ).filter(
        DonHang.trang_thai == 'completed'
    ).group_by(
        SanPham.id, SanPham.ten, SanPham.gia, SanPham.hinh_anh
    ).order_by(
        func.sum(ChiTietDonHang.so_luong).desc()
    ).limit(10).all()
    
    # 7. Tổng số thống kê cơ bản
    total_products = db.query(SanPham).filter(SanPham.trang_thai == 'active').count()
    total_users = db.query(NguoiDung).filter(NguoiDung.vai_tro == 'user').count()
    total_orders = db.query(DonHang).count()
    
    return {
        "revenue": {
            "current_month": float(current_month_revenue),
            "previous_month": float(previous_month_revenue),
            "change_percent": round(revenue_change_percent, 2),
            "month": current_month,
            "year": current_year
        },
        "orders": {
            "completed_count": completed_orders_count,
            "total_count": total_orders
        },
        "order_status_chart": [
            {
                "status": status,
                "count": count,
                "label": {
                    "pending": "Chờ xử lý",
                    "completed": "Hoàn thành",
                    "cancelled": "Đã hủy"
                }.get(status, status)
            }
            for status, count in order_status_breakdown
        ],
        "top_selling_products": [
            {
                "id": product.id,
                "name": product.ten,
                "price": float(product.gia),
                "image": product.hinh_anh,
                "total_sold": int(product.total_sold),
                "total_revenue": float(product.total_revenue)
            }
            for product in top_selling_products
        ],
        "summary": {
            "total_products": total_products,
            "total_users": total_users,
            "total_orders": total_orders
        }
    }


@router.get("/revenue")
async def get_revenue_stats(
    start_date: Optional[str] = Query(None, description="Ngày bắt đầu (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Ngày kết thúc (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """
    Thống kê doanh thu chi tiết
    
    - Tổng doanh thu (chỉ completed)
    - Doanh thu theo trạng thái
    - Giá trị đơn hàng trung bình
    - Doanh thu theo tháng (12 tháng gần nhất)
    - Tổng tiền giảm giá
    
    Requires: Admin/Manager role
    """
    # Parse date filters
    query_filter = [DonHang.trang_thai == 'completed']
    
    if start_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            query_filter.append(DonHang.ngay_tao >= start)
        except ValueError:
            pass
    
    if end_date:
        try:
            end = datetime.strptime(end_date, "%Y-%m-%d")
            query_filter.append(DonHang.ngay_tao <= end)
        except ValueError:
            pass
    
    # 1. Tổng doanh thu (completed)
    total_revenue = db.query(func.sum(DonHang.tong_tien)).filter(
        and_(*query_filter)
    ).scalar() or 0
    
    # 2. Doanh thu theo trạng thái
    revenue_by_status = db.query(
        DonHang.trang_thai,
        func.sum(DonHang.tong_tien).label('revenue'),
        func.count(DonHang.id).label('count')
    ).group_by(DonHang.trang_thai).all()
    
    # 3. Giá trị đơn hàng trung bình
    avg_order_value = db.query(func.avg(DonHang.tong_tien)).filter(
        and_(*query_filter)
    ).scalar() or 0
    
    # 4. Doanh thu theo tháng (12 tháng gần nhất)
    monthly_revenue = db.query(
        extract('year', DonHang.ngay_tao).label('year'),
        extract('month', DonHang.ngay_tao).label('month'),
        func.sum(DonHang.tong_tien).label('revenue'),
        func.count(DonHang.id).label('order_count')
    ).filter(
        DonHang.trang_thai == 'completed'
    ).group_by(
        extract('year', DonHang.ngay_tao),
        extract('month', DonHang.ngay_tao)
    ).order_by(
        extract('year', DonHang.ngay_tao).desc(),
        extract('month', DonHang.ngay_tao).desc()
    ).limit(12).all()
    
    # 5. Tổng tiền giảm giá
    total_discount = db.query(func.sum(DonHang.so_tien_giam)).filter(
        DonHang.trang_thai == 'completed'
    ).scalar() or 0
    
    return {
        "total_revenue": float(total_revenue),
        "average_order_value": float(avg_order_value),
        "total_discount": float(total_discount),
        "by_status": [
            {
                "status": status,
                "revenue": float(revenue),
                "order_count": count,
                "label": {
                    "pending": "Chờ xử lý",
                    "completed": "Hoàn thành",
                    "cancelled": "Đã hủy"
                }.get(status, status)
            }
            for status, revenue, count in revenue_by_status
        ],
        "monthly_revenue": [
            {
                "year": int(year),
                "month": int(month),
                "revenue": float(revenue),
                "order_count": order_count,
                "month_name": datetime(int(year), int(month), 1).strftime("%B %Y")
            }
            for year, month, revenue, order_count in monthly_revenue
        ]
    }


@router.get("/products")
async def get_product_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """
    Thống kê sản phẩm
    
    - Sản phẩm theo danh mục
    - Thống kê giá (min, max, avg)
    - Sản phẩm sắp hết hàng (tồn kho < 10)
    - Sản phẩm hết hàng
    
    Requires: Admin/Manager role
    """
    # 1. Sản phẩm theo danh mục
    products_by_category = db.query(
        DanhMuc.ten,
        func.count(SanPham.id).label('count')
    ).join(
        SanPham, DanhMuc.id == SanPham.danh_muc_id
    ).filter(
        SanPham.trang_thai == 'active'
    ).group_by(
        DanhMuc.id, DanhMuc.ten
    ).all()
    
    # 2. Thống kê giá
    price_stats = db.query(
        func.min(SanPham.gia).label('min_price'),
        func.max(SanPham.gia).label('max_price'),
        func.avg(SanPham.gia).label('avg_price')
    ).filter(SanPham.trang_thai == 'active').first()
    
    # 3. Sản phẩm sắp hết hàng (tồn kho < 10)
    low_stock_products = db.query(
        SanPham.id,
        SanPham.ten,
        SanPham.ton_kho,
        SanPham.gia,
        DanhMuc.ten.label('danh_muc')
    ).join(
        DanhMuc, SanPham.danh_muc_id == DanhMuc.id
    ).filter(
        and_(
            SanPham.ton_kho < 10,
            SanPham.ton_kho > 0,
            SanPham.trang_thai == 'active'
        )
    ).order_by(SanPham.ton_kho.asc()).all()
    
    # 4. Sản phẩm hết hàng
    out_of_stock_count = db.query(func.count(SanPham.id)).filter(
        and_(
            SanPham.ton_kho == 0,
            SanPham.trang_thai == 'active'
        )
    ).scalar() or 0
    
    return {
        "by_category": [
            {"category": name, "count": count}
            for name, count in products_by_category
        ],
        "price_range": {
            "min": float(price_stats.min_price or 0),
            "max": float(price_stats.max_price or 0),
            "average": float(price_stats.avg_price or 0)
        },
        "low_stock_products": [
            {
                "id": product.id,
                "name": product.ten,
                "stock": product.ton_kho,
                "price": float(product.gia),
                "category": product.danh_muc
            }
            for product in low_stock_products
        ],
        "out_of_stock_count": out_of_stock_count
    }


@router.get("/coupons")
async def get_coupon_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """
    Thống kê mã giảm giá
    
    - Hiệu quả mã giảm giá (số lần dùng, tổng tiền giảm)
    - Tỷ lệ sử dụng mã giảm giá
    - Tổng tiết kiệm của khách hàng
    - Mã giảm giá sắp hết hạn
    
    Requires: Admin/Manager role
    """
    # 1. Hiệu quả mã giảm giá
    coupon_effectiveness = db.query(
        MaGiamGia.id,
        MaGiamGia.ma_code,
        MaGiamGia.mo_ta,
        MaGiamGia.loai_giam,
        MaGiamGia.gia_tri_giam,
        func.count(DonHang.id).label('usage_count'),
        func.sum(DonHang.so_tien_giam).label('total_discount'),
        func.avg(DonHang.tong_tien).label('avg_order_value')
    ).outerjoin(
        DonHang, MaGiamGia.id == DonHang.ma_giam_gia_id
    ).filter(
        DonHang.trang_thai == 'completed'
    ).group_by(
        MaGiamGia.id, MaGiamGia.ma_code, MaGiamGia.mo_ta,
        MaGiamGia.loai_giam, MaGiamGia.gia_tri_giam
    ).order_by(
        func.sum(DonHang.so_tien_giam).desc()
    ).all()
    
    # 2. Tỷ lệ sử dụng mã giảm giá
    total_completed_orders = db.query(func.count(DonHang.id)).filter(
        DonHang.trang_thai == 'completed'
    ).scalar() or 0
    
    orders_with_coupon = db.query(func.count(DonHang.id)).filter(
        and_(
            DonHang.trang_thai == 'completed',
            DonHang.ma_giam_gia_id.isnot(None)
        )
    ).scalar() or 0
    
    usage_rate = (orders_with_coupon / total_completed_orders * 100) if total_completed_orders > 0 else 0
    
    # 3. Tổng tiết kiệm của khách hàng
    total_savings = db.query(func.sum(DonHang.so_tien_giam)).filter(
        DonHang.trang_thai == 'completed'
    ).scalar() or 0
    
    # 4. Mã giảm giá sắp hết hạn (trong 7 ngày tới)
    seven_days_later = datetime.utcnow() + timedelta(days=7)
    expiring_soon = db.query(
        MaGiamGia.id,
        MaGiamGia.ma_code,
        MaGiamGia.mo_ta,
        MaGiamGia.ngay_ket_thuc,
        MaGiamGia.so_luong,
        MaGiamGia.da_su_dung
    ).filter(
        and_(
            MaGiamGia.hoat_dong == True,
            MaGiamGia.ngay_ket_thuc <= seven_days_later,
            MaGiamGia.ngay_ket_thuc >= datetime.utcnow()
        )
    ).order_by(MaGiamGia.ngay_ket_thuc.asc()).all()
    
    return {
        "coupon_effectiveness": [
            {
                "id": coupon.id,
                "code": coupon.ma_code,
                "description": coupon.mo_ta,
                "type": coupon.loai_giam,
                "value": float(coupon.gia_tri_giam),
                "usage_count": coupon.usage_count or 0,
                "total_discount": float(coupon.total_discount or 0),
                "avg_order_value": float(coupon.avg_order_value or 0)
            }
            for coupon in coupon_effectiveness
        ],
        "usage_statistics": {
            "total_orders": total_completed_orders,
            "orders_with_coupon": orders_with_coupon,
            "usage_rate": round(usage_rate, 2),
            "total_savings": float(total_savings)
        },
        "expiring_soon": [
            {
                "id": coupon.id,
                "code": coupon.ma_code,
                "description": coupon.mo_ta,
                "expiry_date": coupon.ngay_ket_thuc.isoformat(),
                "remaining_quantity": coupon.so_luong - coupon.da_su_dung,
                "days_left": (coupon.ngay_ket_thuc - datetime.utcnow()).days
            }
            for coupon in expiring_soon
        ]
    }


@router.get("/customers")
async def get_customer_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """
    Thống kê khách hàng
    
    - Top 10 khách hàng VIP (mua nhiều nhất)
    - Tổng số khách hàng
    - Khách hàng mới trong tháng
    
    Requires: Admin/Manager role
    """
    # 1. Top 10 khách hàng VIP
    top_customers = db.query(
        NguoiDung.id,
        NguoiDung.ho_ten,
        NguoiDung.email,
        NguoiDung.so_dien_thoai,
        func.count(DonHang.id).label('total_orders'),
        func.sum(DonHang.tong_tien).label('total_spent')
    ).join(
        DonHang, NguoiDung.id == DonHang.nguoi_dung_id
    ).filter(
        DonHang.trang_thai == 'completed'
    ).group_by(
        NguoiDung.id, NguoiDung.ho_ten, NguoiDung.email, NguoiDung.so_dien_thoai
    ).order_by(
        func.sum(DonHang.tong_tien).desc()
    ).limit(10).all()
    
    # 2. Tổng số khách hàng
    total_customers = db.query(func.count(NguoiDung.id)).filter(
        NguoiDung.vai_tro == 'user'
    ).scalar() or 0
    
    # 3. Khách hàng mới trong tháng
    now = datetime.utcnow()
    new_customers_this_month = db.query(func.count(NguoiDung.id)).filter(
        and_(
            NguoiDung.vai_tro == 'user',
            extract('month', NguoiDung.ngay_tao) == now.month,
            extract('year', NguoiDung.ngay_tao) == now.year
        )
    ).scalar() or 0
    
    return {
        "top_customers": [
            {
                "id": customer.id,
                "name": customer.ho_ten,
                "email": customer.email,
                "phone": customer.so_dien_thoai,
                "total_orders": customer.total_orders,
                "total_spent": float(customer.total_spent)
            }
            for customer in top_customers
        ],
        "total_customers": total_customers,
        "new_customers_this_month": new_customers_this_month
    }


@router.get("/export")
async def export_statistics(
    report_type: str = Query(..., description="Loại báo cáo: revenue, products, customers, coupons"),
    format: str = Query("json", description="Định dạng: json, csv"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """
    Export báo cáo thống kê
    
    Hỗ trợ export ra JSON hoặc CSV (tùy chọn)
    
    Requires: Admin/Manager role
    """
    # Placeholder cho tính năng export
    # Có thể mở rộng để export ra CSV hoặc PDF
    
    if report_type == "revenue":
        data = await get_revenue_stats(db=db, current_user=current_user)
    elif report_type == "products":
        data = await get_product_stats(db=db, current_user=current_user)
    elif report_type == "customers":
        data = await get_customer_stats(db=db, current_user=current_user)
    elif report_type == "coupons":
        data = await get_coupon_stats(db=db, current_user=current_user)
    else:
        return {"error": "Invalid report type"}
    
    return {
        "report_type": report_type,
        "format": format,
        "generated_at": datetime.utcnow().isoformat(),
        "data": data
    }

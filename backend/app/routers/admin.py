"""
Admin Router
============
Router cho các chức năng quản trị hệ thống.

⚠️  CẢNH BÁO: Các endpoint này CHỈ SỬ DỤNG TRONG DEVELOPMENT!
KHÔNG BAO GIỜ enable trong production!
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import (
    get_db,
    engine,
    Base,
    SessionLocal,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
)
from app.models import (
    NguoiDung,
    DanhMuc,
    SanPham,
    DonHang,
    ChiTietDonHang,
    LichSuChat,
)
import logging
import os

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)


def check_dev_environment():
    """
    Check if running in development environment.
    Raises HTTPException if not in development.
    """
    app_env = os.getenv("APP_ENV", "production").lower()
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    if app_env != "development" and not debug:
        raise HTTPException(
            status_code=403,
            detail="Admin endpoints are only available in development environment"
        )


@router.get("/info")
async def get_database_info(db: Session = Depends(get_db)):
    """
    Lấy thông tin về database hiện tại.
    
    Returns:
        - Database connection info
        - Current database name
        - List of tables
        - Record counts
    """
    try:
        # Get current database and version (MySQL syntax)
        result = db.execute(text("SELECT DATABASE(), VERSION()"))
        current_db, version = result.fetchone()
        
        # Get all tables
        result = db.execute(text(f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = '{DB_NAME}'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result]
        
        # Get record counts
        counts = {}
        if "danh_muc" in tables:
            counts["categories"] = db.query(DanhMuc).count()
        if "san_pham" in tables:
            counts["products"] = db.query(SanPham).count()
        if "nguoi_dung" in tables:
            counts["users"] = db.query(NguoiDung).count()
        if "don_hang" in tables:
            counts["orders"] = db.query(DonHang).count()
        if "chi_tiet_don_hang" in tables:
            counts["order_details"] = db.query(ChiTietDonHang).count()
        if "lich_su_chat" in tables:
            counts["chat_history"] = db.query(LichSuChat).count()
        
        return {
            "status": "success",
            "connection": {
                "host": DB_HOST,
                "port": DB_PORT,
                "database": DB_NAME,
                "user": DB_USER,
                "current_database": current_db,
                "database_correct": current_db == DB_NAME,
            },
            "version": version.split(",")[0],
            "tables": tables,
            "table_count": len(tables),
            "record_counts": counts,
            "total_records": sum(counts.values()),
        }
    except Exception as e:
        logger.error(f"Failed to get database info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset-db")
async def reset_database():
    """
    Reset toàn bộ database: xóa tất cả bảng, tạo lại, và seed dữ liệu mẫu.
    
    ⚠️  CẢNH BÁO: Endpoint này sẽ XÓA TOÀN BỘ DỮ LIỆU!
    CHỈ SỬ DỤNG TRONG DEVELOPMENT!
    
    Returns:
        - Status của từng bước
        - Thống kê dữ liệu sau khi reset
    """
    # Check if in development environment
    check_dev_environment()
    
    logger.warning("⚠️  Admin endpoint /reset-db called - resetting database...")
    
    result = {
        "status": "in_progress",
        "steps": {},
        "errors": []
    }
    
    try:
        # Step 1: Drop all tables
        logger.info("Step 1: Dropping all tables...")
        try:
            # Get tables before dropping
            with engine.connect() as conn:
                tables_result = conn.execute(text(f"""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = '{DB_NAME}'
                """))
                tables_before = [row[0] for row in tables_result]
            
            Base.metadata.drop_all(bind=engine)
            
            result["steps"]["drop_tables"] = {
                "status": "success",
                "tables_dropped": tables_before,
                "count": len(tables_before)
            }
            logger.info(f"✅ Dropped {len(tables_before)} tables")
        except Exception as e:
            error_msg = f"Failed to drop tables: {str(e)}"
            logger.error(error_msg)
            result["steps"]["drop_tables"] = {"status": "failed", "error": error_msg}
            result["errors"].append(error_msg)
            raise
        
        # Step 2: Create all tables
        logger.info("Step 2: Creating all tables...")
        try:
            Base.metadata.create_all(bind=engine)
            
            # Verify tables created
            with engine.connect() as conn:
                tables_result = conn.execute(text(f"""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = '{DB_NAME}'
                    ORDER BY table_name
                """))
                tables_created = [row[0] for row in tables_result]
            
            result["steps"]["create_tables"] = {
                "status": "success",
                "tables_created": tables_created,
                "count": len(tables_created)
            }
            logger.info(f"✅ Created {len(tables_created)} tables")
        except Exception as e:
            error_msg = f"Failed to create tables: {str(e)}"
            logger.error(error_msg)
            result["steps"]["create_tables"] = {"status": "failed", "error": error_msg}
            result["errors"].append(error_msg)
            raise
        
        # Step 3: Seed initial data
        logger.info("Step 3: Seeding initial data...")
        try:
            db = SessionLocal()
            try:
                # Seed categories
                categories_data = [
                    {"ten": "Điện thoại"},
                    {"ten": "Laptop"},
                    {"ten": "Tablet"},
                    {"ten": "Phụ kiện"},
                    {"ten": "Tai nghe"},
                    {"ten": "Đồng hồ thông minh"},
                ]
                
                categories = {}
                for cat_data in categories_data:
                    category = DanhMuc(**cat_data)
                    db.add(category)
                    db.flush()
                    categories[cat_data["ten"]] = category.id
                
                db.commit()
                
                # Seed products
                products_data = [
                    {
                        "ten": "iPhone 15 Pro Max",
                        "mo_ta": "iPhone 15 Pro Max 256GB - Titan tự nhiên",
                        "gia": 29990000,
                        "hinh_anh": "https://cdn.tgdd.vn/Products/Images/42/305658/iphone-15-pro-max-blue-thumbnew-600x600.jpg",
                        "danh_muc_id": categories["Điện thoại"],
                    },
                    {
                        "ten": "Samsung Galaxy S24 Ultra",
                        "mo_ta": "Samsung Galaxy S24 Ultra 12GB 256GB",
                        "gia": 27990000,
                        "hinh_anh": "https://cdn.tgdd.vn/Products/Images/42/320721/samsung-galaxy-s24-ultra-grey-thumbnew-600x600.jpg",
                        "danh_muc_id": categories["Điện thoại"],
                    },
                    {
                        "ten": "MacBook Pro 14 M3",
                        "mo_ta": "MacBook Pro 14 inch M3 Pro 18GB 512GB",
                        "gia": 52990000,
                        "hinh_anh": "https://cdn.tgdd.vn/Products/Images/44/309016/macbook-pro-14-inch-m3-pro-2023-xam-thumbnew-600x600.jpg",
                        "danh_muc_id": categories["Laptop"],
                    },
                    {
                        "ten": "iPad Pro M2 11 inch",
                        "mo_ta": "iPad Pro M2 11 inch WiFi 128GB",
                        "gia": 21990000,
                        "hinh_anh": "https://cdn.tgdd.vn/Products/Images/522/325514/ipad-pro-11-inch-m2-wifi-128gb-2024-xam-thumb-600x600.jpg",
                        "danh_muc_id": categories["Tablet"],
                    },
                    {
                        "ten": "AirPods Pro 2",
                        "mo_ta": "Apple AirPods Pro 2 USB-C",
                        "gia": 5990000,
                        "hinh_anh": "https://cdn.tgdd.vn/Products/Images/54/325265/airpods-pro-2-usb-c-thumb-600x600.jpg",
                        "danh_muc_id": categories["Tai nghe"],
                    },
                    {
                        "ten": "Apple Watch Series 9",
                        "mo_ta": "Apple Watch Series 9 GPS 45mm",
                        "gia": 10990000,
                        "hinh_anh": "https://cdn.tgdd.vn/Products/Images/7077/309732/apple-watch-s9-gps-45mm-vien-nhom-day-cao-su-thumb-xanh-duong-600x600.jpg",
                        "danh_muc_id": categories["Đồng hồ thông minh"],
                    },
                ]
                
                for prod_data in products_data:
                    product = SanPham(**prod_data)
                    db.add(product)
                
                db.commit()
                
                # Get final counts
                cat_count = db.query(DanhMuc).count()
                prod_count = db.query(SanPham).count()
                
                result["steps"]["seed_data"] = {
                    "status": "success",
                    "categories_seeded": cat_count,
                    "products_seeded": prod_count,
                }
                logger.info(f"✅ Seeded {cat_count} categories and {prod_count} products")
                
            finally:
                db.close()
                
        except Exception as e:
            error_msg = f"Failed to seed data: {str(e)}"
            logger.error(error_msg)
            result["steps"]["seed_data"] = {"status": "failed", "error": error_msg}
            result["errors"].append(error_msg)
            raise
        
        # Success
        result["status"] = "success"
        result["message"] = "Database reset completed successfully!"
        logger.info("✅ Database reset completed successfully!")
        
        return result
        
    except Exception as e:
        result["status"] = "failed"
        result["message"] = f"Database reset failed: {str(e)}"
        logger.error(f"❌ Database reset failed: {e}")
        raise HTTPException(status_code=500, detail=result)


@router.get("/tables")
async def list_tables(db: Session = Depends(get_db)):
    """
    Liệt kê tất cả các bảng trong database.
    
    Returns:
        - List of table names
        - Table count
        - Registered models vs actual tables
    """
    try:
        # Get registered models
        registered_tables = list(Base.metadata.tables.keys())
        
        # Get actual tables in database
        result = db.execute(text(f"""
            SELECT table_name
            FROM information_schema.tables 
            WHERE table_schema = '{DB_NAME}'
            ORDER BY table_name
        """))
        actual_tables = [{"name": row[0], "size": "N/A"} for row in result]
        
        # Check for missing tables
        actual_names = [t["name"] for t in actual_tables]
        missing = set(registered_tables) - set(actual_names)
        extra = set(actual_names) - set(registered_tables)
        
        return {
            "status": "success",
            "registered_models": sorted(registered_tables),
            "registered_count": len(registered_tables),
            "actual_tables": actual_tables,
            "actual_count": len(actual_tables),
            "missing_tables": list(missing),
            "extra_tables": list(extra),
            "sync_status": "synced" if not missing and not extra else "out_of_sync"
        }
    except Exception as e:
        logger.error(f"Failed to list tables: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear-table/{table_name}")
async def clear_table(table_name: str, db: Session = Depends(get_db)):
    """
    Xóa toàn bộ dữ liệu trong một bảng cụ thể (không xóa bảng).
    
    ⚠️  CẢNH BÁO: Endpoint này sẽ XÓA TOÀN BỘ DỮ LIỆU trong bảng!
    CHỈ SỬ DỤNG TRONG DEVELOPMENT!
    
    Args:
        table_name: Tên bảng cần xóa dữ liệu
    """
    # Check if in development environment
    check_dev_environment()
    
    # Validate table name
    allowed_tables = [
        "nguoi_dung", "danh_muc", "san_pham",
        "don_hang", "chi_tiet_don_hang", "lich_su_chat"
    ]
    
    if table_name not in allowed_tables:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid table name. Allowed tables: {', '.join(allowed_tables)}"
        )
    
    try:
        # Get count before deletion
        result = db.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        count_before = result.fetchone()[0]
        
        # Delete all records (MySQL uses DELETE instead of TRUNCATE for better compatibility)
        db.execute(text(f"DELETE FROM {table_name}"))
        db.commit()
        
        logger.info(f"✅ Cleared table '{table_name}' ({count_before} records deleted)")
        
        return {
            "status": "success",
            "table": table_name,
            "records_deleted": count_before,
            "message": f"Successfully cleared {count_before} records from {table_name}"
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to clear table '{table_name}': {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# CHATBOX MANAGEMENT ENDPOINTS
# ============================================

@router.get("/chatbox/stats")
async def get_chatbox_stats(db: Session = Depends(get_db)):
    """
    Lấy thống kê về chatbox.
    
    Returns:
        - Tổng số tin nhắn
        - Số người dùng đã chat
        - Tin nhắn theo ngày
        - Top người dùng chat nhiều nhất
    """
    try:
        from sqlalchemy import func
        from datetime import datetime, timedelta
        
        # Tổng số tin nhắn
        total_messages = db.query(LichSuChat).count()
        
        # Số người dùng đã chat (không null)
        unique_users = db.query(func.count(func.distinct(LichSuChat.nguoi_dung_id)))\
            .filter(LichSuChat.nguoi_dung_id.isnot(None)).scalar()
        
        # Tin nhắn khách (guest)
        guest_messages = db.query(LichSuChat)\
            .filter(LichSuChat.nguoi_dung_id.is_(None)).count()
        
        # Tin nhắn 7 ngày gần đây
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_messages = db.query(LichSuChat)\
            .filter(LichSuChat.ngay_tao >= seven_days_ago).count()
        
        # Top 5 người dùng chat nhiều nhất
        top_users = db.query(
            NguoiDung.id,
            NguoiDung.ho_ten,
            NguoiDung.email,
            func.count(LichSuChat.id).label('message_count')
        ).join(LichSuChat, NguoiDung.id == LichSuChat.nguoi_dung_id)\
         .group_by(NguoiDung.id)\
         .order_by(func.count(LichSuChat.id).desc())\
         .limit(5).all()
        
        # Tin nhắn theo ngày (7 ngày gần đây)
        messages_by_day = db.query(
            func.date(LichSuChat.ngay_tao).label('date'),
            func.count(LichSuChat.id).label('count')
        ).filter(LichSuChat.ngay_tao >= seven_days_ago)\
         .group_by(func.date(LichSuChat.ngay_tao))\
         .order_by(func.date(LichSuChat.ngay_tao)).all()
        
        return {
            "status": "success",
            "total_messages": total_messages,
            "unique_users": unique_users,
            "guest_messages": guest_messages,
            "recent_messages_7days": recent_messages,
            "top_users": [
                {
                    "id": user.id,
                    "name": user.ho_ten or "N/A",
                    "email": user.email,
                    "message_count": user.message_count
                }
                for user in top_users
            ],
            "messages_by_day": [
                {
                    "date": str(day.date),
                    "count": day.count
                }
                for day in messages_by_day
            ]
        }
    except Exception as e:
        logger.error(f"Failed to get chatbox stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chatbox/history")
async def get_all_chat_history(
    skip: int = 0,
    limit: int = 50,
    user_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Lấy lịch sử chat của tất cả người dùng (cho admin).
    
    Args:
        skip: Số bản ghi bỏ qua
        limit: Số bản ghi tối đa
        user_id: Lọc theo ID người dùng (optional)
    """
    try:
        query = db.query(LichSuChat)
        
        if user_id:
            query = query.filter(LichSuChat.nguoi_dung_id == user_id)
        
        total = query.count()
        chats = query.order_by(LichSuChat.ngay_tao.desc())\
                    .offset(skip)\
                    .limit(limit)\
                    .all()
        
        # Lấy thông tin người dùng
        result = []
        for chat in chats:
            user_info = None
            if chat.nguoi_dung_id:
                user = db.query(NguoiDung).filter(NguoiDung.id == chat.nguoi_dung_id).first()
                if user:
                    user_info = {
                        "id": user.id,
                        "name": user.ho_ten,
                        "email": user.email
                    }
            
            result.append({
                "id": chat.id,
                "user": user_info or {"id": None, "name": "Khách", "email": "N/A"},
                "message": chat.tin_nhan,
                "response": chat.phan_hoi,
                "created_at": chat.ngay_tao.isoformat() if chat.ngay_tao else None
            })
        
        return {
            "status": "success",
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": result
        }
    except Exception as e:
        logger.error(f"Failed to get chat history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/chatbox/clear")
async def clear_chat_history(
    user_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Xóa lịch sử chat.
    
    Args:
        user_id: Nếu có, chỉ xóa chat của user này. Nếu không, xóa tất cả.
    
    ⚠️  CẢNH BÁO: Endpoint này sẽ XÓA DỮ LIỆU!
    """
    check_dev_environment()
    
    try:
        query = db.query(LichSuChat)
        
        if user_id:
            query = query.filter(LichSuChat.nguoi_dung_id == user_id)
            count = query.count()
            query.delete()
            db.commit()
            message = f"Đã xóa {count} tin nhắn của user ID {user_id}"
        else:
            count = query.count()
            query.delete()
            db.commit()
            message = f"Đã xóa toàn bộ {count} tin nhắn"
        
        logger.info(f"✅ {message}")
        
        return {
            "status": "success",
            "deleted_count": count,
            "message": message
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to clear chat history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chatbox/config")
async def get_chatbox_config():
    """
    Lấy cấu hình hiện tại của chatbox.
    
    Returns:
        - AI provider (openai/gemini)
        - API key status (có/không)
        - Environment variables
    """
    try:
        ai_provider = os.getenv("AI_PROVIDER", "openai")
        openai_key = os.getenv("OPENAI_API_KEY", "")
        gemini_key = os.getenv("GEMINI_API_KEY", "")
        
        return {
            "status": "success",
            "config": {
                "ai_provider": ai_provider,
                "openai_configured": bool(openai_key and len(openai_key) > 10),
                "gemini_configured": bool(gemini_key and len(gemini_key) > 10),
                "openai_key_preview": f"{openai_key[:10]}..." if openai_key else "Not set",
                "gemini_key_preview": f"{gemini_key[:10]}..." if gemini_key else "Not set",
            }
        }
    except Exception as e:
        logger.error(f"Failed to get chatbox config: {e}")
        raise HTTPException(status_code=500, detail=str(e))

"""
Reset Database Script
======================
Script để reset và seed lại toàn bộ database.

⚠️  CẢNH BÁO: Script này sẽ XÓA TOÀN BỘ DỮ LIỆU trong database!
Chỉ sử dụng trong môi trường development/testing.

Cách sử dụng:
    python reset_db.py

Hoặc từ Docker:
    docker exec -it electronics_backend python reset_db.py
"""
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import (
    engine, 
    SessionLocal, 
    Base,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    check_db_connection
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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print script banner"""
    print("\n" + "=" * 70)
    print("🔄 DATABASE RESET SCRIPT")
    print("=" * 70)
    print("⚠️  WARNING: This will DELETE ALL DATA in the database!")
    print("=" * 70 + "\n")


def verify_database_info():
    """Verify and display database connection info"""
    logger.info("📊 Database Connection Info:")
    logger.info(f"   Host: {DB_HOST}")
    logger.info(f"   Port: {DB_PORT}")
    logger.info(f"   Database: {DB_NAME}")
    logger.info(f"   User: {DB_USER}")
    logger.info("")
    
    # Check connection
    if not check_db_connection():
        logger.error("❌ Cannot connect to database!")
        logger.error("   Please check your database configuration and ensure MySQL is running.")
        return False
    
    return True


def get_current_tables():
    """Get list of current tables in database"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = '{DB_NAME}'
                ORDER BY table_name
            """))
            return [row[0] for row in result]
    except Exception as e:
        logger.error(f"❌ Failed to get table list: {e}")
        return []


def drop_all_tables():
    """Drop all tables from database"""
    logger.info("🗑️  Step 1: Dropping all existing tables...")
    
    try:
        # Get current tables before dropping
        tables_before = get_current_tables()
        if tables_before:
            logger.info(f"   Found {len(tables_before)} tables to drop:")
            for table in tables_before:
                logger.info(f"      - {table}")
        else:
            logger.info("   No tables found in database")
        
        # Drop all tables using SQLAlchemy metadata
        Base.metadata.drop_all(bind=engine)
        
        # Verify tables were dropped
        tables_after = get_current_tables()
        if not tables_after:
            logger.info("   ✅ All tables dropped successfully!")
        else:
            logger.warning(f"   ⚠️  Some tables still exist: {tables_after}")
        
        return True
    except Exception as e:
        logger.error(f"   ❌ Failed to drop tables: {e}")
        return False


def create_all_tables():
    """Create all tables in database"""
    logger.info("🔨 Step 2: Creating all tables...")
    
    try:
        # Log registered models
        logger.info(f"   Registered models ({len(Base.metadata.tables)} tables):")
        for table_name in sorted(Base.metadata.tables.keys()):
            logger.info(f"      - {table_name}")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Verify tables were created
        tables_created = get_current_tables()
        logger.info(f"   ✅ Created {len(tables_created)} tables:")
        for table in sorted(tables_created):
            logger.info(f"      - {table}")
        
        # Check if all expected tables exist
        expected_tables = {
            "nguoi_dung", "danh_muc", "san_pham",
            "don_hang", "chi_tiet_don_hang", "lich_su_chat"
        }
        missing = expected_tables - set(tables_created)
        if missing:
            logger.warning(f"   ⚠️  Missing tables: {missing}")
            return False
        
        return True
    except Exception as e:
        logger.error(f"   ❌ Failed to create tables: {e}")
        return False


def seed_initial_data():
    """Seed initial data into database"""
    logger.info("🌱 Step 3: Seeding initial data...")
    
    db = SessionLocal()
    try:
        # Seed categories
        logger.info("   📁 Seeding categories...")
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
            db.flush()  # Get ID without committing
            categories[cat_data["ten"]] = category.id
            logger.info(f"      ✅ {cat_data['ten']} (ID: {category.id})")
        
        db.commit()
        logger.info(f"   ✅ Seeded {len(categories)} categories")
        
        # Seed products
        logger.info("   📦 Seeding products...")
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
            logger.info(f"      ✅ {prod_data['ten']}")
        
        db.commit()
        logger.info(f"   ✅ Seeded {len(products_data)} products")
        
        return True
    except Exception as e:
        logger.error(f"   ❌ Failed to seed data: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def verify_final_state():
    """Verify final database state"""
    logger.info("🔍 Step 4: Verifying final state...")
    
    db = SessionLocal()
    try:
        # Count records
        cat_count = db.query(DanhMuc).count()
        prod_count = db.query(SanPham).count()
        user_count = db.query(NguoiDung).count()
        order_count = db.query(DonHang).count()
        
        logger.info("   📊 Database Statistics:")
        logger.info(f"      Categories: {cat_count}")
        logger.info(f"      Products: {prod_count}")
        logger.info(f"      Users: {user_count}")
        logger.info(f"      Orders: {order_count}")
        
        # Verify tables exist
        tables = get_current_tables()
        logger.info(f"   📋 Tables in database ({len(tables)}):")
        for table in sorted(tables):
            logger.info(f"      - {table}")
        
        return True
    except Exception as e:
        logger.error(f"   ❌ Verification failed: {e}")
        return False
    finally:
        db.close()


def main():
    """Main reset function"""
    print_banner()
    
    # Step 0: Verify database connection
    if not verify_database_info():
        logger.error("\n❌ Database reset aborted due to connection failure!")
        return False
    
    # Confirm action
    print("⚠️  You are about to DELETE ALL DATA from the database!")
    print(f"   Database: {DB_NAME}")
    print(f"   Host: {DB_HOST}:{DB_PORT}")
    print("")
    
    # Auto-confirm in Docker environment
    if os.getenv("DOCKER_ENV") or os.getenv("APP_ENV") == "development":
        logger.info("🐳 Running in Docker/Development environment - auto-confirming...")
        confirm = "yes"
    else:
        confirm = input("Type 'yes' to continue: ").strip().lower()
    
    if confirm != "yes":
        logger.info("❌ Reset cancelled by user")
        return False
    
    print("")
    logger.info("🚀 Starting database reset...")
    logger.info("")
    
    # Execute reset steps
    success = True
    
    # Step 1: Drop tables
    if not drop_all_tables():
        success = False
    
    print("")
    
    # Step 2: Create tables
    if success and not create_all_tables():
        success = False
    
    print("")
    
    # Step 3: Seed data
    if success and not seed_initial_data():
        success = False
    
    print("")
    
    # Step 4: Verify
    if success:
        verify_final_state()
    
    # Final result
    print("")
    print("=" * 70)
    if success:
        logger.info("✅ DATABASE RESET COMPLETED SUCCESSFULLY!")
        logger.info("")
        logger.info("🎉 Your database is now fresh and ready to use!")
        logger.info("📚 You can view the data in phpMyAdmin at http://localhost/phpmyadmin")
    else:
        logger.error("❌ DATABASE RESET FAILED!")
        logger.error("   Please check the errors above and try again.")
    print("=" * 70)
    print("")
    
    return success


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Reset cancelled by user (Ctrl+C)")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

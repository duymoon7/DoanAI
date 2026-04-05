"""
Seed initial data for the electronics e-commerce database.
This script populates categories and products.
"""
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, init_db
from app.models import DanhMuc, SanPham
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_categories(db: Session):
    """Seed product categories"""
    categories = [
        {"ten": "Điện thoại"},
        {"ten": "Laptop"},
        {"ten": "Tablet"},
        {"ten": "Phụ kiện"},
        {"ten": "Tai nghe"},
        {"ten": "Đồng hồ thông minh"},
    ]
    
    logger.info("🏷️  Seeding categories...")
    for cat_data in categories:
        existing = db.query(DanhMuc).filter(DanhMuc.ten == cat_data["ten"]).first()
        if not existing:
            category = DanhMuc(**cat_data)
            db.add(category)
            logger.info(f"   ✅ Added category: {cat_data['ten']}")
        else:
            logger.info(f"   ⏭️  Category already exists: {cat_data['ten']}")
    
    db.commit()
    logger.info("✅ Categories seeded successfully!")


def seed_products(db: Session):
    """Seed products"""
    # Get category IDs
    categories = {cat.ten: cat.id for cat in db.query(DanhMuc).all()}
    
    products = [
        # Điện thoại
        {
            "ten": "iPhone 15 Pro Max",
            "mo_ta": "iPhone 15 Pro Max 256GB - Titan tự nhiên",
            "gia": 29990000,
            "hinh_anh": "https://cdn.tgdd.vn/Products/Images/42/305658/iphone-15-pro-max-blue-thumbnew-600x600.jpg",
            "danh_muc_id": categories.get("Điện thoại"),
        },
        {
            "ten": "Samsung Galaxy S24 Ultra",
            "mo_ta": "Samsung Galaxy S24 Ultra 12GB 256GB",
            "gia": 27990000,
            "hinh_anh": "https://cdn.tgdd.vn/Products/Images/42/320721/samsung-galaxy-s24-ultra-grey-thumbnew-600x600.jpg",
            "danh_muc_id": categories.get("Điện thoại"),
        },
        {
            "ten": "Xiaomi 14 Ultra",
            "mo_ta": "Xiaomi 14 Ultra 16GB 512GB",
            "gia": 24990000,
            "hinh_anh": "https://cdn.tgdd.vn/Products/Images/42/322096/xiaomi-14-ultra-black-thumbnew-600x600.jpg",
            "danh_muc_id": categories.get("Điện thoại"),
        },
        # Laptop
        {
            "ten": "MacBook Pro 14 M3",
            "mo_ta": "MacBook Pro 14 inch M3 Pro 18GB 512GB",
            "gia": 52990000,
            "hinh_anh": "https://cdn.tgdd.vn/Products/Images/44/309016/macbook-pro-14-inch-m3-pro-2023-xam-thumbnew-600x600.jpg",
            "danh_muc_id": categories.get("Laptop"),
        },
        {
            "ten": "Dell XPS 15",
            "mo_ta": "Dell XPS 15 9530 i7 13700H 16GB 512GB RTX 4050",
            "gia": 45990000,
            "hinh_anh": "https://cdn.tgdd.vn/Products/Images/44/307214/dell-xps-15-9530-i7-nxl1sv001-thumb-600x600.jpg",
            "danh_muc_id": categories.get("Laptop"),
        },
        {
            "ten": "ASUS ROG Zephyrus G14",
            "mo_ta": "ASUS ROG Zephyrus G14 Ryzen 9 8945HS 32GB 1TB RTX 4060",
            "gia": 42990000,
            "hinh_anh": "https://cdn.tgdd.vn/Products/Images/44/321636/asus-rog-zephyrus-g14-ga403uv-qs096w-thumb-600x600.jpg",
            "danh_muc_id": categories.get("Laptop"),
        },
        # Tablet
        {
            "ten": "iPad Pro M2 11 inch",
            "mo_ta": "iPad Pro M2 11 inch WiFi 128GB",
            "gia": 21990000,
            "hinh_anh": "https://cdn.tgdd.vn/Products/Images/522/325514/ipad-pro-11-inch-m2-wifi-128gb-2024-xam-thumb-600x600.jpg",
            "danh_muc_id": categories.get("Tablet"),
        },
        {
            "ten": "Samsung Galaxy Tab S9",
            "mo_ta": "Samsung Galaxy Tab S9 11 inch WiFi 128GB",
            "gia": 18990000,
            "hinh_anh": "https://cdn.tgdd.vn/Products/Images/522/309816/samsung-galaxy-tab-s9-wifi-thumb-xam-600x600.jpg",
            "danh_muc_id": categories.get("Tablet"),
        },
        # Tai nghe
        {
            "ten": "AirPods Pro 2",
            "mo_ta": "Apple AirPods Pro 2 USB-C",
            "gia": 5990000,
            "hinh_anh": "https://cdn.tgdd.vn/Products/Images/54/325265/airpods-pro-2-usb-c-thumb-600x600.jpg",
            "danh_muc_id": categories.get("Tai nghe"),
        },
        {
            "ten": "Sony WH-1000XM5",
            "mo_ta": "Tai nghe Sony WH-1000XM5 chống ồn",
            "gia": 7990000,
            "hinh_anh": "https://cdn.tgdd.vn/Products/Images/54/289780/tai-nghe-bluetooth-sony-wh-1000xm5-den-thumb-1-600x600.jpg",
            "danh_muc_id": categories.get("Tai nghe"),
        },
        # Đồng hồ thông minh
        {
            "ten": "Apple Watch Series 9",
            "mo_ta": "Apple Watch Series 9 GPS 45mm",
            "gia": 10990000,
            "hinh_anh": "https://cdn.tgdd.vn/Products/Images/7077/309732/apple-watch-s9-gps-45mm-vien-nhom-day-cao-su-thumb-xanh-duong-600x600.jpg",
            "danh_muc_id": categories.get("Đồng hồ thông minh"),
        },
        {
            "ten": "Samsung Galaxy Watch 6",
            "mo_ta": "Samsung Galaxy Watch 6 LTE 44mm",
            "gia": 7990000,
            "hinh_anh": "https://cdn.tgdd.vn/Products/Images/7077/309733/samsung-galaxy-watch-6-lte-44mm-thumb-xam-600x600.jpg",
            "danh_muc_id": categories.get("Đồng hồ thông minh"),
        },
        # Phụ kiện
        {
            "ten": "Sạc nhanh Apple 20W",
            "mo_ta": "Adapter sạc Apple 20W USB-C",
            "gia": 490000,
            "hinh_anh": "https://cdn.tgdd.vn/Products/Images/58/228716/adapter-sac-type-c-pd-20w-apple-mhje3-thumb-600x600.jpg",
            "danh_muc_id": categories.get("Phụ kiện"),
        },
        {
            "ten": "Cáp sạc Type-C to Lightning",
            "mo_ta": "Cáp sạc Apple Type-C to Lightning 1m",
            "gia": 390000,
            "hinh_anh": "https://cdn.tgdd.vn/Products/Images/58/228715/cap-type-c-lightning-1m-apple-mqgj2-thumb-600x600.jpg",
            "danh_muc_id": categories.get("Phụ kiện"),
        },
    ]
    
    logger.info("📦 Seeding products...")
    for prod_data in products:
        existing = db.query(SanPham).filter(SanPham.ten == prod_data["ten"]).first()
        if not existing:
            product = SanPham(**prod_data)
            db.add(product)
            logger.info(f"   ✅ Added product: {prod_data['ten']}")
        else:
            logger.info(f"   ⏭️  Product already exists: {prod_data['ten']}")
    
    db.commit()
    logger.info("✅ Products seeded successfully!")


def main():
    """Main seeding function"""
    logger.info("=" * 60)
    logger.info("🌱 Starting database seeding...")
    logger.info("=" * 60)
    
    try:
        # Initialize database tables
        logger.info("🔧 Initializing database tables...")
        init_db()
        
        # Create database session
        db = SessionLocal()
        
        try:
            # Seed data
            seed_categories(db)
            seed_products(db)
            
            # Verify data
            cat_count = db.query(DanhMuc).count()
            prod_count = db.query(SanPham).count()
            
            logger.info("=" * 60)
            logger.info("✅ Database seeding completed successfully!")
            logger.info(f"📊 Total categories: {cat_count}")
            logger.info(f"📦 Total products: {prod_count}")
            logger.info("=" * 60)
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"❌ Seeding failed: {e}")
        raise


if __name__ == "__main__":
    main()

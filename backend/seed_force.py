#!/usr/bin/env python3
"""
Force seed database with sample data (no confirmation)
"""

import logging
from app.database import SessionLocal
from app.models import (
    NguoiDung, DanhMuc, SanPham,
    DonHang, ChiTietDonHang, LichSuChat
)
from app.models.nguoi_dung import VaiTro
from app.models.don_hang import TrangThai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_database():
    """Seed database with sample data (force mode)"""
    db = SessionLocal()
    
    try:
        logger.info("=" * 60)
        logger.info("🌱 FORCE SEEDING DATABASE WITH SAMPLE DATA")
        logger.info("=" * 60)
        
        # Clear existing data
        logger.info("🗑️  Clearing existing data...")
        db.query(ChiTietDonHang).delete()
        db.query(LichSuChat).delete()
        db.query(DonHang).delete()
        db.query(SanPham).delete()
        db.query(DanhMuc).delete()
        db.query(NguoiDung).delete()
        db.commit()
        logger.info("✅ Existing data cleared")
        
        # 1. Create Users
        logger.info("\n👥 Creating users...")
        users = [
            NguoiDung(
                email="admin@electronics.com",
                mat_khau="admin123",  # In production, use hashed passwords
                vai_tro=VaiTro.ADMIN
            ),
            NguoiDung(
                email="user1@example.com",
                mat_khau="user123",
                vai_tro=VaiTro.USER
            ),
            NguoiDung(
                email="user2@example.com",
                mat_khau="user123",
                vai_tro=VaiTro.USER
            ),
        ]
        
        for user in users:
            db.add(user)
        db.commit()
        logger.info(f"✅ Created {len(users)} users")
        
        # 2. Create Categories
        logger.info("\n📁 Creating categories...")
        categories = [
            DanhMuc(ten="Dien thoai"),
            DanhMuc(ten="Laptop"),
            DanhMuc(ten="Tai nghe"),
            DanhMuc(ten="Phu kien"),
        ]
        
        for category in categories:
            db.add(category)
        db.commit()
        
        # Refresh to get IDs
        for category in categories:
            db.refresh(category)
        
        logger.info(f"✅ Created {len(categories)} categories")
        
        # 3. Create Products
        logger.info("\n📦 Creating products...")
        products = [
            # Điện thoại
            SanPham(
                ten="iPhone 15 Pro Max",
                gia=1299.99,
                mo_ta="Latest iPhone with A17 Pro chip",
                hinh_anh="https://example.com/iphone15.jpg",
                danh_muc_id=categories[0].id
            ),
            SanPham(
                ten="Samsung Galaxy S24 Ultra",
                gia=1199.99,
                mo_ta="Flagship Samsung phone with S Pen",
                hinh_anh="https://example.com/s24.jpg",
                danh_muc_id=categories[0].id
            ),
            SanPham(
                ten="Google Pixel 8 Pro",
                gia=999.99,
                mo_ta="Google's flagship with AI features",
                hinh_anh="https://example.com/pixel8.jpg",
                danh_muc_id=categories[0].id
            ),
            # Laptop
            SanPham(
                ten="MacBook Pro 16 M3",
                gia=2499.99,
                mo_ta="Powerful laptop for professionals",
                hinh_anh="https://example.com/macbook.jpg",
                danh_muc_id=categories[1].id
            ),
            SanPham(
                ten="Dell XPS 15",
                gia=1799.99,
                mo_ta="Premium Windows laptop",
                hinh_anh="https://example.com/xps15.jpg",
                danh_muc_id=categories[1].id
            ),
            SanPham(
                ten="Lenovo ThinkPad X1 Carbon",
                gia=1599.99,
                mo_ta="Business laptop with great keyboard",
                hinh_anh="https://example.com/thinkpad.jpg",
                danh_muc_id=categories[1].id
            ),
            # Tai nghe
            SanPham(
                ten="AirPods Pro 2",
                gia=249.99,
                mo_ta="Premium wireless earbuds",
                hinh_anh="https://example.com/airpods.jpg",
                danh_muc_id=categories[2].id
            ),
            SanPham(
                ten="Sony WH-1000XM5",
                gia=399.99,
                mo_ta="Best noise cancelling headphones",
                hinh_anh="https://example.com/sony.jpg",
                danh_muc_id=categories[2].id
            ),
            # Phụ kiện
            SanPham(
                ten="USB-C Cable 2m",
                gia=19.99,
                mo_ta="Fast charging cable",
                hinh_anh="https://example.com/cable.jpg",
                danh_muc_id=categories[3].id
            ),
            SanPham(
                ten="Wireless Charger",
                gia=39.99,
                mo_ta="15W fast wireless charging",
                hinh_anh="https://example.com/charger.jpg",
                danh_muc_id=categories[3].id
            ),
        ]
        
        for product in products:
            db.add(product)
        db.commit()
        
        # Refresh to get IDs
        for product in products:
            db.refresh(product)
        
        logger.info(f"✅ Created {len(products)} products")
        
        # 4. Create Orders
        logger.info("\n🛒 Creating orders...")
        orders = [
            DonHang(
                nguoi_dung_id=users[1].id,  # user1
                tong_tien=1549.98,  # iPhone + AirPods
                trang_thai=TrangThai.COMPLETED
            ),
            DonHang(
                nguoi_dung_id=users[2].id,  # user2
                tong_tien=2499.99,  # MacBook
                trang_thai=TrangThai.PENDING
            ),
            DonHang(
                nguoi_dung_id=users[1].id,  # user1
                tong_tien=59.98,  # Cable + Charger
                trang_thai=TrangThai.COMPLETED
            ),
        ]
        
        for order in orders:
            db.add(order)
        db.commit()
        
        # Refresh to get IDs
        for order in orders:
            db.refresh(order)
        
        logger.info(f"✅ Created {len(orders)} orders")
        
        # 5. Create Order Items
        logger.info("\n📋 Creating order items...")
        order_items = [
            # Order 1: iPhone + AirPods
            ChiTietDonHang(don_hang_id=orders[0].id, san_pham_id=products[0].id, so_luong=1),  # iPhone
            ChiTietDonHang(don_hang_id=orders[0].id, san_pham_id=products[6].id, so_luong=1),  # AirPods
            # Order 2: MacBook
            ChiTietDonHang(don_hang_id=orders[1].id, san_pham_id=products[3].id, so_luong=1),  # MacBook
            # Order 3: Accessories
            ChiTietDonHang(don_hang_id=orders[2].id, san_pham_id=products[8].id, so_luong=1),  # Cable
            ChiTietDonHang(don_hang_id=orders[2].id, san_pham_id=products[9].id, so_luong=1),  # Charger
        ]
        
        for item in order_items:
            db.add(item)
        db.commit()
        logger.info(f"✅ Created {len(order_items)} order items")
        
        # 6. Create Chat History
        logger.info("\n💬 Creating chat history...")
        chats = [
            LichSuChat(
                nguoi_dung_id=users[1].id,
                cau_hoi="What is the best phone under $1000?",
                cau_tra_loi="The Google Pixel 8 Pro is an excellent choice at $999.99 with great AI features and camera."
            ),
            LichSuChat(
                nguoi_dung_id=users[1].id,
                cau_hoi="Do you have wireless chargers?",
                cau_tra_loi="Yes! We have a 15W fast wireless charger for $39.99."
            ),
            LichSuChat(
                nguoi_dung_id=users[2].id,
                cau_hoi="Which laptop is best for programming?",
                cau_tra_loi="The MacBook Pro 16 M3 or Lenovo ThinkPad X1 Carbon are both excellent for programming."
            ),
        ]
        
        for chat in chats:
            db.add(chat)
        db.commit()
        logger.info(f"✅ Created {len(chats)} chat messages")
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("✅ DATABASE SEEDING COMPLETED!")
        logger.info("=" * 60)
        logger.info("\n📊 Summary:")
        logger.info(f"   👥 Users: {len(users)}")
        logger.info(f"   📁 Categories: {len(categories)}")
        logger.info(f"   📦 Products: {len(products)}")
        logger.info(f"   🛒 Orders: {len(orders)}")
        logger.info(f"   📋 Order Items: {len(order_items)}")
        logger.info(f"   💬 Chat Messages: {len(chats)}")
        logger.info("\n🎉 You can now test the API!")
        logger.info("   Start server: python run.py")
        logger.info("   API Docs: http://localhost:8000/docs")
        logger.info("=" * 60)
        
    except Exception as e:
        db.rollback()
        logger.error(f"\n❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

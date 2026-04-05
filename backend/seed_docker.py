"""
Seed script for Docker environment
Auto-seeds database with sample data on startup
"""
import logging
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models import NguoiDung, DanhMuc, SanPham, DonHang, ChiTietDonHang

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_data():
    """Seed database with sample data"""
    db = SessionLocal()
    
    try:
        logger.info("🌱 Starting database seeding...")
        
        # Check if data already exists
        existing_categories = db.query(DanhMuc).count()
        if existing_categories > 0:
            logger.info("✅ Database already seeded. Skipping...")
            return
        
        # Create categories
        logger.info("📦 Creating categories...")
        categories = [
            DanhMuc(ten="Dien thoai"),
            DanhMuc(ten="Laptop"),
            DanhMuc(ten="Tai nghe"),
            DanhMuc(ten="Phu kien"),
        ]
        db.add_all(categories)
        db.commit()
        logger.info(f"✅ Created {len(categories)} categories")
        
        # Refresh to get IDs
        for cat in categories:
            db.refresh(cat)
        
        # Create users
        logger.info("👥 Creating users...")
        users = [
            NguoiDung(
                email="admin@electronics.com",
                mat_khau="hashed_admin_password",
                vai_tro="admin"
            ),
            NguoiDung(
                email="user1@example.com",
                mat_khau="hashed_user_password",
                vai_tro="user"
            ),
            NguoiDung(
                email="user2@example.com",
                mat_khau="hashed_user_password",
                vai_tro="user"
            ),
        ]
        db.add_all(users)
        db.commit()
        logger.info(f"✅ Created {len(users)} users")
        
        # Refresh users
        for user in users:
            db.refresh(user)
        
        # Create products
        logger.info("📱 Creating products...")
        products = [
            # Phones
            SanPham(
                ten="iPhone 15 Pro Max",
                gia=1299.99,
                mo_ta="Latest iPhone with A17 Pro chip, titanium design, and advanced camera system",
                hinh_anh="https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=500",
                danh_muc_id=categories[0].id
            ),
            SanPham(
                ten="Samsung Galaxy S24 Ultra",
                gia=1199.99,
                mo_ta="Flagship Samsung phone with S Pen, 200MP camera, and AI features",
                hinh_anh="https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=500",
                danh_muc_id=categories[0].id
            ),
            SanPham(
                ten="Google Pixel 8 Pro",
                gia=999.99,
                mo_ta="Google's flagship with advanced AI, excellent camera, and pure Android",
                hinh_anh="https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500",
                danh_muc_id=categories[0].id
            ),
            # Laptops
            SanPham(
                ten="MacBook Pro 16 M3",
                gia=2499.99,
                mo_ta="Powerful MacBook Pro with M3 chip, 16-inch Liquid Retina XDR display",
                hinh_anh="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500",
                danh_muc_id=categories[1].id
            ),
            SanPham(
                ten="Dell XPS 15",
                gia=1799.99,
                mo_ta="Premium Windows laptop with InfinityEdge display and powerful performance",
                hinh_anh="https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500",
                danh_muc_id=categories[1].id
            ),
            SanPham(
                ten="Lenovo ThinkPad X1 Carbon",
                gia=1599.99,
                mo_ta="Business ultrabook with legendary keyboard and military-grade durability",
                hinh_anh="https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500",
                danh_muc_id=categories[1].id
            ),
            # Headphones
            SanPham(
                ten="AirPods Pro 2",
                gia=249.99,
                mo_ta="Premium wireless earbuds with active noise cancellation and spatial audio",
                hinh_anh="https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=500",
                danh_muc_id=categories[2].id
            ),
            SanPham(
                ten="Sony WH-1000XM5",
                gia=399.99,
                mo_ta="Industry-leading noise canceling headphones with exceptional sound quality",
                hinh_anh="https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=500",
                danh_muc_id=categories[2].id
            ),
            # Accessories
            SanPham(
                ten="USB-C Cable 2m",
                gia=19.99,
                mo_ta="High-quality braided USB-C cable with fast charging support",
                hinh_anh="https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=500",
                danh_muc_id=categories[3].id
            ),
            SanPham(
                ten="Wireless Charger",
                gia=39.99,
                mo_ta="Fast wireless charging pad compatible with all Qi-enabled devices",
                hinh_anh="https://images.unsplash.com/photo-1591290619762-c588f0e8e23f?w=500",
                danh_muc_id=categories[3].id
            ),
        ]
        db.add_all(products)
        db.commit()
        logger.info(f"✅ Created {len(products)} products")
        
        # Refresh products
        for product in products:
            db.refresh(product)
        
        # Create sample orders
        logger.info("🛒 Creating sample orders...")
        orders = [
            DonHang(
                nguoi_dung_id=users[1].id,
                tong_tien=1549.98,
                trang_thai="completed"
            ),
            DonHang(
                nguoi_dung_id=users[2].id,
                tong_tien=2499.99,
                trang_thai="pending"
            ),
            DonHang(
                nguoi_dung_id=users[1].id,
                tong_tien=59.98,
                trang_thai="completed"
            ),
        ]
        db.add_all(orders)
        db.commit()
        logger.info(f"✅ Created {len(orders)} orders")
        
        # Refresh orders
        for order in orders:
            db.refresh(order)
        
        # Create order items
        logger.info("📦 Creating order items...")
        order_items = [
            # Order 1: iPhone + AirPods
            ChiTietDonHang(
                don_hang_id=orders[0].id,
                san_pham_id=products[0].id,
                so_luong=1
            ),
            ChiTietDonHang(
                don_hang_id=orders[0].id,
                san_pham_id=products[6].id,
                so_luong=1
            ),
            # Order 2: MacBook
            ChiTietDonHang(
                don_hang_id=orders[1].id,
                san_pham_id=products[3].id,
                so_luong=1
            ),
            # Order 3: Accessories
            ChiTietDonHang(
                don_hang_id=orders[2].id,
                san_pham_id=products[8].id,
                so_luong=1
            ),
            ChiTietDonHang(
                don_hang_id=orders[2].id,
                san_pham_id=products[9].id,
                so_luong=1
            ),
        ]
        db.add_all(order_items)
        db.commit()
        logger.info(f"✅ Created {len(order_items)} order items")
        
        logger.info("=" * 60)
        logger.info("🎉 Database seeding completed successfully!")
        logger.info("=" * 60)
        logger.info(f"📊 Summary:")
        logger.info(f"   - Categories: {len(categories)}")
        logger.info(f"   - Users: {len(users)}")
        logger.info(f"   - Products: {len(products)}")
        logger.info(f"   - Orders: {len(orders)}")
        logger.info(f"   - Order Items: {len(order_items)}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # Initialize database tables
    init_db()
    
    # Seed data
    seed_data()

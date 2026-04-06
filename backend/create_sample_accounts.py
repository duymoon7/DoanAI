"""
Script để tạo các tài khoản mẫu
"""
from app.database import SessionLocal
from app.models import NguoiDung
from app.auth import get_password_hash

def create_sample_accounts():
    db = SessionLocal()
    
    accounts = [
        {
            "email": "admin@aishop.com",
            "password": "admin123",
            "ho_ten": "Admin System",
            "vai_tro": "admin"
        },
        {
            "email": "manager@aishop.com",
            "password": "manager123",
            "ho_ten": "Quản lý hệ thống",
            "vai_tro": "manager"
        },
        {
            "email": "user@aishop.com",
            "password": "user123",
            "ho_ten": "Người dùng mẫu",
            "vai_tro": "user"
        }
    ]
    
    try:
        created = 0
        skipped = 0
        
        for acc in accounts:
            # Kiểm tra xem tài khoản đã tồn tại chưa
            existing = db.query(NguoiDung).filter(NguoiDung.email == acc["email"]).first()
            
            if existing:
                print(f"⏭️  Bỏ qua: {acc['email']} (đã tồn tại)")
                skipped += 1
                continue
            
            # Tạo tài khoản mới
            user = NguoiDung(
                email=acc["email"],
                mat_khau=get_password_hash(acc["password"]),
                ho_ten=acc["ho_ten"],
                vai_tro=acc["vai_tro"]
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            print(f"✅ Đã tạo: {acc['email']} ({acc['vai_tro']})")
            created += 1
        
        print("\n" + "=" * 60)
        print(f"📊 Kết quả:")
        print(f"   Đã tạo: {created}")
        print(f"   Bỏ qua: {skipped}")
        print("=" * 60)
        
        if created > 0:
            print("\n🔑 Thông tin đăng nhập:")
            print("-" * 60)
            for acc in accounts:
                print(f"   {acc['vai_tro'].upper()}")
                print(f"   Email: {acc['email']}")
                print(f"   Password: {acc['password']}")
                print("-" * 60)
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("TẠO TÀI KHOẢN MẪU")
    print("=" * 60)
    create_sample_accounts()

"""
Script để migrate database - thêm các cột mới
Chạy script này để cập nhật database với các trường mới
"""
from sqlalchemy import create_engine, text
from app.database import DATABASE_URL
import sys

def migrate_database():
    """Thêm các cột mới vào database"""
    engine = create_engine(DATABASE_URL)
    
    migrations = [
        # Bảng nguoi_dung
        "ALTER TABLE nguoi_dung ADD COLUMN IF NOT EXISTS dia_chi TEXT NULL",
        "ALTER TABLE nguoi_dung ADD COLUMN IF NOT EXISTS avatar VARCHAR(500) NULL",
        "ALTER TABLE nguoi_dung ADD COLUMN IF NOT EXISTS ngay_cap_nhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
        
        # Bảng san_pham
        "ALTER TABLE san_pham ADD COLUMN IF NOT EXISTS ton_kho INT NOT NULL DEFAULT 0",
        "ALTER TABLE san_pham ADD COLUMN IF NOT EXISTS trang_thai VARCHAR(20) NOT NULL DEFAULT 'active'",
        "ALTER TABLE san_pham ADD COLUMN IF NOT EXISTS ngay_cap_nhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
        
        # Bảng don_hang
        "ALTER TABLE don_hang ADD COLUMN IF NOT EXISTS ten_nguoi_nhan VARCHAR(255) NULL",
        "ALTER TABLE don_hang ADD COLUMN IF NOT EXISTS so_dien_thoai_nguoi_nhan VARCHAR(20) NULL",
        "ALTER TABLE don_hang ADD COLUMN IF NOT EXISTS dia_chi_giao_hang TEXT NULL",
        "ALTER TABLE don_hang ADD COLUMN IF NOT EXISTS ghi_chu TEXT NULL",
        "ALTER TABLE don_hang ADD COLUMN IF NOT EXISTS ma_giam_gia_id INT NULL",
        "ALTER TABLE don_hang ADD COLUMN IF NOT EXISTS so_tien_giam DECIMAL(10,2) NOT NULL DEFAULT 0",
        "ALTER TABLE don_hang ADD COLUMN IF NOT EXISTS ngay_cap_nhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
        
        # Thêm foreign key cho ma_giam_gia_id
        """
        ALTER TABLE don_hang 
        ADD CONSTRAINT fk_don_hang_ma_giam_gia 
        FOREIGN KEY (ma_giam_gia_id) 
        REFERENCES ma_giam_gia(id) 
        ON DELETE SET NULL
        """,
        
        # Thêm indexes
        "CREATE INDEX IF NOT EXISTS idx_san_pham_trang_thai ON san_pham(trang_thai)",
        "CREATE INDEX IF NOT EXISTS idx_don_hang_ma_giam_gia ON don_hang(ma_giam_gia_id)",
    ]
    
    print("🚀 Bắt đầu migration database...")
    
    with engine.connect() as conn:
        for i, migration in enumerate(migrations, 1):
            try:
                print(f"[{i}/{len(migrations)}] Đang thực thi: {migration[:80]}...")
                conn.execute(text(migration))
                conn.commit()
                print(f"✅ Thành công!")
            except Exception as e:
                error_msg = str(e)
                # Bỏ qua lỗi nếu cột/index đã tồn tại
                if "Duplicate column" in error_msg or "already exists" in error_msg:
                    print(f"⚠️  Đã tồn tại, bỏ qua")
                else:
                    print(f"❌ Lỗi: {error_msg}")
                    if "foreign key" not in error_msg.lower():
                        print("⚠️  Tiếp tục với migration tiếp theo...")
    
    print("\n✨ Migration hoàn tất!")
    print("\n📋 CÁC TRƯỜNG MỚI ĐÃ THÊM:")
    print("\n1. Bảng nguoi_dung:")
    print("   - dia_chi: Địa chỉ mặc định")
    print("   - avatar: URL ảnh đại diện")
    print("   - ngay_cap_nhat: Ngày cập nhật")
    
    print("\n2. Bảng san_pham:")
    print("   - ton_kho: Số lượng tồn kho")
    print("   - trang_thai: active/inactive")
    print("   - ngay_cap_nhat: Ngày cập nhật")
    
    print("\n3. Bảng don_hang:")
    print("   - ten_nguoi_nhan: Tên người nhận")
    print("   - so_dien_thoai_nguoi_nhan: SĐT người nhận")
    print("   - dia_chi_giao_hang: Địa chỉ giao hàng")
    print("   - ghi_chu: Ghi chú đơn hàng")
    print("   - ma_giam_gia_id: ID mã giảm giá")
    print("   - so_tien_giam: Số tiền được giảm")
    print("   - ngay_cap_nhat: Ngày cập nhật")
    
    print("\n⚠️  LƯU Ý:")
    print("- Các trường mới đều cho phép NULL hoặc có giá trị mặc định")
    print("- Dữ liệu cũ không bị ảnh hưởng")
    print("- Cần cập nhật API schemas và frontend để sử dụng các trường mới")

if __name__ == "__main__":
    try:
        migrate_database()
    except Exception as e:
        print(f"\n❌ LỖI NGHIÊM TRỌNG: {e}")
        sys.exit(1)

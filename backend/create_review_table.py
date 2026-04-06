"""
Script để tạo bảng đánh giá và thêm dữ liệu mẫu
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models.base import Base
from app.models import DanhGia, NguoiDung, SanPham
import random

def create_table():
    """Tạo bảng danh_gia"""
    print("=" * 60)
    print("TẠO BẢNG ĐÁNH GIÁ")
    print("=" * 60)
    
    try:
        # Tạo bảng
        Base.metadata.create_all(bind=engine)
        print("✅ Đã tạo bảng danh_gia")
        
        # Thêm dữ liệu mẫu
        db = SessionLocal()
        try:
            # Lấy danh sách user và sản phẩm
            users = db.query(NguoiDung).filter(NguoiDung.vai_tro == "user").all()
            products = db.query(SanPham).all()
            
            if not users:
                print("⚠️  Không có user nào trong database")
                return
            
            if not products:
                print("⚠️  Không có sản phẩm nào trong database")
                return
            
            # Tạo đánh giá mẫu
            reviews_data = [
                {"diem_so": 5, "binh_luan": "Sản phẩm rất tốt, đáng tiền!"},
                {"diem_so": 4, "binh_luan": "Chất lượng ổn, giao hàng nhanh"},
                {"diem_so": 5, "binh_luan": "Tuyệt vời, sẽ mua lại lần sau"},
                {"diem_so": 3, "binh_luan": "Tạm được, giá hơi cao"},
                {"diem_so": 4, "binh_luan": "Sản phẩm đẹp, đóng gói cẩn thận"},
                {"diem_so": 5, "binh_luan": "Rất hài lòng với sản phẩm này"},
                {"diem_so": 4, "binh_luan": "Chất lượng tốt, ship nhanh"},
                {"diem_so": 5, "binh_luan": "Sản phẩm chính hãng, giá tốt"},
            ]
            
            added = 0
            # Tạo 2-3 đánh giá cho mỗi sản phẩm
            for product in products[:10]:  # Chỉ tạo cho 10 sản phẩm đầu
                num_reviews = random.randint(2, 3)
                selected_users = random.sample(users, min(num_reviews, len(users)))
                
                for user in selected_users:
                    # Kiểm tra đã đánh giá chưa
                    existing = db.query(DanhGia).filter(
                        DanhGia.nguoi_dung_id == user.id,
                        DanhGia.san_pham_id == product.id
                    ).first()
                    
                    if not existing:
                        review_data = random.choice(reviews_data)
                        review = DanhGia(
                            nguoi_dung_id=user.id,
                            san_pham_id=product.id,
                            diem_so=review_data["diem_so"],
                            binh_luan=review_data["binh_luan"]
                        )
                        db.add(review)
                        added += 1
            
            db.commit()
            
            total = db.query(DanhGia).count()
            print(f"\n✅ Đã thêm {added} đánh giá mới")
            print(f"📊 Tổng số đánh giá: {total}")
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_table()

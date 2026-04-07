# -*- coding: utf-8 -*-
"""
Script seed du lieu danh gia mau
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import random
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root@localhost/electronics_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Du lieu mau
SAMPLE_REVIEWS = [
    {"diem_so": 5, "binh_luan": "San pham rat tot, dang tien! Giao hang nhanh, dong goi can than."},
    {"diem_so": 4, "binh_luan": "Chat luong on, giao hang nhanh. San pham dung nhu mo ta."},
    {"diem_so": 5, "binh_luan": "Tuyet voi, se mua lai lan sau. Shop phuc vu nhiet tinh!"},
    {"diem_so": 5, "binh_luan": "San pham chat luong cao, gia ca hop ly. Rat dang mua!"},
    {"diem_so": 4, "binh_luan": "Tot, nhung gia hoi cao mot chut. Nhin chung van hai long."},
    {"diem_so": 5, "binh_luan": "Minh rat thich san pham nay. Chat luong tuyet voi."},
    {"diem_so": 3, "binh_luan": "San pham tam on, khong co gi dac biet."},
    {"diem_so": 4, "binh_luan": "Dong goi can than, san pham dep. Gia hop ly."},
    {"diem_so": 5, "binh_luan": "Xuat sac! Vuot mong doi cua minh. Se gioi thieu cho ban be."},
    {"diem_so": 4, "binh_luan": "San pham tot, giao hang dung hen. Recommend!"},
    {"diem_so": 5, "binh_luan": "Chat luong nhu mo ta, rat hai long. Shop uy tin!"},
    {"diem_so": 3, "binh_luan": "Binh thuong, khong co gi noi bat."},
    {"diem_so": 4, "binh_luan": "Tot, dang gia tien. Se mua lai neu can."},
    {"diem_so": 5, "binh_luan": "Rat hai long voi san pham. Chat luong tot, gia ca phai chang."},
    {"diem_so": 2, "binh_luan": "Khong nhu mong doi. Chat luong chua tot lam."},
]

def seed_reviews():
    """Seed du lieu danh gia"""
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("SEED DU LIEU DANH GIA")
        print("=" * 80)
        
        # Lay danh sach nguoi dung
        users = db.execute(text("SELECT id FROM nguoi_dung")).fetchall()
        if not users:
            print("Khong co nguoi dung nao trong database!")
            print("Chay script: python create_sample_accounts.py")
            return
        
        user_ids = [user[0] for user in users]
        print(f"Tim thay {len(user_ids)} nguoi dung")
        
        # Lay danh sach san pham
        products = db.execute(text("SELECT id, ten FROM san_pham")).fetchall()
        if not products:
            print("Khong co san pham nao trong database!")
            return
        
        print(f"Tim thay {len(products)} san pham")
        
        # Xoa danh gia cu (neu co)
        confirm = input("\nBan co muon xoa danh gia cu va tao moi? (yes/no): ")
        if confirm.lower() == 'yes':
            db.execute(text("DELETE FROM danh_gia"))
            db.commit()
            print("Da xoa danh gia cu")
        
        # Tao danh gia cho moi san pham
        total_reviews = 0
        
        for product_id, product_name in products:
            # Moi san pham co 3-8 danh gia ngau nhien
            num_reviews = random.randint(3, 8)
            
            # Chon ngau nhien nguoi dung (khong trung)
            selected_users = random.sample(user_ids, min(num_reviews, len(user_ids)))
            
            for user_id in selected_users:
                # Chon ngau nhien mot danh gia
                review_data = random.choice(SAMPLE_REVIEWS)
                
                # Ngay tao ngau nhien trong 30 ngay qua
                days_ago = random.randint(1, 30)
                ngay_tao = datetime.now() - timedelta(days=days_ago)
                
                # Insert danh gia
                db.execute(text("""
                    INSERT INTO danh_gia (nguoi_dung_id, san_pham_id, diem_so, binh_luan, ngay_tao)
                    VALUES (:nguoi_dung_id, :san_pham_id, :diem_so, :binh_luan, :ngay_tao)
                """), {
                    "nguoi_dung_id": user_id,
                    "san_pham_id": product_id,
                    "diem_so": review_data["diem_so"],
                    "binh_luan": review_data["binh_luan"],
                    "ngay_tao": ngay_tao
                })
                
                total_reviews += 1
            
            if total_reviews <= 10:
                print(f"+ {product_name[:50]:<50} - {num_reviews} danh gia")
        
        db.commit()
        
        print("\n" + "=" * 80)
        print(f"+ Da tao {total_reviews} danh gia cho {len(products)} san pham!")
        print("=" * 80)
        
        # Thong ke
        print("\nThong ke:")
        result = db.execute(text("""
            SELECT 
                COUNT(*) as total,
                AVG(diem_so) as avg_rating,
                MIN(diem_so) as min_rating,
                MAX(diem_so) as max_rating
            FROM danh_gia
        """)).fetchone()
        
        print(f"- Tong danh gia: {result[0]}")
        print(f"- Diem trung binh: {result[1]:.2f}")
        print(f"- Diem thap nhat: {result[2]}")
        print(f"- Diem cao nhat: {result[3]}")
        
        # Phan bo theo sao
        print("\nPhan bo theo so sao:")
        for star in range(5, 0, -1):
            count = db.execute(text("""
                SELECT COUNT(*) FROM danh_gia 
                WHERE diem_so >= :star AND diem_so < :star_plus_1
            """), {"star": star, "star_plus_1": star + 1}).scalar()
            
            percentage = (count / result[0] * 100) if result[0] > 0 else 0
            bar = "#" * int(percentage / 2)
            print(f"{star} sao: {bar:<50} {count:>4} ({percentage:.1f}%)")
        
    except Exception as e:
        print(f"Loi: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_reviews()

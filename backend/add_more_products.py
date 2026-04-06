"""
Script để thêm nhiều sản phẩm hơn cho các danh mục
"""
from app.database import SessionLocal
from app.models import SanPham, DanhMuc
from decimal import Decimal

def add_products():
    db = SessionLocal()
    
    try:
        # Lấy danh mục
        categories = {cat.ten: cat.id for cat in db.query(DanhMuc).all()}
        
        products = [
            # Điện thoại (10 sản phẩm)
            {"ten": "iPhone 15 Pro Max 256GB", "gia": 29990000, "danh_muc": "Điện thoại", "mo_ta": "Chip A17 Pro, Camera 48MP, Titanium", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/42/305658/iphone-15-pro-max-blue-thumbnew-600x600.jpg"},
            {"ten": "iPhone 14 Pro 128GB", "gia": 24990000, "danh_muc": "Điện thoại", "mo_ta": "Chip A16 Bionic, Dynamic Island", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/42/289700/iphone-14-pro-purple-1-600x600.jpg"},
            {"ten": "Samsung Galaxy S24 Ultra", "gia": 31990000, "danh_muc": "Điện thoại", "mo_ta": "Snapdragon 8 Gen 3, S Pen, Camera 200MP", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/42/320721/samsung-galaxy-s24-ultra-grey-thumbnew-600x600.jpg"},
            {"ten": "Samsung Galaxy S23 FE", "gia": 14990000, "danh_muc": "Điện thoại", "mo_ta": "Snapdragon 8 Gen 1, Camera 50MP", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/42/316771/samsung-galaxy-s23-fe-mint-thumbnew-600x600.jpg"},
            {"ten": "Xiaomi 14 Ultra", "gia": 27990000, "danh_muc": "Điện thoại", "mo_ta": "Snapdragon 8 Gen 3, Camera Leica", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/42/322096/xiaomi-14-ultra-black-thumbnew-600x600.jpg"},
            {"ten": "OPPO Find X7 Ultra", "gia": 25990000, "danh_muc": "Điện thoại", "mo_ta": "Snapdragon 8 Gen 3, Camera Hasselblad", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/42/321471/oppo-find-x7-ultra-black-thumbnew-600x600.jpg"},
            {"ten": "Vivo X100 Pro", "gia": 23990000, "danh_muc": "Điện thoại", "mo_ta": "Dimensity 9300, Camera Zeiss", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/42/320891/vivo-x100-pro-blue-thumbnew-600x600.jpg"},
            {"ten": "Google Pixel 8 Pro", "gia": 24990000, "danh_muc": "Điện thoại", "mo_ta": "Google Tensor G3, AI Camera", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/42/316769/google-pixel-8-pro-blue-thumbnew-600x600.jpg"},
            {"ten": "OnePlus 12", "gia": 21990000, "danh_muc": "Điện thoại", "mo_ta": "Snapdragon 8 Gen 3, Sạc nhanh 100W", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/42/320892/oneplus-12-green-thumbnew-600x600.jpg"},
            {"ten": "Realme GT 5 Pro", "gia": 15990000, "danh_muc": "Điện thoại", "mo_ta": "Snapdragon 8 Gen 3, Màn hình 144Hz", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/42/321472/realme-gt-5-pro-green-thumbnew-600x600.jpg"},
            
            # Laptop (10 sản phẩm)
            {"ten": "MacBook Pro 14 M3 Pro", "gia": 52990000, "danh_muc": "Laptop", "mo_ta": "Chip M3 Pro, 18GB RAM, 512GB SSD", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/44/309016/macbook-pro-14-m3-pro-2023-space-black-thumbnew-600x600.jpg"},
            {"ten": "MacBook Air 13 M3", "gia": 32990000, "danh_muc": "Laptop", "mo_ta": "Chip M3, 8GB RAM, 256GB SSD", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/44/322096/macbook-air-13-m3-2024-midnight-thumbnew-600x600.jpg"},
            {"ten": "Dell XPS 15 9530", "gia": 45990000, "danh_muc": "Laptop", "mo_ta": "Intel Core i7-13700H, RTX 4060, 16GB RAM", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/44/309017/dell-xps-15-9530-i7-13700h-thumbnew-600x600.jpg"},
            {"ten": "ASUS ROG Zephyrus G14", "gia": 42990000, "danh_muc": "Laptop", "mo_ta": "AMD Ryzen 9 7940HS, RTX 4060, 16GB RAM", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/44/309018/asus-rog-zephyrus-g14-ga402xv-thumbnew-600x600.jpg"},
            {"ten": "Lenovo ThinkPad X1 Carbon Gen 11", "gia": 48990000, "danh_muc": "Laptop", "mo_ta": "Intel Core i7-1355U, 16GB RAM, 512GB SSD", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/44/309019/lenovo-thinkpad-x1-carbon-gen-11-thumbnew-600x600.jpg"},
            {"ten": "HP Spectre x360 14", "gia": 39990000, "danh_muc": "Laptop", "mo_ta": "Intel Core i7-1355U, 16GB RAM, Màn hình cảm ứng", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/44/309020/hp-spectre-x360-14-thumbnew-600x600.jpg"},
            {"ten": "Acer Predator Helios 16", "gia": 44990000, "danh_muc": "Laptop", "mo_ta": "Intel Core i9-13900HX, RTX 4070, 32GB RAM", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/44/309021/acer-predator-helios-16-thumbnew-600x600.jpg"},
            {"ten": "MSI Stealth 15M", "gia": 35990000, "danh_muc": "Laptop", "mo_ta": "Intel Core i7-13620H, RTX 4050, 16GB RAM", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/44/309022/msi-stealth-15m-thumbnew-600x600.jpg"},
            {"ten": "LG Gram 17", "gia": 41990000, "danh_muc": "Laptop", "mo_ta": "Intel Core i7-1360P, 16GB RAM, Siêu nhẹ 1.35kg", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/44/309023/lg-gram-17-thumbnew-600x600.jpg"},
            {"ten": "Microsoft Surface Laptop 5", "gia": 37990000, "danh_muc": "Laptop", "mo_ta": "Intel Core i7-1255U, 16GB RAM, Màn hình PixelSense", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/44/309024/microsoft-surface-laptop-5-thumbnew-600x600.jpg"},
            
            # Tablet (10 sản phẩm)
            {"ten": "iPad Pro 12.9 M2 WiFi 128GB", "gia": 29990000, "danh_muc": "Tablet", "mo_ta": "Chip M2, Màn hình Liquid Retina XDR", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/522/289699/ipad-pro-129-m2-wifi-gray-thumbnew-600x600.jpg"},
            {"ten": "iPad Air 5 M1 WiFi 64GB", "gia": 16990000, "danh_muc": "Tablet", "mo_ta": "Chip M1, Màn hình Liquid Retina 10.9 inch", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/522/274443/ipad-air-5-wifi-purple-thumbnew-600x600.jpg"},
            {"ten": "iPad Gen 10 WiFi 64GB", "gia": 11990000, "danh_muc": "Tablet", "mo_ta": "Chip A14 Bionic, Màn hình 10.9 inch", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/522/289700/ipad-gen-10-wifi-blue-thumbnew-600x600.jpg"},
            {"ten": "Samsung Galaxy Tab S9 Ultra", "gia": 31990000, "danh_muc": "Tablet", "mo_ta": "Snapdragon 8 Gen 2, Màn hình 14.6 inch, S Pen", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/522/309025/samsung-galaxy-tab-s9-ultra-thumbnew-600x600.jpg"},
            {"ten": "Samsung Galaxy Tab S9 FE", "gia": 12990000, "danh_muc": "Tablet", "mo_ta": "Exynos 1380, Màn hình 10.9 inch, S Pen", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/522/309026/samsung-galaxy-tab-s9-fe-thumbnew-600x600.jpg"},
            {"ten": "Xiaomi Pad 6", "gia": 8990000, "danh_muc": "Tablet", "mo_ta": "Snapdragon 870, Màn hình 11 inch 144Hz", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/522/309027/xiaomi-pad-6-thumbnew-600x600.jpg"},
            {"ten": "Lenovo Tab P12", "gia": 14990000, "danh_muc": "Tablet", "mo_ta": "Dimensity 7050, Màn hình 12.7 inch", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/522/309028/lenovo-tab-p12-thumbnew-600x600.jpg"},
            {"ten": "OPPO Pad Air", "gia": 6990000, "danh_muc": "Tablet", "mo_ta": "Snapdragon 680, Màn hình 10.36 inch", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/522/309029/oppo-pad-air-thumbnew-600x600.jpg"},
            {"ten": "Huawei MatePad Pro 12.6", "gia": 18990000, "danh_muc": "Tablet", "mo_ta": "Kirin 9000E, Màn hình OLED 12.6 inch", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/522/309030/huawei-matepad-pro-thumbnew-600x600.jpg"},
            {"ten": "Microsoft Surface Pro 9", "gia": 27990000, "danh_muc": "Tablet", "mo_ta": "Intel Core i7-1255U, Màn hình PixelSense 13 inch", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/522/309031/microsoft-surface-pro-9-thumbnew-600x600.jpg"},
            
            # Phụ kiện (10 sản phẩm)
            {"ten": "Apple Pencil Gen 2", "gia": 3490000, "danh_muc": "Phụ kiện", "mo_ta": "Bút cảm ứng cho iPad, sạc không dây", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/1924/230529/apple-pencil-2-thumbnew-600x600.jpg"},
            {"ten": "Magic Keyboard cho iPad Pro", "gia": 8990000, "danh_muc": "Phụ kiện", "mo_ta": "Bàn phím có trackpad, cổng USB-C", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/1924/230530/magic-keyboard-ipad-pro-thumbnew-600x600.jpg"},
            {"ten": "Samsung S Pen Pro", "gia": 2490000, "danh_muc": "Phụ kiện", "mo_ta": "Bút S Pen cho Galaxy Tab, Note", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/1924/309032/samsung-s-pen-pro-thumbnew-600x600.jpg"},
            {"ten": "Logitech MX Master 3S", "gia": 2790000, "danh_muc": "Phụ kiện", "mo_ta": "Chuột không dây cao cấp, 8000 DPI", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/86/309033/logitech-mx-master-3s-thumbnew-600x600.jpg"},
            {"ten": "Logitech MX Keys", "gia": 3290000, "danh_muc": "Phụ kiện", "mo_ta": "Bàn phím không dây, đèn nền thông minh", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/4547/309034/logitech-mx-keys-thumbnew-600x600.jpg"},
            {"ten": "Anker PowerCore 20000mAh", "gia": 1290000, "danh_muc": "Phụ kiện", "mo_ta": "Pin sạc dự phòng, sạc nhanh PD 20W", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/57/309035/anker-powercore-20000-thumbnew-600x600.jpg"},
            {"ten": "Belkin BoostCharge Pro 3-in-1", "gia": 4990000, "danh_muc": "Phụ kiện", "mo_ta": "Đế sạc không dây cho iPhone, Watch, AirPods", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/9499/309036/belkin-boostcharge-pro-thumbnew-600x600.jpg"},
            {"ten": "Ugreen Nexode 100W GaN", "gia": 1790000, "danh_muc": "Phụ kiện", "mo_ta": "Sạc nhanh 4 cổng, công nghệ GaN", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/9499/309037/ugreen-nexode-100w-thumbnew-600x600.jpg"},
            {"ten": "Baseus 65W GaN Charger", "gia": 990000, "danh_muc": "Phụ kiện", "mo_ta": "Sạc nhanh 3 cổng, nhỏ gọn", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/9499/309038/baseus-65w-gan-thumbnew-600x600.jpg"},
            {"ten": "Anker USB-C Hub 7-in-1", "gia": 1490000, "danh_muc": "Phụ kiện", "mo_ta": "Hub đa năng: HDMI, USB 3.0, SD Card", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/9499/309039/anker-usb-c-hub-thumbnew-600x600.jpg"},
            
            # Tai nghe (10 sản phẩm)
            {"ten": "AirPods Pro 2 USB-C", "gia": 6490000, "danh_muc": "Tai nghe", "mo_ta": "Chip H2, ANC, Spatial Audio", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/54/289700/airpods-pro-2-usb-c-thumbnew-600x600.jpg"},
            {"ten": "AirPods Max", "gia": 13990000, "danh_muc": "Tai nghe", "mo_ta": "Chip H1, ANC, Spatial Audio, Over-ear", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/54/230531/airpods-max-silver-thumbnew-600x600.jpg"},
            {"ten": "Sony WH-1000XM5", "gia": 8990000, "danh_muc": "Tai nghe", "mo_ta": "ANC hàng đầu, 30h pin, LDAC", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/54/289701/sony-wh-1000xm5-black-thumbnew-600x600.jpg"},
            {"ten": "Sony WF-1000XM5", "gia": 6490000, "danh_muc": "Tai nghe", "mo_ta": "True Wireless, ANC, LDAC, 8h pin", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/54/309040/sony-wf-1000xm5-thumbnew-600x600.jpg"},
            {"ten": "Bose QuietComfort Ultra", "gia": 9990000, "danh_muc": "Tai nghe", "mo_ta": "ANC tuyệt vời, Spatial Audio, 24h pin", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/54/309041/bose-quietcomfort-ultra-thumbnew-600x600.jpg"},
            {"ten": "Samsung Galaxy Buds2 Pro", "gia": 4490000, "danh_muc": "Tai nghe", "mo_ta": "ANC, 360 Audio, 8h pin", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/54/289702/samsung-galaxy-buds2-pro-thumbnew-600x600.jpg"},
            {"ten": "Jabra Elite 85t", "gia": 5490000, "danh_muc": "Tai nghe", "mo_ta": "ANC, 6 mic, 25h pin", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/54/309042/jabra-elite-85t-thumbnew-600x600.jpg"},
            {"ten": "Sennheiser Momentum 4", "gia": 8490000, "danh_muc": "Tai nghe", "mo_ta": "ANC, 60h pin, âm thanh Hi-Res", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/54/309043/sennheiser-momentum-4-thumbnew-600x600.jpg"},
            {"ten": "JBL Tour One M2", "gia": 6990000, "danh_muc": "Tai nghe", "mo_ta": "ANC, Spatial Audio, 30h pin", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/54/309044/jbl-tour-one-m2-thumbnew-600x600.jpg"},
            {"ten": "Beats Studio Pro", "gia": 7990000, "danh_muc": "Tai nghe", "mo_ta": "ANC, Spatial Audio, 40h pin", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/54/309045/beats-studio-pro-thumbnew-600x600.jpg"},
            
            # Đồng hồ thông minh (10 sản phẩm)
            {"ten": "Apple Watch Series 9 GPS 45mm", "gia": 11990000, "danh_muc": "Đồng hồ thông minh", "mo_ta": "Chip S9, Always-On Retina, ECG", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/7077/309046/apple-watch-series-9-gps-45mm-thumbnew-600x600.jpg"},
            {"ten": "Apple Watch Ultra 2", "gia": 21990000, "danh_muc": "Đồng hồ thông minh", "mo_ta": "Chip S9, Titanium, 36h pin, GPS kép", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/7077/309047/apple-watch-ultra-2-thumbnew-600x600.jpg"},
            {"ten": "Samsung Galaxy Watch6 Classic", "gia": 8990000, "danh_muc": "Đồng hồ thông minh", "mo_ta": "Wear OS, Vòng xoay, ECG, 40h pin", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/7077/309048/samsung-galaxy-watch6-classic-thumbnew-600x600.jpg"},
            {"ten": "Samsung Galaxy Watch6", "gia": 6990000, "danh_muc": "Đồng hồ thông minh", "mo_ta": "Wear OS, Màn hình AMOLED, ECG", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/7077/309049/samsung-galaxy-watch6-thumbnew-600x600.jpg"},
            {"ten": "Garmin Fenix 7", "gia": 18990000, "danh_muc": "Đồng hồ thông minh", "mo_ta": "GPS, 18 ngày pin, 60+ môn thể thao", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/7077/309050/garmin-fenix-7-thumbnew-600x600.jpg"},
            {"ten": "Huawei Watch GT 4", "gia": 6490000, "danh_muc": "Đồng hồ thông minh", "mo_ta": "AMOLED, 14 ngày pin, 100+ môn thể thao", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/7077/309051/huawei-watch-gt-4-thumbnew-600x600.jpg"},
            {"ten": "Xiaomi Watch S2", "gia": 4990000, "danh_muc": "Đồng hồ thông minh", "mo_ta": "AMOLED, 12 ngày pin, GPS", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/7077/309052/xiaomi-watch-s2-thumbnew-600x600.jpg"},
            {"ten": "Amazfit GTR 4", "gia": 5490000, "danh_muc": "Đồng hồ thông minh", "mo_ta": "AMOLED, 14 ngày pin, GPS kép", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/7077/309053/amazfit-gtr-4-thumbnew-600x600.jpg"},
            {"ten": "Fitbit Sense 2", "gia": 7490000, "danh_muc": "Đồng hồ thông minh", "mo_ta": "ECG, EDA, 6+ ngày pin", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/7077/309054/fitbit-sense-2-thumbnew-600x600.jpg"},
            {"ten": "OPPO Watch 3 Pro", "gia": 8990000, "danh_muc": "Đồng hồ thông minh", "mo_ta": "Wear OS, AMOLED, 5 ngày pin", "hinh_anh": "https://cdn.tgdd.vn/Products/Images/7077/309055/oppo-watch-3-pro-thumbnew-600x600.jpg"},
        ]
        
        added = 0
        skipped = 0
        
        for product in products:
            # Kiểm tra sản phẩm đã tồn tại chưa
            existing = db.query(SanPham).filter(SanPham.ten == product["ten"]).first()
            
            if existing:
                skipped += 1
                continue
            
            # Tạo sản phẩm mới
            new_product = SanPham(
                ten=product["ten"],
                gia=Decimal(str(product["gia"])),
                mo_ta=product["mo_ta"],
                hinh_anh=product["hinh_anh"],
                danh_muc_id=categories[product["danh_muc"]]
            )
            
            db.add(new_product)
            added += 1
        
        db.commit()
        
        print("\n" + "=" * 60)
        print(f"📊 Kết quả:")
        print(f"   Đã thêm: {added} sản phẩm")
        print(f"   Bỏ qua: {skipped} sản phẩm")
        print("=" * 60)
        
        # Thống kê sau khi thêm
        print("\n📈 Thống kê sản phẩm theo danh mục:")
        for cat_name, cat_id in categories.items():
            count = db.query(SanPham).filter(SanPham.danh_muc_id == cat_id).count()
            print(f"   {cat_name}: {count} sản phẩm")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("THÊM SẢN PHẨM CHO CÁC DANH MỤC")
    print("=" * 60)
    add_products()

"""
Script để cập nhật ảnh sản phẩm với ảnh thật
"""
from app.database import SessionLocal
from app.models import SanPham

def update_images():
    db = SessionLocal()
    
    try:
        # Mapping tên sản phẩm với URL ảnh
        product_images = {
            # Điện thoại
            "iPhone 15 Pro Max 256GB": "https://cdn.tgdd.vn/Products/Images/42/305658/iphone-15-pro-max-blue-thumbnew-600x600.jpg",
            "iPhone 15 Pro Max": "https://cdn.tgdd.vn/Products/Images/42/305658/iphone-15-pro-max-blue-thumbnew-600x600.jpg",
            "iPhone 14 Pro 128GB": "https://cdn.tgdd.vn/Products/Images/42/289700/iphone-14-pro-purple-1-600x600.jpg",
            "Samsung Galaxy S24 Ultra": "https://cdn.tgdd.vn/Products/Images/42/320721/samsung-galaxy-s24-ultra-grey-thumbnew-600x600.jpg",
            "Samsung Galaxy S23 FE": "https://cdn.tgdd.vn/Products/Images/42/316771/samsung-galaxy-s23-fe-mint-thumbnew-600x600.jpg",
            "Xiaomi 14 Ultra": "https://cdn.tgdd.vn/Products/Images/42/322096/xiaomi-14-ultra-black-thumbnew-600x600.jpg",
            "OPPO Find X7 Ultra": "https://cdn.tgdd.vn/Products/Images/42/321471/oppo-find-x7-ultra-black-thumbnew-600x600.jpg",
            "Vivo X100 Pro": "https://cdn.tgdd.vn/Products/Images/42/320891/vivo-x100-pro-blue-thumbnew-600x600.jpg",
            "Google Pixel 8 Pro": "https://cdn.tgdd.vn/Products/Images/42/316769/google-pixel-8-pro-blue-thumbnew-600x600.jpg",
            "OnePlus 12": "https://cdn.tgdd.vn/Products/Images/42/320892/oneplus-12-green-thumbnew-600x600.jpg",
            "Realme GT 5 Pro": "https://cdn.tgdd.vn/Products/Images/42/321472/realme-gt-5-pro-green-thumbnew-600x600.jpg",
            
            # Laptop
            "MacBook Pro 14 M3 Pro": "https://cdn.tgdd.vn/Products/Images/44/309016/macbook-pro-14-m3-pro-2023-space-black-thumbnew-600x600.jpg",
            "MacBook Pro 14 M3": "https://cdn.tgdd.vn/Products/Images/44/309016/macbook-pro-14-m3-pro-2023-space-black-thumbnew-600x600.jpg",
            "MacBook Air 13 M3": "https://cdn.tgdd.vn/Products/Images/44/322096/macbook-air-13-m3-2024-midnight-thumbnew-600x600.jpg",
            "Dell XPS 15 9530": "https://cdn.tgdd.vn/Products/Images/44/309017/dell-xps-15-9530-i7-13700h-thumbnew-600x600.jpg",
            "Dell XPS 15": "https://cdn.tgdd.vn/Products/Images/44/309017/dell-xps-15-9530-i7-13700h-thumbnew-600x600.jpg",
            "ASUS ROG Zephyrus G14": "https://cdn.tgdd.vn/Products/Images/44/309018/asus-rog-zephyrus-g14-ga402xv-thumbnew-600x600.jpg",
            "Lenovo ThinkPad X1 Carbon Gen 11": "https://cdn.tgdd.vn/Products/Images/44/309019/lenovo-thinkpad-x1-carbon-gen-11-thumbnew-600x600.jpg",
            "HP Spectre x360 14": "https://cdn.tgdd.vn/Products/Images/44/309020/hp-spectre-x360-14-thumbnew-600x600.jpg",
            "Acer Predator Helios 16": "https://cdn.tgdd.vn/Products/Images/44/309021/acer-predator-helios-16-thumbnew-600x600.jpg",
            "MSI Stealth 15M": "https://cdn.tgdd.vn/Products/Images/44/309022/msi-stealth-15m-thumbnew-600x600.jpg",
            "LG Gram 17": "https://cdn.tgdd.vn/Products/Images/44/309023/lg-gram-17-thumbnew-600x600.jpg",
            "Microsoft Surface Laptop 5": "https://cdn.tgdd.vn/Products/Images/44/309024/microsoft-surface-laptop-5-thumbnew-600x600.jpg",
            
            # Tablet
            "iPad Pro 12.9 M2 WiFi 128GB": "https://cdn.tgdd.vn/Products/Images/522/289699/ipad-pro-129-m2-wifi-gray-thumbnew-600x600.jpg",
            "iPad Pro M2 11 inch": "https://cdn.tgdd.vn/Products/Images/522/289699/ipad-pro-129-m2-wifi-gray-thumbnew-600x600.jpg",
            "iPad Air 5 M1 WiFi 64GB": "https://cdn.tgdd.vn/Products/Images/522/274443/ipad-air-5-wifi-purple-thumbnew-600x600.jpg",
            "iPad Gen 10 WiFi 64GB": "https://cdn.tgdd.vn/Products/Images/522/289700/ipad-gen-10-wifi-blue-thumbnew-600x600.jpg",
            "Samsung Galaxy Tab S9 Ultra": "https://cdn.tgdd.vn/Products/Images/522/309025/samsung-galaxy-tab-s9-ultra-thumbnew-600x600.jpg",
            "Samsung Galaxy Tab S9": "https://cdn.tgdd.vn/Products/Images/522/309025/samsung-galaxy-tab-s9-ultra-thumbnew-600x600.jpg",
            "Samsung Galaxy Tab S9 FE": "https://cdn.tgdd.vn/Products/Images/522/309026/samsung-galaxy-tab-s9-fe-thumbnew-600x600.jpg",
            "Xiaomi Pad 6": "https://cdn.tgdd.vn/Products/Images/522/309027/xiaomi-pad-6-thumbnew-600x600.jpg",
            "Lenovo Tab P12": "https://cdn.tgdd.vn/Products/Images/522/309028/lenovo-tab-p12-thumbnew-600x600.jpg",
            "OPPO Pad Air": "https://cdn.tgdd.vn/Products/Images/522/309029/oppo-pad-air-thumbnew-600x600.jpg",
            "Huawei MatePad Pro 12.6": "https://cdn.tgdd.vn/Products/Images/522/309030/huawei-matepad-pro-thumbnew-600x600.jpg",
            "Microsoft Surface Pro 9": "https://cdn.tgdd.vn/Products/Images/522/309031/microsoft-surface-pro-9-thumbnew-600x600.jpg",
            
            # Phụ kiện
            "Apple Pencil Gen 2": "https://cdn.tgdd.vn/Products/Images/1924/230529/apple-pencil-2-thumbnew-600x600.jpg",
            "Magic Keyboard cho iPad Pro": "https://cdn.tgdd.vn/Products/Images/1924/230530/magic-keyboard-ipad-pro-thumbnew-600x600.jpg",
            "Samsung S Pen Pro": "https://cdn.tgdd.vn/Products/Images/1924/309032/samsung-s-pen-pro-thumbnew-600x600.jpg",
            "Logitech MX Master 3S": "https://cdn.tgdd.vn/Products/Images/86/309033/logitech-mx-master-3s-thumbnew-600x600.jpg",
            "Logitech MX Keys": "https://cdn.tgdd.vn/Products/Images/4547/309034/logitech-mx-keys-thumbnew-600x600.jpg",
            "Anker PowerCore 20000mAh": "https://cdn.tgdd.vn/Products/Images/57/309035/anker-powercore-20000-thumbnew-600x600.jpg",
            "Belkin BoostCharge Pro 3-in-1": "https://cdn.tgdd.vn/Products/Images/9499/309036/belkin-boostcharge-pro-thumbnew-600x600.jpg",
            "Ugreen Nexode 100W GaN": "https://cdn.tgdd.vn/Products/Images/9499/309037/ugreen-nexode-100w-thumbnew-600x600.jpg",
            "Baseus 65W GaN Charger": "https://cdn.tgdd.vn/Products/Images/9499/309038/baseus-65w-gan-thumbnew-600x600.jpg",
            "Anker USB-C Hub 7-in-1": "https://cdn.tgdd.vn/Products/Images/9499/309039/anker-usb-c-hub-thumbnew-600x600.jpg",
            "Sạc nhanh Apple 20W": "https://cdn.tgdd.vn/Products/Images/9499/309037/ugreen-nexode-100w-thumbnew-600x600.jpg",
            "Cáp sạc Type-C to Lightning": "https://cdn.tgdd.vn/Products/Images/9499/309038/baseus-65w-gan-thumbnew-600x600.jpg",
            
            # Tai nghe
            "AirPods Pro 2 USB-C": "https://cdn.tgdd.vn/Products/Images/54/289700/airpods-pro-2-usb-c-thumbnew-600x600.jpg",
            "AirPods Pro 2": "https://cdn.tgdd.vn/Products/Images/54/289700/airpods-pro-2-usb-c-thumbnew-600x600.jpg",
            "AirPods Max": "https://cdn.tgdd.vn/Products/Images/54/230531/airpods-max-silver-thumbnew-600x600.jpg",
            "Sony WH-1000XM5": "https://cdn.tgdd.vn/Products/Images/54/289701/sony-wh-1000xm5-black-thumbnew-600x600.jpg",
            "Sony WF-1000XM5": "https://cdn.tgdd.vn/Products/Images/54/309040/sony-wf-1000xm5-thumbnew-600x600.jpg",
            "Bose QuietComfort Ultra": "https://cdn.tgdd.vn/Products/Images/54/309041/bose-quietcomfort-ultra-thumbnew-600x600.jpg",
            "Samsung Galaxy Buds2 Pro": "https://cdn.tgdd.vn/Products/Images/54/289702/samsung-galaxy-buds2-pro-thumbnew-600x600.jpg",
            "Jabra Elite 85t": "https://cdn.tgdd.vn/Products/Images/54/309042/jabra-elite-85t-thumbnew-600x600.jpg",
            "Sennheiser Momentum 4": "https://cdn.tgdd.vn/Products/Images/54/309043/sennheiser-momentum-4-thumbnew-600x600.jpg",
            "JBL Tour One M2": "https://cdn.tgdd.vn/Products/Images/54/309044/jbl-tour-one-m2-thumbnew-600x600.jpg",
            "Beats Studio Pro": "https://cdn.tgdd.vn/Products/Images/54/309045/beats-studio-pro-thumbnew-600x600.jpg",
            
            # Đồng hồ thông minh
            "Apple Watch Series 9 GPS 45mm": "https://cdn.tgdd.vn/Products/Images/7077/309046/apple-watch-series-9-gps-45mm-thumbnew-600x600.jpg",
            "Apple Watch Series 9": "https://cdn.tgdd.vn/Products/Images/7077/309046/apple-watch-series-9-gps-45mm-thumbnew-600x600.jpg",
            "Apple Watch Ultra 2": "https://cdn.tgdd.vn/Products/Images/7077/309047/apple-watch-ultra-2-thumbnew-600x600.jpg",
            "Samsung Galaxy Watch6 Classic": "https://cdn.tgdd.vn/Products/Images/7077/309048/samsung-galaxy-watch6-classic-thumbnew-600x600.jpg",
            "Samsung Galaxy Watch6": "https://cdn.tgdd.vn/Products/Images/7077/309049/samsung-galaxy-watch6-thumbnew-600x600.jpg",
            "Samsung Galaxy Watch 6": "https://cdn.tgdd.vn/Products/Images/7077/309049/samsung-galaxy-watch6-thumbnew-600x600.jpg",
            "Garmin Fenix 7": "https://cdn.tgdd.vn/Products/Images/7077/309050/garmin-fenix-7-thumbnew-600x600.jpg",
            "Huawei Watch GT 4": "https://cdn.tgdd.vn/Products/Images/7077/309051/huawei-watch-gt-4-thumbnew-600x600.jpg",
            "Xiaomi Watch S2": "https://cdn.tgdd.vn/Products/Images/7077/309052/xiaomi-watch-s2-thumbnew-600x600.jpg",
            "Amazfit GTR 4": "https://cdn.tgdd.vn/Products/Images/7077/309053/amazfit-gtr-4-thumbnew-600x600.jpg",
            "Fitbit Sense 2": "https://cdn.tgdd.vn/Products/Images/7077/309054/fitbit-sense-2-thumbnew-600x600.jpg",
            "OPPO Watch 3 Pro": "https://cdn.tgdd.vn/Products/Images/7077/309055/oppo-watch-3-pro-thumbnew-600x600.jpg",
        }
        
        updated = 0
        not_found = []
        
        for product_name, image_url in product_images.items():
            product = db.query(SanPham).filter(SanPham.ten == product_name).first()
            
            if product:
                product.hinh_anh = image_url
                updated += 1
                print(f"✅ Updated: {product_name}")
            else:
                not_found.append(product_name)
        
        db.commit()
        
        print("\n" + "=" * 60)
        print(f"📊 Kết quả:")
        print(f"   Đã cập nhật: {updated} sản phẩm")
        print(f"   Không tìm thấy: {len(not_found)} sản phẩm")
        if not_found:
            print("\n❌ Sản phẩm không tìm thấy:")
            for name in not_found:
                print(f"   - {name}")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("CẬP NHẬT ẢNH SẢN PHẨM")
    print("=" * 60)
    update_images()

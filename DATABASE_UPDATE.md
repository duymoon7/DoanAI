# 🔄 CẬP NHẬT DATABASE

## Các Trường Mới Đã Thêm

### 1. Bảng `nguoi_dung`
- `dia_chi` (TEXT): Địa chỉ mặc định của người dùng
- `avatar` (VARCHAR(500)): URL ảnh đại diện
- `ngay_cap_nhat` (DATETIME): Ngày cập nhật thông tin

### 2. Bảng `san_pham`
- `ton_kho` (INT): Số lượng tồn kho (mặc định: 0)
- `trang_thai` (VARCHAR(20)): Trạng thái sản phẩm (active/inactive)
- `ngay_cap_nhat` (DATETIME): Ngày cập nhật sản phẩm

### 3. Bảng `don_hang`
- `ten_nguoi_nhan` (VARCHAR(255)): Tên người nhận hàng
- `so_dien_thoai_nguoi_nhan` (VARCHAR(20)): Số điện thoại người nhận
- `dia_chi_giao_hang` (TEXT): Địa chỉ giao hàng
- `ghi_chu` (TEXT): Ghi chú đơn hàng
- `ma_giam_gia_id` (INT): ID mã giảm giá (foreign key)
- `so_tien_giam` (DECIMAL(10,2)): Số tiền được giảm (mặc định: 0)
- `ngay_cap_nhat` (DATETIME): Ngày cập nhật đơn hàng

---

## Cách Chạy Migration

### Bước 1: Backup Database (Quan trọng!)
```bash
# Trong phpMyAdmin, chọn database electronics_db
# Export -> SQL -> Lưu file backup
```

### Bước 2: Chạy Migration Script
```bash
cd backend
python migrate_database.py
```

### Bước 3: Kiểm Tra Kết Quả
```bash
# Mở phpMyAdmin
# Kiểm tra cấu trúc các bảng đã được cập nhật
```

---

## Hoặc Chạy Thủ Công (SQL)

Nếu script Python không chạy được, bạn có thể chạy SQL trực tiếp trong phpMyAdmin:

```sql
-- Bảng nguoi_dung
ALTER TABLE nguoi_dung ADD COLUMN dia_chi TEXT NULL;
ALTER TABLE nguoi_dung ADD COLUMN avatar VARCHAR(500) NULL;
ALTER TABLE nguoi_dung ADD COLUMN ngay_cap_nhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- Bảng san_pham
ALTER TABLE san_pham ADD COLUMN ton_kho INT NOT NULL DEFAULT 0;
ALTER TABLE san_pham ADD COLUMN trang_thai VARCHAR(20) NOT NULL DEFAULT 'active';
ALTER TABLE san_pham ADD COLUMN ngay_cap_nhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- Bảng don_hang
ALTER TABLE don_hang ADD COLUMN ten_nguoi_nhan VARCHAR(255) NULL;
ALTER TABLE don_hang ADD COLUMN so_dien_thoai_nguoi_nhan VARCHAR(20) NULL;
ALTER TABLE don_hang ADD COLUMN dia_chi_giao_hang TEXT NULL;
ALTER TABLE don_hang ADD COLUMN ghi_chu TEXT NULL;
ALTER TABLE don_hang ADD COLUMN ma_giam_gia_id INT NULL;
ALTER TABLE don_hang ADD COLUMN so_tien_giam DECIMAL(10,2) NOT NULL DEFAULT 0;
ALTER TABLE don_hang ADD COLUMN ngay_cap_nhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- Foreign key
ALTER TABLE don_hang 
ADD CONSTRAINT fk_don_hang_ma_giam_gia 
FOREIGN KEY (ma_giam_gia_id) 
REFERENCES ma_giam_gia(id) 
ON DELETE SET NULL;

-- Indexes
CREATE INDEX idx_san_pham_trang_thai ON san_pham(trang_thai);
CREATE INDEX idx_don_hang_ma_giam_gia ON don_hang(ma_giam_gia_id);
```

---

## Cập Nhật Schemas (Backend)

Cần cập nhật các file schema để sử dụng trường mới:

### `schemas/nguoi_dung.py`
```python
class NguoiDungBase(BaseModel):
    email: str
    ho_ten: Optional[str] = None
    so_dien_thoai: Optional[str] = None
    dia_chi: Optional[str] = None  # MỚI
    avatar: Optional[str] = None   # MỚI
```

### `schemas/san_pham.py`
```python
class SanPhamBase(BaseModel):
    ten: str
    gia: float
    mo_ta: Optional[str] = None
    hinh_anh: Optional[str] = None
    danh_muc_id: int
    ton_kho: int = 0           # MỚI
    trang_thai: str = "active" # MỚI
```

### `schemas/don_hang.py`
```python
class DonHangCreate(BaseModel):
    chi_tiet: List[ChiTietDonHangCreate]
    phuong_thuc_thanh_toan: str = "cod"
    
    # Thông tin giao hàng - MỚI
    ten_nguoi_nhan: Optional[str] = None
    so_dien_thoai_nguoi_nhan: Optional[str] = None
    dia_chi_giao_hang: Optional[str] = None
    ghi_chu: Optional[str] = None
    
    # Mã giảm giá - MỚI
    ma_giam_gia_code: Optional[str] = None
```

---

## Cập Nhật Frontend

### Trang Đặt Hàng (Checkout)
Thêm form nhập thông tin giao hàng:
- Tên người nhận
- Số điện thoại
- Địa chỉ giao hàng
- Ghi chú
- Mã giảm giá

### Trang Quản Lý Sản Phẩm (Admin)
Thêm trường:
- Tồn kho
- Trạng thái (Active/Inactive)

### Trang Profile
Thêm trường:
- Địa chỉ mặc định
- Upload avatar

---

## Lợi Ích Của Cập Nhật

✅ **Quản lý tồn kho**: Biết sản phẩm còn bao nhiêu, tránh bán quá số lượng

✅ **Thông tin giao hàng đầy đủ**: Lưu địa chỉ, SĐT người nhận cho mỗi đơn

✅ **Tích hợp mã giảm giá**: Liên kết đơn hàng với mã giảm giá đã dùng

✅ **Quản lý sản phẩm tốt hơn**: Ẩn/hiện sản phẩm không cần xóa

✅ **Trải nghiệm người dùng**: Lưu địa chỉ, avatar cá nhân hóa

---

## Lưu Ý Quan Trọng

⚠️ **Backup trước khi chạy migration!**

⚠️ **Các trường mới đều nullable hoặc có default** - dữ liệu cũ không bị ảnh hưởng

⚠️ **Cần restart backend** sau khi chạy migration để models được cập nhật

⚠️ **Cập nhật API và Frontend** để sử dụng đầy đủ tính năng mới

---

## Kiểm Tra Sau Migration

```bash
# 1. Restart backend
cd backend
# Ctrl+C để dừng
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 2. Kiểm tra API docs
# Mở: http://localhost:8000/docs
# Xem các schema đã cập nhật chưa

# 3. Test tạo đơn hàng mới với thông tin giao hàng
# 4. Test cập nhật profile với địa chỉ
# 5. Test quản lý tồn kho sản phẩm
```

---

## Rollback (Nếu Cần)

Nếu có vấn đề, restore từ backup:

```bash
# Trong phpMyAdmin
# Import -> Chọn file backup -> Go
```

Hoặc xóa các cột đã thêm:

```sql
-- Xóa cột (cẩn thận!)
ALTER TABLE nguoi_dung DROP COLUMN dia_chi;
ALTER TABLE nguoi_dung DROP COLUMN avatar;
-- ... (các cột khác)
```

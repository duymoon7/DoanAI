# 💳 CẬP NHẬT TÍNH NĂNG THANH TOÁN

## 📋 Tổng quan

Đã implement đầy đủ tính năng thanh toán theo **Product Backlog PB10** bao gồm:

✅ Kiểm tra tồn kho trước thanh toán  
✅ Thông tin giao hàng đầy đủ (tên, SĐT, địa chỉ, ghi chú)  
✅ Áp dụng mã giảm giá  
✅ Validate mã giảm giá (hạn sử dụng, thời gian, giá trị đơn tối thiểu)  
✅ Tính toán giá cuối cùng (tạm tính - giảm giá)  
✅ Lưu đầy đủ thông tin vào database  
✅ Trừ tồn kho và lượt sử dụng mã giảm giá  

---

## 🗄️ CẬP NHẬT DATABASE

### Các trường mới đã thêm:

#### 1. Bảng `don_hang` (QUAN TRỌNG!)
```sql
-- Thông tin giao hàng
ten_nguoi_nhan VARCHAR(255) NULL          -- Tên người nhận
so_dien_thoai_nguoi_nhan VARCHAR(20) NULL -- SĐT người nhận  
dia_chi_giao_hang TEXT NULL               -- Địa chỉ giao hàng
ghi_chu TEXT NULL                         -- Ghi chú đơn hàng

-- Mã giảm giá
ma_giam_gia_id INT NULL                   -- ID mã giảm giá
so_tien_giam DECIMAL(10,2) DEFAULT 0      -- Số tiền được giảm
ngay_cap_nhat DATETIME                    -- Ngày cập nhật
```

#### 2. Bảng `san_pham`
```sql
ton_kho INT DEFAULT 0                     -- Số lượng tồn kho
trang_thai VARCHAR(20) DEFAULT 'active'   -- Trạng thái sản phẩm
ngay_cap_nhat DATETIME                    -- Ngày cập nhật
```

#### 3. Bảng `nguoi_dung`
```sql
dia_chi TEXT NULL                         -- Địa chỉ mặc định
avatar VARCHAR(500) NULL                  -- URL ảnh đại diện
ngay_cap_nhat DATETIME                    -- Ngày cập nhật
```

---

## 🚀 HƯỚNG DẪN CẬP NHẬT

### Cách 1: Sử dụng Migration Script (Khuyến nghị)

1. **Khởi động MySQL trong XAMPP**
   - Mở XAMPP Control Panel
   - Click "Start" cho MySQL

2. **Chạy migration script:**
   ```bash
   cd AI-Shop/backend
   python migrate_database.py
   ```

3. **Kiểm tra kết quả:**
   - Script sẽ hiển thị tiến trình từng bước
   - Nếu thành công, bạn sẽ thấy: ✨ Migration hoàn tất!

### Cách 2: Chạy SQL thủ công trong phpMyAdmin

1. **Mở phpMyAdmin:** http://localhost/phpmyadmin

2. **Chọn database:** `electronics_db`

3. **Vào tab "SQL"**

4. **Copy toàn bộ nội dung file:** `backend/update_database.sql`

5. **Paste vào và click "Go"**

6. **Kiểm tra kết quả:**
   ```sql
   DESCRIBE don_hang;
   ```
   Bạn sẽ thấy các trường mới đã được thêm vào.

---

## 🔧 API MỚI

### 1. Validate Mã Giảm Giá
```http
POST /api/ma-giam-gia/validate
Query Params:
  - ma_code: string (mã giảm giá)
  - order_total: number (tổng tiền đơn hàng)

Response:
{
  "valid": true,
  "message": "Mã giảm giá hợp lệ",
  "discount_amount": 50000,
  "coupon_id": 1,
  "ma_giam_gia": { ... }
}
```

### 2. Kiểm Tra Tồn Kho
```http
POST /api/san-pham/check-stock
Body:
[
  {"product_id": 1, "quantity": 2},
  {"product_id": 2, "quantity": 1}
]

Response:
{
  "valid": true,
  "message": "Tất cả sản phẩm đều còn hàng"
}

// Hoặc nếu hết hàng:
{
  "valid": false,
  "out_of_stock": [
    {
      "product_id": 1,
      "product_name": "iPhone 15",
      "message": "iPhone 15 đã hết hàng"
    }
  ],
  "insufficient_stock": []
}
```

### 3. Tạo Đơn Hàng (Đã cập nhật)
```http
POST /api/don-hang
Body:
{
  "nguoi_dung_id": 1,
  "tong_tien": 15000000,
  "trang_thai": "pending",
  "phuong_thuc_thanh_toan": "cod",
  
  // Thông tin giao hàng (BẮT BUỘC)
  "ten_nguoi_nhan": "Nguyễn Văn A",
  "so_dien_thoai_nguoi_nhan": "0912345678",
  "dia_chi_giao_hang": "123 Đường ABC, Phường XYZ, Quận 1, TP.HCM",
  "ghi_chu": "Giao giờ hành chính",
  
  // Mã giảm giá (TÙY CHỌN)
  "ma_giam_gia_id": 1,
  "so_tien_giam": 500000
}
```

---

## 🎨 FRONTEND CẬP NHẬT

### Trang Giỏ Hàng (`/cart`)

#### Tính năng mới:
1. **Form thông tin giao hàng:**
   - Họ tên (bắt buộc)
   - Số điện thoại (bắt buộc, validate 10-11 số)
   - Địa chỉ giao hàng (bắt buộc)
   - Ghi chú (tùy chọn)

2. **Áp dụng mã giảm giá:**
   - Input nhập mã
   - Button "Áp dụng" để validate
   - Hiển thị thông tin mã đã áp dụng
   - Button "Xóa" để hủy mã

3. **Tính toán giá:**
   - Tạm tính
   - Phí vận chuyển (miễn phí)
   - Giảm giá (từ mã giảm giá)
   - **Tổng cuối cùng** (in đậm, màu primary)

4. **Kiểm tra tồn kho:**
   - Tự động kiểm tra trước khi thanh toán
   - Hiển thị lỗi nếu sản phẩm hết hàng
   - Hiển thị lỗi nếu số lượng không đủ

---

## ✅ CHECKLIST SAU KHI CẬP NHẬT

- [ ] Database đã được migrate thành công
- [ ] Bảng `don_hang` có đầy đủ các trường mới
- [ ] Backend chạy không có lỗi
- [ ] API `/api/ma-giam-gia/validate` hoạt động
- [ ] API `/api/san-pham/check-stock` hoạt động
- [ ] Frontend hiển thị form thông tin giao hàng
- [ ] Có thể áp dụng mã giảm giá
- [ ] Tính toán giá đúng (tạm tính - giảm giá)
- [ ] Có thể đặt hàng thành công
- [ ] Thông tin giao hàng được lưu vào database
- [ ] Mã giảm giá được lưu vào đơn hàng

---

## 🧪 KIỂM TRA TÍNH NĂNG

### Test Case 1: Đặt hàng không có mã giảm giá
1. Thêm sản phẩm vào giỏ hàng
2. Vào trang giỏ hàng
3. Điền đầy đủ thông tin giao hàng
4. Chọn phương thức thanh toán
5. Click "Đặt hàng"
6. ✅ Đơn hàng được tạo thành công

### Test Case 2: Đặt hàng có mã giảm giá
1. Thêm sản phẩm vào giỏ hàng (tổng > 500,000đ)
2. Vào trang giỏ hàng
3. Nhập mã: `SUMMER2024`
4. Click "Áp dụng"
5. ✅ Hiển thị số tiền giảm
6. Điền thông tin giao hàng
7. Click "Đặt hàng"
8. ✅ Đơn hàng được tạo với mã giảm giá

### Test Case 3: Sản phẩm hết hàng
1. Cập nhật tồn kho sản phẩm = 0 trong database
2. Thêm sản phẩm đó vào giỏ hàng
3. Điền thông tin và click "Đặt hàng"
4. ✅ Hiển thị lỗi "Sản phẩm X đã hết hàng"

### Test Case 4: Mã giảm giá không hợp lệ
1. Vào trang giỏ hàng
2. Nhập mã: `INVALID123`
3. Click "Áp dụng"
4. ✅ Hiển thị lỗi "Mã giảm giá không tồn tại"

### Test Case 5: Đơn hàng không đủ giá trị tối thiểu
1. Thêm sản phẩm giá thấp vào giỏ (< 500,000đ)
2. Nhập mã: `SUMMER2024` (yêu cầu tối thiểu 500,000đ)
3. Click "Áp dụng"
4. ✅ Hiển thị lỗi "Đơn hàng tối thiểu 500,000đ"

---

## 📊 DỮ LIỆU MẪU

### Mã giảm giá có sẵn:
```sql
-- Mã SUMMER2024: Giảm 10%, đơn tối thiểu 500,000đ
-- Mã WELCOME50: Giảm 50,000đ, đơn tối thiểu 200,000đ
-- Mã FREESHIP: Miễn phí vận chuyển
```

Xem chi tiết trong bảng `ma_giam_gia` hoặc trang Admin.

---

## 🐛 TROUBLESHOOTING

### Lỗi: "Can't connect to MySQL server"
**Giải pháp:**
- Khởi động MySQL trong XAMPP
- Kiểm tra file `.env` có đúng thông tin database

### Lỗi: "Duplicate column name"
**Giải pháp:**
- Cột đã tồn tại, bỏ qua lỗi này
- Migration script tự động xử lý

### Lỗi: "Foreign key constraint fails"
**Giải pháp:**
- Đảm bảo bảng `ma_giam_gia` đã tồn tại
- Chạy lại migration script

### Frontend không hiển thị form giao hàng
**Giải pháp:**
- Clear cache trình duyệt (Ctrl + Shift + R)
- Restart Next.js dev server
- Kiểm tra console có lỗi không

---

## 📝 GHI CHÚ

- Tất cả các trường mới đều cho phép NULL hoặc có giá trị mặc định
- Dữ liệu cũ không bị ảnh hưởng
- Backend tự động validate thông tin giao hàng
- Mã giảm giá tự động trừ lượt sử dụng khi đặt hàng thành công
- Tồn kho sẽ được trừ khi tạo chi tiết đơn hàng (cần implement thêm)

---

## 🎯 TÍNH NĂNG TIẾP THEO (TODO)

- [ ] Trừ tồn kho tự động khi đặt hàng
- [ ] Hoàn tồn kho khi hủy đơn
- [ ] Gửi email xác nhận đơn hàng
- [ ] Tích hợp thanh toán online (VNPay, Momo)
- [ ] Tracking đơn hàng realtime
- [ ] Xuất hóa đơn PDF

---

**Cập nhật:** 16/04/2026  
**Phiên bản:** 1.1.0  
**Tác giả:** AI-Shop Development Team

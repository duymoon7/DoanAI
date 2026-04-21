# 📊 HƯỚNG DẪN SỬ DỤNG DATABASE DIAGRAM

## 🎯 File: `database_diagram.dbml`

File này chứa schema đầy đủ của database được viết bằng **DBML (Database Markup Language)**.

---

## 🌐 XEM DIAGRAM TRỰC TUYẾN

### Cách 1: Sử dụng dbdiagram.io (Khuyến nghị)

1. **Truy cập:** https://dbdiagram.io/

2. **Import file:**
   - Click vào "Import" ở góc trên bên trái
   - Chọn "From DBML"
   - Copy toàn bộ nội dung file `database_diagram.dbml`
   - Paste vào và click "Import"

3. **Xem diagram:**
   - Diagram sẽ tự động render với giao diện đẹp
   - Có thể zoom in/out, kéo thả các bảng
   - Click vào bảng để xem chi tiết
   - Click vào mũi tên để xem relationship

4. **Export:**
   - Export to PDF
   - Export to PNG
   - Export to SQL (MySQL, PostgreSQL, etc.)

### Cách 2: Sử dụng VS Code Extension

1. **Cài đặt extension:**
   - Tìm "DBML Viewer" trong VS Code Marketplace
   - Hoặc: "Database Markup Language (DBML)"

2. **Mở file:**
   - Mở file `database_diagram.dbml`
   - Click vào icon "Preview" ở góc trên bên phải
   - Diagram sẽ hiển thị trong VS Code

---

## 📋 CẤU TRÚC DATABASE

### 8 Bảng Chính:

1. **nguoi_dung** - Người dùng (Admin/Manager/User)
2. **danh_muc** - Danh mục sản phẩm
3. **san_pham** - Sản phẩm điện tử
4. **don_hang** - Đơn hàng ⭐ ĐÃ CẬP NHẬT
5. **chi_tiet_don_hang** - Chi tiết đơn hàng
6. **danh_gia** - Đánh giá sản phẩm
7. **ma_giam_gia** - Mã giảm giá
8. **lich_su_chat** - Lịch sử chat AI

---

## ⭐ CẬP NHẬT MỚI NHẤT (16/04/2026)

### Tính năng THANH TOÁN (Product Backlog PB10)

#### Bảng `don_hang` - Các trường mới:

```dbml
// Thông tin giao hàng
ten_nguoi_nhan VARCHAR(255)           -- Tên người nhận
so_dien_thoai_nguoi_nhan VARCHAR(20)  -- SĐT người nhận
dia_chi_giao_hang TEXT                -- Địa chỉ giao hàng
ghi_chu TEXT                          -- Ghi chú đơn hàng

// Mã giảm giá
ma_giam_gia_id INT                    -- ID mã giảm giá
so_tien_giam DECIMAL(10,2)            -- Số tiền được giảm
ngay_cap_nhat DATETIME                -- Ngày cập nhật
```

#### Bảng `san_pham` - Các trường mới:

```dbml
ton_kho INT                           -- Số lượng tồn kho
trang_thai VARCHAR(20)                -- active/inactive
ngay_cap_nhat DATETIME                -- Ngày cập nhật
```

#### Bảng `nguoi_dung` - Các trường mới:

```dbml
dia_chi TEXT                          -- Địa chỉ mặc định
avatar VARCHAR(500)                   -- URL ảnh đại diện
ngay_cap_nhat DATETIME                -- Ngày cập nhật
```

---

## 🔗 RELATIONSHIPS (Mối quan hệ)

### Các mối quan hệ chính:

```
danh_muc (1) ----< (N) san_pham
nguoi_dung (1) ----< (N) don_hang
nguoi_dung (1) ----< (N) danh_gia
nguoi_dung (1) ----< (N) lich_su_chat
don_hang (1) ----< (N) chi_tiet_don_hang
san_pham (1) ----< (N) chi_tiet_don_hang
san_pham (1) ----< (N) danh_gia
ma_giam_gia (1) ----< (N) don_hang  ⭐ MỚI
```

### Delete Rules:

- **CASCADE**: Xóa cha → xóa con
  - Xóa user → xóa đơn hàng của user
  - Xóa đơn hàng → xóa chi tiết đơn hàng

- **RESTRICT**: Không cho xóa nếu còn con
  - Không xóa sản phẩm nếu đã có trong đơn hàng
  - Không xóa danh mục nếu còn sản phẩm

- **SET NULL**: Xóa cha → set con = null
  - Xóa mã giảm giá → đơn hàng vẫn giữ nhưng mã = null

---

## 📊 INDEXES (Tối ưu hiệu suất)

### Indexes đã tạo:

```sql
-- Bảng nguoi_dung
idx_email (email)                     -- Unique
idx_vai_tro (vai_tro)

-- Bảng san_pham
idx_danh_muc (danh_muc_id)
idx_ten_san_pham (ten)
idx_trang_thai (trang_thai)          -- ⭐ MỚI

-- Bảng don_hang
idx_nguoi_dung (nguoi_dung_id)
idx_trang_thai (trang_thai)
idx_ngay_tao (ngay_tao)
idx_ma_giam_gia (ma_giam_gia_id)     -- ⭐ MỚI

-- Bảng danh_gia
idx_nguoi_dung_dg (nguoi_dung_id)
idx_san_pham_dg (san_pham_id)
idx_diem_so (diem_so)

-- Bảng ma_giam_gia
idx_ma_code (ma_code)                 -- Unique
idx_hoat_dong (hoat_dong)
idx_ngay_bat_dau (ngay_bat_dau)
idx_ngay_ket_thuc (ngay_ket_thuc)

-- Bảng lich_su_chat
idx_nguoi_dung_chat (nguoi_dung_id)
idx_ngay_tao_chat (ngay_tao)
```

---

## 📈 THỐNG KÊ HỮU ÍCH

### Thống kê thanh toán mới:

```sql
-- 1. Tỷ lệ sử dụng mã giảm giá
SELECT 
  COUNT(CASE WHEN ma_giam_gia_id IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) as usage_rate
FROM don_hang
WHERE trang_thai = 'completed';

-- 2. Phương thức thanh toán phổ biến
SELECT phuong_thuc_thanh_toan, COUNT(*) as count
FROM don_hang
GROUP BY phuong_thuc_thanh_toan;

-- 3. Giá trị đơn hàng trung bình
SELECT AVG(tong_tien) as avg_order_value
FROM don_hang
WHERE trang_thai = 'completed';

-- 4. Tổng tiết kiệm của khách hàng
SELECT SUM(so_tien_giam) as total_savings
FROM don_hang
WHERE trang_thai = 'completed';

-- 5. Hiệu quả mã giảm giá
SELECT 
  mg.ma_code,
  COUNT(dh.id) as usage_count,
  SUM(dh.so_tien_giam) as total_discount,
  AVG(dh.tong_tien) as avg_order_value
FROM don_hang dh
JOIN ma_giam_gia mg ON dh.ma_giam_gia_id = mg.id
WHERE dh.trang_thai = 'completed'
GROUP BY mg.ma_code
ORDER BY total_discount DESC;
```

---

## 🎨 MÀU SẮC TRONG DIAGRAM

Khi xem trên dbdiagram.io, các bảng sẽ được tô màu theo nhóm:

- 🔵 **Xanh dương**: Bảng người dùng và xác thực
- 🟢 **Xanh lá**: Bảng sản phẩm và danh mục
- 🟡 **Vàng**: Bảng đơn hàng và thanh toán
- 🟣 **Tím**: Bảng đánh giá và chat
- 🔴 **Đỏ**: Bảng mã giảm giá

---

## 🔧 CHỈNH SỬA DIAGRAM

### Cú pháp DBML cơ bản:

```dbml
// Định nghĩa bảng
Table table_name {
  column_name data_type [pk, increment, not null, default: value, note: 'description']
  
  indexes {
    column_name [unique, name: 'index_name']
  }
  
  Note: '''
    Mô tả bảng
  '''
}

// Định nghĩa relationship
Ref: table1.column < table2.column [delete: cascade]
// < : one-to-many
// > : many-to-one
// - : one-to-one
// <> : many-to-many
```

### Ví dụ thêm trường mới:

```dbml
Table don_hang {
  // ... các trường hiện có
  
  // Thêm trường mới
  trang_thai_thanh_toan varchar(20) [default: 'unpaid', note: 'Trạng thái thanh toán']
}
```

---

## 📚 TÀI LIỆU THAM KHẢO

- **DBML Documentation**: https://dbml.dbdiagram.io/docs/
- **dbdiagram.io**: https://dbdiagram.io/
- **DBML CLI**: https://github.com/holistics/dbml

---

## ✅ CHECKLIST

- [ ] Đã xem diagram trên dbdiagram.io
- [ ] Hiểu rõ 8 bảng chính
- [ ] Hiểu các mối quan hệ giữa các bảng
- [ ] Biết các trường mới đã thêm cho thanh toán
- [ ] Biết cách export diagram ra PDF/PNG
- [ ] Biết cách chỉnh sửa DBML nếu cần

---

**Cập nhật:** 16/04/2026  
**Phiên bản:** 2.0.0  
**Tác giả:** AI-Shop Development Team

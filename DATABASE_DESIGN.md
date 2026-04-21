# ĐẠI HỌC DUY TÂN

# KHOA CÔNG NGHỆ THÔNG TIN

**Tên đề tài:**

# XÂY DỰNG WEBSITE BÁN THIẾT BỊ ĐIỆN TỬ TÍCH HỢP CHAT BOX AI

**Mã dự án: AI-SHOP | Phiên bản: Ver_2.0 (DATABASE DESIGN DOCUMENT)**

---

## THÔNG TIN DỰ ÁN

| Hạng mục | Chi tiết |
|----------|----------|
| **Dự án viết tắt** | AI-SHOP |
| **Tên dự án** | XÂY DỰNG WEBSITE BÁN THIẾT BỊ ĐIỆN TỬ TÍCH HỢP CHAT BOX AI |
| **Thời gian bắt đầu** | 27/03/2026 |
| **Thời gian kết thúc** | 15/05/2026 |
| **Đơn vị chủ quản** | Khoa Công nghệ thông tin – Đại học Duy Tân |
| **Giảng viên hướng dẫn** | ThS. Lưu Văn Hiền |
| **Chủ sở hữu dự án** | Hoàng Hải Minh Duy (Email: hoanghaiminhduy20004@gmail.com) |
| **Quản lý & Scrum Master** | Hoàng Hải Minh Duy |
| **Thành viên nhóm** | Phạm Hữu Học, Lê Trần Anh Tuấn, Nguyễn Minh Hoàng, Hoàng Nhật Khánh |

---

## THÔNG TIN TÀI LIỆU

| Mục tiêu | Chi tiết |
|----------|----------|
| **Tác giả** | Hoàng Hải Minh Duy |
| **Chức vụ** | Trưởng nhóm |
| **Ngày lập** | 16/04/2026 |
| **Tên tệp** | DATABASE_DESIGN.md |
| **Quyền truy cập** | Khoa CNTT |

---

## LỊCH SỬ THAY ĐỔI (REVISION HISTORY)

| Phiên bản | Người thực hiện | Ngày | Mô tả |
|-----------|----------------|------|-------|
| 1.0 | Hoàng Hải Minh Duy | 05/04/2026 | Bản nháp |
| 1.1 | Nguyễn Minh Hoàng | 07/04/2026 | Chỉnh sửa |
| 2.0 | Hoàng Hải Minh Duy | 16/04/2026 | Cập nhật tính năng thanh toán |
| 2.1 | Hoàng Hải Minh Duy | 16/04/2026 | Thêm báo cáo thống kê với biểu đồ (PB31) |

---

# 1. TỔNG QUAN

## 1.1. Mục đích

Tài liệu này giúp hiểu rõ hơn về Cơ sở dữ liệu của Website "Bán thiết bị điện tử tích hợp AI Chatbot". Cơ sở dữ liệu là nền tảng để triển khai phần mềm, cung cấp khả năng hiển thị thiết kế và thông tin cần thiết cho việc phát triển và hỗ trợ hệ thống.

## 1.2. Các bên liên quan

- **Kỹ sư hệ thống**: Thiết kế kiến trúc tổng thể.
- **Nhà thiết kế**: Thiết kế giao diện tổng thể.
- **Lập trình viên**: Phát triển phần mềm theo yêu cầu.
- **Người kiểm thử**: Tạo kế hoạch và thiết kế các trường hợp kiểm thử.

## 1.3. Phạm vi

- Mô tả cách lưu trữ dữ liệu cho Website bán thiết bị điện tử.
- Mô tả giao diện và cấu trúc của cơ sở dữ liệu.
- Tích hợp AI Chatbot với OpenAI/Gemini API.
- Hỗ trợ tính năng thanh toán đầy đủ với mã giảm giá.

---

# 2. THIẾT KẾ CƠ SỞ DỮ LIỆU

## 2.1. Lựa chọn cơ sở dữ liệu

**Hệ quản trị cơ sở dữ liệu:** MySQL

**Lý do lựa chọn:** 
- Tính linh hoạt cao
- Hiệu năng tốt với dữ liệu lớn
- Dễ quản lý và bảo trì
- Chi phí thấp (open-source)
- Hỗ trợ tốt với Python (SQLAlchemy)
- Tích hợp dễ dàng với FastAPI

## 2.2. Lược đồ cơ sở dữ liệu (Summary)

Hệ thống bao gồm **8 bảng chính**:

1. **nguoi_dung** - Quản lý tài khoản người dùng (Admin/Manager/User)
2. **danh_muc** - Phân loại sản phẩm điện tử
3. **san_pham** - Thông tin chi tiết sản phẩm
4. **don_hang** - Thông tin đơn hàng và thanh toán ⭐ CẬP NHẬT
5. **chi_tiet_don_hang** - Chi tiết sản phẩm trong đơn hàng
6. **danh_gia** - Đánh giá và nhận xét sản phẩm
7. **ma_giam_gia** - Mã giảm giá và khuyến mãi
8. **lich_su_chat** - Lịch sử chat với AI Chatbot

**Tính năng mới:**
- ✅ Thanh toán đầy đủ với thông tin giao hàng (PB10)
- ✅ Báo cáo thống kê với biểu đồ trực quan (PB31)

---

# 3. ĐỊNH NGHĨA CÁC BẢNG

## 3.1. Bảng Người dùng (nguoi_dung)

**Mô tả:** Lưu trữ thông tin tài khoản người dùng với 3 vai trò: Admin, Manager, User.

| Column | Data type | Size | Description |
|--------|-----------|------|-------------|
| id | INT | - | Mã người dùng (PK, Auto Increment) |
| email | VARCHAR | 255 | Email đăng nhập (Unique, Not Null) |
| mat_khau | VARCHAR | 255 | Mật khẩu đã hash (Not Null) |
| ho_ten | VARCHAR | 255 | Họ và tên |
| so_dien_thoai | VARCHAR | 20 | Số điện thoại |
| dia_chi | TEXT | - | Địa chỉ mặc định ⭐ MỚI |
| avatar | VARCHAR | 500 | URL ảnh đại diện ⭐ MỚI |
| vai_tro | VARCHAR | 20 | Vai trò: admin, manager, user (Default: 'user') |
| ngay_tao | DATETIME | - | Ngày tạo tài khoản (Default: NOW()) |
| ngay_cap_nhat | DATETIME | - | Ngày cập nhật ⭐ MỚI |

**Indexes:**
- `idx_email` (email) - Unique
- `idx_vai_tro` (vai_tro)

**Constraints:**
- PRIMARY KEY: id
- UNIQUE: email

---

## 3.2. Bảng Danh mục (danh_muc)

**Mô tả:** Phân loại sản phẩm điện tử (Laptop, Điện thoại, Tablet, Tai nghe, v.v.)

| Column | Data type | Size | Description |
|--------|-----------|------|-------------|
| id | INT | - | Mã danh mục (PK, Auto Increment) |
| ten | VARCHAR | 255 | Tên danh mục (Unique, Not Null) |

**Indexes:**
- `idx_ten_danh_muc` (ten) - Unique

**Constraints:**
- PRIMARY KEY: id
- UNIQUE: ten

---

## 3.3. Bảng Sản phẩm (san_pham)

**Mô tả:** Thông tin chi tiết về sản phẩm điện tử.

| Column | Data type | Size | Description |
|--------|-----------|------|-------------|
| id | INT | - | Mã sản phẩm (PK, Auto Increment) |
| ten | VARCHAR | 255 | Tên sản phẩm (Not Null) |
| gia | DECIMAL | 10,2 | Giá bán (VNĐ, Not Null) |
| mo_ta | TEXT | - | Mô tả chi tiết sản phẩm |
| hinh_anh | VARCHAR | 500 | URL hình ảnh sản phẩm |
| danh_muc_id | INT | - | Mã danh mục (FK, Not Null) |
| ton_kho | INT | - | Số lượng tồn kho (Default: 0) ⭐ MỚI |
| trang_thai | VARCHAR | 20 | Trạng thái: active, inactive (Default: 'active') ⭐ MỚI |
| ngay_tao | DATETIME | - | Ngày tạo sản phẩm (Default: NOW()) |
| ngay_cap_nhat | DATETIME | - | Ngày cập nhật ⭐ MỚI |

**Indexes:**
- `idx_danh_muc` (danh_muc_id)
- `idx_ten_san_pham` (ten)
- `idx_trang_thai` (trang_thai) ⭐ MỚI

**Constraints:**
- PRIMARY KEY: id
- FOREIGN KEY: danh_muc_id REFERENCES danh_muc(id) ON DELETE RESTRICT

---

## 3.4. Bảng Đơn hàng (don_hang) ⭐ ĐÃ CẬP NHẬT

**Mô tả:** Lưu trữ thông tin đơn hàng với đầy đủ thông tin giao hàng và mã giảm giá.

| Column | Data type | Size | Description |
|--------|-----------|------|-------------|
| id | INT | - | Mã đơn hàng (PK, Auto Increment) |
| nguoi_dung_id | INT | - | Mã người đặt hàng (FK, Not Null) |
| tong_tien | DECIMAL | 10,2 | Tổng tiền đơn hàng (sau giảm giá, Not Null) |
| trang_thai | VARCHAR | 20 | Trạng thái: pending, completed, cancelled (Default: 'pending') |
| phuong_thuc_thanh_toan | VARCHAR | 20 | Phương thức: cod, bank (Default: 'cod') |
| **ten_nguoi_nhan** | VARCHAR | 255 | Tên người nhận hàng ⭐ MỚI |
| **so_dien_thoai_nguoi_nhan** | VARCHAR | 20 | SĐT người nhận ⭐ MỚI |
| **dia_chi_giao_hang** | TEXT | - | Địa chỉ giao hàng ⭐ MỚI |
| **ghi_chu** | TEXT | - | Ghi chú đơn hàng ⭐ MỚI |
| **ma_giam_gia_id** | INT | - | ID mã giảm giá (FK) ⭐ MỚI |
| **so_tien_giam** | DECIMAL | 10,2 | Số tiền được giảm (Default: 0) ⭐ MỚI |
| ngay_tao | DATETIME | - | Ngày đặt hàng (Default: NOW()) |
| ngay_cap_nhat | DATETIME | - | Ngày cập nhật ⭐ MỚI |

**Indexes:**
- `idx_nguoi_dung` (nguoi_dung_id)
- `idx_trang_thai` (trang_thai)
- `idx_ngay_tao` (ngay_tao)
- `idx_ma_giam_gia` (ma_giam_gia_id) ⭐ MỚI

**Constraints:**
- PRIMARY KEY: id
- FOREIGN KEY: nguoi_dung_id REFERENCES nguoi_dung(id) ON DELETE CASCADE
- FOREIGN KEY: ma_giam_gia_id REFERENCES ma_giam_gia(id) ON DELETE SET NULL

**Validation Rules:**
- ten_nguoi_nhan: Bắt buộc, không để trống
- so_dien_thoai_nguoi_nhan: Bắt buộc, 10-11 số
- dia_chi_giao_hang: Bắt buộc, không để trống
- ma_giam_gia_id: Tùy chọn, validate hạn sử dụng, thời gian, giá trị đơn tối thiểu

---

## 3.5. Bảng Chi tiết đơn hàng (chi_tiet_don_hang)

**Mô tả:** Chi tiết từng sản phẩm trong đơn hàng.

| Column | Data type | Size | Description |
|--------|-----------|------|-------------|
| id | INT | - | Mã chi tiết (PK, Auto Increment) |
| don_hang_id | INT | - | Mã đơn hàng (FK, Not Null) |
| san_pham_id | INT | - | Mã sản phẩm (FK, Not Null) |
| so_luong | INT | - | Số lượng mua (Not Null) |

**Indexes:**
- `idx_don_hang` (don_hang_id)
- `idx_san_pham` (san_pham_id)

**Constraints:**
- PRIMARY KEY: id
- FOREIGN KEY: don_hang_id REFERENCES don_hang(id) ON DELETE CASCADE
- FOREIGN KEY: san_pham_id REFERENCES san_pham(id) ON DELETE RESTRICT

---

## 3.6. Bảng Đánh giá (danh_gia)

**Mô tả:** Đánh giá sản phẩm từ khách hàng (1-5 sao).

| Column | Data type | Size | Description |
|--------|-----------|------|-------------|
| id | INT | - | Mã đánh giá (PK, Auto Increment) |
| nguoi_dung_id | INT | - | Mã người đánh giá (FK, Not Null) |
| san_pham_id | INT | - | Mã sản phẩm (FK, Not Null) |
| diem_so | FLOAT | - | Điểm đánh giá (1-5 sao, Not Null) |
| binh_luan | TEXT | - | Bình luận đánh giá |
| ngay_tao | DATETIME | - | Ngày đánh giá (Default: NOW()) |

**Indexes:**
- `idx_nguoi_dung_dg` (nguoi_dung_id)
- `idx_san_pham_dg` (san_pham_id)
- `idx_diem_so` (diem_so)

**Constraints:**
- PRIMARY KEY: id
- FOREIGN KEY: nguoi_dung_id REFERENCES nguoi_dung(id) ON DELETE CASCADE
- FOREIGN KEY: san_pham_id REFERENCES san_pham(id) ON DELETE CASCADE

---

## 3.7. Bảng Mã giảm giá (ma_giam_gia)

**Mô tả:** Quản lý mã giảm giá và khuyến mãi.

| Column | Data type | Size | Description |
|--------|-----------|------|-------------|
| id | INT | - | Mã giảm giá (PK, Auto Increment) |
| ma_code | VARCHAR | 50 | Mã giảm giá (Unique, Not Null, VD: SUMMER2024) |
| mo_ta | VARCHAR | 255 | Mô tả mã giảm giá |
| loai_giam | VARCHAR | 20 | Loại: percent (%) hoặc fixed (VNĐ) (Default: 'percent') |
| gia_tri_giam | DECIMAL | 10,2 | Giá trị giảm (% hoặc VNĐ, Not Null) |
| gia_tri_don_toi_thieu | DECIMAL | 10,2 | Giá trị đơn hàng tối thiểu (Default: 0) |
| so_luong | INT | - | Số lượng mã có thể dùng (Default: 1) |
| da_su_dung | INT | - | Số lượng đã sử dụng (Default: 0) |
| ngay_bat_dau | DATETIME | - | Ngày bắt đầu hiệu lực (Default: NOW()) |
| ngay_ket_thuc | DATETIME | - | Ngày hết hạn |
| hoat_dong | BOOLEAN | - | Trạng thái hoạt động (Default: TRUE) |
| ngay_tao | DATETIME | - | Ngày tạo mã (Default: NOW()) |
| ngay_cap_nhat | DATETIME | - | Ngày cập nhật |

**Indexes:**
- `idx_ma_code` (ma_code) - Unique
- `idx_hoat_dong` (hoat_dong)
- `idx_ngay_bat_dau` (ngay_bat_dau)
- `idx_ngay_ket_thuc` (ngay_ket_thuc)

**Constraints:**
- PRIMARY KEY: id
- UNIQUE: ma_code

**Validation Rules:**
- Kiểm tra số lượng: da_su_dung < so_luong
- Kiểm tra thời gian: NOW() BETWEEN ngay_bat_dau AND ngay_ket_thuc
- Kiểm tra giá trị đơn: tong_tien >= gia_tri_don_toi_thieu

---

## 3.8. Bảng Lịch sử chat (lich_su_chat)

**Mô tả:** Lưu trữ hội thoại giữa user và AI Chatbot.

| Column | Data type | Size | Description |
|--------|-----------|------|-------------|
| id | INT | - | Mã lịch sử (PK, Auto Increment) |
| nguoi_dung_id | INT | - | Mã người dùng (FK, Not Null) |
| cau_hoi | TEXT | - | Câu hỏi từ người dùng (Not Null) |
| cau_tra_loi | TEXT | - | Câu trả lời từ AI (Not Null) |
| ngay_tao | DATETIME | - | Thời gian chat (Default: NOW()) |

**Indexes:**
- `idx_nguoi_dung_chat` (nguoi_dung_id)
- `idx_ngay_tao_chat` (ngay_tao)

**Constraints:**
- PRIMARY KEY: id
- FOREIGN KEY: nguoi_dung_id REFERENCES nguoi_dung(id) ON DELETE CASCADE

---

# 4. SƠ ĐỒ LIÊN KẾT (ERD)

## 4.1. Mối quan hệ chính

Hệ thống bao gồm các mối liên kết sau:

### 1. Người dùng và Vai trò
- **Mối quan hệ:** 1-N
- **Mô tả:** Một người dùng có một vai trò (admin/manager/user)

### 2. Sản phẩm và Danh mục
- **Mối quan hệ:** N-1
- **Mô tả:** Nhiều sản phẩm thuộc về một danh mục
- **Foreign Key:** san_pham.danh_muc_id → danh_muc.id
- **Delete Rule:** RESTRICT (không cho xóa danh mục nếu còn sản phẩm)

### 3. Người dùng và Đơn hàng
- **Mối quan hệ:** 1-N
- **Mô tả:** Một người dùng có thể tạo nhiều đơn hàng
- **Foreign Key:** don_hang.nguoi_dung_id → nguoi_dung.id
- **Delete Rule:** CASCADE (xóa user → xóa đơn hàng)

### 4. Đơn hàng và Chi tiết đơn hàng
- **Mối quan hệ:** 1-N
- **Mô tả:** Một đơn hàng có nhiều chi tiết sản phẩm
- **Foreign Key:** chi_tiet_don_hang.don_hang_id → don_hang.id
- **Delete Rule:** CASCADE (xóa đơn hàng → xóa chi tiết)

### 5. Sản phẩm và Chi tiết đơn hàng
- **Mối quan hệ:** 1-N
- **Mô tả:** Một sản phẩm có thể có trong nhiều đơn hàng
- **Foreign Key:** chi_tiet_don_hang.san_pham_id → san_pham.id
- **Delete Rule:** RESTRICT (không cho xóa sản phẩm nếu đã có trong đơn hàng)

### 6. Người dùng và Đánh giá
- **Mối quan hệ:** 1-N
- **Mô tả:** Một người dùng có thể đánh giá nhiều sản phẩm
- **Foreign Key:** danh_gia.nguoi_dung_id → nguoi_dung.id
- **Delete Rule:** CASCADE (xóa user → xóa đánh giá)

### 7. Sản phẩm và Đánh giá
- **Mối quan hệ:** 1-N
- **Mô tả:** Một sản phẩm có nhiều đánh giá
- **Foreign Key:** danh_gia.san_pham_id → san_pham.id
- **Delete Rule:** CASCADE (xóa sản phẩm → xóa đánh giá)

### 8. Mã giảm giá và Đơn hàng ⭐ MỚI
- **Mối quan hệ:** 1-N
- **Mô tả:** Một mã giảm giá có thể dùng cho nhiều đơn hàng
- **Foreign Key:** don_hang.ma_giam_gia_id → ma_giam_gia.id
- **Delete Rule:** SET NULL (xóa mã → đơn hàng vẫn giữ nhưng mã = null)

### 9. Người dùng và Lịch sử chat
- **Mối quan hệ:** 1-N
- **Mô tả:** Một người dùng có nhiều lịch sử chat
- **Foreign Key:** lich_su_chat.nguoi_dung_id → nguoi_dung.id
- **Delete Rule:** CASCADE (xóa user → xóa lịch sử chat)

---

# 5. QUY TRÌNH NGHIỆP VỤ

## 5.1. Quy trình Đăng ký và Đăng nhập

1. Khách vãng lai truy cập website
2. Đăng ký tài khoản với email, mật khẩu, họ tên, SĐT
3. Hệ thống hash mật khẩu và lưu vào bảng `nguoi_dung`
4. Vai trò mặc định: 'user'
5. Đăng nhập với email và mật khẩu
6. Hệ thống xác thực và cấp JWT token

## 5.2. Quy trình Mua hàng và Thanh toán ⭐ MỚI

### Bước 1: Thêm sản phẩm vào giỏ hàng
- User chọn sản phẩm và số lượng
- Lưu vào Context/LocalStorage (frontend)

### Bước 2: Xem giỏ hàng
- Hiển thị danh sách sản phẩm
- Tính tạm tính = SUM(gia × so_luong)

### Bước 3: Kiểm tra tồn kho
- API: `POST /api/san-pham/check-stock`
- Kiểm tra từng sản phẩm trong giỏ
- Nếu hết hàng → Hiển thị lỗi
- Nếu không đủ số lượng → Hiển thị lỗi

### Bước 4: Nhập thông tin giao hàng (BẮT BUỘC)
- Tên người nhận (validate không trống)
- Số điện thoại (validate 10-11 số)
- Địa chỉ giao hàng (validate không trống)
- Ghi chú (tùy chọn)

### Bước 5: Áp dụng mã giảm giá (TÙY CHỌN)
- User nhập mã giảm giá
- API: `POST /api/ma-giam-gia/validate`
- Kiểm tra:
  - Mã có tồn tại không
  - Còn lượt sử dụng không
  - Còn trong thời gian hiệu lực không
  - Đơn hàng đủ giá trị tối thiểu không
- Tính số tiền giảm:
  - Nếu loai_giam = 'percent': giảm = tạm_tính × (gia_tri_giam / 100)
  - Nếu loai_giam = 'fixed': giảm = gia_tri_giam
- Hiển thị số tiền giảm

### Bước 6: Chọn phương thức thanh toán
- COD: Thanh toán khi nhận hàng
- Bank: Chuyển khoản ngân hàng

### Bước 7: Xác nhận đặt hàng
- Tính tổng cuối = tạm_tính - giảm_giá
- Tạo record trong bảng `don_hang`:
  - Lưu đầy đủ thông tin giao hàng
  - Lưu ma_giam_gia_id và so_tien_giam
  - trang_thai = 'pending'
- Tạo records trong bảng `chi_tiet_don_hang`
- Trừ lượt sử dụng mã giảm giá (da_su_dung += 1)
- Xóa giỏ hàng
- Hiển thị mã đơn hàng

## 5.3. Quy trình Quản lý đơn hàng (Admin/Manager)

1. Xem danh sách đơn hàng
2. Lọc theo trạng thái, ngày tạo
3. Xem chi tiết đơn hàng (thông tin giao hàng, sản phẩm, mã giảm giá)
4. Cập nhật trạng thái:
   - pending → completed
   - pending → cancelled

## 5.4. Quy trình Chat với AI

1. User nhập câu hỏi
2. Gửi request đến backend
3. Backend gọi OpenAI/Gemini API
4. Nhận câu trả lời từ AI
5. Lưu vào bảng `lich_su_chat`
6. Trả về câu trả lời cho user

---

# 6. THỐNG KÊ VÀ BÁO CÁO (PB31)

## 6.1. Thống kê Dashboard

### 6.1.1. Doanh thu tháng hiện tại

```sql
-- Doanh thu tháng hiện tại
SELECT SUM(tong_tien) as current_month_revenue
FROM don_hang
WHERE MONTH(ngay_tao) = MONTH(NOW())
  AND YEAR(ngay_tao) = YEAR(NOW())
  AND trang_thai = 'completed';

-- Doanh thu tháng trước
SELECT SUM(tong_tien) as previous_month_revenue
FROM don_hang
WHERE MONTH(ngay_tao) = MONTH(DATE_SUB(NOW(), INTERVAL 1 MONTH))
  AND YEAR(ngay_tao) = YEAR(DATE_SUB(NOW(), INTERVAL 1 MONTH))
  AND trang_thai = 'completed';

-- Tính % biến động
-- change_percent = ((current - previous) / previous) * 100
```

### 6.1.2. Số lượng đơn hàng

```sql
-- Đơn hàng hoàn thành
SELECT COUNT(*) as completed_count
FROM don_hang
WHERE trang_thai = 'completed';

-- Tổng đơn hàng
SELECT COUNT(*) as total_count
FROM don_hang;
```

### 6.1.3. Pie Chart - Trạng thái đơn hàng

```sql
SELECT 
  trang_thai,
  COUNT(*) as count,
  COUNT(*) * 100.0 / (SELECT COUNT(*) FROM don_hang) as percentage
FROM don_hang
GROUP BY trang_thai;
```

### 6.1.4. Top 10 sản phẩm bán chạy

```sql
SELECT 
  sp.id,
  sp.ten,
  sp.gia,
  sp.hinh_anh,
  SUM(ctdh.so_luong) as total_sold,
  SUM(ctdh.so_luong * sp.gia) as total_revenue
FROM san_pham sp
JOIN chi_tiet_don_hang ctdh ON sp.id = ctdh.san_pham_id
JOIN don_hang dh ON ctdh.don_hang_id = dh.id
WHERE dh.trang_thai = 'completed'
GROUP BY sp.id, sp.ten, sp.gia, sp.hinh_anh
ORDER BY total_sold DESC
LIMIT 10;
```

## 6.2. Thống kê Doanh thu

### 6.2.1. Doanh thu theo tháng (12 tháng gần nhất)

```sql
SELECT 
  YEAR(ngay_tao) as year,
  MONTH(ngay_tao) as month,
  SUM(tong_tien) as revenue,
  COUNT(*) as order_count
FROM don_hang
WHERE trang_thai = 'completed'
GROUP BY YEAR(ngay_tao), MONTH(ngay_tao)
ORDER BY year DESC, month DESC
LIMIT 12;
```

### 6.2.2. Giá trị đơn hàng trung bình

```sql
SELECT AVG(tong_tien) as avg_order_value
FROM don_hang
WHERE trang_thai = 'completed';
```

### 6.2.3. Tổng tiền giảm giá

```sql
SELECT SUM(so_tien_giam) as total_discount
FROM don_hang
WHERE trang_thai = 'completed';
```

## 6.3. Thống kê Sản phẩm

### 6.3.1. Sản phẩm theo danh mục

```sql
SELECT 
  dm.ten as category,
  COUNT(sp.id) as count
FROM danh_muc dm
JOIN san_pham sp ON dm.id = sp.danh_muc_id
WHERE sp.trang_thai = 'active'
GROUP BY dm.id, dm.ten;
```

### 6.3.2. Sản phẩm sắp hết hàng

```sql
SELECT 
  sp.id,
  sp.ten,
  sp.ton_kho,
  sp.gia,
  dm.ten as danh_muc
FROM san_pham sp
JOIN danh_muc dm ON sp.danh_muc_id = dm.id
WHERE sp.ton_kho < 10 
  AND sp.ton_kho > 0
  AND sp.trang_thai = 'active'
ORDER BY sp.ton_kho ASC;
```

### 6.3.3. Thống kê giá

```sql
SELECT 
  MIN(gia) as min_price,
  MAX(gia) as max_price,
  AVG(gia) as avg_price
FROM san_pham
WHERE trang_thai = 'active';
```

## 6.4. Thống kê Mã giảm giá

### 6.4.1. Hiệu quả mã giảm giá

```sql
SELECT 
  mg.id,
  mg.ma_code,
  mg.mo_ta,
  COUNT(dh.id) as usage_count,
  SUM(dh.so_tien_giam) as total_discount,
  AVG(dh.tong_tien) as avg_order_value
FROM ma_giam_gia mg
LEFT JOIN don_hang dh ON mg.id = dh.ma_giam_gia_id
WHERE dh.trang_thai = 'completed'
GROUP BY mg.id, mg.ma_code, mg.mo_ta
ORDER BY total_discount DESC;
```

### 6.4.2. Tỷ lệ sử dụng mã giảm giá

```sql
SELECT 
  COUNT(CASE WHEN ma_giam_gia_id IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) as usage_rate
FROM don_hang
WHERE trang_thai = 'completed';
```

### 6.4.3. Mã giảm giá sắp hết hạn

```sql
SELECT 
  id,
  ma_code,
  mo_ta,
  ngay_ket_thuc,
  so_luong - da_su_dung as remaining_quantity,
  DATEDIFF(ngay_ket_thuc, NOW()) as days_left
FROM ma_giam_gia
WHERE hoat_dong = TRUE
  AND ngay_ket_thuc <= DATE_ADD(NOW(), INTERVAL 7 DAY)
  AND ngay_ket_thuc >= NOW()
ORDER BY ngay_ket_thuc ASC;
```

## 6.5. Thống kê Khách hàng

### 6.5.1. Top 10 khách hàng VIP

```sql
SELECT 
  nd.id,
  nd.ho_ten,
  nd.email,
  nd.so_dien_thoai,
  COUNT(dh.id) as total_orders,
  SUM(dh.tong_tien) as total_spent
FROM nguoi_dung nd
JOIN don_hang dh ON nd.id = dh.nguoi_dung_id
WHERE dh.trang_thai = 'completed'
GROUP BY nd.id, nd.ho_ten, nd.email, nd.so_dien_thoai
ORDER BY total_spent DESC
LIMIT 10;
```

### 6.5.2. Khách hàng mới trong tháng

```sql
SELECT COUNT(*) as new_customers
FROM nguoi_dung
WHERE vai_tro = 'user'
  AND MONTH(ngay_tao) = MONTH(NOW())
  AND YEAR(ngay_tao) = YEAR(NOW());
```

## 6.6. Biểu đồ (Charts)

### 6.6.1. Pie Chart - Trạng thái đơn hàng
- **Công nghệ:** Recharts (React charting library)
- **Loại:** Pie Chart
- **Dữ liệu:** Tỷ lệ % của pending, completed, cancelled
- **Màu sắc:**
  - Xanh lá (#10B981): Hoàn thành
  - Vàng (#FCD34D): Chờ xử lý
  - Đỏ (#EF4444): Đã hủy
- **Tính năng:**
  - Label hiển thị % trên biểu đồ
  - Tooltip khi hover
  - Legend phân biệt màu

### 6.6.2. Area Chart - Doanh thu 12 tháng
- **Công nghệ:** Recharts
- **Loại:** Area Chart (Biểu đồ vùng)
- **Dữ liệu:** Doanh thu 12 tháng gần nhất
- **Màu sắc:** Gradient xanh dương (#3B82F6)
- **Trục X:** Tháng/Năm (xoay 45 độ)
- **Trục Y:** Doanh thu (định dạng triệu VNĐ)
- **Tính năng:**
  - Gradient fill đẹp mắt
  - Grid lines để dễ đọc
  - Tooltip hiển thị số tiền chính xác

### 6.6.3. Bar Chart - Top 10 sản phẩm
- **Công nghệ:** Recharts
- **Loại:** Bar Chart (Biểu đồ cột kép)
- **Dữ liệu:** Top 10 sản phẩm bán chạy
- **Cột 1 (Tím #8B5CF6):** Số lượng bán (trục trái)
- **Cột 2 (Xanh #3B82F6):** Doanh thu (trục phải)
- **Tính năng:**
  - Dual Y-axis (2 trục Y)
  - Tên sản phẩm xoay 45 độ
  - Bo tròn góc cột
  - Tooltip hiển thị cả 2 giá trị

## 6.7. API Endpoints

### 6.7.1. Dashboard Statistics
```
GET /api/statistics/dashboard
Authorization: Bearer {token}
```

**Response:**
```json
{
  "revenue": {
    "current_month": 50000000,
    "previous_month": 45000000,
    "change_percent": 11.11,
    "month": 4,
    "year": 2026
  },
  "orders": {
    "completed_count": 150,
    "total_count": 200
  },
  "order_status_chart": [...],
  "top_selling_products": [...],
  "summary": {
    "total_products": 100,
    "total_users": 500,
    "total_orders": 200
  }
}
```

### 6.7.2. Revenue Statistics
```
GET /api/statistics/revenue?start_date=2026-01-01&end_date=2026-12-31
Authorization: Bearer {token}
```

### 6.7.3. Product Statistics
```
GET /api/statistics/products
Authorization: Bearer {token}
```

### 6.7.4. Coupon Statistics
```
GET /api/statistics/coupons
Authorization: Bearer {token}
```

### 6.7.5. Customer Statistics
```
GET /api/statistics/customers
Authorization: Bearer {token}
```

### 6.7.6. Export Statistics
```
GET /api/statistics/export?report_type=revenue&format=json
Authorization: Bearer {token}
```

---

# 7. BẢO MẬT VÀ HIỆU SUẤT

## 7.1. Bảo mật

### 7.1.1. Mật khẩu
- Sử dụng bcrypt để hash mật khẩu
- Không lưu mật khẩu dạng plain text
- Độ dài tối thiểu: 8 ký tự

### 7.1.2. Authentication
- Sử dụng JWT (JSON Web Token)
- Token có thời gian hết hạn
- Refresh token để gia hạn session

### 7.1.3. Authorization
- Phân quyền theo vai trò (RBAC)
- Admin: Toàn quyền
- Manager: Quản lý sản phẩm, đơn hàng, đánh giá, mã giảm giá
- User: Chỉ xem và mua hàng

### 7.1.4. SQL Injection
- Sử dụng ORM (SQLAlchemy)
- Parameterized queries
- Validate input từ user

### 7.1.5. XSS (Cross-Site Scripting)
- Sanitize input
- Escape output
- Content Security Policy

## 7.2. Hiệu suất

### 7.2.1. Indexes
- Tạo index cho các cột thường xuyên query
- Composite index cho query phức tạp
- Unique index cho các cột unique

### 7.2.2. Query Optimization
- Sử dụng JOIN thay vì multiple queries
- LIMIT kết quả khi không cần tất cả
- Sử dụng pagination
- Cache kết quả query thường xuyên

### 7.2.3. Database Connection
- Connection pooling
- Đóng connection sau khi sử dụng
- Timeout cho slow queries

### 7.2.4. Caching
- Cache sản phẩm nổi bật
- Cache danh mục
- Cache thống kê
- Sử dụng Redis cho caching

---

# 8. BACKUP VÀ RECOVERY

## 8.1. Backup Strategy

### 8.1.1. Full Backup
- Thực hiện: Hàng ngày lúc 2:00 AM
- Lưu trữ: 30 ngày
- Location: External storage

### 8.1.2. Incremental Backup
- Thực hiện: Mỗi 6 giờ
- Lưu trữ: 7 ngày

### 8.1.3. Transaction Log Backup
- Thực hiện: Mỗi giờ
- Lưu trữ: 24 giờ

## 8.2. Recovery Plan

### 8.2.1. Disaster Recovery
1. Restore từ full backup gần nhất
2. Apply incremental backups
3. Apply transaction logs
4. Verify data integrity
5. Test application

### 8.2.2. Point-in-Time Recovery
- Sử dụng transaction logs
- Restore đến thời điểm cụ thể
- Verify data consistency

---

# 9. MIGRATION VÀ VERSIONING

## 9.1. Database Migration

### 9.1.1. Migration Script
File: `backend/migrate_database.py`

Chức năng:
- Thêm các cột mới
- Tạo indexes
- Tạo foreign keys
- Cập nhật dữ liệu

### 9.1.2. Migration History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | 05/04/2026 | Initial database schema |
| 1.1 | 07/04/2026 | Add ton_kho, trang_thai to san_pham |
| 2.0 | 16/04/2026 | Add payment fields to don_hang |

## 9.2. Version Control

- Sử dụng Git để version control
- Mỗi migration có file riêng
- Rollback script cho mỗi migration
- Test migration trên staging trước production

---

# 10. TESTING

## 10.1. Unit Testing

### 10.1.1. Model Testing
- Test CRUD operations
- Test relationships
- Test constraints
- Test validation

### 10.1.2. API Testing
- Test endpoints
- Test authentication
- Test authorization
- Test error handling

## 10.2. Integration Testing

### 10.2.1. Database Integration
- Test connection
- Test transactions
- Test rollback
- Test concurrent access

### 10.2.2. API Integration
- Test complete workflows
- Test payment flow
- Test order creation
- Test coupon validation

## 10.3. Performance Testing

### 10.3.1. Load Testing
- Concurrent users: 100
- Response time: < 200ms
- Throughput: 1000 requests/second

### 10.3.2. Stress Testing
- Maximum load
- Breaking point
- Recovery time

---

# 11. DEPLOYMENT

## 11.1. Development Environment

- **Database:** MySQL 8.0 (XAMPP)
- **Backend:** FastAPI + Python 3.11
- **Frontend:** Next.js 14
- **OS:** Windows/Mac/Linux

## 11.2. Production Environment

- **Database:** MySQL 8.0 (Cloud)
- **Backend:** Docker container
- **Frontend:** Vercel/Netlify
- **CDN:** Cloudflare

## 11.3. Deployment Checklist

- [ ] Backup database
- [ ] Run migration scripts
- [ ] Test all endpoints
- [ ] Verify data integrity
- [ ] Update environment variables
- [ ] Deploy backend
- [ ] Deploy frontend
- [ ] Monitor logs
- [ ] Verify production

---

# 12. MONITORING VÀ MAINTENANCE

## 12.1. Monitoring

### 12.1.1. Database Monitoring
- Query performance
- Connection pool
- Disk space
- Memory usage
- CPU usage

### 12.1.2. Application Monitoring
- API response time
- Error rate
- User activity
- Payment success rate

## 12.2. Maintenance

### 12.2.1. Regular Maintenance
- Optimize tables (weekly)
- Update statistics (daily)
- Clean old logs (monthly)
- Review indexes (monthly)

### 12.2.2. Emergency Maintenance
- Database corruption
- Performance degradation
- Security breach
- Data loss

---

# 13. PHỤ LỤC

## 13.1. Tài liệu tham khảo

1. **MySQL Documentation**: https://dev.mysql.com/doc/
2. **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
3. **FastAPI Documentation**: https://fastapi.tiangolo.com/
4. **DBML Documentation**: https://dbml.dbdiagram.io/docs/

## 13.2. Công cụ

1. **dbdiagram.io**: Visualize database schema
2. **MySQL Workbench**: Database design and management
3. **phpMyAdmin**: Web-based database management
4. **DBeaver**: Universal database tool

## 13.3. Liên hệ

**Nhóm phát triển:**
- Hoàng Hải Minh Duy: hoanghaiminhduy20004@gmail.com
- Phạm Hữu Học: Phamhuuhoc3014q@gmail.com
- Lê Trần Anh Tuấn: tuan81609@gmail.com
- Nguyễn Minh Hoàng: Hominh8951@gmail.com
- Hoàng Nhật Khánh: Khanhịpk9@gmail.com

**Giảng viên hướng dẫn:**
- ThS. Lưu Văn Hiền

---

# 14. KẾT LUẬN

Tài liệu này mô tả chi tiết thiết kế cơ sở dữ liệu cho Website bán thiết bị điện tử tích hợp AI Chatbot. Database được thiết kế với 8 bảng chính, hỗ trợ đầy đủ các tính năng:

✅ Quản lý người dùng với 3 vai trò  
✅ Quản lý sản phẩm và danh mục  
✅ Quản lý đơn hàng với thông tin giao hàng đầy đủ  
✅ Hệ thống mã giảm giá với validation đầy đủ  
✅ Đánh giá sản phẩm  
✅ Tích hợp AI Chatbot  

Database được tối ưu với indexes, foreign keys, và validation rules để đảm bảo tính toàn vẹn dữ liệu và hiệu suất cao.

---

**Ngày hoàn thành:** 16/04/2026  
**Phiên bản:** 2.1 (Có báo cáo thống kê với biểu đồ)  
**Trạng thái:** Đã phê duyệt  

**Tính năng mới:**
- ✅ Thanh toán đầy đủ (PB10)
- ✅ Báo cáo thống kê với biểu đồ (PB31)
  - Pie Chart (Trạng thái đơn hàng)
  - Area Chart (Doanh thu 12 tháng)
  - Bar Chart (Top 10 sản phẩm)

---

**CHỮ KÝ PHÊ DUYỆT**

| Vai trò | Họ tên | Chữ ký | Ngày |
|---------|--------|--------|------|
| Giảng viên hướng dẫn | ThS. Lưu Văn Hiền | | …./…./2026 |
| Trưởng nhóm | Hoàng Hải Minh Duy | | …./…./2026 |
| Thành viên | Phạm Hữu Học | | …./…./2026 |
| Thành viên | Lê Trần Anh Tuấn | | …./…./2026 |
| Thành viên | Nguyễn Minh Hoàng | | …./…./2026 |
| Thành viên | Hoàng Nhật Khánh | | …./…./2026 |

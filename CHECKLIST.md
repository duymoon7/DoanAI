# ✅ CHECKLIST CÀI ĐẶT

Đánh dấu ✅ khi hoàn thành mỗi bước.

---

## 📋 TRƯỚC KHI BẮT ĐẦU

- [ ] Đã đọc [GETTING_STARTED.md](GETTING_STARTED.md)
- [ ] Đã đọc [HUONG_DAN_CAI_DAT.md](HUONG_DAN_CAI_DAT.md)
- [ ] Có kết nối internet ổn định
- [ ] Có ít nhất 5GB ổ cứng trống
- [ ] Có ít nhất 4GB RAM trống

---

## 🛠️ CÀI ĐẶT CÔNG CỤ

### Docker Desktop
- [ ] Đã tải Docker Desktop
- [ ] Đã cài đặt Docker Desktop
- [ ] Docker Desktop đang chạy
- [ ] Biểu tượng Docker màu xanh (không phải xám)
- [ ] Chạy `docker --version` thành công
- [ ] Chạy `docker-compose --version` thành công

### Node.js
- [ ] Đã tải Node.js LTS
- [ ] Đã cài đặt Node.js
- [ ] Chạy `node --version` thành công (v18+)
- [ ] Chạy `npm --version` thành công (v9+)

### Git
- [ ] Đã cài đặt Git
- [ ] Chạy `git --version` thành công

---

## 📥 CLONE DỰ ÁN

- [ ] Đã mở Terminal/Command Prompt
- [ ] Đã di chuyển đến thư mục muốn lưu dự án
- [ ] Đã chạy `git clone <URL>`
- [ ] Đã di chuyển vào thư mục dự án: `cd doanAi`
- [ ] Thấy các thư mục: backend/, frontend/, docker-compose.yml

---

## ⚙️ CẤU HÌNH

- [ ] Đã kiểm tra file `backend/.env` tồn tại
- [ ] Đã kiểm tra file `frontend/.env.local` tồn tại
- [ ] Không cần tạo file .env mới (đã có sẵn)

---

## 🚀 KHỞI ĐỘNG BACKEND

- [ ] Docker Desktop đang chạy
- [ ] Đã mở terminal trong thư mục dự án
- [ ] Đã chạy `docker-compose up --build`
- [ ] Đợi 1-2 phút
- [ ] Thấy log: "✅ Application started successfully!"
- [ ] Thấy log: "📚 API Documentation: http://localhost:8000/docs"
- [ ] Không đóng terminal này

---

## 🎨 KHỞI ĐỘNG FRONTEND

- [ ] Đã mở terminal MỚI
- [ ] Đã di chuyển vào thư mục frontend: `cd frontend`
- [ ] Đã chạy `npm install`
- [ ] Đợi 2-3 phút cho npm install
- [ ] Đã chạy `npm run dev`
- [ ] Thấy log: "✓ Ready in 677ms"
- [ ] Thấy log: "- Local: http://localhost:3000"

---

## ✅ KIỂM TRA

### Docker Containers
- [ ] Chạy `docker-compose ps` trong terminal mới
- [ ] Thấy 3 containers:
  - [ ] electronics_postgres (Up, healthy)
  - [ ] electronics_pgadmin (Up)
  - [ ] electronics_backend (Up, healthy)

### Backend Health
- [ ] Mở browser: http://localhost:8000/health
- [ ] Thấy: `{"status":"healthy","database":"connected"}`

### Backend API
- [ ] Mở browser: http://localhost:8000/docs
- [ ] Thấy Swagger UI
- [ ] Thấy danh sách API endpoints

### Backend Products
- [ ] Mở browser: http://localhost:8000/api/san-pham
- [ ] Thấy danh sách 14 sản phẩm
- [ ] Sản phẩm có đầy đủ thông tin (ten, gia, hinh_anh, etc.)

### Frontend
- [ ] Mở browser: http://localhost:3000
- [ ] Thấy trang chủ
- [ ] Thấy 14 sản phẩm hiển thị
- [ ] Giá tiền hiển thị đúng định dạng VNĐ
- [ ] Có thể click vào sản phẩm
- [ ] Trang chi tiết sản phẩm hiển thị đúng
- [ ] Có thể thêm vào giỏ hàng
- [ ] Giỏ hàng hoạt động đúng
- [ ] Có thể tìm kiếm sản phẩm
- [ ] Có thể lọc theo danh mục

### pgAdmin (Optional)
- [ ] Mở browser: http://localhost:5050
- [ ] Thấy trang login pgAdmin
- [ ] Đăng nhập với admin@admin.com / admin
- [ ] Có thể kết nối đến PostgreSQL server

---

## 🎯 TÍNH NĂNG

### Frontend
- [ ] Trang chủ hoạt động
- [ ] Danh sách sản phẩm hoạt động
- [ ] Chi tiết sản phẩm hoạt động
- [ ] Giỏ hàng hoạt động
- [ ] Thêm vào giỏ hàng hoạt động
- [ ] Xóa khỏi giỏ hàng hoạt động
- [ ] Cập nhật số lượng hoạt động
- [ ] Tìm kiếm hoạt động
- [ ] Lọc theo danh mục hoạt động
- [ ] Responsive design (mobile) hoạt động

### Backend
- [ ] API GET /san-pham hoạt động
- [ ] API GET /san-pham/{id} hoạt động
- [ ] API GET /danh-muc hoạt động
- [ ] Health check hoạt động
- [ ] Swagger UI hoạt động
- [ ] Database có 6 tables
- [ ] Database có 6 danh mục
- [ ] Database có 14 sản phẩm

---

## 📊 DỮ LIỆU

### Danh Mục (6)
- [ ] Điện thoại
- [ ] Laptop
- [ ] Tablet
- [ ] Phụ kiện
- [ ] Tai nghe
- [ ] Đồng hồ thông minh

### Sản Phẩm (14)
- [ ] iPhone 15 Pro Max
- [ ] Samsung Galaxy S24 Ultra
- [ ] Xiaomi 14 Ultra
- [ ] MacBook Pro 14 M3
- [ ] Dell XPS 15
- [ ] ASUS ROG Zephyrus G14
- [ ] iPad Pro M2 11 inch
- [ ] Samsung Galaxy Tab S9
- [ ] AirPods Pro 2
- [ ] Sony WH-1000XM5
- [ ] Apple Watch Series 9
- [ ] Samsung Galaxy Watch 6
- [ ] Sạc nhanh Apple 20W
- [ ] Cáp sạc Type-C to Lightning

---

## 🐛 XỬ LÝ LỖI

Nếu có lỗi, đã thử:

- [ ] Đọc phần "Xử Lý Lỗi" trong [HUONG_DAN_CAI_DAT.md](HUONG_DAN_CAI_DAT.md)
- [ ] Kiểm tra Docker Desktop đang chạy
- [ ] Kiểm tra logs: `docker-compose logs -f`
- [ ] Restart backend: `docker-compose restart backend`
- [ ] Restart frontend: `Ctrl+C` rồi `npm run dev`
- [ ] Xem console browser (F12)
- [ ] Kiểm tra ports không bị chiếm dụng

---

## 📚 TÀI LIỆU

Đã đọc:

- [ ] [GETTING_STARTED.md](GETTING_STARTED.md) - Bắt đầu nhanh
- [ ] [HUONG_DAN_CAI_DAT.md](HUONG_DAN_CAI_DAT.md) - Hướng dẫn chi tiết
- [ ] [SUCCESS.md](SUCCESS.md) - Hướng dẫn sử dụng
- [ ] [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Tham khảo nhanh
- [ ] [README.md](README.md) - Tổng quan dự án

---

## 🎉 HOÀN THÀNH

Nếu tất cả checklist đã ✅, chúc mừng bạn!

### Truy cập ngay:
- 🛍️ **Frontend**: http://localhost:3000
- 📚 **API Docs**: http://localhost:8000/docs
- 🗄️ **pgAdmin**: http://localhost:5050

### Lần sau chỉ cần:
```bash
# Terminal 1
docker-compose up -d

# Terminal 2
cd frontend
npm run dev
```

---

## 📝 GHI CHÚ

Ghi lại các vấn đề gặp phải và cách giải quyết:

```
[Ghi chú của bạn ở đây]




```

---

**Ngày hoàn thành**: _______________

**Thời gian cài đặt**: _______________

**Đánh giá**: ⭐⭐⭐⭐⭐

---

**Chúc mừng bạn đã cài đặt thành công! 🎊**

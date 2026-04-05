# 📖 HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY DỰ ÁN

Hướng dẫn chi tiết từ A-Z để cài đặt và chạy dự án E-Commerce sau khi clone từ Git.

---

## 📋 MỤC LỤC

1. [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
2. [Cài Đặt Công Cụ](#cài-đặt-công-cụ)
3. [Clone Dự Án](#clone-dự-án)
4. [Cấu Hình Dự Án](#cấu-hình-dự-án)
5. [Chạy Dự Án](#chạy-dự-án)
6. [Kiểm Tra](#kiểm-tra)
7. [Xử Lý Lỗi](#xử-lý-lỗi)

---

## 🖥️ YÊU CẦU HỆ THỐNG

### Hệ điều hành:
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 20.04+)

### Phần cứng tối thiểu:
- RAM: 4GB (khuyến nghị 8GB)
- Ổ cứng trống: 5GB
- CPU: 2 cores

---

## 🛠️ CÀI ĐẶT CÔNG CỤ

### 1. Cài Đặt Docker Desktop

Docker Desktop bao gồm Docker và Docker Compose.

#### Windows:
1. Tải Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Chạy file cài đặt `Docker Desktop Installer.exe`
3. Làm theo hướng dẫn cài đặt
4. Khởi động lại máy tính
5. Mở Docker Desktop và đợi nó khởi động

#### macOS:
1. Tải Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Kéo Docker.app vào thư mục Applications
3. Mở Docker từ Applications
4. Cho phép các quyền cần thiết

#### Linux (Ubuntu):
```bash
# Cập nhật package
sudo apt-get update

# Cài đặt Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Thêm user vào docker group
sudo usermod -aG docker $USER

# Cài đặt Docker Compose
sudo apt-get install docker-compose-plugin

# Khởi động lại để áp dụng thay đổi
sudo reboot
```

#### Kiểm tra cài đặt:
```bash
docker --version
docker-compose --version
```

Kết quả mong đợi:
```
Docker version 24.x.x
Docker Compose version v2.x.x
```

### 2. Cài Đặt Node.js

#### Windows & macOS:
1. Tải Node.js LTS: https://nodejs.org/
2. Chạy file cài đặt
3. Làm theo hướng dẫn (chọn tất cả options mặc định)

#### Linux (Ubuntu):
```bash
# Cài đặt Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### Kiểm tra cài đặt:
```bash
node --version
npm --version
```

Kết quả mong đợi:
```
v18.x.x hoặc cao hơn
9.x.x hoặc cao hơn
```

### 3. Cài Đặt Git (nếu chưa có)

#### Windows:
1. Tải Git: https://git-scm.com/download/win
2. Chạy file cài đặt
3. Chọn tất cả options mặc định

#### macOS:
```bash
# Sử dụng Homebrew
brew install git

# Hoặc tải từ: https://git-scm.com/download/mac
```

#### Linux (Ubuntu):
```bash
sudo apt-get install git
```

#### Kiểm tra cài đặt:
```bash
git --version
```

---

## 📥 CLONE DỰ ÁN

### 1. Mở Terminal/Command Prompt

**Windows:**
- Nhấn `Win + R`
- Gõ `cmd` hoặc `powershell`
- Nhấn Enter

**macOS:**
- Nhấn `Cmd + Space`
- Gõ `terminal`
- Nhấn Enter

**Linux:**
- Nhấn `Ctrl + Alt + T`

### 2. Di chuyển đến thư mục muốn lưu dự án

```bash
# Ví dụ: Di chuyển đến Desktop
cd Desktop

# Hoặc tạo thư mục mới
mkdir Projects
cd Projects
```

### 3. Clone repository

```bash
git clone <URL_REPOSITORY_CUA_BAN>
```

Ví dụ:
```bash
git clone https://github.com/username/doanAi.git
```

### 4. Di chuyển vào thư mục dự án

```bash
cd doanAi
```

---

## ⚙️ CẤU HÌNH DỰ ÁN

### 1. Kiểm tra cấu trúc thư mục

```bash
# Windows
dir

# macOS/Linux
ls -la
```

Bạn sẽ thấy:
```
backend/
frontend/
docker-compose.yml
README.md
...
```

### 2. Cấu hình Backend (Không cần làm gì)

File `.env` đã được cấu hình sẵn trong `backend/.env`:
```env
DB_HOST=postgres
DB_PORT=5432
DB_NAME=electronics_db
DB_USER=postgres
DB_PASSWORD=123456
```

⚠️ **Lưu ý**: Không cần tạo file `.env` mới, đã có sẵn!

### 3. Cấu hình Frontend

Kiểm tra file `frontend/.env.local`:

```bash
# Windows
type frontend\.env.local

# macOS/Linux
cat frontend/.env.local
```

Nội dung:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

⚠️ **Lưu ý**: File này đã có sẵn, không cần tạo mới!

---

## 🚀 CHẠY DỰ ÁN

### BƯỚC 1: Khởi động Docker Desktop

**Quan trọng**: Đảm bảo Docker Desktop đang chạy!

**Windows/macOS:**
- Mở Docker Desktop từ Start Menu/Applications
- Đợi cho đến khi thấy biểu tượng Docker ở system tray
- Biểu tượng Docker phải màu xanh (không phải xám)

**Linux:**
```bash
sudo systemctl start docker
```

### BƯỚC 2: Khởi động Backend (Docker)

Mở terminal trong thư mục dự án:

```bash
# Đảm bảo bạn đang ở thư mục gốc của dự án
cd doanAi

# Khởi động Docker containers
docker-compose up --build
```

⏳ **Đợi 1-2 phút** để Docker:
- Tải images (lần đầu tiên)
- Build backend image
- Khởi động PostgreSQL
- Khởi động pgAdmin
- Khởi động Backend
- Tạo tables tự động
- Seed dữ liệu tự động

#### Dấu hiệu thành công:

Bạn sẽ thấy các dòng log như:
```
electronics_postgres   | database system is ready to accept connections
electronics_backend    | ✅ Database connection successful!
electronics_backend    | ✅ Application started successfully!
electronics_backend    | 📚 API Documentation: http://localhost:8000/docs
electronics_pgadmin    | Listening at: http://[::]:80
```

⚠️ **Lưu ý**: 
- Không đóng terminal này!
- Nếu muốn chạy ở background, dùng: `docker-compose up -d`

### BƯỚC 3: Cài đặt Frontend Dependencies

**Mở terminal MỚI** (giữ terminal cũ đang chạy Docker):

```bash
# Di chuyển vào thư mục frontend
cd frontend

# Cài đặt dependencies
npm install
```

⏳ **Đợi 2-3 phút** để npm cài đặt tất cả packages.

### BƯỚC 4: Khởi động Frontend

Trong cùng terminal frontend:

```bash
npm run dev
```

⏳ **Đợi 10-20 giây** để Next.js khởi động.

#### Dấu hiệu thành công:

```
▲ Next.js 16.2.2 (Turbopack)
- Local:         http://localhost:3000
✓ Ready in 677ms
```

---

## ✅ KIỂM TRA

### 1. Kiểm tra Docker Containers

Mở terminal mới:

```bash
docker-compose ps
```

Kết quả mong đợi (3 containers "Up"):
```
NAME                   STATUS
electronics_backend    Up (healthy)
electronics_pgadmin    Up
electronics_postgres   Up (healthy)
```

### 2. Kiểm tra Backend

Mở trình duyệt và truy cập:

**Health Check:**
```
http://localhost:8000/health
```

Kết quả mong đợi:
```json
{"status":"healthy","database":"connected"}
```

**API Documentation:**
```
http://localhost:8000/docs
```

Bạn sẽ thấy Swagger UI với tất cả API endpoints.

**Kiểm tra sản phẩm:**
```
http://localhost:8000/api/san-pham
```

Bạn sẽ thấy danh sách 14 sản phẩm.

### 3. Kiểm tra Frontend

Mở trình duyệt:
```
http://localhost:3000
```

Bạn sẽ thấy:
- ✅ Trang chủ với danh sách sản phẩm
- ✅ 14 sản phẩm hiển thị
- ✅ Giá tiền định dạng VNĐ
- ✅ Có thể click vào sản phẩm
- ✅ Có thể thêm vào giỏ hàng

### 4. Kiểm tra pgAdmin (Optional)

```
http://localhost:5050
```

Đăng nhập:
- Email: `admin@admin.com`
- Password: `admin`

---

## 🎯 TÓM TẮT NHANH

Sau khi clone, chỉ cần 4 lệnh:

```bash
# 1. Khởi động Docker (terminal 1)
docker-compose up --build

# 2. Cài đặt frontend (terminal 2)
cd frontend
npm install

# 3. Chạy frontend
npm run dev

# 4. Truy cập
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/docs
# pgAdmin: http://localhost:5050
```

---

## 🐛 XỬ LÝ LỖI

### Lỗi 1: "Docker daemon is not running"

**Nguyên nhân**: Docker Desktop chưa khởi động

**Giải pháp**:
1. Mở Docker Desktop
2. Đợi cho đến khi biểu tượng Docker màu xanh
3. Chạy lại `docker-compose up --build`

### Lỗi 2: "Port 8000 is already in use"

**Nguyên nhân**: Port đã được sử dụng bởi ứng dụng khác

**Giải pháp Windows**:
```bash
# Tìm process đang dùng port
netstat -ano | findstr :8000

# Kill process (thay <PID> bằng số PID tìm được)
taskkill /PID <PID> /F
```

**Giải pháp macOS/Linux**:
```bash
# Tìm và kill process
lsof -ti:8000 | xargs kill -9
```

### Lỗi 3: "Port 3000 is already in use"

**Giải pháp**: Tương tự lỗi 2, thay 8000 bằng 3000

### Lỗi 4: "npm install" bị lỗi

**Giải pháp**:
```bash
# Xóa node_modules và package-lock.json
rm -rf node_modules package-lock.json

# Cài đặt lại
npm install
```

### Lỗi 5: Backend không kết nối database

**Giải pháp**:
```bash
# Xem logs
docker-compose logs backend

# Restart backend
docker-compose restart backend

# Nếu vẫn lỗi, restart tất cả
docker-compose down
docker-compose up --build
```

### Lỗi 6: Frontend không hiển thị sản phẩm

**Giải pháp**:
1. Kiểm tra Backend đang chạy: http://localhost:8000/health
2. Kiểm tra API có dữ liệu: http://localhost:8000/api/san-pham
3. Xem console trong browser (F12)
4. Restart frontend: `Ctrl+C` rồi `npm run dev`

### Lỗi 7: Database không có dữ liệu

**Giải pháp**:
```bash
# Chạy seed script thủ công
docker-compose exec backend python seed_initial_data.py
```

### Lỗi 8: "Cannot connect to Docker daemon"

**Giải pháp Linux**:
```bash
# Thêm user vào docker group
sudo usermod -aG docker $USER

# Logout và login lại
# Hoặc chạy:
newgrp docker
```

---

## 🛑 DỪNG DỰ ÁN

### Dừng Frontend
Trong terminal đang chạy frontend:
```
Ctrl + C
```

### Dừng Backend
Trong terminal đang chạy Docker:
```
Ctrl + C
```

Sau đó:
```bash
docker-compose down
```

### Dừng và xóa tất cả dữ liệu
```bash
docker-compose down -v
```

⚠️ **Cảnh báo**: Lệnh này sẽ xóa tất cả dữ liệu trong database!

---

## 🔄 KHỞI ĐỘNG LẠI

### Lần sau chỉ cần:

```bash
# Terminal 1: Backend
docker-compose up -d

# Terminal 2: Frontend
cd frontend
npm run dev
```

Không cần `--build` và `npm install` nữa!

---

## 📊 DỮ LIỆU MẶC ĐỊNH

Sau khi chạy thành công, hệ thống có sẵn:

### Danh mục (6):
- Điện thoại
- Laptop
- Tablet
- Phụ kiện
- Tai nghe
- Đồng hồ thông minh

### Sản phẩm (14):
- iPhone 15 Pro Max (29,990,000đ)
- Samsung Galaxy S24 Ultra (27,990,000đ)
- Xiaomi 14 Ultra (24,990,000đ)
- MacBook Pro 14 M3 (52,990,000đ)
- Dell XPS 15 (45,990,000đ)
- ASUS ROG Zephyrus G14 (42,990,000đ)
- iPad Pro M2 11 inch (21,990,000đ)
- Samsung Galaxy Tab S9 (18,990,000đ)
- AirPods Pro 2 (5,990,000đ)
- Sony WH-1000XM5 (7,990,000đ)
- Apple Watch Series 9 (10,990,000đ)
- Samsung Galaxy Watch 6 (7,990,000đ)
- Sạc nhanh Apple 20W (490,000đ)
- Cáp sạc Type-C to Lightning (390,000đ)

---

## 📚 TÀI LIỆU THAM KHẢO

Sau khi chạy thành công, đọc thêm:

- **[SUCCESS.md](SUCCESS.md)** - Hướng dẫn sử dụng chi tiết
- **[RUNNING_NOW.md](RUNNING_NOW.md)** - Thông tin về ứng dụng đang chạy
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Tham khảo nhanh các lệnh
- **[PGADMIN_SETUP.md](PGADMIN_SETUP.md)** - Hướng dẫn sử dụng pgAdmin
- **[README.md](README.md)** - Tổng quan dự án

---

## 💡 MẸO HỮU ÍCH

### Chạy Docker ở background:
```bash
docker-compose up -d
```

### Xem logs:
```bash
# Tất cả services
docker-compose logs -f

# Chỉ backend
docker-compose logs -f backend
```

### Restart một service:
```bash
docker-compose restart backend
```

### Kiểm tra trạng thái:
```bash
docker-compose ps
```

### Truy cập PostgreSQL shell:
```bash
docker-compose exec postgres psql -U postgres -d electronics_db
```

---

## 🎓 VIDEO HƯỚNG DẪN (Nếu có)

[Link video hướng dẫn chi tiết]

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề không có trong tài liệu:

1. Kiểm tra logs: `docker-compose logs -f`
2. Kiểm tra health: http://localhost:8000/health
3. Xem console browser (F12)
4. Đọc phần [Xử Lý Lỗi](#xử-lý-lỗi)
5. Liên hệ: [email hoặc link support]

---

## ✅ CHECKLIST CÀI ĐẶT

Đánh dấu khi hoàn thành:

- [ ] Đã cài Docker Desktop
- [ ] Đã cài Node.js
- [ ] Đã cài Git
- [ ] Đã clone repository
- [ ] Docker Desktop đang chạy
- [ ] Đã chạy `docker-compose up --build`
- [ ] Thấy 3 containers "Up"
- [ ] Backend health check OK
- [ ] Đã chạy `npm install` trong frontend
- [ ] Đã chạy `npm run dev`
- [ ] Frontend hiển thị trang chủ
- [ ] Thấy 14 sản phẩm
- [ ] Có thể thêm vào giỏ hàng

---

## 🎉 HOÀN THÀNH!

Nếu tất cả checklist đã hoàn thành, chúc mừng bạn đã cài đặt thành công!

**Truy cập ngay:**
- 🛍️ Frontend: http://localhost:3000
- 📚 API Docs: http://localhost:8000/docs
- 🗄️ pgAdmin: http://localhost:5050

**Chúc bạn code vui vẻ! 🚀**

---

**Cập nhật lần cuối**: [Ngày tháng năm]
**Phiên bản**: 1.0

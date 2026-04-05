# 🚀 GETTING STARTED - Bắt Đầu Nhanh

Hướng dẫn nhanh để chạy dự án sau khi clone.

---

## ⚡ NHANH NHẤT (3 Bước)

### Bước 1: Cài đặt công cụ cần thiết

- **Docker Desktop**: https://www.docker.com/products/docker-desktop/
- **Node.js 18+**: https://nodejs.org/

### Bước 2: Clone và cài đặt

```bash
# Clone repository
git clone <URL_REPOSITORY>
cd doanAi

# Khởi động backend (terminal 1)
docker-compose up --build

# Cài đặt frontend (terminal 2 - mở terminal mới)
cd frontend
npm install
npm run dev
```

### Bước 3: Truy cập

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050

---

## 📋 YÊU CẦU

### Phải có:
- Docker Desktop (đang chạy)
- Node.js 18+
- 4GB RAM trống
- 5GB ổ cứng trống

### Ports cần thiết:
- 3000 (Frontend)
- 8000 (Backend)
- 5432 (PostgreSQL)
- 5050 (pgAdmin)

---

## 🎯 CHI TIẾT TỪNG BƯỚC

### 1. Cài đặt Docker Desktop

**Windows/macOS:**
1. Tải: https://www.docker.com/products/docker-desktop/
2. Cài đặt và khởi động
3. Đợi biểu tượng Docker màu xanh

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

Kiểm tra:
```bash
docker --version
docker-compose --version
```

### 2. Cài đặt Node.js

**Windows/macOS:**
- Tải: https://nodejs.org/
- Chọn phiên bản LTS
- Cài đặt với options mặc định

**Linux:**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

Kiểm tra:
```bash
node --version  # v18.x.x hoặc cao hơn
npm --version   # 9.x.x hoặc cao hơn
```

### 3. Clone Repository

```bash
git clone <URL_REPOSITORY>
cd doanAi
```

### 4. Khởi động Backend

**Quan trọng**: Đảm bảo Docker Desktop đang chạy!

```bash
docker-compose up --build
```

Đợi 1-2 phút cho đến khi thấy:
```
✅ Application started successfully!
📚 API Documentation: http://localhost:8000/docs
```

**Lưu ý**: Giữ terminal này mở!

### 5. Khởi động Frontend

Mở terminal MỚI:

```bash
cd frontend
npm install
npm run dev
```

Đợi cho đến khi thấy:
```
✓ Ready in 677ms
- Local: http://localhost:3000
```

---

## ✅ KIỂM TRA

### Backend đang chạy?
```bash
curl http://localhost:8000/health
```

Kết quả: `{"status":"healthy","database":"connected"}`

### Frontend đang chạy?
Mở browser: http://localhost:3000

Bạn sẽ thấy 14 sản phẩm.

### Docker containers?
```bash
docker-compose ps
```

Kết quả: 3 containers "Up"

---

## 🐛 GẶP LỖI?

### Docker không chạy
```bash
# Kiểm tra Docker Desktop đã mở chưa
# Windows/Mac: Mở Docker Desktop
# Linux: sudo systemctl start docker
```

### Port đã được sử dụng
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### Backend không kết nối database
```bash
docker-compose restart backend
docker-compose logs backend
```

### Frontend không hiển thị sản phẩm
1. Kiểm tra backend: http://localhost:8000/health
2. Xem console browser (F12)
3. Restart: `Ctrl+C` rồi `npm run dev`

### Database không có dữ liệu
```bash
docker-compose exec backend python seed_initial_data.py
```

---

## 🛑 DỪNG DỰ ÁN

```bash
# Dừng frontend: Ctrl + C trong terminal frontend

# Dừng backend:
docker-compose down
```

---

## 🔄 KHỞI ĐỘNG LẠI

Lần sau chỉ cần:

```bash
# Terminal 1
docker-compose up -d

# Terminal 2
cd frontend
npm run dev
```

---

## 📊 DỮ LIỆU MẶC ĐỊNH

Sau khi chạy, hệ thống có sẵn:
- ✅ 6 danh mục
- ✅ 14 sản phẩm
- ✅ Tất cả API endpoints

---

## 📚 TÀI LIỆU CHI TIẾT

- **[HUONG_DAN_CAI_DAT.md](HUONG_DAN_CAI_DAT.md)** ⭐ - Hướng dẫn chi tiết từ A-Z
- **[SUCCESS.md](SUCCESS.md)** - Hướng dẫn sử dụng
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Tham khảo nhanh
- **[README.md](README.md)** - Tổng quan dự án

---

## 🎯 CÔNG NGHỆ SỬ DỤNG

### Backend:
- FastAPI (Python)
- PostgreSQL
- SQLAlchemy
- Docker

### Frontend:
- Next.js 14
- TypeScript
- Tailwind CSS
- React Context

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề:
1. Đọc [HUONG_DAN_CAI_DAT.md](HUONG_DAN_CAI_DAT.md)
2. Xem logs: `docker-compose logs -f`
3. Kiểm tra health: http://localhost:8000/health

---

## ✨ TÍNH NĂNG

- ✅ Xem danh sách sản phẩm
- ✅ Chi tiết sản phẩm
- ✅ Giỏ hàng
- ✅ Tìm kiếm
- ✅ Lọc theo danh mục
- ✅ Responsive design
- ✅ API documentation (Swagger)
- ✅ Database management (pgAdmin)

---

**Chúc bạn thành công! 🚀**

Nếu cần hướng dẫn chi tiết hơn, xem **[HUONG_DAN_CAI_DAT.md](HUONG_DAN_CAI_DAT.md)**

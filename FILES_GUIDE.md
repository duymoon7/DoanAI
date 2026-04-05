# 📁 HƯỚNG DẪN CÁC FILE TRONG DỰ ÁN

Giải thích ý nghĩa và cách sử dụng từng file/thư mục trong dự án.

---

## 📚 CÁC FILE HƯỚNG DẪN (Đọc theo thứ tự)

### 1. Bắt đầu
| File | Mô tả | Khi nào đọc |
|------|-------|-------------|
| **[GETTING_STARTED.md](GETTING_STARTED.md)** ⭐ | Bắt đầu nhanh (3 bước) | Đọc đầu tiên khi clone về |
| **[HUONG_DAN_CAI_DAT.md](HUONG_DAN_CAI_DAT.md)** 📖 | Hướng dẫn chi tiết từ A-Z | Nếu cần hướng dẫn chi tiết |
| **[CHECKLIST.md](CHECKLIST.md)** ✅ | Checklist cài đặt | Để đánh dấu tiến độ |

### 2. Tham khảo
| File | Mô tả | Khi nào đọc |
|------|-------|-------------|
| **[README.md](README.md)** | Tổng quan dự án | Để hiểu tổng quan |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | Tham khảo nhanh các lệnh | Khi cần tra cứu lệnh |
| **[SUCCESS.md](SUCCESS.md)** | Hướng dẫn sử dụng | Sau khi cài đặt xong |
| **[RUNNING_NOW.md](RUNNING_NOW.md)** | Thông tin ứng dụng đang chạy | Khi ứng dụng đang chạy |

### 3. Docker
| File | Mô tả | Khi nào đọc |
|------|-------|-------------|
| **[DOCKER_QUICK_START.md](DOCKER_QUICK_START.md)** | Hướng dẫn Docker chi tiết | Nếu gặp vấn đề với Docker |
| **[DOCKER_COMPLETE_SETUP.md](DOCKER_COMPLETE_SETUP.md)** | Chi tiết kỹ thuật Docker | Để hiểu sâu về Docker setup |
| **[START_SERVICES.md](START_SERVICES.md)** | Hướng dẫn start/stop services | Khi cần quản lý services |

### 4. Database
| File | Mô tả | Khi nào đọc |
|------|-------|-------------|
| **[PGADMIN_SETUP.md](PGADMIN_SETUP.md)** | Hướng dẫn sử dụng pgAdmin | Khi cần quản lý database |

### 5. Khác
| File | Mô tả | Khi nào đọc |
|------|-------|-------------|
| **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** | Danh mục tất cả tài liệu | Để tìm tài liệu cụ thể |
| **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** | Tóm tắt implementation | Để hiểu chi tiết kỹ thuật |
| **[FILES_GUIDE.md](FILES_GUIDE.md)** | File này - Hướng dẫn các file | Bạn đang đọc đây |

---

## 📂 CẤU TRÚC THỨ MỤC

```
doanAi/
│
├── 📚 Hướng dẫn cài đặt (ĐỌC ĐẦU TIÊN)
│   ├── GETTING_STARTED.md ⭐⭐⭐
│   ├── HUONG_DAN_CAI_DAT.md ⭐⭐⭐
│   └── CHECKLIST.md ⭐⭐
│
├── 📖 Tài liệu tham khảo
│   ├── README.md
│   ├── SUCCESS.md
│   ├── RUNNING_NOW.md
│   ├── QUICK_REFERENCE.md
│   └── FILES_GUIDE.md
│
├── 🐳 Docker
│   ├── docker-compose.yml (Cấu hình Docker)
│   ├── DOCKER_QUICK_START.md
│   ├── DOCKER_COMPLETE_SETUP.md
│   ├── START_SERVICES.md
│   └── DOCKER_GUIDE.md
│
├── 🗄️ Database
│   ├── PGADMIN_SETUP.md
│   └── SETUP_GUIDE.md
│
├── 🔧 Scripts
│   ├── verify_docker.ps1 (Windows)
│   ├── verify_docker.sh (Linux/Mac)
│   └── test_docker_setup.py (Python)
│
├── 🖥️ Backend (FastAPI)
│   ├── backend/
│   │   ├── app/
│   │   │   ├── main.py (Entry point)
│   │   │   ├── database.py (Database config)
│   │   │   ├── models/ (SQLAlchemy models)
│   │   │   ├── routers/ (API endpoints)
│   │   │   └── schemas/ (Pydantic schemas)
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── .env (Cấu hình database)
│   │   ├── seed_initial_data.py (Seed data)
│   │   ├── README.md
│   │   └── API_GUIDE.md
│   │
│   └── Các file khác:
│       ├── setup_db.py
│       ├── diagnose_db.py
│       └── seed_*.py
│
├── 🎨 Frontend (Next.js)
│   ├── frontend/
│   │   ├── app/ (Pages)
│   │   │   ├── page.tsx (Trang chủ)
│   │   │   ├── products/ (Trang sản phẩm)
│   │   │   ├── cart/ (Giỏ hàng)
│   │   │   └── auth/ (Đăng nhập/Đăng ký)
│   │   ├── components/ (React components)
│   │   ├── contexts/ (State management)
│   │   ├── lib/ (API & types)
│   │   ├── public/ (Static files)
│   │   ├── .env.local (Cấu hình API)
│   │   ├── package.json
│   │   └── README.md
│   │
│   └── Các file config:
│       ├── next.config.ts
│       ├── tailwind.config.ts
│       └── tsconfig.json
│
└── 📝 Khác
    ├── .gitignore
    ├── DOCUMENTATION_INDEX.md
    └── IMPLEMENTATION_SUMMARY.md
```

---

## 🎯 LỘ TRÌNH ĐỌC TÀI LIỆU

### Lần đầu clone về:
1. **[GETTING_STARTED.md](GETTING_STARTED.md)** - Đọc để biết cần làm gì
2. **[HUONG_DAN_CAI_DAT.md](HUONG_DAN_CAI_DAT.md)** - Làm theo từng bước
3. **[CHECKLIST.md](CHECKLIST.md)** - Đánh dấu tiến độ

### Sau khi cài đặt xong:
1. **[SUCCESS.md](SUCCESS.md)** - Xem các tính năng
2. **[RUNNING_NOW.md](RUNNING_NOW.md)** - Hiểu ứng dụng đang chạy
3. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Lưu để tra cứu

### Khi gặp vấn đề:
1. **[HUONG_DAN_CAI_DAT.md](HUONG_DAN_CAI_DAT.md)** - Phần "Xử Lý Lỗi"
2. **[DOCKER_QUICK_START.md](DOCKER_QUICK_START.md)** - Troubleshooting Docker
3. **[START_SERVICES.md](START_SERVICES.md)** - Restart services

### Khi muốn hiểu sâu:
1. **[README.md](README.md)** - Tổng quan dự án
2. **[DOCKER_COMPLETE_SETUP.md](DOCKER_COMPLETE_SETUP.md)** - Chi tiết Docker
3. **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Chi tiết kỹ thuật
4. **[backend/README.md](backend/README.md)** - Backend documentation
5. **[backend/API_GUIDE.md](backend/API_GUIDE.md)** - API documentation

---

## 📋 FILE QUAN TRỌNG NHẤT

### Top 5 file phải đọc:
1. **[GETTING_STARTED.md](GETTING_STARTED.md)** ⭐⭐⭐
2. **[HUONG_DAN_CAI_DAT.md](HUONG_DAN_CAI_DAT.md)** ⭐⭐⭐
3. **[CHECKLIST.md](CHECKLIST.md)** ⭐⭐
4. **[SUCCESS.md](SUCCESS.md)** ⭐⭐
5. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** ⭐⭐

---

## 🔧 FILE CẤU HÌNH

### Backend:
- **backend/.env** - Cấu hình database
  ```env
  DB_HOST=postgres
  DB_PORT=5432
  DB_NAME=electronics_db
  DB_USER=postgres
  DB_PASSWORD=123456
  ```

### Frontend:
- **frontend/.env.local** - Cấu hình API
  ```env
  NEXT_PUBLIC_API_URL=http://localhost:8000/api
  ```

### Docker:
- **docker-compose.yml** - Cấu hình Docker services
  - PostgreSQL (port 5432)
  - pgAdmin (port 5050)
  - Backend (port 8000)

---

## 📝 FILE KHÔNG CẦN QUAN TÂM

Các file này là tài liệu bổ sung, không bắt buộc đọc:

- DOCKER_GUIDE.md
- DOCKER_SETUP.md
- START_DOCKER.md
- SETUP_GUIDE.md
- SETUP_COMPLETE.md
- DOCUMENTATION_INDEX.md
- IMPLEMENTATION_SUMMARY.md
- test_docker_setup.py
- verify_docker.ps1/sh

---

## 🎓 HỌC TẬP

### Muốn học Backend:
1. Đọc **[backend/README.md](backend/README.md)**
2. Xem **[backend/API_GUIDE.md](backend/API_GUIDE.md)**
3. Xem code trong `backend/app/`

### Muốn học Frontend:
1. Đọc **[frontend/README.md](frontend/README.md)**
2. Xem code trong `frontend/app/`
3. Xem components trong `frontend/components/`

### Muốn học Docker:
1. Đọc **[DOCKER_QUICK_START.md](DOCKER_QUICK_START.md)**
2. Đọc **[DOCKER_COMPLETE_SETUP.md](DOCKER_COMPLETE_SETUP.md)**
3. Xem `docker-compose.yml`

---

## 💡 MẸO

### Tìm nhanh thông tin:
1. Dùng Ctrl+F để tìm trong file
2. Xem [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) để tìm file cụ thể
3. Xem [QUICK_REFERENCE.md](QUICK_REFERENCE.md) để tra cứu lệnh

### Lưu bookmark:
- http://localhost:3000 (Frontend)
- http://localhost:8000/docs (API Docs)
- http://localhost:5050 (pgAdmin)

---

## 📞 CẦN GIÚP ĐỠ?

### Thứ tự xử lý:
1. Tìm trong file tài liệu liên quan
2. Xem phần "Xử Lý Lỗi" trong [HUONG_DAN_CAI_DAT.md](HUONG_DAN_CAI_DAT.md)
3. Xem logs: `docker-compose logs -f`
4. Kiểm tra health: http://localhost:8000/health

---

## 🎯 TÓM TẮT

### Chỉ cần đọc 3 file này:
1. **[GETTING_STARTED.md](GETTING_STARTED.md)** - Bắt đầu
2. **[HUONG_DAN_CAI_DAT.md](HUONG_DAN_CAI_DAT.md)** - Chi tiết
3. **[CHECKLIST.md](CHECKLIST.md)** - Đánh dấu

### Các file khác đọc khi cần:
- Gặp lỗi → Xem phần troubleshooting
- Muốn hiểu sâu → Xem technical docs
- Cần tra cứu → Xem quick reference

---

**Chúc bạn thành công! 🚀**

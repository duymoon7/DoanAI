# 🛒 AI-Shop - E-Commerce Platform

Hệ thống thương mại điện tử bán thiết bị điện tử với tích hợp AI chatbot.

---

## 🚀 HƯỚNG DẪN CHẠY CODE

### Bước 1: Chuẩn Bị Database

1. Mở **XAMPP** và khởi động **MySQL**
2. Truy cập **phpMyAdmin**: http://localhost/phpmyadmin
3. Tạo database mới tên: `electronics_db`

### Bước 2: Chạy Backend (FastAPI)

Mở terminal và chạy:

```bash
# Di chuyển vào thư mục backend
cd backend

# Cài đặt dependencies (chỉ lần đầu tiên)
pip install -r requirements.txt

# Chạy server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend chạy tại: **http://localhost:8000**  
📚 API Documentation: **http://localhost:8000/docs**

### Bước 3: Chạy Frontend (Next.js)

Mở terminal mới và chạy:

```bash
# Di chuyển vào thư mục frontend
cd frontend

# Cài đặt dependencies (chỉ lần đầu tiên)
npm install

# Chạy development server
npm run dev
```

✅ Frontend chạy tại: **http://localhost:3000**

---

## 🎯 Tech Stack

### Backend
- **FastAPI** - Python web framework
- **SQLAlchemy** - ORM
- **MySQL** - Database (XAMPP)
- **OpenAI API** - AI Chatbot

### Frontend
- **Next.js 16** - React framework
- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Axios** - HTTP client

---

## � Features

- 🛍️ Quản lý sản phẩm và danh mục
- 👤 Quản lý người dùng và đơn hàng
- 🛒 Giỏ hàng với localStorage
- 🤖 AI Chatbot hỗ trợ khách hàng
- 📊 Admin dashboard
- 🔐 Authentication & Authorization
- 📱 Responsive design

---

## 🗄️ Database Schema

### 6 Tables
1. **nguoi_dung** - Người dùng (admin/user)
2. **danh_muc** - Danh mục sản phẩm
3. **san_pham** - Sản phẩm
4. **don_hang** - Đơn hàng
5. **chi_tiet_don_hang** - Chi tiết đơn hàng
6. **lich_su_chat** - Lịch sử chat với AI

---

## � API Endpoints

Base URL: `http://localhost:8000/api`

### Sản Phẩm
- `GET /api/san-pham` - Lấy danh sách sản phẩm
- `GET /api/san-pham/{id}` - Chi tiết sản phẩm
- `POST /api/san-pham` - Tạo sản phẩm mới
- `PUT /api/san-pham/{id}` - Cập nhật sản phẩm
- `DELETE /api/san-pham/{id}` - Xóa sản phẩm

### Danh Mục
- `GET /api/danh-muc` - Lấy danh sách danh mục
- `GET /api/danh-muc/{id}` - Chi tiết danh mục
- `POST /api/danh-muc` - Tạo danh mục mới

### Người Dùng
- `GET /api/nguoi-dung` - Lấy danh sách người dùng
- `POST /api/nguoi-dung` - Tạo người dùng mới

### Đơn Hàng
- `GET /api/don-hang` - Lấy danh sách đơn hàng
- `POST /api/don-hang` - Tạo đơn hàng mới

📚 **Xem đầy đủ tại:** http://localhost:8000/docs

---

## 📁 Cấu Trúc Thư Mục

```
AI-Shop/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── models/      # Database models (SQLAlchemy)
│   │   ├── routers/     # API endpoints
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── database.py  # Database configuration
│   │   └── main.py      # FastAPI application
│   ├── requirements.txt
│   ├── seed_initial_data.py
│   └── reset_db.py
├── frontend/            # Next.js frontend
│   ├── app/            # Pages & routes (App Router)
│   │   ├── admin/      # Admin pages
│   │   ├── auth/       # Login/Register
│   │   ├── cart/       # Shopping cart
│   │   ├── chat/       # AI Chatbot
│   │   ├── orders/     # Order history
│   │   ├── products/   # Product pages
│   │   └── profile/    # User profile
│   ├── components/     # React components
│   ├── contexts/       # Context API (Cart)
│   ├── lib/           # API client & types
│   └── package.json
├── .env               # Environment variables
├── .gitignore
└── README.md
```

---

## ⚙️ Cấu Hình

### File .env (Backend)
```env
# MySQL Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=electronics_db
DB_USER=root
DB_PASSWORD=

# Backend Configuration
APP_ENV=development
DEBUG=True
```

### File lib/api.ts (Frontend)
```typescript
const API_BASE_URL = 'http://localhost:8000/api';
```

---

## 🔍 Kiểm Tra Hệ Thống

Sau khi chạy, kiểm tra các URL sau:

- ✅ Backend Health: http://localhost:8000/health
- ✅ API Docs: http://localhost:8000/docs
- ✅ Frontend: http://localhost:3000
- ✅ phpMyAdmin: http://localhost/phpmyadmin

---

## � Troubleshooting

### Backend không kết nối được database
```bash
# Kiểm tra:
1. XAMPP MySQL đã chạy chưa?
2. Database 'electronics_db' đã tạo chưa?
3. File .env có đúng thông tin không?
```

### Frontend không gọi được API
```bash
# Kiểm tra:
1. Backend đã chạy tại port 8000 chưa?
2. Truy cập http://localhost:8000/health
3. Kiểm tra CORS trong backend/app/main.py
```

### Port đã được sử dụng
```bash
# Backend (port 8000)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Frontend (port 3000)
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

---

## 🔄 Reset Database

Nếu cần reset database và tạo lại dữ liệu mẫu:

```bash
cd backend
python reset_db.py
```

---

## � Lệnh Thường Dùng

```bash
# Backend
cd backend
pip install -r requirements.txt          # Cài dependencies
uvicorn app.main:app --reload            # Chạy server
python reset_db.py                       # Reset database
python seed_initial_data.py              # Seed dữ liệu mẫu

# Frontend
cd frontend
npm install                              # Cài dependencies
npm run dev                              # Chạy dev server
npm run build                            # Build production
npm start                                # Chạy production server
```

---

## 📚 Tài Liệu

### Bắt đầu
- [QUICK_START.md](QUICK_START.md) - ⚡ Khởi động nhanh trong 3 bước
- [README.md](README.md) - 📖 Hướng dẫn đầy đủ (file này)

### Quản trị
- [ADMIN_GUIDE.md](ADMIN_GUIDE.md) - 🔐 Hướng dẫn tài khoản Admin
- [SCRIPTS.md](SCRIPTS.md) - 🛠️ Tổng hợp scripts hữu ích

### Khắc phục sự cố
- [FIX_LOGIN.md](FIX_LOGIN.md) - 🔧 Fix lỗi đăng nhập

### Tham khảo
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 📁 Cấu trúc project
- [backend/API_COMPLETE.md](backend/API_COMPLETE.md) - 🌐 API documentation

---

## � Yêu Cầu Hệ Thống

- **Python**: 3.11+
- **Node.js**: 18+
- **MySQL**: 5.7+ (XAMPP)
- **RAM**: 4GB+
- **OS**: Windows/Mac/Linux

---

## ✅ Checklist Sau Khi Setup

- [ ] XAMPP MySQL đang chạy
- [ ] Database `electronics_db` đã tạo
- [ ] Backend chạy tại http://localhost:8000
- [ ] API docs mở được: http://localhost:8000/docs
- [ ] Database có 6 tables
- [ ] Frontend chạy tại http://localhost:3000
- [ ] Có thể xem danh sách sản phẩm
- [ ] Có thể thêm sản phẩm vào giỏ hàng
- [ ] Giỏ hàng lưu được khi refresh

---

## 🎉 Bắt Đầu Phát Triển

Hệ thống đã sẵn sàng! Bạn có thể:

1. Xem danh sách sản phẩm tại trang chủ
2. Thêm sản phẩm vào giỏ hàng
3. Chat với AI chatbot
4. Đăng ký/Đăng nhập
5. Xem API documentation
6. Bắt đầu customize theo ý muốn

**Happy Coding! 🚀**

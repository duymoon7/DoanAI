# 🛒 AI-Shop - E-Commerce Platform

Hệ thống thương mại điện tử bán thiết bị điện tử với tích hợp AI chatbot.

---

## 🚀 HƯỚNG DẪN CHẠY CODE

### Bước 1: Chuẩn Bị Database

1. Mở **XAMPP** và khởi động **MySQL**
2. Truy cập **phpMyAdmin**: http://localhost/phpmyadmin
3. Tạo database mới tên: `electronics_db`

### Bước 2: Cấu hình môi trường

Sao chép file `.env.example` thành `.env` và cập nhật thông tin:

```bash
# Trong thư mục AI-Shop
cp .env.example .env
```

Sau đó chỉnh sửa file `.env` với thông tin của bạn:
```env
# MySQL Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=electronics_db
DB_USER=root
DB_PASSWORD=

# JWT Secret Key (đổi key này trong production!)
SECRET_KEY=your-super-secret-key-change-this-in-production

# AI API Keys (lấy từ OpenAI hoặc Google Gemini)
AI_PROVIDER=openai
OPENAI_API_KEY=your-openai-api-key-here
# GEMINI_API_KEY=your-gemini-api-key-here
```

⚠️ **Lưu ý:** File `.env` chứa thông tin nhạy cảm và không được đẩy lên GitHub

### Bước 3: Chạy Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend chạy tại: **http://localhost:8000**  
📚 API Documentation: **http://localhost:8000/docs**

Backend sẽ tự động:
- Tạo các bảng trong database
- Seed dữ liệu mẫu (sản phẩm, danh mục, người dùng)

### Bước 4: Chạy Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

✅ Frontend chạy tại: **http://localhost:3000**

---

## 👤 Tài khoản mẫu

### Admin
- Email: admin@aishop.com
- Password: admin123
- Quyền: Toàn quyền quản trị

### Manager
- Email: manager@aishop.com
- Password: manager123
- Quyền: Quản lý sản phẩm, đơn hàng, đánh giá, mã giảm giá

### User
- Email: quynhhuong@gmail.com
- Password: password123

---

## 🎯 Tech Stack

### Backend
- **FastAPI** - Python web framework
- **SQLAlchemy** - ORM
- **MySQL** - Database
- **JWT** - Authentication
- **OpenAI API** - AI Chatbot

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Axios** - HTTP client

---

## ✨ Tính năng

### Khách hàng
- ✅ Đăng ký/Đăng nhập
- ✅ Quên mật khẩu
- ✅ Xem sản phẩm theo danh mục
- ✅ Tìm kiếm sản phẩm (hỗ trợ tiếng Việt có dấu)
- ✅ Giỏ hàng
- ✅ Đặt hàng
- ✅ Xem lịch sử đơn hàng
- ✅ Xem chi tiết đơn hàng
- ✅ Đánh giá sản phẩm
- ✅ Chat với AI chatbot

### Admin
- ✅ Quản lý sản phẩm (CRUD)
- ✅ Quản lý danh mục (CRUD)
- ✅ Quản lý đơn hàng (xem, cập nhật trạng thái)
- ✅ Quản lý người dùng (xem, cập nhật vai trò)
- ✅ Quản lý đánh giá (xem, xóa)
- ✅ Quản lý mã giảm giá (CRUD)
- ✅ Thống kê dashboard

### Manager
- ✅ Quản lý sản phẩm
- ✅ Quản lý đơn hàng
- ✅ Quản lý đánh giá
- ✅ Quản lý mã giảm giá (tạo, sửa)
- ❌ Không có quyền: Quản lý danh mục, xóa mã giảm giá

---

## 🗄️ Database Schema

### 8 Tables
1. **nguoi_dung** - Người dùng (admin/manager/user)
2. **danh_muc** - Danh mục sản phẩm
3. **san_pham** - Sản phẩm
4. **don_hang** - Đơn hàng
5. **chi_tiet_don_hang** - Chi tiết đơn hàng
6. **danh_gia** - Đánh giá sản phẩm
7. **ma_giam_gia** - Mã giảm giá
8. **lich_su_chat** - Lịch sử chat với AI

Chi tiết xem file `backend/database_diagram.dbml`

---

## 📁 Cấu Trúc Thư Mục

```
AI-Shop/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── models/      # Database models (SQLAlchemy)
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── routers/     # API endpoints
│   │   ├── auth.py      # Authentication
│   │   ├── database.py  # Database config
│   │   └── main.py      # FastAPI app
│   ├── requirements.txt
│   └── seed_*.py        # Seed scripts
├── frontend/            # Next.js frontend
│   ├── app/
│   │   ├── admin/      # Admin pages
│   │   ├── auth/       # Auth pages
│   │   ├── cart/       # Cart page
│   │   ├── orders/     # Orders pages
│   │   ├── products/   # Products pages
│   │   └── profile/    # Profile page
│   ├── components/     # React components
│   ├── contexts/       # React contexts (Cart)
│   ├── lib/           # API client & types
│   └── package.json
├── .env               # Database config
└── README.md
```

Chi tiết xem file `PROJECT_STRUCTURE.md`

---

## 🔍 Kiểm Tra Hệ Thống

Sau khi chạy, kiểm tra các URL sau:

- ✅ Backend Health: http://localhost:8000/health
- ✅ API Docs: http://localhost:8000/docs
- ✅ Frontend: http://localhost:3000
- ✅ Admin Dashboard: http://localhost:3000/admin
- ✅ phpMyAdmin: http://localhost/phpmyadmin

---

## 🛠️ Scripts hữu ích

### Backend
```bash
# Seed dữ liệu sản phẩm
python seed_initial_data.py

# Seed đánh giá mẫu
python seed_reviews.py
```

---

## 🔧 Troubleshooting

### Backend không kết nối database
- Kiểm tra MySQL đang chạy trong XAMPP
- Kiểm tra thông tin trong file `.env`
- Đảm bảo database `electronics_db` đã được tạo

### Frontend không gọi được API
- Kiểm tra backend đang chạy ở port 8000
- Truy cập http://localhost:8000/health
- Kiểm tra CORS settings trong `backend/app/main.py`

### Lỗi 401 Unauthorized
- Đăng nhập lại để lấy token mới
- Kiểm tra token trong localStorage chưa hết hạn
- Xóa localStorage và đăng nhập lại

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

## � API Endpoints

Base URL: `http://localhost:8000/api`

### Authentication
- `POST /auth/login` - Đăng nhập
- `POST /auth/register` - Đăng ký
- `POST /nguoi-dung/check-email/{email}` - Kiểm tra email
- `POST /nguoi-dung/reset-password` - Đặt lại mật khẩu

### Sản phẩm
- `GET /san-pham` - Lấy danh sách (hỗ trợ search, category)
- `GET /san-pham/{id}` - Chi tiết sản phẩm
- `POST /san-pham` - Tạo sản phẩm (Admin/Manager)
- `PUT /san-pham/{id}` - Cập nhật (Admin/Manager)
- `DELETE /san-pham/{id}` - Xóa (Admin/Manager)

### Danh mục
- `GET /danh-muc` - Lấy danh sách
- `POST /danh-muc` - Tạo danh mục (Admin)
- `PUT /danh-muc/{id}` - Cập nhật (Admin)
- `DELETE /danh-muc/{id}` - Xóa (Admin)

### Đơn hàng
- `GET /don-hang` - Lấy đơn hàng của user
- `GET /don-hang/all` - Lấy tất cả (Admin/Manager)
- `POST /don-hang` - Tạo đơn hàng
- `PUT /don-hang/{id}` - Cập nhật trạng thái (Admin/Manager)

### Đánh giá
- `GET /danh-gia/san-pham/{id}` - Lấy đánh giá của sản phẩm
- `GET /danh-gia/all` - Lấy tất cả (Admin/Manager)
- `POST /danh-gia` - Tạo đánh giá
- `DELETE /danh-gia/{id}` - Xóa (Admin/Manager)

### Mã giảm giá
- `GET /ma-giam-gia` - Lấy danh sách
- `POST /ma-giam-gia/validate` - Validate mã
- `POST /ma-giam-gia` - Tạo mã (Admin/Manager)
- `PUT /ma-giam-gia/{id}` - Cập nhật (Admin/Manager)
- `DELETE /ma-giam-gia/{id}` - Xóa (Admin)

📚 **Xem đầy đủ tại:** http://localhost:8000/docs

---

## 📋 Yêu Cầu Hệ Thống

- **Python**: 3.11+
- **Node.js**: 18+
- **MySQL**: 5.7+ (XAMPP)
- **RAM**: 4GB+
- **OS**: Windows/Mac/Linux

---

## ✅ Checklist Sau Khi Setup

- [ ] XAMPP MySQL đang chạy
- [ ] Database `electronics_db` đã tạo
- [ ] File `.env` đã cấu hình đúng
- [ ] Backend chạy tại http://localhost:8000
- [ ] API docs mở được: http://localhost:8000/docs
- [ ] Database có 8 tables
- [ ] Frontend chạy tại http://localhost:3000
- [ ] Có thể đăng nhập với tài khoản mẫu
- [ ] Có thể xem danh sách sản phẩm
- [ ] Có thể thêm sản phẩm vào giỏ hàng

---

## 🎉 Bắt Đầu Phát Triển

Hệ thống đã sẵn sàng! Bạn có thể:

1. Xem danh sách sản phẩm tại trang chủ
2. Tìm kiếm sản phẩm (hỗ trợ tiếng Việt)
3. Thêm sản phẩm vào giỏ hàng
4. Đặt hàng và theo dõi đơn hàng
5. Đánh giá sản phẩm
6. Chat với AI chatbot
7. Quản trị hệ thống (Admin/Manager)

**Happy Coding! 🚀**

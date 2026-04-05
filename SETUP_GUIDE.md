# 🚀 Setup Guide - ElectroShop E-Commerce

## 📋 Tổng quan

Hệ thống E-Commerce hoàn chỉnh với:
- **Backend**: FastAPI + PostgreSQL
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS

---

## 🔧 Yêu cầu hệ thống

- Node.js 18+ (cho frontend)
- Python 3.8+ (cho backend)
- PostgreSQL 12+ (đã cài đặt và đang chạy)

---

## 📦 Cài đặt

### 1. Backend Setup

```bash
# Di chuyển vào thư mục backend
cd backend

# Cài đặt dependencies (nếu chưa có)
pip install -r requirements.txt

# File .env đã được cấu hình sẵn
# Kiểm tra kết nối database
python test_connection.py
```

### 2. Frontend Setup

```bash
# Di chuyển vào thư mục frontend
cd frontend

# Cài đặt dependencies (đã cài rồi)
npm install

# Build production (đã build rồi)
npm run build
```

---

## 🏃 Chạy ứng dụng

### Bước 1: Start Backend

```bash
cd backend
python run.py
```

Backend sẽ chạy tại: **http://localhost:8000**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Bước 2: Start Frontend

Mở terminal mới:

```bash
cd frontend
npm run dev
```

Frontend sẽ chạy tại: **http://localhost:3000**

---

## ✅ Kiểm tra

### 1. Kiểm tra Backend

```bash
# Test API
curl http://localhost:8000/health

# Xem danh sách sản phẩm
curl http://localhost:8000/api/san-pham
```

### 2. Kiểm tra Frontend

Mở trình duyệt: **http://localhost:3000**

Bạn sẽ thấy:
- ✅ Homepage với hero banner
- ✅ Danh mục sản phẩm
- ✅ Sản phẩm nổi bật
- ✅ Navbar với search bar
- ✅ Footer

---

## 🎯 Tính năng chính

### Frontend

1. **Homepage** (`/`)
   - Hero banner
   - Categories
   - Featured products
   - Newsletter signup

2. **Products Page** (`/products`)
   - Product grid (4 columns)
   - Filters (category, price)
   - Sort options
   - Search

3. **Product Detail** (`/products/[id]`)
   - Large image
   - Product info
   - Add to cart
   - Buy now

4. **Cart** (`/cart`)
   - Cart items
   - Quantity controls
   - Order summary
   - Checkout

5. **Auth Pages**
   - Login (`/auth/login`)
   - Register (`/auth/register`)

### Backend

- ✅ 6 API modules (Users, Categories, Products, Orders, Order Items, Chat)
- ✅ CRUD operations đầy đủ
- ✅ PostgreSQL database
- ✅ SQLAlchemy ORM
- ✅ Auto table creation
- ✅ Sample data seeding

---

## 📊 Database

Database đã được setup với:
- ✅ 6 tables (nguoi_dung, danh_muc, san_pham, don_hang, chi_tiet_don_hang, lich_su_chat)
- ✅ Sample data (users, categories, products, orders)

### Seed thêm data (nếu cần)

```bash
cd backend
python seed_force.py
```

---

## 🎨 UI/UX Features

- ✅ Clean, minimalist design (Amazon + Shopee style)
- ✅ Responsive (mobile-first)
- ✅ Loading skeletons
- ✅ Toast notifications
- ✅ Smooth animations
- ✅ Cart persistence (localStorage)
- ✅ Search functionality
- ✅ Filter & sort

---

## 🔗 API Endpoints

Base URL: `http://localhost:8000/api`

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/san-pham` | GET, POST, PUT, DELETE | Products |
| `/danh-muc` | GET, POST, PUT, DELETE | Categories |
| `/don-hang` | GET, POST, PUT, DELETE | Orders |
| `/nguoi-dung` | GET, POST, PUT, DELETE | Users |
| `/chi-tiet-don-hang` | GET, POST | Order Items |
| `/lich-su-chat` | GET, POST | Chat History |

---

## 🐛 Troubleshooting

### Backend không start

```bash
# Kiểm tra PostgreSQL đang chạy
# Kiểm tra .env file
cd backend
python test_connection.py
```

### Frontend không kết nối được API

```bash
# Kiểm tra backend đang chạy
curl http://localhost:8000/health

# Kiểm tra .env.local
cat frontend/.env.local
```

### Port đã được sử dụng

```bash
# Backend (port 8000)
# Tìm và kill process
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Frontend (port 3000)
netstat -ano | findstr :3000
taskkill /PID <process_id> /F
```

---

## 📝 Quick Commands

```bash
# Start backend
cd backend && python run.py

# Start frontend (terminal mới)
cd frontend && npm run dev

# Seed database
cd backend && python seed_force.py

# Check database
cd backend && python test_connection.py
```

---

## 🎉 Hoàn tất!

Hệ thống đã sẵn sàng:

- ✅ Backend: http://localhost:8000
- ✅ Frontend: http://localhost:3000
- ✅ API Docs: http://localhost:8000/docs

**Chúc bạn phát triển thành công! 🚀**

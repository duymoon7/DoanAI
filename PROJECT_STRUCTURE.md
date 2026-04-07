# Cấu trúc Project AI-Shop

## Tổng quan

```
AI-Shop/
├── backend/              # FastAPI Backend
├── frontend/             # Next.js Frontend
├── .env                  # Database configuration
├── .gitignore
├── PROJECT_STRUCTURE.md  # File này
└── README.md            # Hướng dẫn chính
```

---

## Backend Structure

```
backend/
├── app/
│   ├── models/              # SQLAlchemy Models
│   │   ├── base.py         # Base model với timestamps
│   │   ├── nguoi_dung.py   # User model
│   │   ├── danh_muc.py     # Category model
│   │   ├── san_pham.py     # Product model
│   │   ├── don_hang.py     # Order model
│   │   ├── chi_tiet_don_hang.py  # Order detail model
│   │   ├── danh_gia.py     # Review model
│   │   ├── ma_giam_gia.py  # Coupon model
│   │   ├── lich_su_chat.py # Chat history model
│   │   └── __init__.py
│   │
│   ├── schemas/            # Pydantic Schemas
│   │   ├── auth.py         # Login/Register schemas
│   │   ├── nguoi_dung.py   # User schemas
│   │   ├── danh_muc.py     # Category schemas
│   │   ├── san_pham.py     # Product schemas
│   │   ├── don_hang.py     # Order schemas
│   │   ├── chi_tiet_don_hang.py  # Order detail schemas
│   │   ├── danh_gia.py     # Review schemas
│   │   ├── ma_giam_gia.py  # Coupon schemas
│   │   ├── lich_su_chat.py # Chat schemas
│   │   └── __init__.py
│   │
│   ├── routers/            # API Endpoints
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── nguoi_dung.py   # User endpoints
│   │   ├── danh_muc.py     # Category endpoints
│   │   ├── san_pham.py     # Product endpoints
│   │   ├── don_hang.py     # Order endpoints
│   │   ├── chi_tiet_don_hang.py  # Order detail endpoints
│   │   ├── danh_gia.py     # Review endpoints
│   │   ├── ma_giam_gia.py  # Coupon endpoints
│   │   ├── lich_su_chat.py # Chat endpoints
│   │   ├── chatbot.py      # AI chatbot endpoints
│   │   ├── statistics.py   # Statistics endpoints
│   │   ├── admin.py        # Admin endpoints
│   │   └── __init__.py
│   │
│   ├── auth.py             # JWT authentication logic
│   ├── database.py         # Database configuration
│   ├── main.py             # FastAPI application
│   └── __init__.py
│
├── database_diagram.dbml   # Database diagram
├── requirements.txt        # Python dependencies
├── seed_initial_data.py    # Seed products & categories
└── seed_reviews.py         # Seed reviews
```

---

## Frontend Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── admin/             # Admin pages
│   │   ├── categories/    # Category management
│   │   ├── coupons/       # Coupon management
│   │   ├── orders/        # Order management
│   │   ├── products/      # Product management
│   │   ├── reviews/       # Review management
│   │   ├── users/         # User management
│   │   └── page.tsx       # Admin dashboard
│   │
│   ├── api/               # API routes (Next.js)
│   │   └── auth/
│   │       ├── login/
│   │       └── register/
│   │
│   ├── auth/              # Authentication pages
│   │   ├── forgot-password/
│   │   ├── login/
│   │   └── register/
│   │
│   ├── cart/              # Shopping cart
│   │   └── page.tsx
│   │
│   ├── chat/              # AI chatbot
│   │   └── page.tsx
│   │
│   ├── orders/            # Order pages
│   │   ├── [id]/         # Order detail
│   │   └── page.tsx      # Order list
│   │
│   ├── products/          # Product pages
│   │   ├── [id]/         # Product detail
│   │   └── page.tsx      # Product list
│   │
│   ├── profile/           # User profile
│   │   └── page.tsx
│   │
│   ├── favicon.ico
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
│
├── components/            # React Components
│   ├── Footer.tsx
│   ├── LoadingSkeleton.tsx
│   ├── Navbar.tsx
│   └── ProductCard.tsx
│
├── contexts/              # React Contexts
│   └── CartContext.tsx   # Shopping cart state
│
├── lib/                   # Utilities
│   ├── api.ts            # API client (Axios)
│   └── types.ts          # TypeScript types
│
├── public/               # Static files
│   └── placeholder.png
│
├── .env.local            # Environment variables
├── .gitignore
├── eslint.config.mjs
├── next.config.ts
├── package.json
├── postcss.config.mjs
├── tailwind.config.ts
└── tsconfig.json
```

---

## Database Schema

### 1. nguoi_dung (Users)
```sql
- id: INT (PK)
- email: VARCHAR(255) UNIQUE
- mat_khau: VARCHAR(255)
- ho_ten: VARCHAR(255)
- so_dien_thoai: VARCHAR(20)
- dia_chi: TEXT
- vai_tro: ENUM('admin', 'manager', 'user')
- ngay_tao: DATETIME
- ngay_cap_nhat: DATETIME
```

### 2. danh_muc (Categories)
```sql
- id: INT (PK)
- ten_danh_muc: VARCHAR(255)
- mo_ta: TEXT
- ngay_tao: DATETIME
- ngay_cap_nhat: DATETIME
```

### 3. san_pham (Products)
```sql
- id: INT (PK)
- ten_san_pham: VARCHAR(255)
- mo_ta: TEXT
- gia: DECIMAL(10,2)
- so_luong_ton: INT
- hinh_anh: VARCHAR(500)
- danh_muc_id: INT (FK -> danh_muc)
- ngay_tao: DATETIME
- ngay_cap_nhat: DATETIME
```

### 4. don_hang (Orders)
```sql
- id: INT (PK)
- nguoi_dung_id: INT (FK -> nguoi_dung)
- tong_tien: DECIMAL(10,2)
- trang_thai: ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled')
- dia_chi_giao_hang: TEXT
- ghi_chu: TEXT
- ngay_tao: DATETIME
- ngay_cap_nhat: DATETIME
```

### 5. chi_tiet_don_hang (Order Details)
```sql
- id: INT (PK)
- don_hang_id: INT (FK -> don_hang)
- san_pham_id: INT (FK -> san_pham)
- so_luong: INT
- gia: DECIMAL(10,2)
- ngay_tao: DATETIME
- ngay_cap_nhat: DATETIME
```

### 6. danh_gia (Reviews)
```sql
- id: INT (PK)
- san_pham_id: INT (FK -> san_pham)
- nguoi_dung_id: INT (FK -> nguoi_dung)
- diem_danh_gia: INT (1-5)
- noi_dung: TEXT
- ngay_tao: DATETIME
- ngay_cap_nhat: DATETIME
```

### 7. ma_giam_gia (Coupons)
```sql
- id: INT (PK)
- ma_code: VARCHAR(50) UNIQUE
- mo_ta: VARCHAR(255)
- loai_giam: ENUM('percent', 'fixed')
- gia_tri_giam: DECIMAL(10,2)
- gia_tri_don_toi_thieu: DECIMAL(10,2)
- so_luong: INT
- da_su_dung: INT
- ngay_bat_dau: DATETIME
- ngay_ket_thuc: DATETIME
- hoat_dong: BOOLEAN
- ngay_tao: DATETIME
- ngay_cap_nhat: DATETIME
```

### 8. lich_su_chat (Chat History)
```sql
- id: INT (PK)
- nguoi_dung_id: INT (FK -> nguoi_dung)
- tin_nhan: TEXT
- phan_hoi: TEXT
- ngay_tao: DATETIME
- ngay_cap_nhat: DATETIME
```

---

## API Routes

### Authentication
- `POST /auth/login` - Đăng nhập
- `POST /auth/register` - Đăng ký
- `GET /auth/me` - Lấy thông tin user hiện tại

### Users
- `GET /api/nguoi-dung` - Lấy danh sách users (Admin)
- `GET /api/nguoi-dung/{id}` - Chi tiết user
- `PUT /api/nguoi-dung/{id}` - Cập nhật user
- `GET /api/nguoi-dung/check-email/{email}` - Kiểm tra email
- `POST /api/nguoi-dung/reset-password` - Đặt lại mật khẩu

### Categories
- `GET /api/danh-muc` - Lấy danh sách
- `GET /api/danh-muc/{id}` - Chi tiết
- `POST /api/danh-muc` - Tạo mới (Admin)
- `PUT /api/danh-muc/{id}` - Cập nhật (Admin)
- `DELETE /api/danh-muc/{id}` - Xóa (Admin)

### Products
- `GET /api/san-pham` - Lấy danh sách (search, category)
- `GET /api/san-pham/{id}` - Chi tiết
- `POST /api/san-pham` - Tạo mới (Admin/Manager)
- `PUT /api/san-pham/{id}` - Cập nhật (Admin/Manager)
- `DELETE /api/san-pham/{id}` - Xóa (Admin/Manager)

### Orders
- `GET /api/don-hang` - Lấy đơn hàng của user
- `GET /api/don-hang/all` - Lấy tất cả (Admin/Manager)
- `GET /api/don-hang/{id}` - Chi tiết
- `POST /api/don-hang` - Tạo đơn hàng
- `PUT /api/don-hang/{id}` - Cập nhật trạng thái (Admin/Manager)

### Reviews
- `GET /api/danh-gia/san-pham/{id}` - Lấy đánh giá của sản phẩm
- `GET /api/danh-gia/all` - Lấy tất cả (Admin/Manager)
- `POST /api/danh-gia` - Tạo đánh giá
- `DELETE /api/danh-gia/{id}` - Xóa (Admin/Manager)

### Coupons
- `GET /api/ma-giam-gia` - Lấy danh sách
- `GET /api/ma-giam-gia/{id}` - Chi tiết
- `POST /api/ma-giam-gia/validate` - Validate mã
- `POST /api/ma-giam-gia` - Tạo mã (Admin/Manager)
- `PUT /api/ma-giam-gia/{id}` - Cập nhật (Admin/Manager)
- `DELETE /api/ma-giam-gia/{id}` - Xóa (Admin)
- `POST /api/ma-giam-gia/{id}/use` - Đánh dấu đã sử dụng

### Chatbot
- `POST /api/chatbot` - Chat với AI
- `GET /api/lich-su-chat` - Lấy lịch sử chat

### Statistics
- `GET /api/statistics/overview` - Thống kê tổng quan

### Admin
- `GET /admin/info` - Thông tin hệ thống

---

## Environment Variables

### Backend (.env)
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=electronics_db
DB_USER=root
DB_PASSWORD=
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Tech Stack Details

### Backend
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM
- **Pydantic**: Data validation
- **PyMySQL**: MySQL driver
- **python-jose**: JWT tokens
- **passlib**: Password hashing
- **python-multipart**: File uploads

### Frontend
- **Next.js 14**: React framework
- **React 19**: UI library
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Axios**: HTTP client
- **React Hot Toast**: Notifications
- **Lucide React**: Icons

---

## Quyền truy cập

| Chức năng | Admin | Manager | User |
|-----------|-------|---------|------|
| Xem sản phẩm | ✅ | ✅ | ✅ |
| Quản lý sản phẩm | ✅ | ✅ | ❌ |
| Quản lý danh mục | ✅ | ❌ | ❌ |
| Quản lý đơn hàng | ✅ | ✅ | Chỉ của mình |
| Quản lý người dùng | ✅ | ❌ | ❌ |
| Quản lý đánh giá | ✅ | ✅ | Tạo mới |
| Quản lý mã giảm giá | ✅ | Tạo/Sửa | ❌ |
| Xóa mã giảm giá | ✅ | ❌ | ❌ |

---

## Development Workflow

### 1. Thêm tính năng mới

#### Backend
1. Tạo model trong `app/models/`
2. Tạo schema trong `app/schemas/`
3. Tạo router trong `app/routers/`
4. Import router vào `app/main.py`
5. Chạy migration (hoặc restart để tạo bảng)

#### Frontend
1. Tạo page trong `app/`
2. Tạo component trong `components/` (nếu cần)
3. Thêm API call trong `lib/api.ts`
4. Thêm types trong `lib/types.ts`

### 2. Testing
- Backend: http://localhost:8000/docs (Swagger UI)
- Frontend: Kiểm tra trực tiếp trên browser

### 3. Deployment
- Backend: Uvicorn + Gunicorn
- Frontend: Vercel hoặc build static
- Database: MySQL production server

---

## Maintenance

### Backup Database
```bash
mysqldump -u root -p electronics_db > backup.sql
```

### Restore Database
```bash
mysql -u root -p electronics_db < backup.sql
```

### Update Dependencies
```bash
# Backend
pip install -r requirements.txt --upgrade

# Frontend
npm update
```

---

## Notes

- Tất cả models kế thừa từ `BaseModel` có `ngay_tao` và `ngay_cap_nhat` tự động
- JWT token hết hạn sau 7 ngày
- Giỏ hàng lưu trong localStorage (frontend)
- Tìm kiếm sản phẩm hỗ trợ tiếng Việt có dấu (accent-insensitive)
- Format tiền tệ: VNĐ (Intl.NumberFormat)
- Responsive design cho mobile/tablet/desktop

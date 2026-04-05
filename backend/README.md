# E-Commerce Backend API

FastAPI backend for electronics e-commerce platform with PostgreSQL database.

---

## 🚀 Quick Start with Docker (Recommended)

### Prerequisites
- Docker Desktop
- Docker Compose

### Start Everything
```bash
# From project root
docker-compose up --build
```

This will:
- ✅ Start PostgreSQL database (port 5432)
- ✅ Start pgAdmin (port 5050)
- ✅ Start FastAPI backend (port 8000)
- ✅ Auto-create all tables
- ✅ Auto-seed initial data (categories & products)

### Access Services
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health
- **pgAdmin**: http://localhost:5050
  - Email: `admin@admin.com`
  - Password: `admin`

### Database Connection
- **Host**: `postgres` (inside Docker) or `localhost` (from host)
- **Port**: `5432`
- **Database**: `electronics_db`
- **User**: `postgres`
- **Password**: `123456`

📖 **See [DOCKER_QUICK_START.md](../DOCKER_QUICK_START.md) for detailed Docker instructions.**

---

## 🛠️ Manual Setup (Alternative)

## Cấu trúc Database

### 1. Bảng `nguoi_dung` (Users)
- `id`: Primary key
- `email`: Email người dùng (unique)
- `mat_khau`: Mật khẩu đã hash
- `vai_tro`: Vai trò (admin/user)
- `ngay_tao`: Ngày tạo tài khoản

**Relationships:**
- Có nhiều `don_hang` (orders)
- Có nhiều `lich_su_chat` (chat history)

### 2. Bảng `danh_muc` (Categories)
- `id`: Primary key
- `ten`: Tên danh mục

**Relationships:**
- Có nhiều `san_pham` (products)

### 3. Bảng `san_pham` (Products)
- `id`: Primary key
- `ten`: Tên sản phẩm
- `gia`: Giá sản phẩm
- `mo_ta`: Mô tả sản phẩm
- `hinh_anh`: URL hình ảnh
- `danh_muc_id`: Foreign key → `danh_muc.id`
- `ngay_tao`: Ngày tạo sản phẩm

**Relationships:**
- Thuộc về một `danh_muc` (category)
- Có nhiều `chi_tiet_don_hang` (order items)

### 4. Bảng `don_hang` (Orders)
- `id`: Primary key
- `nguoi_dung_id`: Foreign key → `nguoi_dung.id`
- `tong_tien`: Tổng tiền đơn hàng
- `trang_thai`: Trạng thái (pending/completed/cancelled)
- `ngay_tao`: Ngày tạo đơn hàng

**Relationships:**
- Thuộc về một `nguoi_dung` (user)
- Có nhiều `chi_tiet_don_hang` (order items)

### 5. Bảng `chi_tiet_don_hang` (Order Items)
- `id`: Primary key
- `don_hang_id`: Foreign key → `don_hang.id`
- `san_pham_id`: Foreign key → `san_pham.id`
- `so_luong`: Số lượng sản phẩm

**Relationships:**
- Thuộc về một `don_hang` (order)
- Liên kết với một `san_pham` (product)

### 6. Bảng `lich_su_chat` (Chat History)
- `id`: Primary key
- `nguoi_dung_id`: Foreign key → `nguoi_dung.id`
- `cau_hoi`: Câu hỏi của người dùng
- `cau_tra_loi`: Câu trả lời từ AI
- `ngay_tao`: Ngày tạo

**Relationships:**
- Thuộc về một `nguoi_dung` (user)

---

## Cài đặt và Cấu hình

### 1. Cài đặt Dependencies

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Cấu hình Database

Tạo file `.env` từ `.env.example`:

```bash
cp .env.example .env
```

Chỉnh sửa file `.env` với thông tin database của bạn:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### 3. Tạo Database

Trước khi chạy ứng dụng, tạo database trong PostgreSQL:

```sql
CREATE DATABASE ecommerce_db;
```

Hoặc sử dụng psql:

```bash
psql -U postgres -c "CREATE DATABASE ecommerce_db;"
```

### 4. Kiểm tra Kết nối

Chạy script test để kiểm tra kết nối database:

```bash
python test_connection.py
```

Script này sẽ:
- ✅ Kiểm tra kết nối database
- ✅ Tạo tất cả các bảng
- ✅ Test CRUD operations
- ✅ Hiển thị kết quả chi tiết

### 5. Chạy Ứng Dụng

```bash
# Sử dụng script run.py
python run.py

# Hoặc sử dụng uvicorn trực tiếp
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Ứng dụng sẽ chạy tại: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

---

## Database Configuration (database.py)

### Các Tính Năng

✅ **Environment Variables**: Sử dụng `python-dotenv` để load biến môi trường
- `DB_HOST`: Database host
- `DB_PORT`: Database port
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password

✅ **SQLAlchemy Engine**: 
- `pool_pre_ping=True`: Kiểm tra connection trước khi sử dụng
- `pool_size=10`: Số lượng connection tối đa trong pool
- `max_overflow=20`: Số lượng connection overflow tối đa

✅ **SessionLocal**: 
- `autocommit=False`: Không tự động commit
- `autoflush=False`: Không tự động flush

✅ **Base Class**: Sử dụng `declarative_base()` cho models

✅ **Dependency `get_db()`**: 
- Yield database session
- Tự động đóng session sau request
- Sử dụng với FastAPI Depends

✅ **Auto Table Creation**: 
- Import tất cả models
- Sử dụng `Base.metadata.create_all(bind=engine)`

✅ **Connection Check**: 
- Function `check_db_connection()` để kiểm tra kết nối

---

## Sử dụng trong FastAPI

### 1. Dependency Injection

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(SanPham).all()
    return products
```

### 2. CRUD Operations

```python
from app.models import NguoiDung, DanhMuc, SanPham
from app.database import SessionLocal

# Tạo session
db = SessionLocal()

# CREATE
nguoi_dung = NguoiDung(
    email="user@example.com",
    mat_khau="hashed_password",
    vai_tro="user"
)
db.add(nguoi_dung)
db.commit()
db.refresh(nguoi_dung)

# READ
users = db.query(NguoiDung).all()
user = db.query(NguoiDung).filter(NguoiDung.email == "user@example.com").first()

# UPDATE
user.vai_tro = "admin"
db.commit()

# DELETE
db.delete(user)
db.commit()

# Đóng session
db.close()
```

### 3. Sử dụng Relationships

```python
# Query với relationships
don_hang = db.query(DonHang).filter(DonHang.id == 1).first()

# Access user through relationship
print(don_hang.nguoi_dung.email)

# Access order items
for item in don_hang.chi_tiet_don_hang:
    print(f"Product: {item.san_pham.ten}, Quantity: {item.so_luong}")

# Access user's orders
user = db.query(NguoiDung).filter(NguoiDung.id == 1).first()
for order in user.don_hang:
    print(f"Order #{order.id}: {order.tong_tien}")
```

---

## Cấu trúc Thư mục

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   └── models/              # SQLAlchemy models
│       ├── __init__.py
│       ├── base.py
│       ├── nguoi_dung.py
│       ├── danh_muc.py
│       ├── san_pham.py
│       ├── don_hang.py
│       ├── chi_tiet_don_hang.py
│       └── lich_su_chat.py
├── .env                     # Environment variables (not in git)
├── .env.example             # Example environment variables
├── .gitignore
├── requirements.txt         # Python dependencies
├── run.py                   # Application runner
└── test_connection.py       # Database test script
```

---

## Production Best Practices

✅ **Security**:
- Sử dụng environment variables cho sensitive data
- Không commit file `.env` vào git
- Sử dụng strong passwords

✅ **Connection Pooling**:
- `pool_pre_ping=True`: Kiểm tra connection health
- `pool_size=10`: Đủ cho most applications
- `max_overflow=20`: Handle traffic spikes

✅ **Session Management**:
- Sử dụng `get_db()` dependency
- Tự động close sessions
- Avoid session leaks

✅ **Error Handling**:
- Try-except blocks trong CRUD operations
- Rollback on errors
- Proper logging

✅ **Performance**:
- Sử dụng indexes trên các cột thường query
- Eager loading với relationships khi cần
- Connection pooling

---

## Troubleshooting

### Lỗi: "could not connect to server"
- Kiểm tra PostgreSQL đang chạy
- Kiểm tra DB_HOST và DB_PORT trong `.env`
- Kiểm tra firewall settings

### Lỗi: "password authentication failed"
- Kiểm tra DB_USER và DB_PASSWORD trong `.env`
- Kiểm tra user có quyền truy cập database

### Lỗi: "database does not exist"
- Tạo database: `CREATE DATABASE ecommerce_db;`
- Kiểm tra DB_NAME trong `.env`

### Lỗi: "relation does not exist"
- Chạy `init_db()` để tạo tables
- Hoặc chạy `python test_connection.py`

---

## Đặc điểm

- ✅ Sử dụng SQLAlchemy ORM
- ✅ PostgreSQL với psycopg2-binary driver
- ✅ Environment variables với python-dotenv
- ✅ Connection pooling với pool_pre_ping
- ✅ Production-ready configuration
- ✅ Tên bảng và cột bằng tiếng Việt không dấu
- ✅ Relationships với back_populates
- ✅ Cascade deletes
- ✅ Enums cho vai_tro và trang_thai
- ✅ Automatic timestamps
- ✅ Clean, extensible code
- ✅ Comprehensive testing script


---

## Troubleshooting Table Creation Issues

If tables are not being created in PostgreSQL, use these diagnostic tools:

### Quick Diagnostic

Run the comprehensive diagnostic script:

```bash
python diagnose_db.py
```

This will check:
1. ✅ Environment variables
2. ✅ PostgreSQL connection
3. ✅ SQLAlchemy setup
4. ✅ Models import
5. ✅ Base metadata registration
6. ✅ Table creation
7. ✅ Table verification in database

### Quick Setup

To automatically create database and tables:

```bash
python setup_db.py
```

This will:
- Create the database if it doesn't exist
- Create all tables
- Verify setup is complete

### Manual Verification

Check if tables exist in PostgreSQL:

```sql
-- Connect to database
psql -U postgres -d ecommerce_db

-- List all tables
\dt

-- Or use SQL query
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

### Debug Endpoint

When the application is running, visit:

```
http://localhost:8000/debug/tables
```

This will show:
- Registered models in SQLAlchemy
- Actual tables in database
- Comparison between expected and actual

### Common Issues and Solutions

#### Issue 1: Models not registered with Base

**Symptom**: `Base.metadata.tables` is empty

**Solution**: Ensure all models inherit from the same `Base` instance:

```python
# ❌ Wrong - creates separate Base
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# ✅ Correct - use Base from database.py
from app.database import Base
```

#### Issue 2: Models not imported before create_all()

**Symptom**: Tables not created even though models exist

**Solution**: Import all models before calling `create_all()`:

```python
# Import all models first
from app.models import (
    NguoiDung,
    DanhMuc,
    SanPham,
    DonHang,
    ChiTietDonHang,
    LichSuChat,
)

# Then create tables
Base.metadata.create_all(bind=engine)
```

#### Issue 3: Wrong database URL

**Symptom**: Connection fails or wrong database

**Solution**: Check `.env` file:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=your_password
```

#### Issue 4: Database doesn't exist

**Symptom**: `database "ecommerce_db" does not exist`

**Solution**: Create the database:

```bash
# Using psql
psql -U postgres -c "CREATE DATABASE ecommerce_db;"

# Or run setup script
python setup_db.py
```

#### Issue 5: Permission denied

**Symptom**: `permission denied for schema public`

**Solution**: Grant permissions:

```sql
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO your_user;
GRANT ALL ON SCHEMA public TO your_user;
```

### Logging

Enable SQL query logging for debugging:

```python
# In database.py
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Enable SQL logging
    pool_pre_ping=True,
)
```

This will print all SQL queries to console.

### Reset Database

To completely reset the database (⚠️ deletes all data):

```python
from app.database import reset_db

reset_db()  # Drops and recreates all tables
```

Or manually:

```bash
# Drop and recreate database
psql -U postgres -c "DROP DATABASE IF EXISTS ecommerce_db;"
psql -U postgres -c "CREATE DATABASE ecommerce_db;"

# Run setup
python setup_db.py
```

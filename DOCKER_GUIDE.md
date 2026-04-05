# Docker Setup Guide - Electronics E-Commerce

## 📦 Cấu trúc Docker

Project sử dụng 3 containers:

1. **PostgreSQL** - Database (Port 5432)
2. **pgAdmin** - Database management UI (Port 5050)
3. **FastAPI Backend** - API server (Port 8000)

---

## 🚀 Cách chạy Docker

### Bước 1: Khởi động tất cả services

```bash
docker-compose up -d
```

Lệnh này sẽ:
- ✅ Tạo và khởi động PostgreSQL container
- ✅ Tạo và khởi động pgAdmin container
- ✅ Build và khởi động FastAPI backend container
- ✅ Tự động tạo database `electronics_db`
- ✅ Tự động tạo tất cả 6 tables

### Bước 2: Kiểm tra containers đang chạy

```bash
docker-compose ps
```

Kết quả mong đợi:
```
NAME                    STATUS              PORTS
electronics_postgres    Up                  0.0.0.0:5432->5432/tcp
electronics_pgadmin     Up                  0.0.0.0:5050->80/tcp
electronics_backend     Up                  0.0.0.0:8000->8000/tcp
```

### Bước 3: Xem logs

```bash
# Xem logs tất cả services
docker-compose logs -f

# Xem logs của backend
docker-compose logs -f backend

# Xem logs của PostgreSQL
docker-compose logs -f postgres

# Xem logs của pgAdmin
docker-compose logs -f pgadmin
```

---

## 🗄️ Truy cập pgAdmin

### 1. Mở pgAdmin trong browser

```
http://localhost:5050
```

### 2. Đăng nhập pgAdmin

- **Email**: `admin@admin.com`
- **Password**: `admin`

### 3. Kết nối đến PostgreSQL Server

**Bước 3.1**: Click chuột phải vào "Servers" → "Register" → "Server"

**Bước 3.2**: Tab "General"
- **Name**: `Electronics DB` (hoặc tên bất kỳ)

**Bước 3.3**: Tab "Connection"
- **Host name/address**: `postgres` (tên container)
- **Port**: `5432`
- **Maintenance database**: `postgres`
- **Username**: `postgres`
- **Password**: `123456`
- ✅ Tick "Save password"

**Bước 3.4**: Click "Save"

### 4. Xem Tables trong pgAdmin

Sau khi kết nối thành công:

```
Servers
  └── Electronics DB
      └── Databases
          └── electronics_db
              └── Schemas
                  └── public
                      └── Tables
                          ├── chi_tiet_don_hang
                          ├── danh_muc
                          ├── don_hang
                          ├── lich_su_chat
                          ├── nguoi_dung
                          └── san_pham
```

---

## 🔍 Kiểm tra Tables đã được tạo

### Cách 1: Sử dụng Docker exec

```bash
# Kết nối vào PostgreSQL container
docker exec -it electronics_postgres psql -U postgres -d electronics_db

# Trong psql, chạy:
\dt

# Hoặc query SQL:
SELECT table_name FROM information_schema.tables WHERE table_schema='public';

# Thoát psql:
\q
```

### Cách 2: Sử dụng API endpoint

```bash
# Kiểm tra health
curl http://localhost:8000/health

# Kiểm tra tables
curl http://localhost:8000/debug/tables
```

### Cách 3: Xem trong pgAdmin

1. Mở pgAdmin: http://localhost:5050
2. Navigate: Electronics DB → electronics_db → Schemas → public → Tables
3. Bạn sẽ thấy 6 tables

---

## 📊 Truy cập các Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **FastAPI API** | http://localhost:8000 | - |
| **API Docs** | http://localhost:8000/docs | - |
| **pgAdmin** | http://localhost:5050 | admin@admin.com / admin |
| **PostgreSQL** | localhost:5432 | postgres / 123456 |

---

## 🛠️ Các lệnh Docker hữu ích

### Quản lý containers

```bash
# Khởi động tất cả services
docker-compose up -d

# Dừng tất cả services
docker-compose down

# Dừng và xóa volumes (⚠️ xóa data!)
docker-compose down -v

# Restart tất cả services
docker-compose restart

# Restart một service cụ thể
docker-compose restart backend

# Dừng một service
docker-compose stop backend

# Khởi động một service
docker-compose start backend
```

### Xem logs

```bash
# Logs tất cả services
docker-compose logs -f

# Logs backend only
docker-compose logs -f backend

# Logs 100 dòng cuối
docker-compose logs --tail=100 backend
```

### Rebuild containers

```bash
# Rebuild backend sau khi thay đổi code
docker-compose up -d --build backend

# Rebuild tất cả
docker-compose up -d --build
```

### Truy cập vào container

```bash
# Vào backend container
docker exec -it electronics_backend bash

# Vào PostgreSQL container
docker exec -it electronics_postgres bash

# Chạy psql trực tiếp
docker exec -it electronics_postgres psql -U postgres -d electronics_db
```

---

## 🔧 Chạy lệnh trong container

### Tạo lại tables

```bash
# Chạy fix_tables.py trong container
docker exec -it electronics_backend python fix_tables.py
```

### Chạy migrations

```bash
# Nếu có Alembic migrations
docker exec -it electronics_backend alembic upgrade head
```

### Chạy tests

```bash
# Chạy tests
docker exec -it electronics_backend pytest
```

---

## 📝 Import/Export Data

### Export database

```bash
# Export toàn bộ database
docker exec -it electronics_postgres pg_dump -U postgres electronics_db > backup.sql

# Export chỉ schema (không có data)
docker exec -it electronics_postgres pg_dump -U postgres --schema-only electronics_db > schema.sql

# Export chỉ data
docker exec -it electronics_postgres pg_dump -U postgres --data-only electronics_db > data.sql
```

### Import database

```bash
# Import từ file SQL
docker exec -i electronics_postgres psql -U postgres electronics_db < backup.sql

# Hoặc copy file vào container rồi import
docker cp backup.sql electronics_postgres:/tmp/
docker exec -it electronics_postgres psql -U postgres electronics_db -f /tmp/backup.sql
```

---

## 🐛 Troubleshooting

### Issue 1: Container không start

```bash
# Xem logs để tìm lỗi
docker-compose logs backend

# Kiểm tra status
docker-compose ps
```

### Issue 2: PostgreSQL không ready

```bash
# Kiểm tra health
docker exec -it electronics_postgres pg_isready -U postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### Issue 3: Tables không được tạo

```bash
# Chạy lại script tạo tables
docker exec -it electronics_backend python fix_tables.py

# Hoặc restart backend
docker-compose restart backend
```

### Issue 4: Port đã được sử dụng

Nếu port 5432, 5050, hoặc 8000 đã được sử dụng, sửa trong `docker-compose.yml`:

```yaml
ports:
  - "5433:5432"  # Thay 5432 thành 5433
```

### Issue 5: Xóa và tạo lại từ đầu

```bash
# Dừng và xóa tất cả (bao gồm volumes)
docker-compose down -v

# Xóa images
docker-compose down --rmi all

# Tạo lại từ đầu
docker-compose up -d --build
```

---

## 🔐 Thay đổi Passwords

### Thay đổi PostgreSQL password

Sửa trong `docker-compose.yml`:

```yaml
postgres:
  environment:
    POSTGRES_PASSWORD: your_new_password

backend:
  environment:
    DB_PASSWORD: your_new_password
```

Sau đó:
```bash
docker-compose down -v
docker-compose up -d
```

### Thay đổi pgAdmin password

Sửa trong `docker-compose.yml`:

```yaml
pgadmin:
  environment:
    PGADMIN_DEFAULT_EMAIL: your_email@example.com
    PGADMIN_DEFAULT_PASSWORD: your_new_password
```

---

## 📊 Monitoring

### Xem resource usage

```bash
# Xem CPU, Memory usage
docker stats

# Xem disk usage
docker system df
```

### Xem network

```bash
# List networks
docker network ls

# Inspect network
docker network inspect electronics_network
```

---

## 🎯 Quick Commands

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f backend

# Access PostgreSQL
docker exec -it electronics_postgres psql -U postgres -d electronics_db

# Recreate tables
docker exec -it electronics_backend python fix_tables.py

# Stop everything
docker-compose down

# Clean everything (⚠️ deletes data!)
docker-compose down -v
```

---

## ✅ Verification Checklist

Sau khi chạy `docker-compose up -d`, kiểm tra:

- [ ] 3 containers đang chạy: `docker-compose ps`
- [ ] Backend API: http://localhost:8000
- [ ] API Docs: http://localhost:8000/docs
- [ ] pgAdmin: http://localhost:5050
- [ ] Tables exist: http://localhost:8000/debug/tables
- [ ] PostgreSQL accessible: `docker exec -it electronics_postgres psql -U postgres -d electronics_db -c "\dt"`

---

## 🎉 Success!

Nếu tất cả đều hoạt động:

✅ PostgreSQL running on port 5432
✅ pgAdmin accessible at http://localhost:5050
✅ FastAPI running on port 8000
✅ All 6 tables created in electronics_db
✅ Ready for development!

**Enjoy coding! 🚀**

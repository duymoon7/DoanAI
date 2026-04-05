# 🔧 pgAdmin Setup Guide

Step-by-step guide to connect pgAdmin to your PostgreSQL database.

---

## 📋 Prerequisites

Make sure Docker services are running:
```bash
docker-compose up -d
```

---

## 🌐 Step 1: Access pgAdmin

Open your browser and go to:
```
http://localhost:5050
```

---

## 🔐 Step 2: Login to pgAdmin

Enter the credentials:
- **Email**: `admin@admin.com`
- **Password**: `admin`

Click "Login"

---

## 🖥️ Step 3: Register PostgreSQL Server

### 3.1 Open Server Registration
1. In the left sidebar, right-click on "Servers"
2. Select "Register" → "Server..."

### 3.2 General Tab
Fill in:
- **Name**: `Electronics DB` (or any name you prefer)
- **Server group**: `Servers` (default)
- **Comments**: `E-Commerce PostgreSQL Database` (optional)

### 3.3 Connection Tab
Fill in these EXACT values:

| Field | Value |
|-------|-------|
| **Host name/address** | `postgres` |
| **Port** | `5432` |
| **Maintenance database** | `electronics_db` |
| **Username** | `postgres` |
| **Password** | `123456` |
| **Save password?** | ✅ Check this box |

⚠️ **IMPORTANT**: Use `postgres` as hostname, NOT `localhost`!

### 3.4 SSL Tab (Optional)
- **SSL mode**: `Prefer` (default is fine)

### 3.5 Advanced Tab (Optional)
- Leave as default

---

## ✅ Step 4: Save and Connect

1. Click "Save" button
2. pgAdmin will connect to PostgreSQL
3. You should see "Electronics DB" in the left sidebar

---

## 🗄️ Step 5: Browse Database

### View Tables
1. Expand "Electronics DB" in sidebar
2. Expand "Databases"
3. Expand "electronics_db"
4. Expand "Schemas"
5. Expand "public"
6. Expand "Tables"

You should see 6 tables:
- chi_tiet_don_hang
- danh_muc
- don_hang
- lich_su_chat
- nguoi_dung
- san_pham

### View Data
1. Right-click on any table (e.g., "san_pham")
2. Select "View/Edit Data" → "All Rows"
3. You'll see the data in a grid

---

## 🔍 Step 6: Run SQL Queries

### Open Query Tool
1. Right-click on "electronics_db"
2. Select "Query Tool"

### Example Queries

#### View all products
```sql
SELECT * FROM san_pham;
```

#### View products with categories
```sql
SELECT 
    sp.ten_san_pham,
    sp.gia,
    dm.ten_danh_muc
FROM san_pham sp
JOIN danh_muc dm ON sp.id_danh_muc = dm.id
ORDER BY sp.gia DESC;
```

#### Count products by category
```sql
SELECT 
    dm.ten_danh_muc,
    COUNT(sp.id) as so_luong
FROM danh_muc dm
LEFT JOIN san_pham sp ON dm.id = sp.id_danh_muc
GROUP BY dm.ten_danh_muc
ORDER BY so_luong DESC;
```

#### View expensive products (> 10 million)
```sql
SELECT 
    ten_san_pham,
    gia,
    so_luong_ton_kho
FROM san_pham
WHERE gia > 10000000
ORDER BY gia DESC;
```

---

## 🛠️ Common Tasks

### Export Data
1. Right-click on table
2. Select "Import/Export Data..."
3. Choose format (CSV, JSON, etc.)
4. Click "OK"

### Backup Database
1. Right-click on "electronics_db"
2. Select "Backup..."
3. Choose filename and location
4. Click "Backup"

### Restore Database
1. Right-click on "electronics_db"
2. Select "Restore..."
3. Choose backup file
4. Click "Restore"

### View Table Structure
1. Right-click on table
2. Select "Properties"
3. View columns, constraints, indexes

---

## 🐛 Troubleshooting

### Cannot connect to server
**Error**: "could not connect to server"

**Solutions**:
1. Verify PostgreSQL is running:
   ```bash
   docker-compose ps
   ```
2. Check you used `postgres` as hostname (not `localhost`)
3. Verify credentials are correct
4. Wait 30 seconds for PostgreSQL to start
5. Check logs:
   ```bash
   docker-compose logs postgres
   ```

### Password authentication failed
**Error**: "password authentication failed"

**Solutions**:
1. Verify password is `123456`
2. Verify username is `postgres`
3. Check docker-compose.yml environment variables

### Database does not exist
**Error**: "database 'electronics_db' does not exist"

**Solutions**:
1. Check backend logs:
   ```bash
   docker-compose logs backend
   ```
2. Verify backend started successfully
3. Restart services:
   ```bash
   docker-compose restart
   ```

### Connection timeout
**Error**: "connection timeout"

**Solutions**:
1. Ensure Docker network is working
2. Restart Docker Desktop
3. Check firewall settings
4. Try restarting containers:
   ```bash
   docker-compose restart
   ```

---

## 📊 Useful SQL Queries

### Database Statistics
```sql
-- Count rows in each table
SELECT 
    'nguoi_dung' as table_name, COUNT(*) as rows FROM nguoi_dung
UNION ALL
SELECT 'danh_muc', COUNT(*) FROM danh_muc
UNION ALL
SELECT 'san_pham', COUNT(*) FROM san_pham
UNION ALL
SELECT 'don_hang', COUNT(*) FROM don_hang
UNION ALL
SELECT 'chi_tiet_don_hang', COUNT(*) FROM chi_tiet_don_hang
UNION ALL
SELECT 'lich_su_chat', COUNT(*) FROM lich_su_chat;
```

### Table Sizes
```sql
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Recent Products
```sql
SELECT 
    ten_san_pham,
    gia,
    ngay_tao
FROM san_pham
ORDER BY ngay_tao DESC
LIMIT 10;
```

---

## 🎯 Quick Reference

### Connection Details
```
Host: postgres
Port: 5432
Database: electronics_db
User: postgres
Password: 123456
```

### pgAdmin Access
```
URL: http://localhost:5050
Email: admin@admin.com
Password: admin
```

### Docker Commands
```bash
# View logs
docker-compose logs pgadmin

# Restart pgAdmin
docker-compose restart pgadmin

# Access pgAdmin container
docker-compose exec pgadmin sh
```

---

## 📚 Additional Resources

- pgAdmin Documentation: https://www.pgadmin.org/docs/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- SQL Tutorial: https://www.postgresql.org/docs/current/tutorial.html

---

## ✅ Success Checklist

- [ ] Can access pgAdmin at http://localhost:5050
- [ ] Can login with admin@admin.com / admin
- [ ] Successfully registered PostgreSQL server
- [ ] Can see "Electronics DB" in sidebar
- [ ] Can expand and view 6 tables
- [ ] Can view data in tables
- [ ] Can run SQL queries
- [ ] Can see 14 products in san_pham table
- [ ] Can see 6 categories in danh_muc table

---

**🎉 pgAdmin is now connected to your PostgreSQL database!**

You can now:
- Browse tables and data
- Run SQL queries
- Export/import data
- Backup/restore database
- Monitor database performance

# ⚡ Quick Reference Card

Essential commands and information for the E-Commerce Docker environment.

---

## 🚀 Start

```bash
docker-compose up --build
```

Wait 30-60 seconds for all services to start.

---

## 🌐 Access URLs

| Service | URL | Login |
|---------|-----|-------|
| **API Docs** | http://localhost:8000/docs | - |
| **Health** | http://localhost:8000/health | - |
| **pgAdmin** | http://localhost:5050 | admin@admin.com / admin |
| **Frontend** | http://localhost:3000 | (run separately) |

---

## 🔐 Credentials

### PostgreSQL
```
Host: postgres (Docker) or localhost (host)
Port: 5432
Database: electronics_db
User: postgres
Password: 123456
```

### pgAdmin
```
Email: admin@admin.com
Password: admin
```

---

## 🛠️ Essential Commands

```bash
# Start (foreground)
docker-compose up

# Start (background)
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# View logs
docker-compose logs -f backend

# Check status
docker-compose ps

# Clean restart (deletes data)
docker-compose down -v && docker-compose up --build
```

---

## 🔍 Verify Setup

```bash
# Windows
.\verify_docker.ps1

# Linux/Mac
./verify_docker.sh

# Manual check
curl http://localhost:8000/health
```

---

## 📊 API Endpoints

Base: `http://localhost:8000/api`

```
GET    /san-pham              # List products
GET    /san-pham/{id}         # Get product
POST   /san-pham              # Create product
PUT    /san-pham/{id}         # Update product
DELETE /san-pham/{id}         # Delete product

GET    /danh-muc              # List categories
GET    /don-hang              # List orders
GET    /nguoi-dung            # List users
```

---

## 🐛 Quick Fixes

### Backend not responding
```bash
docker-compose restart backend
docker-compose logs -f backend
```

### Database connection failed
```bash
# Wait 30 seconds, then:
docker-compose restart postgres
docker-compose logs postgres
```

### Port in use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Reset everything
```bash
docker-compose down -v
docker-compose up --build
```

---

## 📦 Data

### Categories (6)
- Điện thoại
- Laptop
- Tablet
- Phụ kiện
- Tai nghe
- Đồng hồ thông minh

### Products (14)
Auto-seeded on first startup.

---

## 🎯 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Access at: http://localhost:3000

---

## 📚 Documentation

- **DOCKER_QUICK_START.md** - Detailed Docker guide
- **DOCKER_COMPLETE_SETUP.md** - Complete setup info
- **START_SERVICES.md** - Service startup guide
- **README.md** - Project overview

---

## ✅ Success Indicators

- ✅ `docker-compose ps` shows 3 services "Up"
- ✅ http://localhost:8000/health returns "healthy"
- ✅ http://localhost:8000/docs shows Swagger UI
- ✅ http://localhost:5050 shows pgAdmin login
- ✅ Can fetch products: `curl http://localhost:8000/api/san-pham`

---

## 🔄 Development Workflow

1. Start Docker: `docker-compose up -d`
2. Edit code in `backend/` folder
3. Changes auto-reload (FastAPI --reload)
4. View logs: `docker-compose logs -f backend`
5. Test API: http://localhost:8000/docs
6. Stop: `docker-compose down`

---

## 💡 Tips

- Use `-d` flag to run in background
- Use `docker-compose logs -f` to follow logs
- Backend auto-reloads on code changes
- Data persists in Docker volumes
- Use `down -v` to delete all data

---

**Need more help?** See [DOCKER_QUICK_START.md](DOCKER_QUICK_START.md)

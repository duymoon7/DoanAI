# 🚀 Start Services - Complete Guide

Quick reference for starting the E-Commerce platform.

---

## 🐳 Method 1: Docker (Recommended)

### Start Everything

```bash
docker-compose up --build
```

Wait for:
- ✅ PostgreSQL ready (10-15 seconds)
- ✅ Backend started (20-30 seconds)
- ✅ Tables created automatically
- ✅ Data seeded automatically

### Verify Services

**Windows:**
```powershell
.\verify_docker.ps1
```

**Linux/Mac:**
```bash
chmod +x verify_docker.sh
./verify_docker.sh
```

### Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| Backend API | http://localhost:8000/docs | - |
| Health Check | http://localhost:8000/health | - |
| pgAdmin | http://localhost:5050 | admin@admin.com / admin |
| PostgreSQL | localhost:5432 | postgres / 123456 |

---

## 💻 Method 2: Local Development

### 1. Start PostgreSQL

Ensure PostgreSQL is running on port 5432.

### 2. Start Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### 3. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔍 Verification Steps

### 1. Check Backend Health

```bash
curl http://localhost:8000/health
```

Expected:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### 2. Check Database Tables

```bash
curl http://localhost:8000/debug/tables
```

Should show 6 tables.

### 3. Check Products

```bash
curl http://localhost:8000/api/san-pham
```

Should return 14 products.

### 4. Check Frontend

Open http://localhost:3000 - should see product listing.

---

## 🛑 Stop Services

### Docker

```bash
# Stop services
docker-compose down

# Stop and remove data
docker-compose down -v
```

### Local

- Press `Ctrl+C` in backend terminal
- Press `Ctrl+C` in frontend terminal

---

## 🔄 Restart Services

### Docker

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Local

Just stop and start again.

---

## 📊 View Logs

### Docker

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f postgres
```

### Local

Logs appear in terminal where service is running.

---

## 🐛 Troubleshooting

### Port Already in Use

**Windows:**
```powershell
# Find process on port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
```

### Docker Not Starting

1. Ensure Docker Desktop is running
2. Check available disk space
3. Try: `docker-compose down -v && docker-compose up --build`

### Backend Can't Connect to Database

1. Wait 30 seconds for PostgreSQL to start
2. Check logs: `docker-compose logs postgres`
3. Verify health: `docker-compose ps`

### Frontend Can't Connect to Backend

1. Ensure backend is running: http://localhost:8000/health
2. Check CORS settings in backend/app/main.py
3. Verify .env.local has correct API URL

---

## 🎯 Quick Commands

```bash
# Start (detached)
docker-compose up -d

# View status
docker-compose ps

# View logs
docker-compose logs -f backend

# Restart backend
docker-compose restart backend

# Stop all
docker-compose down

# Clean restart
docker-compose down -v && docker-compose up --build
```

---

## ✅ Success Indicators

You know everything is working when:

- ✅ `docker-compose ps` shows all services "Up"
- ✅ http://localhost:8000/health returns "healthy"
- ✅ http://localhost:8000/docs shows API documentation
- ✅ http://localhost:5050 shows pgAdmin login
- ✅ http://localhost:3000 shows product listing
- ✅ Can add products to cart
- ✅ Cart persists on page refresh

---

## 📚 Next Steps

1. **Explore API**: http://localhost:8000/docs
2. **View Database**: http://localhost:5050
3. **Test Frontend**: http://localhost:3000
4. **Read Documentation**: See README.md

---

**Need help?** Check [DOCKER_QUICK_START.md](DOCKER_QUICK_START.md) for detailed instructions.

# 🚀 Quick Start - Docker Environment

## ⚠️ Prerequisites

1. **Docker Desktop** must be installed and running
   - Download: https://www.docker.com/products/docker-desktop
   - After installation, start Docker Desktop
   - Wait for Docker to be ready (whale icon in system tray)

---

## 🎯 Step-by-Step Guide

### Step 1: Start Docker Desktop

1. Open Docker Desktop application
2. Wait until you see "Docker Desktop is running" 
3. Verify Docker is running:
   ```bash
   docker --version
   docker-compose --version
   ```

### Step 2: Build and Start Services

```bash
# Navigate to project root
cd D:\doanAi

# Build and start all services
docker-compose up --build
```

**What happens:**
- ✅ Builds FastAPI backend image
- ✅ Pulls PostgreSQL 15 image
- ✅ Pulls pgAdmin 4 image
- ✅ Creates network
- ✅ Starts PostgreSQL
- ✅ Starts pgAdmin
- ✅ Starts FastAPI backend
- ✅ Creates database tables
- ✅ Seeds sample data

**Wait for these messages:**
```
✅ Database seeding completed successfully!
📊 Summary:
   - Categories: 4
   - Users: 3
   - Products: 10
   - Orders: 3
   - Order Items: 5
```

### Step 3: Verify Services

Open in browser:

1. **Backend API**: http://localhost:8000
   - Should show: `{"message": "E-Commerce API is running!"}`

2. **API Documentation**: http://localhost:8000/docs
   - Interactive Swagger UI

3. **pgAdmin**: http://localhost:5050
   - Login: `admin@admin.com` / `admin`

### Step 4: Connect pgAdmin to Database

1. Open http://localhost:5050
2. Login with `admin@admin.com` / `admin`
3. Right-click "Servers" → "Register" → "Server"
4. **General tab**:
   - Name: `Electronics DB`
5. **Connection tab**:
   - Host: `postgres`
   - Port: `5432`
   - Database: `electronics_db`
   - Username: `postgres`
   - Password: `123456`
   - ✅ Save password
6. Click "Save"

### Step 5: Start Frontend

Open new terminal:

```bash
cd frontend
npm run dev
```

Frontend: http://localhost:3000

---

## 🎉 Success!

You should now have:

- ✅ Backend API: http://localhost:8000
- ✅ API Docs: http://localhost:8000/docs
- ✅ pgAdmin: http://localhost:5050
- ✅ Frontend: http://localhost:3000
- ✅ Database with sample data

---

## 🛑 Stop Services

```bash
# Stop all containers (keeps data)
docker-compose down

# Stop and remove all data
docker-compose down -v
```

---

## 🔄 Restart Services

```bash
# Start existing containers
docker-compose up

# Rebuild and start
docker-compose up --build
```

---

## 📊 View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# PostgreSQL only
docker-compose logs -f postgres
```

---

## 🐛 Troubleshooting

### Docker Desktop not running

**Error:**
```
error during connect: ... The system cannot find the file specified
```

**Solution:**
1. Start Docker Desktop
2. Wait for it to be ready
3. Try again

### Port already in use

**Error:**
```
Bind for 0.0.0.0:8000 failed: port is already allocated
```

**Solution:**
```bash
# Find process using port
netstat -ano | findstr :8000

# Kill process
taskkill /PID <process_id> /F

# Or change port in docker-compose.yml
```

### Backend won't start

**Check logs:**
```bash
docker-compose logs backend
```

**Common issues:**
- PostgreSQL not ready (wait 10-20 seconds)
- Database connection error
- Port conflict

**Solution:**
```bash
docker-compose restart backend
```

### Clean slate

```bash
# Remove everything
docker-compose down -v --rmi all

# Start fresh
docker-compose up --build
```

---

## 📝 Quick Commands

```bash
# Start everything
docker-compose up -d

# View status
docker-compose ps

# View logs
docker-compose logs -f backend

# Restart backend
docker-compose restart backend

# Stop everything
docker-compose down

# Clean everything
docker-compose down -v
```

---

## ✅ Verification Checklist

- [ ] Docker Desktop is running
- [ ] `docker-compose up --build` completed successfully
- [ ] Backend responds: http://localhost:8000
- [ ] API docs accessible: http://localhost:8000/docs
- [ ] pgAdmin accessible: http://localhost:5050
- [ ] Can connect to database in pgAdmin
- [ ] 6 tables created
- [ ] 10 products in database
- [ ] Frontend running: http://localhost:3000

---

**🎊 Ready to develop!**

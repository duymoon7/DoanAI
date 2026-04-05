# 🐳 Docker Quick Start Guide

Complete guide to run the E-Commerce application with Docker.

## 📋 Prerequisites

- Docker Desktop installed
- Docker Compose installed
- Ports available: 5432 (PostgreSQL), 8000 (Backend), 5050 (pgAdmin)

## 🚀 Quick Start

### 1. Start All Services

```bash
docker-compose up --build
```

This command will:
- Build the FastAPI backend image
- Start PostgreSQL database
- Start pgAdmin
- Auto-create all database tables
- Auto-seed initial data (categories & products)

### 2. Access Services

Once all services are running:

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050
- **Health Check**: http://localhost:8000/health

## 🔐 Login Credentials

### pgAdmin
- **URL**: http://localhost:5050
- **Email**: admin@admin.com
- **Password**: admin

### PostgreSQL Database
- **Host**: postgres (inside Docker) or localhost (from host)
- **Port**: 5432
- **Database**: electronics_db
- **User**: postgres
- **Password**: 123456

## 📊 Connect pgAdmin to PostgreSQL

1. Open pgAdmin at http://localhost:5050
2. Login with credentials above
3. Right-click "Servers" → "Register" → "Server"
4. **General Tab**:
   - Name: Electronics DB
5. **Connection Tab**:
   - Host: `postgres`
   - Port: `5432`
   - Database: `electronics_db`
   - Username: `postgres`
   - Password: `123456`
6. Click "Save"

## 🛠️ Useful Commands

### Start services (detached mode)
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### Stop and remove volumes (⚠️ deletes all data)
```bash
docker-compose down -v
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f postgres
```

### Restart a service
```bash
docker-compose restart backend
```

### Rebuild backend only
```bash
docker-compose up -d --build backend
```

### Execute commands in containers
```bash
# Access backend shell
docker-compose exec backend bash

# Access PostgreSQL shell
docker-compose exec postgres psql -U postgres -d electronics_db
```

## 🔍 Verify Installation

### 1. Check Backend Health
```bash
curl http://localhost:8000/health
```

Expected response:
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

Should show 6 tables created.

### 3. Check Products
```bash
curl http://localhost:8000/api/san-pham
```

Should return list of products.

## 📦 Initial Data

The system automatically seeds:
- **6 Categories**: Điện thoại, Laptop, Tablet, Phụ kiện, Tai nghe, Đồng hồ thông minh
- **14 Products**: Various electronics products with Vietnamese names

## 🐛 Troubleshooting

### Backend can't connect to database
- Wait 30 seconds for PostgreSQL to fully start
- Check logs: `docker-compose logs postgres`
- Verify health: `docker-compose ps`

### Port already in use
```bash
# Find process using port
netstat -ano | findstr :8000

# Stop the process or change port in docker-compose.yml
```

### Reset everything
```bash
# Stop and remove all containers, networks, and volumes
docker-compose down -v

# Rebuild and start fresh
docker-compose up --build
```

### View container status
```bash
docker-compose ps
```

### Access backend logs
```bash
docker-compose logs -f backend
```

## 🔄 Development Workflow

The backend uses volume mounting, so code changes are reflected immediately:

1. Edit code in `backend/` directory
2. FastAPI auto-reloads (--reload flag)
3. Changes appear instantly

## 🌐 CORS Configuration

Backend allows requests from:
- http://localhost:3000
- http://127.0.0.1:3000
- http://frontend:3000

## 📝 Environment Variables

Backend environment (configured in docker-compose.yml):
```
DB_HOST=postgres
DB_PORT=5432
DB_NAME=electronics_db
DB_USER=postgres
DB_PASSWORD=123456
```

## 🎯 Next Steps

1. Start frontend: `cd frontend && npm run dev`
2. Test API endpoints at http://localhost:8000/docs
3. View database in pgAdmin at http://localhost:5050
4. Build your features!

## 📚 Additional Resources

- FastAPI Documentation: https://fastapi.tiangolo.com
- Docker Compose: https://docs.docker.com/compose
- PostgreSQL: https://www.postgresql.org/docs

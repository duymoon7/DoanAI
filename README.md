# 🛒 ElectroShop - E-Commerce Platform

Modern, full-stack e-commerce platform for electronics with clean UI and professional design.

---

## 🚀 QUICK START

### Mới clone về? Đọc ngay:
- **[GETTING_STARTED.md](GETTING_STARTED.md)** ⭐ - Bắt đầu nhanh (3 bước)
- **[HUONG_DAN_CAI_DAT.md](HUONG_DAN_CAI_DAT.md)** 📖 - Hướng dẫn chi tiết từ A-Z

### Đã cài đặt rồi?
```bash
# Terminal 1: Backend
docker-compose up -d

# Terminal 2: Frontend
cd frontend
npm run dev
```

Truy cập: http://localhost:3000

---

## 🎯 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM
- **Docker** - Containerization

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS
- **Axios** - HTTP client

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker Desktop installed and running

**Steps:**
```bash
# 1. Start Docker environment
docker-compose up --build

# 2. Start frontend (new terminal)
cd frontend
npm run dev
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- pgAdmin: http://localhost:5050

### Option 2: Local Development

**Prerequisites:**
- Python 3.8+
- Node.js 18+
- PostgreSQL 12+

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python run.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 📊 Features

### Frontend
- ✅ Clean, minimalist UI (Amazon + Shopee inspired)
- ✅ Product listing with filters and sorting
- ✅ Product detail pages
- ✅ Shopping cart with localStorage
- ✅ Responsive design (mobile-first)
- ✅ Loading skeletons
- ✅ Toast notifications
- ✅ Search functionality
- ✅ Authentication pages

### Backend
- ✅ RESTful API with FastAPI
- ✅ 6 database models (Users, Categories, Products, Orders, Order Items, Chat)
- ✅ CRUD operations
- ✅ Auto table creation
- ✅ Sample data seeding
- ✅ API documentation (Swagger)
- ✅ CORS configuration
- ✅ Health checks

---

## 🗄️ Database Schema

### Tables (6)
1. **nguoi_dung** - Users (admin/user roles)
2. **danh_muc** - Categories
3. **san_pham** - Products
4. **don_hang** - Orders
5. **chi_tiet_don_hang** - Order items
6. **lich_su_chat** - Chat history

### Sample Data
- 4 categories (Phones, Laptops, Headphones, Accessories)
- 10 products (iPhone, Samsung, MacBook, etc.)
- 3 users (1 admin, 2 regular users)
- 3 sample orders

---

## 📁 Project Structure

```
doanAi/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   ├── routers/         # API endpoints
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── database.py      # DB configuration
│   │   └── main.py          # FastAPI app
│   ├── Dockerfile
│   ├── requirements.txt
│   └── seed_docker.py       # Auto-seed script
├── frontend/
│   ├── app/                 # Next.js pages
│   ├── components/          # React components
│   ├── contexts/            # State management
│   ├── lib/                 # API & types
│   └── public/              # Static files
├── docker-compose.yml
└── README.md
```

---

## 🔌 API Endpoints

Base URL: `http://localhost:8000/api`

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/san-pham` | GET, POST, PUT, DELETE | Products |
| `/danh-muc` | GET, POST, PUT, DELETE | Categories |
| `/don-hang` | GET, POST, PUT, DELETE | Orders |
| `/nguoi-dung` | GET, POST, PUT, DELETE | Users |
| `/chi-tiet-don-hang` | GET, POST | Order Items |
| `/lich-su-chat` | GET, POST | Chat History |

**Documentation:** http://localhost:8000/docs

---

## 🐳 Docker Services

### PostgreSQL
- Port: 5432
- User: `postgres`
- Password: `123456`
- Database: `electronics_db`

### pgAdmin
- Port: 5050
- Email: `admin@admin.com`
- Password: `admin`

### Backend
- Port: 8000
- Auto-reload enabled
- Health checks configured

---

## 📚 Documentation

- **[START_DOCKER.md](START_DOCKER.md)** - Quick start with Docker
- **[DOCKER_SETUP.md](DOCKER_SETUP.md)** - Complete Docker guide
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Local development setup
- **[backend/API_GUIDE.md](backend/API_GUIDE.md)** - API testing guide
- **[backend/README.md](backend/README.md)** - Backend documentation
- **[frontend/README.md](frontend/README.md)** - Frontend documentation

---

## 🛠️ Development

### Backend Development

```bash
cd backend

# Run locally
python run.py

# Run tests
python test_connection.py

# Seed data
python seed_docker.py
```

### Frontend Development

```bash
cd frontend

# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

### Docker Development

```bash
# Start all services
docker-compose up

# Rebuild backend
docker-compose up --build backend

# View logs
docker-compose logs -f backend

# Restart service
docker-compose restart backend

# Stop all
docker-compose down
```

---

## 🎨 Design System

### Colors
- **Primary**: #0ea5e9 (Sky Blue)
- **Accent**: #fb923c (Orange)
- **Background**: #f9fafb (Gray 50)

### Components
- Clean, minimalist cards
- Smooth hover effects
- Soft shadows
- Rounded corners
- Professional typography

---

## 🔐 Environment Variables

### Backend (.env)
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=electronics_db
DB_USER=postgres
DB_PASSWORD=123456
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

---

## 🐛 Troubleshooting

### Docker not starting
- Ensure Docker Desktop is running
- Check ports 5432, 5050, 8000 are available
- View logs: `docker-compose logs`

### Backend connection error
- Verify PostgreSQL is running
- Check database credentials
- Wait for database to be ready (10-20 seconds)

### Frontend can't connect to API
- Ensure backend is running on port 8000
- Check CORS configuration
- Verify API URL in .env.local

---

## 📝 Common Commands

```bash
# Docker
docker-compose up -d              # Start in background
docker-compose down               # Stop services
docker-compose down -v            # Stop and remove data
docker-compose logs -f backend    # View backend logs
docker-compose restart backend    # Restart backend

# Backend
cd backend && python run.py       # Start backend
cd backend && python seed_docker.py  # Seed data

# Frontend
cd frontend && npm run dev        # Start frontend
cd frontend && npm run build      # Build frontend
```

---

## ✅ Success Checklist

After setup, verify:

- [ ] Docker containers running: `docker-compose ps`
- [ ] Backend health: http://localhost:8000/health
- [ ] API docs: http://localhost:8000/docs
- [ ] pgAdmin: http://localhost:5050
- [ ] Database has 6 tables
- [ ] Sample data loaded (10 products)
- [ ] Frontend: http://localhost:3000
- [ ] Can browse products
- [ ] Can add to cart
- [ ] Cart persists on refresh

---

## 🎯 Next Steps

- [ ] Implement JWT authentication
- [ ] Add payment integration
- [ ] User profile management
- [ ] Order tracking
- [ ] Product reviews
- [ ] Wishlist feature
- [ ] Email notifications
- [ ] Admin dashboard
- [ ] Analytics
- [ ] Deploy to production

---

## 📄 License

MIT License - feel free to use for your projects!

---

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

---

## 📧 Contact

For questions or support, please open an issue.

---

**🎉 Happy coding!**

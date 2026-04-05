# API Guide - Electronics E-Commerce

Complete guide for testing all CRUD endpoints in the FastAPI application.

## Quick Start

### 1. Start the Server
```bash
cd backend
python run.py
```

### 2. Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### 3. Seed Sample Data
```bash
python seed_force.py
```

---

## API Endpoints Overview

| Resource | Endpoint | Methods |
|----------|----------|---------|
| Users | `/api/nguoi-dung` | GET, POST, PUT, DELETE |
| Categories | `/api/danh-muc` | GET, POST, PUT, DELETE |
| Products | `/api/san-pham` | GET, POST, PUT, DELETE |
| Orders | `/api/don-hang` | GET, POST, PUT, DELETE |
| Order Items | `/api/chi-tiet-don-hang` | GET, POST |
| Chat History | `/api/lich-su-chat` | GET, POST |

---

## 1. Users (Người dùng) - `/api/nguoi-dung`

### Get All Users
```http
GET /api/nguoi-dung?skip=0&limit=100
```

**Response:**
```json
[
  {
    "id": 1,
    "email": "admin@electronics.com",
    "vai_tro": "admin",
    "ngay_tao": "2024-01-01T00:00:00"
  }
]
```

### Get User by ID
```http
GET /api/nguoi-dung/1
```

### Create User
```http
POST /api/nguoi-dung
Content-Type: application/json

{
  "email": "newuser@example.com",
  "mat_khau": "password123",
  "vai_tro": "user"
}
```

**Response:** `201 Created`
```json
{
  "id": 4,
  "email": "newuser@example.com",
  "vai_tro": "user",
  "ngay_tao": "2024-01-01T00:00:00"
}
```

### Update User
```http
PUT /api/nguoi-dung/4
Content-Type: application/json

{
  "email": "updated@example.com",
  "vai_tro": "admin"
}
```

### Delete User
```http
DELETE /api/nguoi-dung/4
```

**Response:**
```json
{
  "message": "Đã xóa người dùng thành công"
}
```

---

## 2. Categories (Danh mục) - `/api/danh-muc`

### Get All Categories
```http
GET /api/danh-muc?skip=0&limit=100
```

**Response:**
```json
[
  {
    "id": 1,
    "ten": "Dien thoai"
  },
  {
    "id": 2,
    "ten": "Laptop"
  }
]
```

### Get Category by ID
```http
GET /api/danh-muc/1
```

### Create Category
```http
POST /api/danh-muc
Content-Type: application/json

{
  "ten": "May tinh bang"
}
```

**Response:** `201 Created`
```json
{
  "id": 5,
  "ten": "May tinh bang"
}
```

### Update Category
```http
PUT /api/danh-muc/5
Content-Type: application/json

{
  "ten": "Tablet"
}
```

### Delete Category
```http
DELETE /api/danh-muc/5
```

---

## 3. Products (Sản phẩm) - `/api/san-pham`

### Get All Products
```http
GET /api/san-pham?skip=0&limit=100
```

**Response:**
```json
[
  {
    "id": 1,
    "ten": "iPhone 15 Pro Max",
    "gia": 1299.99,
    "mo_ta": "Latest iPhone with A17 Pro chip",
    "hinh_anh": "https://example.com/iphone15.jpg",
    "danh_muc_id": 1,
    "ngay_tao": "2024-01-01T00:00:00",
    "danh_muc": {
      "id": 1,
      "ten": "Dien thoai"
    }
  }
]
```

### Get Product by ID
```http
GET /api/san-pham/1
```

### Create Product
```http
POST /api/san-pham
Content-Type: application/json

{
  "ten": "iPad Pro 12.9",
  "gia": 1099.99,
  "mo_ta": "Powerful tablet for professionals",
  "hinh_anh": "https://example.com/ipad.jpg",
  "danh_muc_id": 1
}
```

**Response:** `201 Created`

### Update Product
```http
PUT /api/san-pham/11
Content-Type: application/json

{
  "ten": "iPad Pro 12.9 M2",
  "gia": 1199.99
}
```

### Delete Product
```http
DELETE /api/san-pham/11
```

---

## 4. Orders (Đơn hàng) - `/api/don-hang`

### Get All Orders
```http
GET /api/don-hang?skip=0&limit=100
```

**Response:**
```json
[
  {
    "id": 1,
    "nguoi_dung_id": 2,
    "tong_tien": 1549.98,
    "trang_thai": "completed",
    "ngay_tao": "2024-01-01T00:00:00",
    "nguoi_dung": {
      "id": 2,
      "email": "user1@example.com"
    },
    "chi_tiet_don_hang": [
      {
        "id": 1,
        "san_pham_id": 1,
        "so_luong": 1,
        "san_pham": {
          "ten": "iPhone 15 Pro Max",
          "gia": 1299.99
        }
      }
    ]
  }
]
```

### Get Order by ID
```http
GET /api/don-hang/1
```

### Create Order
```http
POST /api/don-hang
Content-Type: application/json

{
  "nguoi_dung_id": 2,
  "tong_tien": 999.99,
  "trang_thai": "pending"
}
```

**Response:** `201 Created`

### Update Order Status
```http
PUT /api/don-hang/4
Content-Type: application/json

{
  "trang_thai": "completed"
}
```

### Delete Order
```http
DELETE /api/don-hang/4
```

---

## 5. Order Items (Chi tiết đơn hàng) - `/api/chi-tiet-don-hang`

### Get All Order Items
```http
GET /api/chi-tiet-don-hang?skip=0&limit=100
```

**Response:**
```json
[
  {
    "id": 1,
    "don_hang_id": 1,
    "san_pham_id": 1,
    "so_luong": 1,
    "don_hang": {
      "id": 1,
      "tong_tien": 1549.98
    },
    "san_pham": {
      "id": 1,
      "ten": "iPhone 15 Pro Max",
      "gia": 1299.99
    }
  }
]
```

### Get Order Item by ID
```http
GET /api/chi-tiet-don-hang/1
```

### Create Order Item
```http
POST /api/chi-tiet-don-hang
Content-Type: application/json

{
  "don_hang_id": 1,
  "san_pham_id": 2,
  "so_luong": 2
}
```

**Response:** `201 Created`

---

## 6. Chat History (Lịch sử chat) - `/api/lich-su-chat`

### Get All Chat Messages
```http
GET /api/lich-su-chat?skip=0&limit=100
```

**Response:**
```json
[
  {
    "id": 1,
    "nguoi_dung_id": 2,
    "cau_hoi": "What is the best phone under $1000?",
    "cau_tra_loi": "The Google Pixel 8 Pro is an excellent choice...",
    "ngay_tao": "2024-01-01T00:00:00",
    "nguoi_dung": {
      "id": 2,
      "email": "user1@example.com"
    }
  }
]
```

### Get Chat by ID
```http
GET /api/lich-su-chat/1
```

### Create Chat Message
```http
POST /api/lich-su-chat
Content-Type: application/json

{
  "nguoi_dung_id": 2,
  "cau_hoi": "Do you have iPhone 15?",
  "cau_tra_loi": "Yes! We have iPhone 15 Pro Max for $1299.99"
}
```

**Response:** `201 Created`

---

## Testing with cURL

### Example: Get All Products
```bash
curl -X GET "http://localhost:8000/api/san-pham" -H "accept: application/json"
```

### Example: Create Category
```bash
curl -X POST "http://localhost:8000/api/danh-muc" \
  -H "Content-Type: application/json" \
  -d '{"ten": "Smart Watch"}'
```

### Example: Update Product
```bash
curl -X PUT "http://localhost:8000/api/san-pham/1" \
  -H "Content-Type: application/json" \
  -d '{"gia": 1199.99}'
```

### Example: Delete User
```bash
curl -X DELETE "http://localhost:8000/api/nguoi-dung/4"
```

---

## Testing with Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Get all products
response = requests.get(f"{BASE_URL}/api/san-pham")
products = response.json()
print(f"Found {len(products)} products")

# Create category
response = requests.post(
    f"{BASE_URL}/api/danh-muc",
    json={"ten": "Smart Watch"}
)
category = response.json()
print(f"Created category: {category}")

# Update product
response = requests.put(
    f"{BASE_URL}/api/san-pham/1",
    json={"gia": 1199.99}
)
product = response.json()
print(f"Updated product: {product}")

# Delete user
response = requests.delete(f"{BASE_URL}/api/nguoi-dung/4")
print(response.json())
```

---

## Sample Data

After running `python seed_force.py`, you'll have:

### Users (3)
- admin@electronics.com (admin)
- user1@example.com (user)
- user2@example.com (user)

### Categories (4)
- Dien thoai (Phones)
- Laptop
- Tai nghe (Headphones)
- Phu kien (Accessories)

### Products (10)
- iPhone 15 Pro Max ($1299.99)
- Samsung Galaxy S24 Ultra ($1199.99)
- Google Pixel 8 Pro ($999.99)
- MacBook Pro 16 M3 ($2499.99)
- Dell XPS 15 ($1799.99)
- Lenovo ThinkPad X1 Carbon ($1599.99)
- AirPods Pro 2 ($249.99)
- Sony WH-1000XM5 ($399.99)
- USB-C Cable 2m ($19.99)
- Wireless Charger ($39.99)

### Orders (3)
- Order #1: iPhone + AirPods ($1549.98) - Completed
- Order #2: MacBook ($2499.99) - Pending
- Order #3: Cable + Charger ($59.98) - Completed

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "Sản phẩm không tồn tại"
}
```

### 400 Bad Request
```json
{
  "detail": "Email đã tồn tại"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "gia"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Common Query Parameters

### Pagination
```http
GET /api/san-pham?skip=0&limit=10
```

- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid data |
| 404 | Not Found - Resource doesn't exist |
| 422 | Validation Error - Invalid request body |
| 500 | Internal Server Error |

---

## Next Steps

1. ✅ Test all endpoints in Swagger UI: http://localhost:8000/docs
2. ✅ Verify data in pgAdmin: http://localhost:5050
3. ✅ Add authentication (JWT)
4. ✅ Add filtering and search
5. ✅ Add pagination metadata
6. ✅ Add rate limiting
7. ✅ Add caching
8. ✅ Build frontend

---

## Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <process_id> /F
```

### Database connection error
```bash
# Check database status
python check_tables.py

# Recreate tables if needed
python force_create_tables.py
```

### No data in database
```bash
# Seed sample data
python seed_force.py
```

---

## Quick Commands Reference

```bash
# Start server
python run.py

# Seed database
python seed_force.py

# Check database
python check_tables.py

# Force create tables
python force_create_tables.py

# Run with Docker
docker-compose up -d
```

---

**Happy Testing! 🎉**

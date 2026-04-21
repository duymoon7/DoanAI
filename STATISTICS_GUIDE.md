# HƯỚNG DẪN SỬ DỤNG TÍNH NĂNG BÁO CÁO THỐNG KÊ (PB31)

## Tổng quan

Tính năng Báo cáo thống kê (PB31) cung cấp cái nhìn tổng quan về hoạt động kinh doanh của hệ thống, bao gồm:

- ✅ Doanh thu tháng hiện tại với % biến động so với tháng trước
- ✅ Số lượng đơn hàng (chỉ tính completed)
- ✅ **Pie Chart** trạng thái đơn hàng (pending, completed, cancelled)
- ✅ **Area Chart** doanh thu 12 tháng gần nhất
- ✅ **Bar Chart** top 10 sản phẩm bán chạy nhất
- ✅ Thống kê nhanh (tỷ lệ hoàn thành, giá trị đơn TB, sản phẩm/đơn)
- ✅ Bảng chi tiết sản phẩm với ranking

## Công nghệ sử dụng

- **Backend:** FastAPI + SQLAlchemy + MySQL
- **Frontend:** Next.js 16 + TypeScript + Tailwind CSS
- **Charts:** Recharts 2.12.7 (Thư viện biểu đồ React)

## Yêu cầu

- **Quyền truy cập:** Admin hoặc Manager
- **Backend:** FastAPI đang chạy tại `http://localhost:8000`
- **Frontend:** Next.js đang chạy tại `http://localhost:3000`
- **Thư viện:** Recharts (cài đặt: `npm install recharts`)

## Cài đặt

### Bước 1: Cài đặt dependencies

```bash
cd AI-Shop/frontend
npm install recharts
```

### Bước 2: Khởi động backend

```bash
cd AI-Shop/backend
python -m uvicorn app.main:app --reload
```

### Bước 3: Khởi động frontend

```bash
cd AI-Shop/frontend
npm run dev
```

### Bước 4: Truy cập

Mở trình duyệt: http://localhost:3000/admin/statistics

## API Endpoints

### 1. Dashboard Statistics (PB31 - Chính)

```
GET /api/statistics/dashboard
Authorization: Bearer {token}
```

**Response:**
```json
{
  "revenue": {
    "current_month": 50000000,
    "previous_month": 45000000,
    "change_percent": 11.11,
    "month": 4,
    "year": 2026
  },
  "orders": {
    "completed_count": 150,
    "total_count": 200
  },
  "order_status_chart": [
    {
      "status": "completed",
      "count": 150,
      "label": "Hoàn thành"
    },
    {
      "status": "pending",
      "count": 30,
      "label": "Chờ xử lý"
    },
    {
      "status": "cancelled",
      "count": 20,
      "label": "Đã hủy"
    }
  ],
  "top_selling_products": [
    {
      "id": 1,
      "name": "iPhone 15 Pro Max",
      "price": 29990000,
      "image": "https://...",
      "total_sold": 50,
      "total_revenue": 1499500000
    }
  ],
  "summary": {
    "total_products": 100,
    "total_users": 500,
    "total_orders": 200
  }
}
```

### 2. Revenue Statistics (Chi tiết doanh thu)

```
GET /api/statistics/revenue?start_date=2026-01-01&end_date=2026-12-31
Authorization: Bearer {token}
```

**Response:**
```json
{
  "total_revenue": 500000000,
  "average_order_value": 3333333.33,
  "total_discount": 50000000,
  "by_status": [...],
  "monthly_revenue": [...]
}
```

### 3. Product Statistics (Thống kê sản phẩm)

```
GET /api/statistics/products
Authorization: Bearer {token}
```

**Response:**
```json
{
  "by_category": [...],
  "price_range": {
    "min": 100000,
    "max": 50000000,
    "average": 5000000
  },
  "low_stock_products": [...],
  "out_of_stock_count": 5
}
```

### 4. Coupon Statistics (Thống kê mã giảm giá)

```
GET /api/statistics/coupons
Authorization: Bearer {token}
```

**Response:**
```json
{
  "coupon_effectiveness": [...],
  "usage_statistics": {
    "total_orders": 200,
    "orders_with_coupon": 50,
    "usage_rate": 25.0,
    "total_savings": 10000000
  },
  "expiring_soon": [...]
}
```

### 5. Customer Statistics (Thống kê khách hàng)

```
GET /api/statistics/customers
Authorization: Bearer {token}
```

**Response:**
```json
{
  "top_customers": [...],
  "total_customers": 500,
  "new_customers_this_month": 50
}
```

### 6. Export Statistics (Export báo cáo)

```
GET /api/statistics/export?report_type=revenue&format=json
Authorization: Bearer {token}
```

**Tham số:**
- `report_type`: revenue, products, customers, coupons
- `format`: json, csv (csv đang phát triển)

## Cách sử dụng Frontend

### 1. Truy cập trang thống kê

1. Đăng nhập với tài khoản Admin hoặc Manager
2. Vào trang Admin Dashboard: `http://localhost:3000/admin`
3. Click vào card "Báo cáo thống kê"
4. Hoặc truy cập trực tiếp: `http://localhost:3000/admin/statistics`

### 2. Xem Dashboard

Trang Dashboard hiển thị:

#### Card Doanh thu tháng hiện tại
- Số tiền doanh thu tháng này
- % biến động so với tháng trước (màu xanh nếu tăng, đỏ nếu giảm)
- Doanh thu tháng trước
- Gradient background đẹp mắt

#### Summary Cards
- Đơn hàng hoàn thành (icon giỏ hàng xanh)
- Tổng đơn hàng (icon lịch xanh dương)
- Số lượng sản phẩm (icon package tím)
- Số lượng khách hàng (icon users vàng)

#### 📊 Pie Chart - Trạng thái đơn hàng
- **Loại biểu đồ:** Pie Chart (Biểu đồ tròn)
- **Hiển thị:** Tỷ lệ % của từng trạng thái
- **Màu sắc:**
  - Xanh lá (#10B981): Hoàn thành
  - Vàng (#FCD34D): Chờ xử lý
  - Đỏ (#EF4444): Đã hủy
- **Tính năng:**
  - Label hiển thị % trên biểu đồ
  - Tooltip khi hover
  - Legend phân biệt màu
  - Breakdown chi tiết bên dưới

#### Thống kê nhanh
- Tỷ lệ hoàn thành đơn hàng (gradient xanh lá)
- Giá trị đơn hàng trung bình (gradient xanh dương)
- Số sản phẩm trung bình mỗi đơn (gradient tím)

#### 📈 Area Chart - Doanh thu 12 tháng
- **Loại biểu đồ:** Area Chart (Biểu đồ vùng)
- **Hiển thị:** Xu hướng doanh thu 12 tháng gần nhất
- **Màu sắc:** Gradient xanh dương (#3B82F6)
- **Trục X:** Tháng/Năm (xoay 45 độ)
- **Trục Y:** Doanh thu (định dạng triệu VNĐ)
- **Tính năng:**
  - Gradient fill đẹp mắt
  - Grid lines để dễ đọc
  - Tooltip hiển thị số tiền chính xác
  - Responsive trên mọi thiết bị

#### 📊 Bar Chart - Top 10 sản phẩm
- **Loại biểu đồ:** Bar Chart (Biểu đồ cột kép)
- **Hiển thị:** Top 10 sản phẩm bán chạy nhất
- **Cột 1 (Tím #8B5CF6):** Số lượng bán (trục trái)
- **Cột 2 (Xanh #3B82F6):** Doanh thu (trục phải)
- **Tính năng:**
  - Dual Y-axis (2 trục Y)
  - Tên sản phẩm xoay 45 độ
  - Bo tròn góc cột
  - Tooltip hiển thị cả 2 giá trị
  - Legend phân biệt

#### Bảng chi tiết Top 10 sản phẩm
- Bảng hiển thị chi tiết
- Hình ảnh sản phẩm
- Số lượng đã bán
- Doanh thu từng sản phẩm
- Xếp hạng với badge màu (vàng cho top 1, xám cho top 2, cam cho top 3)

### 3. Tương tác với biểu đồ

#### Hover để xem chi tiết
- Di chuột qua biểu đồ để xem tooltip
- Tooltip hiển thị số liệu chính xác
- Định dạng tiền tệ VNĐ tự động

#### Nút "Làm mới"
- Click để cập nhật dữ liệu mới nhất
- Icon xoay khi đang tải
- Không cần reload trang

#### Responsive
- Biểu đồ tự động điều chỉnh kích thước
- Hoạt động tốt trên mobile, tablet, desktop
- Scroll ngang nếu cần trên mobile

### 4. Export báo cáo

Click nút "Export PDF" ở góc trên bên phải (tính năng đang phát triển)

## Tính năng nổi bật

### 1. Biểu đồ trực quan với Recharts
- **Pie Chart:** Trạng thái đơn hàng với màu sắc phân biệt
- **Area Chart:** Xu hướng doanh thu 12 tháng với gradient đẹp
- **Bar Chart:** Top sản phẩm với dual-axis (2 trục Y)
- **Custom Tooltip:** Hiển thị chi tiết khi hover
- **Responsive:** Tự động điều chỉnh trên mọi thiết bị

### 2. Tốc độ query nhanh
- Sử dụng SQLAlchemy ORM với query tối ưu
- Index trên các cột thường xuyên query
- Chỉ tính đơn hàng completed cho doanh thu

### 3. Responsive Design
- Hiển thị tốt trên mọi thiết bị
- Grid layout tự động điều chỉnh
- Mobile-friendly
- Biểu đồ responsive với ResponsiveContainer

### 4. Real-time Data
- Dữ liệu được tải từ database thời gian thực
- Nút "Làm mới" để cập nhật
- Icon xoay khi đang tải
- Không cache (có thể thêm cache sau)

### 5. Visual Design
- Gradient cards cho doanh thu
- Icon phân biệt từng loại thống kê
- Biểu đồ với màu sắc chuyên nghiệp
- Badge màu sắc cho ranking
- Smooth animations

## Tiêu chí chấp nhận (PB31)

✅ **1. Tốc độ query nhanh**
- Sử dụng query tối ưu với JOIN và GROUP BY
- Index trên các cột quan trọng

✅ **2. Card doanh thu theo tháng**
- Hiển thị doanh thu tháng hiện tại
- % biến động so với tháng trước
- Icon trending up/down

✅ **3. Số lượng đơn hàng**
- Chỉ tính đơn có trạng thái "Giao Thành Công" (completed)

✅ **4. Pie Chart trạng thái đơn hàng**
- Hiển thị tỉ lệ: pending, completed, cancelled
- Biểu đồ tròn với Recharts
- Màu sắc phân biệt rõ ràng
- Tooltip và Legend

✅ **5. Area Chart doanh thu 12 tháng**
- Biểu đồ vùng với gradient
- Hiển thị xu hướng doanh thu
- Trục Y định dạng triệu VNĐ

✅ **6. Bar Chart top 10 sản phẩm**
- Biểu đồ cột kép (dual-axis)
- Hiển thị số lượng và doanh thu
- Bo tròn góc cột đẹp mắt

✅ **7. Export báo cáo**
- Hỗ trợ export ra JSON
- PDF/CSV đang phát triển

## Điều kiện

### Điều kiện trước
- Tài khoản Admin hoặc Manager
- Có dữ liệu đơn hàng trong CSDL

### Điều kiện sau
- Admin/Manager xem được trực quan các Chart
- UI Dashboard trả về số liệu chính xác

## Troubleshooting

### Lỗi 401 Unauthorized
- Kiểm tra token đã hết hạn chưa
- Đăng nhập lại

### Lỗi 403 Forbidden
- Tài khoản không có quyền Admin/Manager
- Liên hệ Admin để cấp quyền

### Không có dữ liệu
- Kiểm tra database có đơn hàng không
- Chạy seed data: `python backend/seed_initial_data.py`

### Biểu đồ không hiển thị
- Kiểm tra đã cài recharts chưa: `npm install recharts`
- Kiểm tra console có lỗi không
- Đảm bảo backend đang chạy
- Restart frontend: `npm run dev`

### Lỗi "Module not found: recharts"
```bash
cd AI-Shop/frontend
npm install recharts
npm run dev
```

### Biểu đồ bị vỡ layout
- Đã xử lý với ResponsiveContainer
- Thử zoom out trình duyệt
- Kiểm tra width của container cha

### Backend không chạy
```bash
cd AI-Shop/backend
python -m uvicorn app.main:app --reload
```

### Frontend không chạy
```bash
cd AI-Shop/frontend
npm run dev
```

## Mở rộng tương lai

### 1. Thêm biểu đồ nâng cao
- ✅ Line chart doanh thu theo tháng (Đã có Area Chart)
- ✅ Bar chart sản phẩm bán chạy (Đã có)
- ✅ Pie chart trạng thái đơn hàng (Đã có)
- ⏳ Donut chart thay Pie chart
- ⏳ Radar chart đánh giá hiệu suất
- ⏳ Heatmap thời gian đặt hàng
- ⏳ Scatter plot phân tích khách hàng

### 2. Filter nâng cao
- Lọc theo khoảng thời gian
- Lọc theo danh mục sản phẩm
- Lọc theo phương thức thanh toán
- So sánh nhiều khoảng thời gian

### 3. Export nâng cao
- Export PDF với chart (canvas to image)
- Export Excel với nhiều sheet
- Tự động gửi email báo cáo
- Schedule báo cáo định kỳ

### 4. Real-time updates
- WebSocket để cập nhật real-time
- Notification khi có đơn hàng mới
- Auto-refresh mỗi 5 phút
- Live counter animation

### 5. Thêm thống kê
- Thống kê theo giờ trong ngày
- Thống kê theo ngày trong tuần
- Dự đoán doanh thu tháng tới (AI/ML)
- Phân tích xu hướng mua hàng
- Customer Lifetime Value (CLV)

### 6. Dashboard customization
- Drag & drop để sắp xếp biểu đồ
- Ẩn/hiện biểu đồ theo ý muốn
- Lưu layout cá nhân
- Dark mode cho biểu đồ

## Liên hệ

**Nhóm phát triển:**
- Hoàng Hải Minh Duy: hoanghaiminhduy20004@gmail.com
- Phạm Hữu Học: Phamhuuhoc3014q@gmail.com
- Lê Trần Anh Tuấn: tuan81609@gmail.com
- Nguyễn Minh Hoàng: Hominh8951@gmail.com
- Hoàng Nhật Khánh: Khanhịpk9@gmail.com

**Giảng viên hướng dẫn:**
- ThS. Lưu Văn Hiền

---

**Ngày hoàn thành:** 16/04/2026  
**Phiên bản:** 2.0 (Có biểu đồ Recharts)  
**Trạng thái:** Hoàn thành

**Biểu đồ:**
- ✅ Pie Chart (Trạng thái đơn hàng)
- ✅ Area Chart (Doanh thu 12 tháng)
- ✅ Bar Chart (Top 10 sản phẩm)

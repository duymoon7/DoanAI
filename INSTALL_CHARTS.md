# HƯỚNG DẪN CÀI ĐẶT BIỂU ĐỒ CHO TRANG THỐNG KÊ

## Bước 1: Cài đặt thư viện Recharts

Mở terminal trong thư mục frontend và chạy lệnh:

```bash
cd AI-Shop/frontend
npm install recharts
```

Hoặc nếu dùng yarn:

```bash
cd AI-Shop/frontend
yarn add recharts
```

## Bước 2: Khởi động lại Frontend

Sau khi cài đặt xong, khởi động lại server Next.js:

```bash
npm run dev
```

## Bước 3: Truy cập trang thống kê

1. Đăng nhập với tài khoản Admin/Manager
2. Vào: http://localhost:3000/admin/statistics

## Các biểu đồ đã được thêm

### 1. **Pie Chart - Trạng thái đơn hàng**
- Hiển thị tỷ lệ % của từng trạng thái (pending, completed, cancelled)
- Màu sắc phân biệt rõ ràng
- Tooltip hiển thị chi tiết khi hover
- Legend để dễ đọc

### 2. **Area Chart - Doanh thu 12 tháng**
- Biểu đồ vùng (Area Chart) hiển thị xu hướng doanh thu
- Gradient màu xanh đẹp mắt
- Trục X: Tháng/Năm
- Trục Y: Doanh thu (định dạng triệu VNĐ)
- Tooltip hiển thị số tiền chính xác

### 3. **Bar Chart - Top 10 sản phẩm bán chạy**
- Biểu đồ cột kép (Dual Axis)
- Cột tím: Số lượng bán (trục trái)
- Cột xanh: Doanh thu (trục phải)
- Tên sản phẩm xoay 45 độ để dễ đọc
- Bo tròn góc cột đẹp mắt

## Tính năng mới

### Nút "Làm mới"
- Icon xoay khi đang tải
- Cập nhật dữ liệu real-time
- Không cần reload trang

### Responsive Design
- Tất cả biểu đồ tự động điều chỉnh kích thước
- Hoạt động tốt trên mobile, tablet, desktop

### Custom Tooltip
- Hiển thị thông tin chi tiết khi hover
- Định dạng tiền tệ VNĐ
- Background trắng với shadow đẹp

## Màu sắc sử dụng

```javascript
const COLORS = {
  pending: '#FCD34D',    // Vàng - Chờ xử lý
  completed: '#10B981',  // Xanh lá - Hoàn thành
  cancelled: '#EF4444',  // Đỏ - Đã hủy
  primary: '#3B82F6',    // Xanh dương - Chính
  secondary: '#8B5CF6',  // Tím - Phụ
  accent: '#F59E0B'      // Cam - Nhấn mạnh
};
```

## Troubleshooting

### Lỗi: Module not found 'recharts'
**Giải pháp:** Chạy lại `npm install recharts`

### Biểu đồ không hiển thị
**Giải pháp:** 
1. Kiểm tra console có lỗi không
2. Đảm bảo backend đang chạy
3. Kiểm tra có dữ liệu trong database không

### Biểu đồ bị vỡ layout trên mobile
**Giải pháp:** Đã được xử lý với ResponsiveContainer, nếu vẫn bị thì thử zoom out trình duyệt

### Tooltip không hiển thị tiền VNĐ
**Giải pháp:** Đã được xử lý với CustomTooltip component

## Demo Screenshots

### Dashboard với biểu đồ đầy đủ:
- Card doanh thu với gradient
- 4 summary cards
- Pie chart trạng thái đơn hàng
- Thống kê nhanh với gradient background
- Area chart doanh thu 12 tháng
- Bar chart top 10 sản phẩm
- Bảng chi tiết sản phẩm bán chạy

## Mở rộng tương lai

### 1. Thêm biểu đồ Line Chart
- So sánh doanh thu năm nay vs năm trước
- Xu hướng số lượng đơn hàng

### 2. Thêm Donut Chart
- Thay thế Pie Chart
- Hiển thị tổng ở giữa

### 3. Thêm Radar Chart
- Đánh giá hiệu suất theo nhiều tiêu chí
- So sánh sản phẩm

### 4. Thêm Heatmap
- Thời gian đặt hàng trong ngày
- Ngày trong tuần bán chạy nhất

### 5. Export biểu đồ
- Export biểu đồ ra PNG
- Export báo cáo PDF có biểu đồ

## Tài liệu tham khảo

- **Recharts Documentation:** https://recharts.org/
- **Recharts Examples:** https://recharts.org/en-US/examples
- **Recharts API:** https://recharts.org/en-US/api

## Liên hệ hỗ trợ

Nếu gặp vấn đề, liên hệ:
- Hoàng Hải Minh Duy: hoanghaiminhduy20004@gmail.com

---

**Ngày cập nhật:** 16/04/2026  
**Phiên bản:** 2.0 (Có biểu đồ)  
**Trạng thái:** Hoàn thành

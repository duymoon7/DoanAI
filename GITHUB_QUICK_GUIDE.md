# ⚡ HƯỚNG DẪN NHANH - ĐẨY LÊN GITHUB

Hướng dẫn siêu nhanh để đẩy code lên GitHub.

---

## 🎯 3 BƯỚC ĐƠN GIẢN

### BƯỚC 1: Tạo Repository trên GitHub

1. Truy cập: https://github.com/new
2. Điền thông tin:
   - **Repository name**: `doanAi-ecommerce`
   - **Description**: `E-Commerce Platform with FastAPI & Next.js`
   - **Public** hoặc **Private**
   - ⬜ **KHÔNG** chọn "Add a README"
3. Click **"Create repository"**

### BƯỚC 2: Kết nối và Push

Mở terminal trong thư mục dự án, chạy:

```bash
# Thay YOUR_USERNAME bằng username GitHub của bạn
git remote add origin https://github.com/YOUR_USERNAME/doanAi-ecommerce.git
git branch -M main
git push -u origin main
```

### BƯỚC 3: Nhập Token

Khi được hỏi password:
1. Tạo token: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Chọn quyền `repo`
4. Copy token
5. Dán token làm password

---

## ✅ XONG!

Truy cập: `https://github.com/YOUR_USERNAME/doanAi-ecommerce`

---

## 🔄 Cập nhật sau này

```bash
git add .
git commit -m "Mô tả thay đổi"
git push
```

---

## 📚 Hướng dẫn chi tiết

Xem [PUSH_TO_GITHUB.md](PUSH_TO_GITHUB.md) để biết thêm chi tiết.

---

**Chúc mừng! 🎉**

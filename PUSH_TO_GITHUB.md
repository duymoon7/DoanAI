# 📤 HƯỚNG DẪN ĐẨY CODE LÊN GITHUB

Hướng dẫn chi tiết để đẩy dự án lên GitHub.

---

## 🎯 CHUẨN BỊ

### Đã hoàn thành:
- ✅ Git đã được cấu hình với email: hoanghminhduy@dtu.edu.vn
- ✅ Git repository đã được khởi tạo
- ✅ Code đã được commit

### Cần làm:
- [ ] Tạo repository trên GitHub
- [ ] Kết nối với GitHub
- [ ] Push code lên

---

## 📝 BƯỚC 1: TẠO REPOSITORY TRÊN GITHUB

### 1.1. Đăng nhập GitHub
1. Truy cập: https://github.com
2. Đăng nhập với tài khoản của bạn

### 1.2. Tạo Repository Mới
1. Click nút **"+"** ở góc trên bên phải
2. Chọn **"New repository"**

### 1.3. Điền Thông Tin Repository

**Repository name**: `doanAi-ecommerce` (hoặc tên bạn muốn)

**Description**: 
```
E-Commerce Platform - Full-stack application with FastAPI backend and Next.js frontend
```

**Visibility**: 
- ✅ **Public** (nếu muốn public)
- ⬜ **Private** (nếu muốn private)

**Initialize repository**:
- ⬜ **KHÔNG** chọn "Add a README file"
- ⬜ **KHÔNG** chọn "Add .gitignore"
- ⬜ **KHÔNG** chọn "Choose a license"

(Vì chúng ta đã có sẵn các file này)

### 1.4. Click "Create repository"

---

## 🔗 BƯỚC 2: KẾT NỐI VỚI GITHUB

Sau khi tạo repository, GitHub sẽ hiển thị hướng dẫn. Làm theo các lệnh sau:

### 2.1. Thêm Remote Repository

Mở terminal trong thư mục dự án và chạy:

```bash
git remote add origin https://github.com/YOUR_USERNAME/doanAi-ecommerce.git
```

**Lưu ý**: Thay `YOUR_USERNAME` bằng username GitHub của bạn.

Ví dụ:
```bash
git remote add origin https://github.com/hoanghminhduy/doanAi-ecommerce.git
```

### 2.2. Kiểm Tra Remote

```bash
git remote -v
```

Kết quả mong đợi:
```
origin  https://github.com/YOUR_USERNAME/doanAi-ecommerce.git (fetch)
origin  https://github.com/YOUR_USERNAME/doanAi-ecommerce.git (push)
```

---

## 🚀 BƯỚC 3: PUSH CODE LÊN GITHUB

### 3.1. Đổi tên branch thành main (nếu cần)

```bash
git branch -M main
```

### 3.2. Push code lên GitHub

```bash
git push -u origin main
```

### 3.3. Nhập Thông Tin Đăng Nhập

GitHub sẽ yêu cầu đăng nhập:

**Cách 1: Sử dụng Personal Access Token (Khuyến nghị)**

1. Truy cập: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Đặt tên: "doanAi-ecommerce"
4. Chọn quyền: `repo` (full control)
5. Click "Generate token"
6. **Copy token** (chỉ hiển thị 1 lần!)
7. Khi push, dùng token này làm password

**Cách 2: Sử dụng GitHub CLI**

```bash
# Cài đặt GitHub CLI
# Windows: winget install --id GitHub.cli
# Mac: brew install gh

# Đăng nhập
gh auth login

# Push
git push -u origin main
```

---

## ✅ BƯỚC 4: KIỂM TRA

### 4.1. Kiểm tra trên GitHub

1. Truy cập repository: `https://github.com/YOUR_USERNAME/doanAi-ecommerce`
2. Bạn sẽ thấy:
   - ✅ Tất cả files đã được upload
   - ✅ README.md hiển thị ở trang chủ
   - ✅ Có 74 files

### 4.2. Kiểm tra README

README.md sẽ tự động hiển thị với:
- Tiêu đề dự án
- Link đến GETTING_STARTED.md
- Link đến HUONG_DAN_CAI_DAT.md
- Hướng dẫn quick start

---

## 📋 LỆNH ĐẦY ĐỦ (Copy & Paste)

```bash
# 1. Thêm remote (thay YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/doanAi-ecommerce.git

# 2. Đổi tên branch
git branch -M main

# 3. Push code
git push -u origin main
```

---

## 🔄 CẬP NHẬT CODE SAU NÀY

Khi có thay đổi, chỉ cần:

```bash
# 1. Add files đã thay đổi
git add .

# 2. Commit với message
git commit -m "Mô tả thay đổi"

# 3. Push lên GitHub
git push
```

---

## 🐛 XỬ LÝ LỖI

### Lỗi 1: "remote origin already exists"

```bash
# Xóa remote cũ
git remote remove origin

# Thêm lại
git remote add origin https://github.com/YOUR_USERNAME/doanAi-ecommerce.git
```

### Lỗi 2: "Authentication failed"

**Giải pháp**: Sử dụng Personal Access Token thay vì password

1. Tạo token: https://github.com/settings/tokens
2. Dùng token làm password khi push

### Lỗi 3: "Updates were rejected"

```bash
# Pull code mới nhất trước
git pull origin main --rebase

# Sau đó push
git push origin main
```

### Lỗi 4: "Large files detected"

Nếu có file quá lớn (>100MB):

```bash
# Xem file lớn
git ls-files -s | awk '$4 > 100000000 {print $4, $2}'

# Xóa file khỏi git
git rm --cached path/to/large/file

# Thêm vào .gitignore
echo "path/to/large/file" >> .gitignore

# Commit và push lại
git add .gitignore
git commit -m "Remove large file"
git push
```

---

## 📝 THÔNG TIN REPOSITORY

### Thông tin đã cấu hình:
- **Email**: hoanghminhduy@dtu.edu.vn
- **Name**: Hoang Minh Duy
- **Branch**: main
- **Files**: 74 files
- **Commit message**: "Initial commit: E-Commerce platform with FastAPI backend and Next.js frontend"

### Repository structure:
```
doanAi-ecommerce/
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend
├── docker-compose.yml
├── README.md
├── GETTING_STARTED.md
├── HUONG_DAN_CAI_DAT.md
└── ... (các file khác)
```

---

## 🎯 SAU KHI PUSH THÀNH CÔNG

### 1. Cập nhật README trên GitHub (Optional)

Thêm badges vào README.md:

```markdown
![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/doanAi-ecommerce)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/doanAi-ecommerce)
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/doanAi-ecommerce)
```

### 2. Thêm Topics

Trên trang repository GitHub:
1. Click "Add topics"
2. Thêm: `ecommerce`, `fastapi`, `nextjs`, `docker`, `postgresql`, `typescript`, `python`

### 3. Thêm Description

Trên trang repository GitHub:
1. Click biểu tượng ⚙️ (Settings) bên phải
2. Thêm description: "Full-stack E-Commerce platform with FastAPI backend and Next.js frontend"
3. Thêm website: URL demo (nếu có)

### 4. Tạo Release (Optional)

1. Click "Releases" → "Create a new release"
2. Tag version: `v1.0.0`
3. Release title: "Initial Release"
4. Description: Mô tả tính năng
5. Click "Publish release"

---

## 📤 CHIA SẺ REPOSITORY

### URL để chia sẻ:
```
https://github.com/YOUR_USERNAME/doanAi-ecommerce
```

### Clone command cho người khác:
```bash
git clone https://github.com/YOUR_USERNAME/doanAi-ecommerce.git
```

### Hướng dẫn cho người clone:
Người khác chỉ cần:
1. Clone repository
2. Đọc [GETTING_STARTED.md](GETTING_STARTED.md)
3. Làm theo 3 bước

---

## 💡 MẸO

### Tạo .gitignore tốt hơn

File `.gitignore` đã được tạo sẵn, bao gồm:
- node_modules/
- __pycache__/
- .env files
- Build outputs
- IDE files

### Bảo vệ sensitive data

Đảm bảo không push:
- ❌ Passwords
- ❌ API keys
- ❌ Database credentials
- ❌ .env files

Các file này đã được thêm vào `.gitignore`.

### Sử dụng GitHub Actions (Advanced)

Tạo file `.github/workflows/ci.yml` để:
- Auto test khi push
- Auto deploy
- Check code quality

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề:
1. Xem phần "Xử Lý Lỗi" ở trên
2. Tìm trên Google: "git [error message]"
3. Hỏi trên Stack Overflow
4. Xem GitHub Docs: https://docs.github.com

---

## ✅ CHECKLIST

- [ ] Đã tạo repository trên GitHub
- [ ] Đã thêm remote origin
- [ ] Đã push code thành công
- [ ] Đã kiểm tra trên GitHub
- [ ] README.md hiển thị đúng
- [ ] Đã thêm topics
- [ ] Đã thêm description
- [ ] Đã test clone về

---

## 🎉 HOÀN THÀNH!

Repository của bạn đã sẵn sàng trên GitHub!

**URL**: https://github.com/YOUR_USERNAME/doanAi-ecommerce

**Người khác có thể clone và chạy ngay với 3 bước trong GETTING_STARTED.md**

---

**Chúc mừng! 🚀**

-- ============================================
-- CẬP NHẬT DATABASE CHO TÍNH NĂNG THANH TOÁN
-- ============================================
-- Chạy file này trong phpMyAdmin hoặc MySQL Workbench
-- Database: electronics_db

USE electronics_db;

-- ============================================
-- 1. CẬP NHẬT BẢNG nguoi_dung
-- ============================================
ALTER TABLE nguoi_dung 
ADD COLUMN IF NOT EXISTS dia_chi TEXT NULL COMMENT 'Địa chỉ mặc định';

ALTER TABLE nguoi_dung 
ADD COLUMN IF NOT EXISTS avatar VARCHAR(500) NULL COMMENT 'URL ảnh đại diện';

ALTER TABLE nguoi_dung 
ADD COLUMN IF NOT EXISTS ngay_cap_nhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Ngày cập nhật';

-- ============================================
-- 2. CẬP NHẬT BẢNG san_pham
-- ============================================
ALTER TABLE san_pham 
ADD COLUMN IF NOT EXISTS ton_kho INT NOT NULL DEFAULT 0 COMMENT 'Số lượng tồn kho';

ALTER TABLE san_pham 
ADD COLUMN IF NOT EXISTS trang_thai VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT 'Trạng thái: active, inactive';

ALTER TABLE san_pham 
ADD COLUMN IF NOT EXISTS ngay_cap_nhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Ngày cập nhật';

-- ============================================
-- 3. CẬP NHẬT BẢNG don_hang (QUAN TRỌNG!)
-- ============================================
-- Thông tin giao hàng
ALTER TABLE don_hang 
ADD COLUMN IF NOT EXISTS ten_nguoi_nhan VARCHAR(255) NULL COMMENT 'Tên người nhận hàng';

ALTER TABLE don_hang 
ADD COLUMN IF NOT EXISTS so_dien_thoai_nguoi_nhan VARCHAR(20) NULL COMMENT 'SĐT người nhận';

ALTER TABLE don_hang 
ADD COLUMN IF NOT EXISTS dia_chi_giao_hang TEXT NULL COMMENT 'Địa chỉ giao hàng';

ALTER TABLE don_hang 
ADD COLUMN IF NOT EXISTS ghi_chu TEXT NULL COMMENT 'Ghi chú đơn hàng';

-- Mã giảm giá
ALTER TABLE don_hang 
ADD COLUMN IF NOT EXISTS ma_giam_gia_id INT NULL COMMENT 'ID mã giảm giá (nếu có)';

ALTER TABLE don_hang 
ADD COLUMN IF NOT EXISTS so_tien_giam DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT 'Số tiền được giảm';

ALTER TABLE don_hang 
ADD COLUMN IF NOT EXISTS ngay_cap_nhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Ngày cập nhật';

-- ============================================
-- 4. THÊM FOREIGN KEY
-- ============================================
-- Kiểm tra và thêm foreign key cho ma_giam_gia_id
SET @fk_exists = (
    SELECT COUNT(*) 
    FROM information_schema.TABLE_CONSTRAINTS 
    WHERE CONSTRAINT_SCHEMA = 'electronics_db' 
    AND TABLE_NAME = 'don_hang' 
    AND CONSTRAINT_NAME = 'fk_don_hang_ma_giam_gia'
);

SET @sql = IF(@fk_exists = 0,
    'ALTER TABLE don_hang ADD CONSTRAINT fk_don_hang_ma_giam_gia FOREIGN KEY (ma_giam_gia_id) REFERENCES ma_giam_gia(id) ON DELETE SET NULL',
    'SELECT "Foreign key already exists" AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ============================================
-- 5. THÊM INDEXES ĐỂ TỐI ƯU HIỆU SUẤT
-- ============================================
CREATE INDEX IF NOT EXISTS idx_san_pham_trang_thai ON san_pham(trang_thai);
CREATE INDEX IF NOT EXISTS idx_don_hang_ma_giam_gia ON don_hang(ma_giam_gia_id);
CREATE INDEX IF NOT EXISTS idx_nguoi_dung_vai_tro ON nguoi_dung(vai_tro);

-- ============================================
-- 6. CẬP NHẬT DỮ LIỆU MẪU (OPTIONAL)
-- ============================================
-- Cập nhật tồn kho cho sản phẩm hiện có
UPDATE san_pham SET ton_kho = 50 WHERE ton_kho = 0;
UPDATE san_pham SET trang_thai = 'active' WHERE trang_thai IS NULL OR trang_thai = '';

-- ============================================
-- HOÀN TẤT!
-- ============================================
SELECT 
    '✅ Cập nhật database thành công!' AS status,
    'Đã thêm các trường mới cho tính năng thanh toán' AS message;

-- Kiểm tra cấu trúc bảng don_hang
DESCRIBE don_hang;

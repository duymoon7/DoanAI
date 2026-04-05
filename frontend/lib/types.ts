export interface Category {
    id: number;
    ten: string;
}

export interface Product {
    id: number;
    ten: string;
    gia: number;
    mo_ta: string;
    hinh_anh: string;
    danh_muc_id: number;
    ngay_tao: string;
    danh_muc?: Category;
}

export interface User {
    id: number;
    email: string;
    vai_tro: 'admin' | 'user';
    ngay_tao: string;
}

export interface Order {
    id: number;
    nguoi_dung_id: number;
    tong_tien: number;
    trang_thai: 'pending' | 'completed' | 'cancelled';
    ngay_tao: string;
}

export interface CartItem {
    product: Product;
    quantity: number;
}

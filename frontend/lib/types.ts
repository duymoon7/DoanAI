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
    phuong_thuc_thanh_toan: 'cod' | 'bank';
    ngay_tao: string;
}

export interface CartItem {
    product: Product;
    quantity: number;
}

export interface Review {
    id: number;
    nguoi_dung_id: number;
    san_pham_id: number;
    diem_so: number;
    binh_luan: string | null;
    ngay_tao: string;
    nguoi_dung?: {
        id: number;
        ho_ten: string;
        email: string;
    };
}

export interface ReviewStats {
    total_reviews: number;
    average_rating: number;
    rating_distribution: {
        [key: number]: number;
    };
}

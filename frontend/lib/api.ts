import axios from 'axios';
import { Product, Category, User, Order } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 10000, // 10 seconds timeout
});

// Products
export const getProducts = async (params?: {
    skip?: number;
    limit?: number;
    search?: string;
    danh_muc_id?: number;
    min_price?: number;
    max_price?: number;
    sort_by?: string;
    order?: string;
}): Promise<Product[]> => {
    const queryParams = new URLSearchParams();
    
    if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString());
    if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());
    if (params?.search) queryParams.append('search', params.search);
    if (params?.danh_muc_id) queryParams.append('danh_muc_id', params.danh_muc_id.toString());
    if (params?.min_price !== undefined) queryParams.append('min_price', params.min_price.toString());
    if (params?.max_price !== undefined) queryParams.append('max_price', params.max_price.toString());
    if (params?.sort_by) queryParams.append('sort_by', params.sort_by);
    if (params?.order) queryParams.append('order', params.order);
    
    const queryString = queryParams.toString();
    const url = queryString ? `/san-pham?${queryString}` : '/san-pham';
    
    const response = await api.get(url);
    return response.data;
};

export const getProduct = async (id: number): Promise<Product> => {
    const response = await api.get(`/san-pham/${id}`);
    return response.data;
};

// Categories
export const getCategories = async (): Promise<Category[]> => {
    const response = await api.get('/danh-muc');
    return response.data;
};

export const getCategory = async (id: number): Promise<Category> => {
    const response = await api.get(`/danh-muc/${id}`);
    return response.data;
};

// Users
export const getUsers = async (): Promise<User[]> => {
    const response = await api.get('/nguoi-dung');
    return response.data;
};

export const createUser = async (data: { email: string; mat_khau: string; vai_tro: string }): Promise<User> => {
    const response = await api.post('/nguoi-dung', data);
    return response.data;
};

// Orders
export const getOrders = async (): Promise<Order[]> => {
    const response = await api.get('/don-hang');
    return response.data;
};

export const createOrder = async (data: { 
    nguoi_dung_id: number; 
    tong_tien: number; 
    trang_thai: string;
    phuong_thuc_thanh_toan: string;
}): Promise<Order> => {
    const response = await api.post('/don-hang', data);
    return response.data;
};

export const updateOrderStatus = async (orderId: number, data: { trang_thai: string }): Promise<Order> => {
    const response = await api.put(`/don-hang/${orderId}`, data);
    return response.data;
};

// Order Items
export const createOrderItem = async (data: {
    don_hang_id: number;
    san_pham_id: number;
    so_luong: number;
    gia: number;
}) => {
    const response = await api.post('/chi-tiet-don-hang', data);
    return response.data;
};

export const getOrderItems = async (orderId: number) => {
    const response = await api.get(`/chi-tiet-don-hang?don_hang_id=${orderId}`);
    return response.data;
};

// Reviews
export const getReviews = async (productId: number, skip = 0, limit = 10) => {
    const response = await api.get(`/danh-gia?san_pham_id=${productId}&skip=${skip}&limit=${limit}`);
    return response.data;
};

export const getReviewStats = async (productId: number) => {
    const response = await api.get(`/danh-gia/stats/${productId}`);
    return response.data;
};

export const createReview = async (data: {
    san_pham_id: number;
    diem_so: number;
    binh_luan?: string;
}, token: string) => {
    const response = await api.post('/danh-gia', data, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    return response.data;
};

export default api;


// Authentication (using Next.js API routes to avoid CORS)
export const register = async (data: { email: string; mat_khau: string; ho_ten: string; so_dien_thoai?: string }) => {
    const response = await axios.post('/api/auth/register', data, {
        headers: {
            'Content-Type': 'application/json',
        },
    });
    return response.data;
};

export const login = async (data: { email: string; mat_khau: string }) => {
    const response = await axios.post('/api/auth/login', data, {
        headers: {
            'Content-Type': 'application/json',
        },
    });
    return response.data;
};

export const getCurrentUser = async (token: string) => {
    const response = await api.get('/auth/me', {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    return response.data;
};

// Coupons
export const validateCoupon = async (ma_code: string, order_total: number) => {
    const response = await api.post('/ma-giam-gia/validate', null, {
        params: {
            ma_code,
            order_total
        }
    });
    return response.data;
};

// Stock Check
export const checkStock = async (items: { product_id: number; quantity: number }[]) => {
    const response = await api.post('/san-pham/check-stock', items);
    return response.data;
};

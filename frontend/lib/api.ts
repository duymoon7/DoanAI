import axios from 'axios';
import { Product, Category, User, Order } from './types';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Products
export const getProducts = async (skip = 0, limit = 100): Promise<Product[]> => {
    const response = await api.get(`/san-pham?skip=${skip}&limit=${limit}`);
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

export const createOrder = async (data: { nguoi_dung_id: number; tong_tien: number; trang_thai: string }): Promise<Order> => {
    const response = await api.post('/don-hang', data);
    return response.data;
};

export default api;

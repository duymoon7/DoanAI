'use client';

import Link from 'next/link';
import { ShoppingCart, Search, User, Menu, LogOut } from 'lucide-react';
import { useCart } from '@/contexts/CartContext';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Navbar() {
    const { getTotalItems } = useCart();
    const [searchQuery, setSearchQuery] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [isAdmin, setIsAdmin] = useState(false);
    const [isManager, setIsManager] = useState(false);
    const [userName, setUserName] = useState('');
    const router = useRouter();

    useEffect(() => {
        // Check if user is logged in
        const token = localStorage.getItem('token');
        const userStr = localStorage.getItem('user');
        
        if (token && userStr) {
            try {
                const user = JSON.parse(userStr);
                setIsLoggedIn(true);
                setIsAdmin(user.vai_tro === 'admin');
                setIsManager(user.vai_tro === 'manager');
                setUserName(user.ho_ten || user.email);
            } catch (error) {
                console.error('Error parsing user data:', error);
                localStorage.removeItem('token');
                localStorage.removeItem('user');
            }
        }
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setIsLoggedIn(false);
        setIsAdmin(false);
        setIsManager(false);
        setUserName('');
        router.push('/');
    };

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        if (searchQuery.trim()) {
            router.push(`/products?search=${encodeURIComponent(searchQuery)}`);
        }
    };

    return (
        <nav className="bg-white shadow-sm sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    {/* Logo */}
                    <Link href="/" className="flex items-center space-x-2">
                        <div className="w-10 h-10 bg-gradient-to-br from-primary to-primary-dark rounded-lg flex items-center justify-center">
                            <span className="text-white font-bold text-xl">AI</span>
                        </div>
                        <span className="text-xl font-bold text-gray-900 hidden sm:block">AI Shop</span>
                    </Link>

                    {/* Search Bar */}
                    <form onSubmit={handleSearch} className="flex-1 max-w-2xl mx-4 sm:mx-8">
                        <div className="relative">
                            <input
                                type="text"
                                placeholder="Tìm kiếm sản phẩm..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="w-full pl-4 pr-12 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                            />
                            <button
                                type="submit"
                                className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-gray-500 hover:text-primary transition-colors"
                            >
                                <Search className="w-5 h-5" />
                            </button>
                        </div>
                    </form>

                    {/* Right Icons */}
                    <div className="flex items-center space-x-4">
                        <Link href="/chat" className="hidden md:block text-sm font-medium text-gray-700 hover:text-primary transition-colors">
                            Tư vấn AI
                        </Link>
                        
                        {isLoggedIn && (
                            <>
                                <Link href="/orders" className="hidden md:block text-sm font-medium text-gray-700 hover:text-primary transition-colors">
                                    Đơn hàng
                                </Link>
                                {(isAdmin || isManager) && (
                                    <Link href="/admin" className="hidden md:block text-sm font-medium text-gray-700 hover:text-primary transition-colors">
                                        {isAdmin ? 'Quản trị' : 'Quản lý'}
                                    </Link>
                                )}
                            </>
                        )}
                        
                        <Link
                            href="/cart"
                            className="relative p-2 text-gray-700 hover:text-primary transition-colors"
                        >
                            <ShoppingCart className="w-6 h-6" />
                            {getTotalItems() > 0 && (
                                <span className="absolute -top-1 -right-1 bg-accent text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                                    {getTotalItems()}
                                </span>
                            )}
                        </Link>

                        {!isLoggedIn ? (
                            <Link
                                href="/auth/login"
                                className="p-2 text-gray-700 hover:text-primary transition-colors"
                                title="Đăng nhập"
                            >
                                <User className="w-6 h-6" />
                            </Link>
                        ) : (
                            <div className="flex items-center space-x-2">
                                <Link
                                    href="/profile"
                                    className="hidden md:block text-sm font-medium text-gray-700 hover:text-primary transition-colors"
                                    title={userName}
                                >
                                    {userName}
                                </Link>
                                <Link
                                    href="/profile"
                                    className="p-2 text-gray-700 hover:text-primary transition-colors"
                                    title="Tài khoản"
                                >
                                    <User className="w-6 h-6" />
                                </Link>
                                <button
                                    onClick={handleLogout}
                                    className="p-2 text-gray-700 hover:text-red-500 transition-colors"
                                    title="Đăng xuất"
                                >
                                    <LogOut className="w-5 h-5" />
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Categories Bar */}
            <div className="border-t border-gray-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center space-x-8 h-12 overflow-x-auto">
                        <Link href="/products" className="text-sm font-medium text-gray-700 hover:text-primary whitespace-nowrap transition-colors">
                            Tất cả sản phẩm
                        </Link>
                        <Link href="/products?category=1" className="text-sm font-medium text-gray-700 hover:text-primary whitespace-nowrap transition-colors">
                            Điện thoại
                        </Link>
                        <Link href="/products?category=2" className="text-sm font-medium text-gray-700 hover:text-primary whitespace-nowrap transition-colors">
                            Laptop
                        </Link>
                        <Link href="/products?category=3" className="text-sm font-medium text-gray-700 hover:text-primary whitespace-nowrap transition-colors">
                            Tablet
                        </Link>
                        <Link href="/products?category=4" className="text-sm font-medium text-gray-700 hover:text-primary whitespace-nowrap transition-colors">
                            Phụ kiện
                        </Link>
                        <Link href="/products?category=5" className="text-sm font-medium text-gray-700 hover:text-primary whitespace-nowrap transition-colors">
                            Tai nghe
                        </Link>
                        <Link href="/products?category=6" className="text-sm font-medium text-gray-700 hover:text-primary whitespace-nowrap transition-colors">
                            Đồng hồ
                        </Link>
                    </div>
                </div>
            </div>
        </nav>
    );
}

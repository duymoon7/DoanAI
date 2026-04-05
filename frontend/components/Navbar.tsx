'use client';

import Link from 'next/link';
import { ShoppingCart, Search, User, Menu } from 'lucide-react';
import { useCart } from '@/contexts/CartContext';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Navbar() {
    const { getTotalItems } = useCart();
    const [searchQuery, setSearchQuery] = useState('');
    const router = useRouter();

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
                            <span className="text-white font-bold text-xl">E</span>
                        </div>
                        <span className="text-xl font-bold text-gray-900 hidden sm:block">ElectroShop</span>
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

                        <Link
                            href="/auth/login"
                            className="p-2 text-gray-700 hover:text-primary transition-colors"
                        >
                            <User className="w-6 h-6" />
                        </Link>
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
                            Tai nghe
                        </Link>
                        <Link href="/products?category=4" className="text-sm font-medium text-gray-700 hover:text-primary whitespace-nowrap transition-colors">
                            Phụ kiện
                        </Link>
                    </div>
                </div>
            </div>
        </nav>
    );
}

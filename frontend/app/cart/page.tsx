'use client';

import { useCart } from '@/contexts/CartContext';
import Image from 'next/image';
import Link from 'next/link';
import { Trash2, Plus, Minus, ShoppingBag, ArrowLeft } from 'lucide-react';

export default function CartPage() {
    const { cart, removeFromCart, updateQuantity, getTotalPrice, clearCart } = useCart();

    if (cart.length === 0) {
        return (
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
                <div className="text-center">
                    <ShoppingBag className="w-24 h-24 text-gray-300 mx-auto mb-6" />
                    <h2 className="text-2xl font-bold text-gray-900 mb-4">
                        Giỏ hàng trống
                    </h2>
                    <p className="text-gray-600 mb-8">
                        Bạn chưa có sản phẩm nào trong giỏ hàng
                    </p>
                    <Link href="/products" className="btn-primary inline-block">
                        Tiếp tục mua sắm
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Header */}
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Giỏ hàng</h1>
                    <p className="text-gray-600 mt-2">
                        {cart.length} sản phẩm
                    </p>
                </div>
                <Link
                    href="/products"
                    className="text-primary hover:text-primary-dark font-medium flex items-center space-x-2"
                >
                    <ArrowLeft className="w-5 h-5" />
                    <span>Tiếp tục mua sắm</span>
                </Link>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Cart Items */}
                <div className="lg:col-span-2 space-y-4">
                    {cart.map((item) => (
                        <div key={item.product.id} className="card p-6">
                            <div className="flex gap-6">
                                {/* Image */}
                                <div className="relative w-24 h-24 flex-shrink-0 bg-gray-100 rounded-lg overflow-hidden">
                                    <Image
                                        src={item.product.hinh_anh || '/placeholder.png'}
                                        alt={item.product.ten}
                                        fill
                                        className="object-cover"
                                    />
                                </div>

                                {/* Info */}
                                <div className="flex-1">
                                    <Link
                                        href={`/products/${item.product.id}`}
                                        className="font-semibold text-gray-900 hover:text-primary transition-colors line-clamp-2"
                                    >
                                        {item.product.ten}
                                    </Link>

                                    {item.product.danh_muc && (
                                        <p className="text-sm text-gray-600 mt-1">
                                            {item.product.danh_muc.ten}
                                        </p>
                                    )}

                                    <div className="flex items-center justify-between mt-4">
                                        {/* Quantity */}
                                        <div className="flex items-center border border-gray-300 rounded-lg">
                                            <button
                                                onClick={() => updateQuantity(item.product.id, item.quantity - 1)}
                                                className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-50"
                                            >
                                                <Minus className="w-4 h-4" />
                                            </button>
                                            <span className="px-4 py-2 text-sm font-medium">
                                                {item.quantity}
                                            </span>
                                            <button
                                                onClick={() => updateQuantity(item.product.id, item.quantity + 1)}
                                                className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-50"
                                            >
                                                <Plus className="w-4 h-4" />
                                            </button>
                                        </div>

                                        {/* Price */}
                                        <div className="text-right">
                                            <p className="text-lg font-bold text-primary">
                                                {(Number(item.product.gia) * item.quantity).toLocaleString('vi-VN')}đ
                                            </p>
                                            <p className="text-sm text-gray-500">
                                                {Number(item.product.gia).toLocaleString('vi-VN')}đ / sản phẩm
                                            </p>
                                        </div>
                                    </div>
                                </div>

                                {/* Remove */}
                                <button
                                    onClick={() => removeFromCart(item.product.id)}
                                    className="text-gray-400 hover:text-red-500 transition-colors"
                                >
                                    <Trash2 className="w-5 h-5" />
                                </button>
                            </div>
                        </div>
                    ))}

                    {/* Clear Cart */}
                    <button
                        onClick={clearCart}
                        className="text-sm text-red-500 hover:text-red-600 font-medium"
                    >
                        Xóa toàn bộ giỏ hàng
                    </button>
                </div>

                {/* Order Summary */}
                <div className="lg:col-span-1">
                    <div className="card p-6 sticky top-20">
                        <h2 className="text-xl font-bold text-gray-900 mb-6">
                            Tóm tắt đơn hàng
                        </h2>

                        <div className="space-y-4 mb-6">
                            <div className="flex justify-between text-gray-600">
                                <span>Tạm tính</span>
                                <span className="font-medium">{getTotalPrice().toLocaleString('vi-VN')}đ</span>
                            </div>
                            <div className="flex justify-between text-gray-600">
                                <span>Phí vận chuyển</span>
                                <span className="font-medium text-green-600">Miễn phí</span>
                            </div>
                            <div className="flex justify-between text-gray-600">
                                <span>Giảm giá</span>
                                <span className="font-medium text-red-600">-$0.00</span>
                            </div>

                            <div className="border-t border-gray-200 pt-4">
                                <div className="flex justify-between items-baseline">
                                    <span className="text-lg font-semibold text-gray-900">Tổng cộng</span>
                                    <span className="text-2xl font-bold text-primary">
                                        {getTotalPrice().toLocaleString('vi-VN')}đ
                                    </span>
                                </div>
                            </div>
                        </div>

                        {/* Promo Code */}
                        <div className="mb-6">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Mã giảm giá
                            </label>
                            <div className="flex gap-2">
                                <input
                                    type="text"
                                    placeholder="Nhập mã"
                                    className="flex-1 input text-sm"
                                />
                                <button className="btn-secondary text-sm px-4">
                                    Áp dụng
                                </button>
                            </div>
                        </div>

                        {/* Checkout Button */}
                        <button className="w-full btn-primary mb-4">
                            Thanh toán
                        </button>

                        {/* Continue Shopping */}
                        <Link
                            href="/products"
                            className="block text-center text-sm text-primary hover:text-primary-dark font-medium"
                        >
                            Tiếp tục mua sắm
                        </Link>

                        {/* Info */}
                        <div className="mt-6 pt-6 border-t border-gray-200 space-y-3 text-sm text-gray-600">
                            <p className="flex items-start space-x-2">
                                <span className="text-green-600">✓</span>
                                <span>Miễn phí vận chuyển cho đơn hàng trên $50</span>
                            </p>
                            <p className="flex items-start space-x-2">
                                <span className="text-green-600">✓</span>
                                <span>Đổi trả trong 30 ngày</span>
                            </p>
                            <p className="flex items-start space-x-2">
                                <span className="text-green-600">✓</span>
                                <span>Bảo hành chính hãng 12 tháng</span>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

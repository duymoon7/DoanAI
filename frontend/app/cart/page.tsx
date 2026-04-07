'use client';

import { useCart } from '@/contexts/CartContext';
import Image from 'next/image';
import Link from 'next/link';
import { Trash2, Plus, Minus, ShoppingBag, ArrowLeft, CreditCard, Truck } from 'lucide-react';
import { useState } from 'react';
import { createOrder, createOrderItem } from '@/lib/api';
import toast from 'react-hot-toast';
import { useRouter } from 'next/navigation';

export default function CartPage() {
    const { cart, removeFromCart, updateQuantity, getTotalPrice, clearCart } = useCart();
    const [paymentMethod, setPaymentMethod] = useState<'cod' | 'bank'>('cod');
    const [isProcessing, setIsProcessing] = useState(false);
    const [shippingInfo, setShippingInfo] = useState({
        fullName: '',
        phone: '',
        address: '',
        note: ''
    });
    const router = useRouter();

    const handleCheckout = async () => {
        // Check if user is logged in
        const userStr = localStorage.getItem('user');
        if (!userStr) {
            toast.error('Vui lòng đăng nhập để đặt hàng');
            router.push('/auth/login');
            return;
        }

        // Validate shipping info
        if (!shippingInfo.fullName.trim()) {
            toast.error('Vui lòng nhập họ tên');
            return;
        }
        if (!shippingInfo.phone.trim()) {
            toast.error('Vui lòng nhập số điện thoại');
            return;
        }
        if (!shippingInfo.address.trim()) {
            toast.error('Vui lòng nhập địa chỉ giao hàng');
            return;
        }

        // Validate phone number (basic)
        const phoneRegex = /^[0-9]{10,11}$/;
        if (!phoneRegex.test(shippingInfo.phone.replace(/\s/g, ''))) {
            toast.error('Số điện thoại không hợp lệ (10-11 số)');
            return;
        }

        const user = JSON.parse(userStr);
        setIsProcessing(true);

        try {
            // Create order
            const orderData = {
                nguoi_dung_id: user.id,
                tong_tien: getTotalPrice(),
                trang_thai: 'pending',
                phuong_thuc_thanh_toan: paymentMethod,
            };

            console.log('Creating order with data:', orderData);
            console.log('Shipping info:', shippingInfo);
            const order = await createOrder(orderData);
            console.log('Order created:', order);

            // Create order items
            for (const item of cart) {
                const itemData = {
                    don_hang_id: order.id,
                    san_pham_id: item.product.id,
                    so_luong: item.quantity,
                    gia: Number(item.product.gia),
                };
                console.log('Creating order item:', itemData);
                await createOrderItem(itemData);
            }

            // Clear cart and shipping info
            clearCart();
            setShippingInfo({ fullName: '', phone: '', address: '', note: '' });
            
            toast.success(`Đặt hàng thành công! Giao hàng đến: ${shippingInfo.address}`);
            router.push('/orders');
        } catch (error: any) {
            console.error('Error creating order:', error);
            
            // More detailed error message
            if (error.response) {
                // Server responded with error
                toast.error(`Lỗi: ${error.response.data.detail || 'Đặt hàng thất bại'}`);
            } else if (error.request) {
                // Request made but no response
                toast.error('Không thể kết nối đến server. Vui lòng kiểm tra backend đã chạy chưa!');
            } else {
                // Something else happened
                toast.error('Đặt hàng thất bại. Vui lòng thử lại!');
            }
        } finally {
            setIsProcessing(false);
        }
    };

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
                                        sizes="96px"
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

                        {/* Shipping Information */}
                        <div className="mb-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-4">
                                Thông tin giao hàng
                            </h3>
                            <div className="space-y-4">
                                {/* Full Name */}
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Họ và tên <span className="text-red-500">*</span>
                                    </label>
                                    <input
                                        type="text"
                                        value={shippingInfo.fullName}
                                        onChange={(e) => setShippingInfo({ ...shippingInfo, fullName: e.target.value })}
                                        placeholder="        Nguyễn Văn A"
                                        className="w-full input"
                                        required
                                    />
                                </div>

                                {/* Phone */}
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Số điện thoại <span className="text-red-500">*</span>
                                    </label>
                                    <input
                                        type="tel"
                                        value={shippingInfo.phone}
                                        onChange={(e) => setShippingInfo({ ...shippingInfo, phone: e.target.value })}
                                        placeholder="        0912345678"
                                        className="w-full input"
                                        required
                                    />
                                </div>

                                {/* Address */}
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Địa chỉ giao hàng <span className="text-red-500">*</span>
                                    </label>
                                    <textarea
                                        value={shippingInfo.address}
                                        onChange={(e) => setShippingInfo({ ...shippingInfo, address: e.target.value })}
                                        placeholder="Số nhà, tên đường, phường/xã, quận/huyện, tỉnh/thành phố"
                                        className="w-full input min-h-[80px] resize-none"
                                        rows={3}
                                        required
                                    />
                                </div>

                                {/* Note (Optional) */}
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Ghi chú (tùy chọn)
                                    </label>
                                    <textarea
                                        value={shippingInfo.note}
                                        onChange={(e) => setShippingInfo({ ...shippingInfo, note: e.target.value })}
                                        placeholder="Ghi chú thêm về đơn hàng (thời gian giao hàng, địa chỉ cụ thể...)"
                                        className="w-full input min-h-[60px] resize-none"
                                        rows={2}
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Payment Method */}
                        <div className="mb-6">
                            <label className="block text-sm font-medium text-gray-700 mb-3">
                                Phương thức thanh toán
                            </label>
                            <div className="space-y-3">
                                {/* COD Option */}
                                <label className={`flex items-center p-4 border-2 rounded-lg cursor-pointer transition-all ${
                                    paymentMethod === 'cod' 
                                        ? 'border-primary bg-primary/5' 
                                        : 'border-gray-200 hover:border-gray-300'
                                }`}>
                                    <input
                                        type="radio"
                                        name="payment"
                                        value="cod"
                                        checked={paymentMethod === 'cod'}
                                        onChange={(e) => setPaymentMethod(e.target.value as 'cod' | 'bank')}
                                        className="w-4 h-4 text-primary"
                                    />
                                    <div className="ml-3 flex items-center flex-1">
                                        <Truck className="w-5 h-5 text-primary mr-2" />
                                        <div>
                                            <p className="font-medium text-gray-900">Ship COD</p>
                                            <p className="text-xs text-gray-500">Thanh toán khi nhận hàng</p>
                                        </div>
                                    </div>
                                </label>

                                {/* Bank Option */}
                                <label className={`flex items-center p-4 border-2 rounded-lg cursor-pointer transition-all ${
                                    paymentMethod === 'bank' 
                                        ? 'border-primary bg-primary/5' 
                                        : 'border-gray-200 hover:border-gray-300'
                                }`}>
                                    <input
                                        type="radio"
                                        name="payment"
                                        value="bank"
                                        checked={paymentMethod === 'bank'}
                                        onChange={(e) => setPaymentMethod(e.target.value as 'cod' | 'bank')}
                                        className="w-4 h-4 text-primary"
                                    />
                                    <div className="ml-3 flex items-center flex-1">
                                        <CreditCard className="w-5 h-5 text-primary mr-2" />
                                        <div>
                                            <p className="font-medium text-gray-900">Chuyển khoản ngân hàng</p>
                                            <p className="text-xs text-gray-500">Thanh toán qua ngân hàng</p>
                                        </div>
                                    </div>
                                </label>
                            </div>
                        </div>

                        {/* Bank Info (show when bank is selected) */}
                        {paymentMethod === 'bank' && (
                            <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                                <p className="text-sm font-medium text-gray-900 mb-2">Thông tin chuyển khoản:</p>
                                <div className="text-sm text-gray-700 space-y-1">
                                    <p><span className="font-medium">Ngân hàng:</span> Vietcombank</p>
                                    <p><span className="font-medium">Số tài khoản:</span> 1234567890</p>
                                    <p><span className="font-medium">Chủ tài khoản:</span> AI Shop</p>
                                    <p><span className="font-medium">Nội dung:</span> [Họ tên] - [Số điện thoại]</p>
                                </div>
                            </div>
                        )}

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
                        <button 
                            onClick={handleCheckout}
                            disabled={isProcessing}
                            className="w-full btn-primary mb-4 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {isProcessing ? 'Đang xử lý...' : (paymentMethod === 'cod' ? 'Đặt hàng' : 'Xác nhận thanh toán')}
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

'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { getProduct } from '@/lib/api';
import { Product } from '@/lib/types';
import { useCart } from '@/contexts/CartContext';
import { Star, ShoppingCart, Heart, Share2, Truck, Shield, ArrowLeft } from 'lucide-react';

export default function ProductDetailPage() {
    const params = useParams();
    const { addToCart } = useCart();
    const [product, setProduct] = useState<Product | null>(null);
    const [loading, setLoading] = useState(true);
    const [quantity, setQuantity] = useState(1);

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const data = await getProduct(Number(params.id));
                setProduct(data);
            } catch (error) {
                console.error('Error fetching product:', error);
            } finally {
                setLoading(false);
            }
        };

        if (params.id) {
            fetchProduct();
        }
    }, [params.id]);

    const handleAddToCart = () => {
        if (product) {
            addToCart(product, quantity);
        }
    };

    const handleBuyNow = () => {
        if (product) {
            addToCart(product, quantity);
            window.location.href = '/cart';
        }
    };

    if (loading) {
        return (
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="animate-pulse">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                        <div className="aspect-square bg-gray-200 rounded-xl" />
                        <div className="space-y-6">
                            <div className="h-8 bg-gray-200 rounded w-3/4" />
                            <div className="h-12 bg-gray-200 rounded w-1/2" />
                            <div className="h-32 bg-gray-200 rounded" />
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    if (!product) {
        return (
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
                <p className="text-gray-500 text-lg">Không tìm thấy sản phẩm</p>
                <Link href="/products" className="text-primary hover:text-primary-dark mt-4 inline-block">
                    Quay lại danh sách sản phẩm
                </Link>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Breadcrumb */}
            <div className="flex items-center space-x-2 text-sm text-gray-600 mb-8">
                <Link href="/" className="hover:text-primary">Trang chủ</Link>
                <span>/</span>
                <Link href="/products" className="hover:text-primary">Sản phẩm</Link>
                <span>/</span>
                <span className="text-gray-900">{product.ten}</span>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                {/* Product Image */}
                <div>
                    <div className="card overflow-hidden">
                        <div className="relative aspect-square bg-gray-100">
                            <Image
                                src={product.hinh_anh || '/placeholder.png'}
                                alt={product.ten}
                                fill
                                className="object-cover"
                                priority
                            />
                        </div>
                    </div>
                </div>

                {/* Product Info */}
                <div>
                    {/* Category */}
                    {product.danh_muc && (
                        <Link
                            href={`/products?category=${product.danh_muc_id}`}
                            className="text-sm text-primary font-medium hover:text-primary-dark"
                        >
                            {product.danh_muc.ten}
                        </Link>
                    )}

                    {/* Title */}
                    <h1 className="text-3xl font-bold text-gray-900 mt-2 mb-4">
                        {product.ten}
                    </h1>

                    {/* Rating */}
                    <div className="flex items-center mb-6">
                        <div className="flex items-center">
                            {[...Array(5)].map((_, i) => (
                                <Star
                                    key={i}
                                    className={`w-5 h-5 ${i < 4 ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'
                                        }`}
                                />
                            ))}
                        </div>
                        <span className="text-sm text-gray-600 ml-3">(4.0) • 128 đánh giá</span>
                    </div>

                    {/* Price */}
                    <div className="bg-gray-50 rounded-xl p-6 mb-6">
                        <div className="flex items-baseline space-x-3">
                            <span className="text-4xl font-bold text-primary">
                                {Number(product.gia).toLocaleString('vi-VN')}đ
                            </span>
                        </div>
                    </div>

                    {/* Description */}
                    <div className="mb-6">
                        <p className="text-gray-600 leading-relaxed">{product.mo_ta}</p>
                    </div>

                    {/* Features */}
                    <div className="grid grid-cols-2 gap-4 mb-6">
                        <div className="flex items-center space-x-3 p-4 bg-gray-50 rounded-lg">
                            <Truck className="w-6 h-6 text-primary" />
                            <div>
                                <p className="text-sm font-medium text-gray-900">Miễn phí vận chuyển</p>
                                <p className="text-xs text-gray-600">Giao hàng nhanh 2h</p>
                            </div>
                        </div>
                        <div className="flex items-center space-x-3 p-4 bg-gray-50 rounded-lg">
                            <Shield className="w-6 h-6 text-primary" />
                            <div>
                                <p className="text-sm font-medium text-gray-900">Bảo hành 12 tháng</p>
                                <p className="text-xs text-gray-600">Chính hãng toàn quốc</p>
                            </div>
                        </div>
                    </div>

                    {/* Quantity */}
                    <div className="mb-6">
                        <label className="block text-sm font-medium text-gray-900 mb-3">
                            Số lượng
                        </label>
                        <div className="flex items-center space-x-4">
                            <div className="flex items-center border border-gray-300 rounded-lg">
                                <button
                                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                                    className="px-4 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-50"
                                >
                                    -
                                </button>
                                <input
                                    type="number"
                                    value={quantity}
                                    onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                                    className="w-16 text-center border-x border-gray-300 py-2 focus:outline-none"
                                />
                                <button
                                    onClick={() => setQuantity(quantity + 1)}
                                    className="px-4 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-50"
                                >
                                    +
                                </button>
                            </div>
                            <span className="text-sm text-gray-600">Còn 50 sản phẩm</span>
                        </div>
                    </div>

                    {/* Actions */}
                    <div className="flex gap-4 mb-6">
                        <button
                            onClick={handleAddToCart}
                            className="flex-1 btn-secondary flex items-center justify-center space-x-2"
                        >
                            <ShoppingCart className="w-5 h-5" />
                            <span>Thêm vào giỏ</span>
                        </button>
                        <button
                            onClick={handleBuyNow}
                            className="flex-1 btn-primary"
                        >
                            Mua ngay
                        </button>
                    </div>

                    {/* Additional Actions */}
                    <div className="flex gap-4">
                        <button className="flex-1 btn-secondary flex items-center justify-center space-x-2">
                            <Heart className="w-5 h-5" />
                            <span>Yêu thích</span>
                        </button>
                        <button className="flex-1 btn-secondary flex items-center justify-center space-x-2">
                            <Share2 className="w-5 h-5" />
                            <span>Chia sẻ</span>
                        </button>
                    </div>
                </div>
            </div>

            {/* Reviews Section */}
            <div className="mt-16">
                <div className="border-t pt-8">
                    <h2 className="text-2xl font-bold text-gray-900 mb-6">Đánh giá sản phẩm</h2>
                    
                    {/* Review Summary */}
                    <div className="bg-gray-50 rounded-xl p-6 mb-8">
                        <div className="flex items-center gap-8">
                            <div className="text-center">
                                <div className="text-5xl font-bold text-gray-900 mb-2">4.0</div>
                                <div className="flex items-center justify-center mb-2">
                                    {[...Array(5)].map((_, i) => (
                                        <Star
                                            key={i}
                                            className={`w-5 h-5 ${i < 4 ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'}`}
                                        />
                                    ))}
                                </div>
                                <p className="text-sm text-gray-600">128 đánh giá</p>
                            </div>
                            <div className="flex-1">
                                {[5, 4, 3, 2, 1].map((star) => (
                                    <div key={star} className="flex items-center gap-3 mb-2">
                                        <span className="text-sm text-gray-600 w-12">{star} sao</span>
                                        <div className="flex-1 bg-gray-200 rounded-full h-2">
                                            <div
                                                className="bg-yellow-400 h-2 rounded-full"
                                                style={{ width: `${star === 5 ? 60 : star === 4 ? 30 : 10}%` }}
                                            />
                                        </div>
                                        <span className="text-sm text-gray-600 w-12 text-right">
                                            {star === 5 ? 77 : star === 4 ? 38 : 13}
                                        </span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Write Review Button */}
                    <button className="btn-primary mb-8">
                        Viết đánh giá
                    </button>

                    {/* Reviews List */}
                    <div className="space-y-6">
                        {/* Sample Review 1 */}
                        <div className="border-b pb-6">
                            <div className="flex items-start gap-4">
                                <div className="w-12 h-12 bg-primary text-white rounded-full flex items-center justify-center font-semibold">
                                    N
                                </div>
                                <div className="flex-1">
                                    <div className="flex items-center justify-between mb-2">
                                        <div>
                                            <h4 className="font-semibold text-gray-900">Nguyễn Văn A</h4>
                                            <div className="flex items-center gap-2 mt-1">
                                                <div className="flex">
                                                    {[...Array(5)].map((_, i) => (
                                                        <Star
                                                            key={i}
                                                            className="w-4 h-4 text-yellow-400 fill-yellow-400"
                                                        />
                                                    ))}
                                                </div>
                                                <span className="text-sm text-gray-500">2 ngày trước</span>
                                            </div>
                                        </div>
                                    </div>
                                    <p className="text-gray-700 leading-relaxed">
                                        Sản phẩm rất tốt, đáng tiền! Giao hàng nhanh, đóng gói cẩn thận. 
                                        Chất lượng như mô tả, rất hài lòng với sản phẩm này.
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* Sample Review 2 */}
                        <div className="border-b pb-6">
                            <div className="flex items-start gap-4">
                                <div className="w-12 h-12 bg-accent text-white rounded-full flex items-center justify-center font-semibold">
                                    T
                                </div>
                                <div className="flex-1">
                                    <div className="flex items-center justify-between mb-2">
                                        <div>
                                            <h4 className="font-semibold text-gray-900">Trần Thị B</h4>
                                            <div className="flex items-center gap-2 mt-1">
                                                <div className="flex">
                                                    {[...Array(5)].map((_, i) => (
                                                        <Star
                                                            key={i}
                                                            className={`w-4 h-4 ${i < 4 ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'}`}
                                                        />
                                                    ))}
                                                </div>
                                                <span className="text-sm text-gray-500">5 ngày trước</span>
                                            </div>
                                        </div>
                                    </div>
                                    <p className="text-gray-700 leading-relaxed">
                                        Chất lượng ổn, giao hàng nhanh. Sản phẩm đúng như mô tả.
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* Sample Review 3 */}
                        <div className="border-b pb-6">
                            <div className="flex items-start gap-4">
                                <div className="w-12 h-12 bg-green-500 text-white rounded-full flex items-center justify-center font-semibold">
                                    L
                                </div>
                                <div className="flex-1">
                                    <div className="flex items-center justify-between mb-2">
                                        <div>
                                            <h4 className="font-semibold text-gray-900">Lê Văn C</h4>
                                            <div className="flex items-center gap-2 mt-1">
                                                <div className="flex">
                                                    {[...Array(5)].map((_, i) => (
                                                        <Star
                                                            key={i}
                                                            className="w-4 h-4 text-yellow-400 fill-yellow-400"
                                                        />
                                                    ))}
                                                </div>
                                                <span className="text-sm text-gray-500">1 tuần trước</span>
                                            </div>
                                        </div>
                                    </div>
                                    <p className="text-gray-700 leading-relaxed">
                                        Tuyệt vời, sẽ mua lại lần sau. Shop phục vụ nhiệt tình!
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Load More */}
                    <div className="text-center mt-8">
                        <button className="btn-secondary">
                            Xem thêm đánh giá
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

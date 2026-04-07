'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { getProduct, getReviews, getReviewStats } from '@/lib/api';
import { Product, Review, ReviewStats } from '@/lib/types';
import { useCart } from '@/contexts/CartContext';
import { Star, ShoppingCart, Heart, Share2, Truck, Shield, ArrowLeft, Package, Award } from 'lucide-react';

export default function ProductDetailPage() {
    const params = useParams();
    const { addToCart } = useCart();
    const [product, setProduct] = useState<Product | null>(null);
    const [reviews, setReviews] = useState<Review[]>([]);
    const [reviewStats, setReviewStats] = useState<ReviewStats | null>(null);
    const [loading, setLoading] = useState(true);
    const [reviewsLoading, setReviewsLoading] = useState(true);
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

        const fetchReviews = async () => {
            try {
                const [reviewsData, statsData] = await Promise.all([
                    getReviews(Number(params.id), 0, 10),
                    getReviewStats(Number(params.id))
                ]);
                setReviews(reviewsData);
                setReviewStats(statsData);
            } catch (error) {
                console.error('Error fetching reviews:', error);
            } finally {
                setReviewsLoading(false);
            }
        };

        if (params.id) {
            fetchProduct();
            fetchReviews();
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
                                    className={`w-5 h-5 ${
                                        i < Math.floor(reviewStats?.average_rating || 0)
                                            ? 'text-yellow-400 fill-yellow-400'
                                            : 'text-gray-300'
                                    }`}
                                />
                            ))}
                        </div>
                        <span className="text-sm text-gray-600 ml-3">
                            ({reviewStats?.average_rating?.toFixed(1) || '0.0'}) • {reviewStats?.total_reviews || 0} đánh giá
                        </span>
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
                        <h3 className="text-lg font-semibold text-gray-900 mb-3">Mô tả sản phẩm</h3>
                        <p className="text-gray-600 leading-relaxed">{product.mo_ta}</p>
                    </div>

                    {/* Product Info/Specs */}
                    <div className="mb-6 bg-gray-50 rounded-xl p-6">
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">Thông tin sản phẩm</h3>
                        <div className="space-y-3">
                            <div className="flex items-center justify-between py-2 border-b border-gray-200">
                                <span className="text-gray-600 flex items-center">
                                    <Package className="w-4 h-4 mr-2" />
                                    Danh mục
                                </span>
                                <span className="font-medium text-gray-900">{product.danh_muc?.ten || 'N/A'}</span>
                            </div>
                            <div className="flex items-center justify-between py-2 border-b border-gray-200">
                                <span className="text-gray-600 flex items-center">
                                    <Award className="w-4 h-4 mr-2" />
                                    Thương hiệu
                                </span>
                                <span className="font-medium text-gray-900">Chính hãng</span>
                            </div>
                            <div className="flex items-center justify-between py-2 border-b border-gray-200">
                                <span className="text-gray-600 flex items-center">
                                    <Shield className="w-4 h-4 mr-2" />
                                    Bảo hành
                                </span>
                                <span className="font-medium text-gray-900">12 tháng</span>
                            </div>
                            <div className="flex items-center justify-between py-2">
                                <span className="text-gray-600 flex items-center">
                                    <Truck className="w-4 h-4 mr-2" />
                                    Giao hàng
                                </span>
                                <span className="font-medium text-gray-900">Miễn phí toàn quốc</span>
                            </div>
                        </div>
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
                    
                    {reviewsLoading ? (
                        <div className="animate-pulse space-y-4">
                            <div className="h-32 bg-gray-200 rounded-xl" />
                            <div className="h-24 bg-gray-200 rounded" />
                            <div className="h-24 bg-gray-200 rounded" />
                        </div>
                    ) : (
                        <>
                            {/* Review Summary */}
                            {reviewStats && reviewStats.total_reviews > 0 ? (
                                <div className="bg-gray-50 rounded-xl p-6 mb-8">
                                    <div className="flex items-center gap-8">
                                        <div className="text-center">
                                            <div className="text-5xl font-bold text-gray-900 mb-2">
                                                {reviewStats.average_rating.toFixed(1)}
                                            </div>
                                            <div className="flex items-center justify-center mb-2">
                                                {[...Array(5)].map((_, i) => (
                                                    <Star
                                                        key={i}
                                                        className={`w-5 h-5 ${
                                                            i < Math.floor(reviewStats.average_rating)
                                                                ? 'text-yellow-400 fill-yellow-400'
                                                                : 'text-gray-300'
                                                        }`}
                                                    />
                                                ))}
                                            </div>
                                            <p className="text-sm text-gray-600">{reviewStats.total_reviews} đánh giá</p>
                                        </div>
                                        <div className="flex-1">
                                            {[5, 4, 3, 2, 1].map((star) => {
                                                const count = reviewStats.rating_distribution[star] || 0;
                                                const percentage = reviewStats.total_reviews > 0
                                                    ? (count / reviewStats.total_reviews) * 100
                                                    : 0;
                                                return (
                                                    <div key={star} className="flex items-center gap-3 mb-2">
                                                        <span className="text-sm text-gray-600 w-12">{star} sao</span>
                                                        <div className="flex-1 bg-gray-200 rounded-full h-2">
                                                            <div
                                                                className="bg-yellow-400 h-2 rounded-full transition-all"
                                                                style={{ width: `${percentage}%` }}
                                                            />
                                                        </div>
                                                        <span className="text-sm text-gray-600 w-12 text-right">
                                                            {count}
                                                        </span>
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <div className="bg-gray-50 rounded-xl p-8 mb-8 text-center">
                                    <p className="text-gray-500">Chưa có đánh giá nào cho sản phẩm này</p>
                                </div>
                            )}

                            {/* Write Review Button */}
                            <button className="btn-primary mb-8">
                                Viết đánh giá
                            </button>

                            {/* Reviews List */}
                            {reviews.length > 0 ? (
                                <div className="space-y-6">
                                    {reviews.map((review) => {
                                        const initials = review.nguoi_dung?.ho_ten
                                            ?.split(' ')
                                            .map(n => n[0])
                                            .join('')
                                            .toUpperCase()
                                            .slice(0, 2) || 'U';
                                        
                                        const colors = ['bg-primary', 'bg-accent', 'bg-green-500', 'bg-blue-500', 'bg-purple-500'];
                                        const colorIndex = review.nguoi_dung_id % colors.length;
                                        
                                        const timeAgo = getTimeAgo(review.ngay_tao);
                                        
                                        return (
                                            <div key={review.id} className="border-b pb-6">
                                                <div className="flex items-start gap-4">
                                                    <div className={`w-12 h-12 ${colors[colorIndex]} text-white rounded-full flex items-center justify-center font-semibold`}>
                                                        {initials}
                                                    </div>
                                                    <div className="flex-1">
                                                        <div className="flex items-center justify-between mb-2">
                                                            <div>
                                                                <h4 className="font-semibold text-gray-900">
                                                                    {review.nguoi_dung?.ho_ten || 'Người dùng'}
                                                                </h4>
                                                                <div className="flex items-center gap-2 mt-1">
                                                                    <div className="flex">
                                                                        {[...Array(5)].map((_, i) => (
                                                                            <Star
                                                                                key={i}
                                                                                className={`w-4 h-4 ${
                                                                                    i < Math.floor(review.diem_so)
                                                                                        ? 'text-yellow-400 fill-yellow-400'
                                                                                        : 'text-gray-300'
                                                                                }`}
                                                                            />
                                                                        ))}
                                                                    </div>
                                                                    <span className="text-sm text-gray-500">{timeAgo}</span>
                                                                </div>
                                                            </div>
                                                        </div>
                                                        {review.binh_luan && (
                                                            <p className="text-gray-700 leading-relaxed">
                                                                {review.binh_luan}
                                                            </p>
                                                        )}
                                                    </div>
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            ) : (
                                <div className="text-center py-8 text-gray-500">
                                    Chưa có đánh giá nào
                                </div>
                            )}

                            {/* Load More */}
                            {reviews.length >= 10 && (
                                <div className="text-center mt-8">
                                    <button className="btn-secondary">
                                        Xem thêm đánh giá
                                    </button>
                                </div>
                            )}
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}

// Helper function to calculate time ago
function getTimeAgo(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);
    
    if (seconds < 60) return 'Vừa xong';
    if (seconds < 3600) return `${Math.floor(seconds / 60)} phút trước`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)} giờ trước`;
    if (seconds < 604800) return `${Math.floor(seconds / 86400)} ngày trước`;
    if (seconds < 2592000) return `${Math.floor(seconds / 604800)} tuần trước`;
    if (seconds < 31536000) return `${Math.floor(seconds / 2592000)} tháng trước`;
    return `${Math.floor(seconds / 31536000)} năm trước`;
}

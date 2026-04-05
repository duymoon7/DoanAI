'use client';

import Link from 'next/link';
import Image from 'next/image';
import { Product } from '@/lib/types';
import { ShoppingCart, Star } from 'lucide-react';
import { useCart } from '@/contexts/CartContext';

interface ProductCardProps {
    product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
    const { addToCart } = useCart();

    const handleAddToCart = (e: React.MouseEvent) => {
        e.preventDefault();
        addToCart(product);
    };

    return (
        <Link href={`/products/${product.id}`}>
            <div className="card group cursor-pointer h-full flex flex-col">
                {/* Image */}
                <div className="relative aspect-square bg-gray-100 overflow-hidden">
                    <Image
                        src={product.hinh_anh || '/placeholder.png'}
                        alt={product.ten}
                        fill
                        className="object-cover group-hover:scale-105 transition-transform duration-300"
                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 25vw"
                    />
                </div>

                {/* Content */}
                <div className="p-4 flex-1 flex flex-col">
                    {/* Category */}
                    {product.danh_muc && (
                        <span className="text-xs text-primary font-medium mb-2">
                            {product.danh_muc.ten}
                        </span>
                    )}

                    {/* Title */}
                    <h3 className="text-sm font-medium text-gray-900 mb-2 line-clamp-2 group-hover:text-primary transition-colors">
                        {product.ten}
                    </h3>

                    {/* Rating */}
                    <div className="flex items-center mb-3">
                        <div className="flex items-center">
                            {[...Array(5)].map((_, i) => (
                                <Star
                                    key={i}
                                    className={`w-4 h-4 ${i < 4 ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'
                                        }`}
                                />
                            ))}
                        </div>
                        <span className="text-xs text-gray-500 ml-2">(4.0)</span>
                    </div>

                    {/* Price & Button */}
                    <div className="mt-auto flex items-center justify-between">
                        <div>
                            <p className="text-lg font-bold text-primary">
                                {Number(product.gia).toLocaleString('vi-VN')}đ
                            </p>
                        </div>
                        <button
                            onClick={handleAddToCart}
                            className="p-2 bg-primary hover:bg-primary-dark text-white rounded-lg transition-colors"
                        >
                            <ShoppingCart className="w-5 h-5" />
                        </button>
                    </div>
                </div>
            </div>
        </Link>
    );
}

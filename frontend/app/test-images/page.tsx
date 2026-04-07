'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';

interface Product {
    id: number;
    ten: string;
    gia: string;
    hinh_anh: string;
    danh_muc?: {
        id: number;
        ten: string;
    };
}

export default function TestImagesPage() {
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/san-pham?limit=5');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                console.log('API Response:', data);
                setProducts(data);
            } catch (err) {
                console.error('Error fetching products:', err);
                setError(err instanceof Error ? err.message : 'Unknown error');
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, []);

    if (loading) {
        return (
            <div className="max-w-7xl mx-auto px-4 py-8">
                <h1 className="text-2xl font-bold mb-4">Test Images - Loading...</h1>
            </div>
        );
    }

    if (error) {
        return (
            <div className="max-w-7xl mx-auto px-4 py-8">
                <h1 className="text-2xl font-bold mb-4 text-red-600">Error: {error}</h1>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold mb-8">Test Images Page</h1>

            <div className="space-y-8">
                {products.map((product) => (
                    <div key={product.id} className="border rounded-lg p-6 bg-white shadow">
                        <h2 className="text-xl font-bold mb-4">
                            #{product.id} - {product.ten}
                        </h2>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {/* Thông tin sản phẩm */}
                            <div className="space-y-2">
                                <p><strong>Giá:</strong> {Number(product.gia).toLocaleString('vi-VN')}đ</p>
                                <p><strong>Danh mục:</strong> {product.danh_muc?.ten || 'N/A'}</p>
                                <p><strong>URL ảnh:</strong></p>
                                <div className="bg-gray-100 p-2 rounded text-xs break-all">
                                    {product.hinh_anh || 'NO IMAGE URL'}
                                </div>
                            </div>

                            {/* Test hiển thị ảnh */}
                            <div className="space-y-4">
                                {/* Method 1: Next.js Image component */}
                                <div>
                                    <p className="font-semibold mb-2">Method 1: Next.js Image</p>
                                    <div className="relative w-full h-48 bg-gray-100 rounded">
                                        {product.hinh_anh ? (
                                            <Image
                                                src={product.hinh_anh}
                                                alt={product.ten}
                                                fill
                                                className="object-contain"
                                                onError={(e) => {
                                                    console.error('Image load error:', product.hinh_anh);
                                                    e.currentTarget.src = '/placeholder.png';
                                                }}
                                            />
                                        ) : (
                                            <div className="flex items-center justify-center h-full text-gray-400">
                                                No Image
                                            </div>
                                        )}
                                    </div>
                                </div>

                                {/* Method 2: Regular img tag */}
                                <div>
                                    <p className="font-semibold mb-2">Method 2: Regular img tag</p>
                                    <div className="w-full h-48 bg-gray-100 rounded overflow-hidden">
                                        {product.hinh_anh ? (
                                            <img
                                                src={product.hinh_anh}
                                                alt={product.ten}
                                                className="w-full h-full object-contain"
                                                onError={(e) => {
                                                    console.error('img tag error:', product.hinh_anh);
                                                    e.currentTarget.src = '/placeholder.png';
                                                }}
                                            />
                                        ) : (
                                            <div className="flex items-center justify-center h-full text-gray-400">
                                                No Image
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {products.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                    Không có sản phẩm nào
                </div>
            )}
        </div>
    );
}

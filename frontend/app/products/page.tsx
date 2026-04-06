'use client';

import { useEffect, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { getProducts, getCategories } from '@/lib/api';
import { Product, Category } from '@/lib/types';
import ProductCard from '@/components/ProductCard';
import { ProductGridSkeleton } from '@/components/LoadingSkeleton';
import { SlidersHorizontal, X } from 'lucide-react';

function ProductsContent() {
    const searchParams = useSearchParams();
    const [products, setProducts] = useState<Product[]>([]);
    const [categories, setCategories] = useState<Category[]>([]);
    const [loading, setLoading] = useState(true);
    const [showFilters, setShowFilters] = useState(false);

    // Filters
    const [selectedCategory, setSelectedCategory] = useState<string>('');
    const [priceRange, setPriceRange] = useState<[number, number]>([0, 50000000]);
    const [sortBy, setSortBy] = useState<string>('newest');
    const [searchQuery, setSearchQuery] = useState<string>('');

    useEffect(() => {
        const category = searchParams.get('category');
        const search = searchParams.get('search');

        if (category) setSelectedCategory(category);
        if (search) setSearchQuery(search);
    }, [searchParams]);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const [productsData, categoriesData] = await Promise.all([
                    getProducts(),
                    getCategories(),
                ]);
                setProducts(productsData);
                setCategories(categoriesData);
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    // Filter and sort products
    const filteredProducts = products
        .filter((product) => {
            // Category filter
            if (selectedCategory && product.danh_muc_id !== parseInt(selectedCategory)) {
                return false;
            }

            // Price filter
            if (product.gia < priceRange[0] || product.gia > priceRange[1]) {
                return false;
            }

            // Search filter
            if (searchQuery && !product.ten.toLowerCase().includes(searchQuery.toLowerCase())) {
                return false;
            }

            return true;
        })
        .sort((a, b) => {
            switch (sortBy) {
                case 'price-asc':
                    return a.gia - b.gia;
                case 'price-desc':
                    return b.gia - a.gia;
                case 'name':
                    return a.ten.localeCompare(b.ten);
                default: // newest
                    return new Date(b.ngay_tao).getTime() - new Date(a.ngay_tao).getTime();
            }
        });

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Header */}
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Sản phẩm</h1>
                    <p className="text-gray-600 mt-2">
                        Tìm thấy {filteredProducts.length} sản phẩm
                    </p>
                </div>

                <button
                    onClick={() => setShowFilters(!showFilters)}
                    className="lg:hidden btn-secondary flex items-center space-x-2"
                >
                    <SlidersHorizontal className="w-5 h-5" />
                    <span>Bộ lọc</span>
                </button>
            </div>

            <div className="flex gap-8">
                {/* Sidebar Filters */}
                <aside
                    className={`${showFilters ? 'block' : 'hidden'
                        } lg:block w-full lg:w-64 flex-shrink-0`}
                >
                    <div className="card p-6 sticky top-20">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-lg font-bold text-gray-900">Bộ lọc</h2>
                            <button
                                onClick={() => setShowFilters(false)}
                                className="lg:hidden text-gray-500 hover:text-gray-700"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        </div>

                        {/* Category Filter */}
                        <div className="mb-6">
                            <h3 className="font-semibold text-gray-900 mb-3">Danh mục</h3>
                            <div className="space-y-2">
                                <label className="flex items-center space-x-2 cursor-pointer">
                                    <input
                                        type="radio"
                                        name="category"
                                        checked={selectedCategory === ''}
                                        onChange={() => setSelectedCategory('')}
                                        className="text-primary focus:ring-primary"
                                    />
                                    <span className="text-sm text-gray-700">Tất cả</span>
                                </label>
                                {categories.map((category) => (
                                    <label key={category.id} className="flex items-center space-x-2 cursor-pointer">
                                        <input
                                            type="radio"
                                            name="category"
                                            checked={selectedCategory === category.id.toString()}
                                            onChange={() => setSelectedCategory(category.id.toString())}
                                            className="text-primary focus:ring-primary"
                                        />
                                        <span className="text-sm text-gray-700">{category.ten}</span>
                                    </label>
                                ))}
                            </div>
                        </div>

                        {/* Price Range */}
                        <div className="mb-6">
                            <h3 className="font-semibold text-gray-900 mb-3">Khoảng giá</h3>
                            <div className="space-y-3">
                                <input
                                    type="range"
                                    min="0"
                                    max="50000000"
                                    step="1000000"
                                    value={priceRange[1]}
                                    onChange={(e) => setPriceRange([0, parseInt(e.target.value)])}
                                    className="w-full"
                                />
                                <div className="flex items-center justify-between text-sm text-gray-600">
                                    <span>{(priceRange[0] / 1000000).toFixed(0)}tr</span>
                                    <span>{(priceRange[1] / 1000000).toFixed(0)}tr</span>
                                </div>
                            </div>
                        </div>

                        {/* Sort */}
                        <div>
                            <h3 className="font-semibold text-gray-900 mb-3">Sắp xếp</h3>
                            <select
                                value={sortBy}
                                onChange={(e) => setSortBy(e.target.value)}
                                className="input text-sm"
                            >
                                <option value="newest">Mới nhất</option>
                                <option value="price-asc">Giá: Thấp đến cao</option>
                                <option value="price-desc">Giá: Cao đến thấp</option>
                                <option value="name">Tên A-Z</option>
                            </select>
                        </div>

                        {/* Reset */}
                        <button
                            onClick={() => {
                                setSelectedCategory('');
                                setPriceRange([0, 50000000]);
                                setSortBy('newest');
                                setSearchQuery('');
                            }}
                            className="w-full mt-6 text-sm text-primary hover:text-primary-dark font-medium"
                        >
                            Xóa bộ lọc
                        </button>
                    </div>
                </aside>

                {/* Products Grid */}
                <div className="flex-1">
                    {loading ? (
                        <ProductGridSkeleton />
                    ) : filteredProducts.length === 0 ? (
                        <div className="text-center py-16">
                            <p className="text-gray-500 text-lg">Không tìm thấy sản phẩm nào</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                            {filteredProducts.map((product) => (
                                <ProductCard key={product.id} product={product} />
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default function ProductsPage() {
    return (
        <Suspense fallback={<ProductGridSkeleton />}>
            <ProductsContent />
        </Suspense>
    );
}

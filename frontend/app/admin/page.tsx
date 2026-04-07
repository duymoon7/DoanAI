'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import toast from 'react-hot-toast';
import { Users, Package, ShoppingCart, FolderTree, MessageSquare, Star, Ticket } from 'lucide-react';

export default function AdminDashboard() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [isAdmin, setIsAdmin] = useState(false);
  const [stats, setStats] = useState({
    products: 0,
    categories: 0,
    users: 0,
    orders: 0
  });

  useEffect(() => {
    // Check if user is admin
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');
    
    if (!token || !userStr) {
      toast.error('Vui lòng đăng nhập!');
      router.push('/auth/login');
      return;
    }

    try {
      const user = JSON.parse(userStr);
      if (user.vai_tro !== 'admin' && user.vai_tro !== 'manager') {
        toast.error('Bạn không có quyền truy cập trang này!');
        router.push('/');
        return;
      }
      
      setIsAdmin(user.vai_tro === 'admin');
      fetchStats();
    } catch (error) {
      console.error('Error parsing user data:', error);
      toast.error('Lỗi xác thực');
      router.push('/auth/login');
    }
  }, [router]);

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/admin/info');
      const data = await response.json();
      if (data.record_counts) {
        setStats({
          products: data.record_counts.products || 0,
          categories: data.record_counts.categories || 0,
          users: data.record_counts.users || 0,
          orders: data.record_counts.orders || 0
        });
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
      toast.error('Không thể tải thống kê');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-8"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-32 bg-gray-200 rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold">Quản trị hệ thống</h1>
        <div className="text-sm text-gray-600">
          Admin Dashboard
        </div>
      </div>
      
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white p-6 rounded-lg shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100 text-sm mb-1">Sản phẩm</p>
              <p className="text-3xl font-bold">{stats.products}</p>
            </div>
            <Package className="w-12 h-12 text-blue-200" />
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-green-500 to-green-600 text-white p-6 rounded-lg shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100 text-sm mb-1">Danh mục</p>
              <p className="text-3xl font-bold">{stats.categories}</p>
            </div>
            <FolderTree className="w-12 h-12 text-green-200" />
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-yellow-500 to-yellow-600 text-white p-6 rounded-lg shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-yellow-100 text-sm mb-1">Người dùng</p>
              <p className="text-3xl font-bold">{stats.users}</p>
            </div>
            <Users className="w-12 h-12 text-yellow-200" />
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 text-white p-6 rounded-lg shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100 text-sm mb-1">Đơn hàng</p>
              <p className="text-3xl font-bold">{stats.orders}</p>
            </div>
            <ShoppingCart className="w-12 h-12 text-purple-200" />
          </div>
        </div>
      </div>

      {/* Management Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Link href="/admin/products" className="card p-6 hover:shadow-lg transition-all group">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center group-hover:bg-blue-200 transition-colors">
              <Package className="w-6 h-6 text-blue-600" />
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-semibold mb-2 group-hover:text-primary transition-colors">
                Quản lý sản phẩm
              </h3>
              <p className="text-gray-600 text-sm">Thêm, sửa, xóa sản phẩm</p>
            </div>
          </div>
        </Link>
        
        {/* Chỉ Admin mới thấy Quản lý danh mục */}
        {isAdmin && (
          <Link href="/admin/categories" className="card p-6 hover:shadow-lg transition-all group">
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center group-hover:bg-green-200 transition-colors">
                <FolderTree className="w-6 h-6 text-green-600" />
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-semibold mb-2 group-hover:text-primary transition-colors">
                  Quản lý danh mục
                </h3>
                <p className="text-gray-600 text-sm">Quản lý danh mục sản phẩm</p>
              </div>
            </div>
          </Link>
        )}
        
        <Link href="/admin/orders" className="card p-6 hover:shadow-lg transition-all group">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center group-hover:bg-purple-200 transition-colors">
              <ShoppingCart className="w-6 h-6 text-purple-600" />
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-semibold mb-2 group-hover:text-primary transition-colors">
                Quản lý đơn hàng
              </h3>
              <p className="text-gray-600 text-sm">Xem và xử lý đơn hàng</p>
            </div>
          </div>
        </Link>
        
        <Link href="/admin/users" className="card p-6 hover:shadow-lg transition-all group">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center group-hover:bg-yellow-200 transition-colors">
              <Users className="w-6 h-6 text-yellow-600" />
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-semibold mb-2 group-hover:text-primary transition-colors">
                Quản lý người dùng
              </h3>
              <p className="text-gray-600 text-sm">Quản lý tài khoản người dùng</p>
            </div>
          </div>
        </Link>
        
        <Link href="/admin/reviews" className="card p-6 hover:shadow-lg transition-all group">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center group-hover:bg-pink-200 transition-colors">
              <Star className="w-6 h-6 text-pink-600" />
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-semibold mb-2 group-hover:text-primary transition-colors">
                Quản lý đánh giá
              </h3>
              <p className="text-gray-600 text-sm">Xem và quản lý đánh giá</p>
            </div>
          </div>
        </Link>
        
        <Link href="/admin/coupons" className="card p-6 hover:shadow-lg transition-all group">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center group-hover:bg-orange-200 transition-colors">
              <Ticket className="w-6 h-6 text-orange-600" />
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-semibold mb-2 group-hover:text-primary transition-colors">
                Quản lý mã giảm giá
              </h3>
              <p className="text-gray-600 text-sm">Tạo và quản lý mã giảm giá</p>
            </div>
          </div>
        </Link>
      </div>
    </div>
  );
}

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Package, ShoppingBag, Truck, CreditCard } from 'lucide-react';
import toast from 'react-hot-toast';

interface Order {
  id: number;
  nguoi_dung_id: number;
  tong_tien: number;
  trang_thai: string;
  phuong_thuc_thanh_toan: string;
  ngay_tao: string;
}

export default function OrdersPage() {
  const router = useRouter();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentUserId, setCurrentUserId] = useState<number | null>(null);

  useEffect(() => {
    // Check if user is logged in
    const userStr = localStorage.getItem('user');
    if (!userStr) {
      toast.error('Vui lòng đăng nhập để xem đơn hàng');
      router.push('/auth/login');
      return;
    }

    try {
      const user = JSON.parse(userStr);
      setCurrentUserId(user.id);
      fetchOrders(user.id);
    } catch (error) {
      console.error('Error parsing user data:', error);
      toast.error('Lỗi xác thực');
      router.push('/auth/login');
    }
  }, [router]);

  const fetchOrders = async (userId: number) => {
    try {
      const response = await fetch('http://localhost:8000/api/don-hang');
      const data = await response.json();
      
      // Lọc chỉ lấy đơn hàng của user hiện tại
      const userOrders = data.filter((order: Order) => order.nguoi_dung_id === userId);
      setOrders(userOrders);
    } catch (error) {
      console.error('Error fetching orders:', error);
      toast.error('Không thể tải danh sách đơn hàng');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelOrder = async (orderId: number) => {
    if (!confirm('Bạn có chắc muốn hủy đơn hàng này?')) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/don-hang/${orderId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ trang_thai: 'cancelled' }),
      });

      if (!response.ok) {
        throw new Error('Failed to cancel order');
      }

      toast.success('Đã hủy đơn hàng');
      if (currentUserId) {
        fetchOrders(currentUserId);
      }
    } catch (error) {
      console.error('Error cancelling order:', error);
      toast.error('Không thể hủy đơn hàng');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'completed':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'cancelled':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'pending':
        return 'Đang xử lý';
      case 'completed':
        return 'Hoàn thành';
      case 'cancelled':
        return 'Đã hủy';
      default:
        return status;
    }
  };

  const getPaymentMethodText = (method: string) => {
    switch (method) {
      case 'cod':
        return 'Ship COD';
      case 'bank':
        return 'Chuyển khoản ngân hàng';
      default:
        return method;
    }
  };

  const getPaymentMethodIcon = (method: string) => {
    return method === 'cod' ? <Truck className="w-4 h-4" /> : <CreditCard className="w-4 h-4" />;
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">Đang tải...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Đơn hàng của tôi</h1>
        <p className="text-gray-600 mt-2">
          {orders.length > 0 ? `Bạn có ${orders.length} đơn hàng` : 'Bạn chưa có đơn hàng nào'}
        </p>
      </div>
      
      {orders.length === 0 ? (
        <div className="card p-12 text-center">
          <ShoppingBag className="w-24 h-24 text-gray-300 mx-auto mb-6" />
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Chưa có đơn hàng nào
          </h2>
          <p className="text-gray-600 mb-8">
            Hãy khám phá và mua sắm những sản phẩm tuyệt vời của chúng tôi
          </p>
          <Link href="/products" className="btn-primary inline-block">
            Tiếp tục mua sắm
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {orders.map((order) => (
            <div key={order.id} className="card p-6 hover:shadow-lg transition-shadow">
              {/* Order Header */}
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4 pb-4 border-b border-gray-200">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    Đơn hàng #{order.id}
                  </h3>
                  <p className="text-sm text-gray-600 mt-1">
                    Đặt ngày {new Date(order.ngay_tao).toLocaleDateString('vi-VN', {
                      day: '2-digit',
                      month: '2-digit',
                      year: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </p>
                </div>
                <span className={`px-4 py-2 rounded-full text-sm font-medium border mt-3 sm:mt-0 inline-block ${getStatusColor(order.trang_thai)}`}>
                  {getStatusText(order.trang_thai)}
                </span>
              </div>
              
              {/* Order Details */}
              <div className="space-y-3 mb-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2 text-gray-600">
                    {getPaymentMethodIcon(order.phuong_thuc_thanh_toan)}
                    <span className="text-sm">Phương thức thanh toán:</span>
                  </div>
                  <span className="font-medium text-gray-900">
                    {getPaymentMethodText(order.phuong_thuc_thanh_toan)}
                  </span>
                </div>
                
                <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                  <span className="text-gray-600">Tổng tiền:</span>
                  <span className="text-2xl font-bold text-primary">
                    {order.tong_tien.toLocaleString('vi-VN')}đ
                  </span>
                </div>
              </div>
              
              {/* Actions */}
              <div className="flex flex-wrap gap-3 pt-4 border-t border-gray-200">
                <Link
                  href={`/orders/${order.id}`}
                  className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors font-medium"
                >
                  Xem chi tiết
                </Link>
                
                {order.trang_thai === 'pending' && (
                  <button
                    onClick={() => handleCancelOrder(order.id)}
                    className="px-6 py-2 bg-white border-2 border-red-500 text-red-500 rounded-lg hover:bg-red-50 transition-colors font-medium"
                  >
                    Hủy đơn
                  </button>
                )}
                
                {order.trang_thai === 'completed' && (
                  <button className="px-6 py-2 bg-white border-2 border-primary text-primary rounded-lg hover:bg-primary/5 transition-colors font-medium">
                    Mua lại
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

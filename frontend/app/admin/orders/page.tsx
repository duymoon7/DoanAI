'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { ArrowLeft, Package, Truck, CreditCard, CheckCircle, XCircle, Clock } from 'lucide-react';
import Link from 'next/link';
import { getOrders, updateOrderStatus } from '@/lib/api';

interface Order {
  id: number;
  nguoi_dung_id: number;
  tong_tien: number;
  trang_thai: string;
  phuong_thuc_thanh_toan: string;
  ngay_tao: string;
  nguoi_dung?: {
    id: number;
    email: string;
    ho_ten: string;
    so_dien_thoai?: string;
  };
  chi_tiet_don_hang?: Array<{
    id: number;
    san_pham_id: number;
    so_luong: number;
    san_pham?: {
      id: number;
      ten: string;
      gia: number;
      hinh_anh?: string;
    };
  }>;
}

export default function AdminOrdersPage() {
  const router = useRouter();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>('all');
  const [expandedOrders, setExpandedOrders] = useState<Set<number>>(new Set());

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
      
      fetchOrders();
    } catch (error) {
      console.error('Error parsing user data:', error);
      toast.error('Lỗi xác thực');
      router.push('/auth/login');
    }
  }, [router]);

  const fetchOrders = async () => {
    try {
      const data = await getOrders();
      setOrders(data);
    } catch (error) {
      console.error('Error fetching orders:', error);
      toast.error('Không thể tải danh sách đơn hàng');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateStatus = async (orderId: number, newStatus: string) => {
    try {
      await updateOrderStatus(orderId, { trang_thai: newStatus });
      toast.success('Cập nhật trạng thái thành công');
      fetchOrders();
    } catch (error) {
      console.error('Error updating order status:', error);
      toast.error('Cập nhật trạng thái thất bại');
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

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending':
        return <Clock className="w-4 h-4" />;
      case 'completed':
        return <CheckCircle className="w-4 h-4" />;
      case 'cancelled':
        return <XCircle className="w-4 h-4" />;
      default:
        return <Package className="w-4 h-4" />;
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
        return 'Chuyển khoản';
      default:
        return method;
    }
  };

  const getPaymentMethodIcon = (method: string) => {
    return method === 'cod' ? <Truck className="w-4 h-4" /> : <CreditCard className="w-4 h-4" />;
  };

  const toggleOrderExpand = (orderId: number) => {
    const newExpanded = new Set(expandedOrders);
    if (newExpanded.has(orderId)) {
      newExpanded.delete(orderId);
    } else {
      newExpanded.add(orderId);
    }
    setExpandedOrders(newExpanded);
  };

  const filteredOrders = filter === 'all' 
    ? orders 
    : orders.filter(order => order.trang_thai === filter);

  const stats = {
    total: orders.length,
    pending: orders.filter(o => o.trang_thai === 'pending').length,
    completed: orders.filter(o => o.trang_thai === 'completed').length,
    cancelled: orders.filter(o => o.trang_thai === 'cancelled').length,
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">Đang tải...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center space-x-4">
          <Link href="/admin" className="text-gray-600 hover:text-gray-900">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <div>
            <h1 className="text-3xl font-bold">Quản lý đơn hàng</h1>
            <p className="text-gray-600 mt-1">Xem và xử lý đơn hàng</p>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="card p-4">
          <div className="text-sm text-gray-600 mb-1">Tổng đơn hàng</div>
          <div className="text-2xl font-bold">{stats.total}</div>
        </div>
        <div className="card p-4 border-l-4 border-yellow-500">
          <div className="text-sm text-gray-600 mb-1">Đang xử lý</div>
          <div className="text-2xl font-bold text-yellow-600">{stats.pending}</div>
        </div>
        <div className="card p-4 border-l-4 border-green-500">
          <div className="text-sm text-gray-600 mb-1">Hoàn thành</div>
          <div className="text-2xl font-bold text-green-600">{stats.completed}</div>
        </div>
        <div className="card p-4 border-l-4 border-red-500">
          <div className="text-sm text-gray-600 mb-1">Đã hủy</div>
          <div className="text-2xl font-bold text-red-600">{stats.cancelled}</div>
        </div>
      </div>

      {/* Filters */}
      <div className="card p-4 mb-6">
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              filter === 'all'
                ? 'bg-primary text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Tất cả ({stats.total})
          </button>
          <button
            onClick={() => setFilter('pending')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              filter === 'pending'
                ? 'bg-yellow-500 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Đang xử lý ({stats.pending})
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              filter === 'completed'
                ? 'bg-green-500 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Hoàn thành ({stats.completed})
          </button>
          <button
            onClick={() => setFilter('cancelled')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              filter === 'cancelled'
                ? 'bg-red-500 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Đã hủy ({stats.cancelled})
          </button>
        </div>
      </div>

      {/* Orders List */}
      {filteredOrders.length === 0 ? (
        <div className="card p-8 text-center">
          <Package className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-600">Không có đơn hàng nào</p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredOrders.map((order) => {
            const isExpanded = expandedOrders.has(order.id);
            const itemCount = order.chi_tiet_don_hang?.length || 0;
            
            return (
              <div key={order.id} className="card hover:shadow-lg transition-shadow">
                {/* Order Header - Clickable */}
                <div 
                  className="p-6 cursor-pointer"
                  onClick={() => toggleOrderExpand(order.id)}
                >
                  <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                    {/* Order Info */}
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-3">
                        <h3 className="text-lg font-semibold">Đơn hàng #{order.id}</h3>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium border flex items-center space-x-1 ${getStatusColor(order.trang_thai)}`}>
                          {getStatusIcon(order.trang_thai)}
                          <span>{getStatusText(order.trang_thai)}</span>
                        </span>
                        <span className="text-sm text-gray-500">
                          ({itemCount} sản phẩm)
                        </span>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
                        <div>
                          <span className="text-gray-600">Khách hàng:</span>
                          <div className="font-medium mt-1">
                            {order.nguoi_dung ? order.nguoi_dung.ho_ten : `#${order.nguoi_dung_id}`}
                          </div>
                          {order.nguoi_dung?.email && (
                            <div className="text-gray-500 text-xs">{order.nguoi_dung.email}</div>
                          )}
                          {order.nguoi_dung?.so_dien_thoai && (
                            <div className="text-gray-500 text-xs">{order.nguoi_dung.so_dien_thoai}</div>
                          )}
                        </div>
                        <div className="flex items-center space-x-2">
                          {getPaymentMethodIcon(order.phuong_thuc_thanh_toan)}
                          <div>
                            <div className="text-gray-600 text-xs">Thanh toán</div>
                            <div className="font-medium">{getPaymentMethodText(order.phuong_thuc_thanh_toan)}</div>
                          </div>
                        </div>
                        <div>
                          <span className="text-gray-600">Ngày đặt:</span>
                          <div className="font-medium mt-1">
                            {new Date(order.ngay_tao).toLocaleDateString('vi-VN', {
                              day: '2-digit',
                              month: '2-digit',
                              year: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </div>
                        </div>
                      </div>
                      
                      <div className="mt-3">
                        <span className="text-lg font-bold text-primary">
                          {new Intl.NumberFormat('vi-VN', { 
                            style: 'currency', 
                            currency: 'VND' 
                          }).format(order.tong_tien)}
                        </span>
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex flex-col space-y-2 lg:w-48">
                      {order.trang_thai === 'pending' && (
                        <>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleUpdateStatus(order.id, 'completed');
                            }}
                            className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors text-sm font-medium"
                          >
                            Hoàn thành
                          </button>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleUpdateStatus(order.id, 'cancelled');
                            }}
                            className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors text-sm font-medium"
                          >
                            Hủy đơn
                          </button>
                        </>
                      )}
                      {order.trang_thai === 'cancelled' && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleUpdateStatus(order.id, 'pending');
                          }}
                          className="px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition-colors text-sm font-medium"
                        >
                          Khôi phục
                        </button>
                      )}
                      {order.trang_thai === 'completed' && (
                        <div className="text-center text-sm text-green-600 font-medium py-2">
                          ✓ Đã hoàn thành
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Order Details - Expandable */}
                {isExpanded && order.chi_tiet_don_hang && order.chi_tiet_don_hang.length > 0 && (
                  <div className="border-t border-gray-200 p-6 bg-gray-50">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                      {/* Left: Order Items */}
                      <div className="lg:col-span-2">
                        <h4 className="font-semibold text-gray-900 mb-4">Chi tiết đơn hàng</h4>
                        <div className="space-y-3">
                          {order.chi_tiet_don_hang.map((item) => (
                            <div key={item.id} className="flex items-center space-x-4 bg-white p-4 rounded-lg">
                              {item.san_pham?.hinh_anh && (
                                <img 
                                  src={item.san_pham.hinh_anh} 
                                  alt={item.san_pham.ten}
                                  className="w-16 h-16 object-cover rounded"
                                />
                              )}
                              <div className="flex-1">
                                <h5 className="font-medium text-gray-900">{item.san_pham?.ten || `Sản phẩm #${item.san_pham_id}`}</h5>
                                <p className="text-sm text-gray-600">
                                  Số lượng: {item.so_luong} × {new Intl.NumberFormat('vi-VN', { 
                                    style: 'currency', 
                                    currency: 'VND' 
                                  }).format(item.san_pham?.gia || 0)}
                                </p>
                              </div>
                              <div className="text-right">
                                <p className="font-semibold text-primary">
                                  {new Intl.NumberFormat('vi-VN', { 
                                    style: 'currency', 
                                    currency: 'VND' 
                                  }).format((item.san_pham?.gia || 0) * item.so_luong)}
                                </p>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Right: Customer & Payment Info */}
                      <div className="space-y-4">
                        {/* Customer Info */}
                        <div className="bg-white p-4 rounded-lg">
                          <h4 className="font-semibold text-gray-900 mb-3">Thông tin khách hàng</h4>
                          <div className="space-y-2 text-sm">
                            <div>
                              <p className="text-gray-600">Họ tên</p>
                              <p className="font-medium text-gray-900">
                                {order.nguoi_dung?.ho_ten || `User #${order.nguoi_dung_id}`}
                              </p>
                            </div>
                            {order.nguoi_dung?.email && (
                              <div>
                                <p className="text-gray-600">Email</p>
                                <p className="font-medium text-gray-900 break-all">
                                  {order.nguoi_dung.email}
                                </p>
                              </div>
                            )}
                            {order.nguoi_dung?.so_dien_thoai && (
                              <div>
                                <p className="text-gray-600">Số điện thoại</p>
                                <p className="font-medium text-gray-900">
                                  {order.nguoi_dung.so_dien_thoai}
                                </p>
                              </div>
                            )}
                          </div>
                        </div>

                        {/* Payment Info */}
                        <div className="bg-white p-4 rounded-lg">
                          <h4 className="font-semibold text-gray-900 mb-3">Thông tin thanh toán</h4>
                          <div className="space-y-2 text-sm">
                            <div>
                              <p className="text-gray-600">Phương thức</p>
                              <div className="flex items-center space-x-2 mt-1">
                                {getPaymentMethodIcon(order.phuong_thuc_thanh_toan)}
                                <p className="font-medium text-gray-900">
                                  {getPaymentMethodText(order.phuong_thuc_thanh_toan)}
                                </p>
                              </div>
                            </div>
                            <div>
                              <p className="text-gray-600">Ngày đặt</p>
                              <p className="font-medium text-gray-900">
                                {new Date(order.ngay_tao).toLocaleDateString('vi-VN', {
                                  day: '2-digit',
                                  month: '2-digit',
                                  year: 'numeric',
                                  hour: '2-digit',
                                  minute: '2-digit'
                                })}
                              </p>
                            </div>
                            <div className="pt-2 border-t border-gray-200">
                              <p className="text-gray-600">Tổng tiền</p>
                              <p className="text-xl font-bold text-primary mt-1">
                                {new Intl.NumberFormat('vi-VN', { 
                                  style: 'currency', 
                                  currency: 'VND' 
                                }).format(order.tong_tien)}
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

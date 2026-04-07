'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Package, Truck, CreditCard, User, Mail, Phone, Calendar } from 'lucide-react';
import toast from 'react-hot-toast';

interface OrderDetail {
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

export default function OrderDetailPage() {
  const router = useRouter();
  const params = useParams();
  const orderId = params.id as string;
  
  const [order, setOrder] = useState<OrderDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in
    const userStr = localStorage.getItem('user');
    if (!userStr) {
      toast.error('Vui lòng đăng nhập để xem đơn hàng');
      router.push('/auth/login');
      return;
    }

    fetchOrderDetail();
  }, [orderId, router]);

  const fetchOrderDetail = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/don-hang/${orderId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch order');
      }
      const data = await response.json();
      setOrder(data);
    } catch (error) {
      console.error('Error fetching order:', error);
      toast.error('Không thể tải thông tin đơn hàng');
    } finally {
      setLoading(false);
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

  if (!order) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="card p-12 text-center">
          <Package className="w-24 h-24 text-gray-300 mx-auto mb-6" />
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Không tìm thấy đơn hàng
          </h2>
          <Link href="/orders" className="btn-primary inline-block">
            Quay lại danh sách đơn hàng
          </Link>
        </div>
      </div>
    );
  }

  const totalAmount = order.chi_tiet_don_hang?.reduce(
    (sum, item) => sum + (item.san_pham?.gia || 0) * item.so_luong,
    0
  ) || 0;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex items-center space-x-4 mb-8">
        <Link href="/orders" className="text-gray-600 hover:text-gray-900">
          <ArrowLeft className="w-6 h-6" />
        </Link>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Chi tiết đơn hàng #{order.id}</h1>
          <p className="text-gray-600 mt-1">
            Đặt ngày {new Date(order.ngay_tao).toLocaleDateString('vi-VN', {
              day: '2-digit',
              month: '2-digit',
              year: 'numeric',
              hour: '2-digit',
              minute: '2-digit'
            })}
          </p>
        </div>
        <span className={`px-4 py-2 rounded-full text-sm font-medium border ml-auto ${getStatusColor(order.trang_thai)}`}>
          {getStatusText(order.trang_thai)}
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Order Info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Customer Info */}
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <User className="w-5 h-5 mr-2" />
              Thông tin người đặt
            </h2>
            <div className="space-y-3">
              <div className="flex items-start">
                <User className="w-5 h-5 text-gray-400 mr-3 mt-0.5" />
                <div>
                  <p className="text-sm text-gray-600">Họ tên</p>
                  <p className="font-medium text-gray-900">
                    {order.nguoi_dung?.ho_ten || 'N/A'}
                  </p>
                </div>
              </div>
              <div className="flex items-start">
                <Mail className="w-5 h-5 text-gray-400 mr-3 mt-0.5" />
                <div>
                  <p className="text-sm text-gray-600">Email</p>
                  <p className="font-medium text-gray-900">
                    {order.nguoi_dung?.email || 'N/A'}
                  </p>
                </div>
              </div>
              {order.nguoi_dung?.so_dien_thoai && (
                <div className="flex items-start">
                  <Phone className="w-5 h-5 text-gray-400 mr-3 mt-0.5" />
                  <div>
                    <p className="text-sm text-gray-600">Số điện thoại</p>
                    <p className="font-medium text-gray-900">
                      {order.nguoi_dung.so_dien_thoai}
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Order Items */}
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Package className="w-5 h-5 mr-2" />
              Chi tiết đơn hàng
            </h2>
            <div className="space-y-4">
              {order.chi_tiet_don_hang && order.chi_tiet_don_hang.length > 0 ? (
                order.chi_tiet_don_hang.map((item) => (
                  <div key={item.id} className="flex items-center space-x-4 pb-4 border-b border-gray-200 last:border-0">
                    {item.san_pham?.hinh_anh ? (
                      <img 
                        src={item.san_pham.hinh_anh} 
                        alt={item.san_pham.ten}
                        className="w-20 h-20 object-cover rounded-lg"
                      />
                    ) : (
                      <div className="w-20 h-20 bg-gray-200 rounded-lg flex items-center justify-center">
                        <Package className="w-8 h-8 text-gray-400" />
                      </div>
                    )}
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900">
                        {item.san_pham?.ten || `Sản phẩm #${item.san_pham_id}`}
                      </h3>
                      <p className="text-sm text-gray-600 mt-1">
                        Số lượng: {item.so_luong} × {new Intl.NumberFormat('vi-VN', { 
                          style: 'currency', 
                          currency: 'VND' 
                        }).format(item.san_pham?.gia || 0)}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold text-gray-900">
                        {new Intl.NumberFormat('vi-VN', { 
                          style: 'currency', 
                          currency: 'VND' 
                        }).format((item.san_pham?.gia || 0) * item.so_luong)}
                      </p>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-gray-500 text-center py-4">Không có sản phẩm nào</p>
              )}
            </div>
          </div>
        </div>

        {/* Right Column - Summary */}
        <div className="space-y-6">
          {/* Payment Info */}
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Thông tin thanh toán</h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2 text-gray-600">
                  {order.phuong_thuc_thanh_toan === 'cod' ? (
                    <Truck className="w-5 h-5" />
                  ) : (
                    <CreditCard className="w-5 h-5" />
                  )}
                  <span className="text-sm">Phương thức</span>
                </div>
                <span className="font-medium text-gray-900">
                  {getPaymentMethodText(order.phuong_thuc_thanh_toan)}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2 text-gray-600">
                  <Calendar className="w-5 h-5" />
                  <span className="text-sm">Ngày đặt</span>
                </div>
                <span className="font-medium text-gray-900">
                  {new Date(order.ngay_tao).toLocaleDateString('vi-VN', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric'
                  })}
                </span>
              </div>
            </div>
          </div>

          {/* Order Summary */}
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Tổng đơn hàng</h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between text-gray-600">
                <span>Tạm tính</span>
                <span>{new Intl.NumberFormat('vi-VN', { 
                  style: 'currency', 
                  currency: 'VND' 
                }).format(totalAmount)}</span>
              </div>
              <div className="flex items-center justify-between text-gray-600">
                <span>Phí vận chuyển</span>
                <span>Miễn phí</span>
              </div>
              <div className="border-t border-gray-200 pt-3 flex items-center justify-between">
                <span className="text-lg font-semibold text-gray-900">Tổng cộng</span>
                <span className="text-2xl font-bold text-primary">
                  {new Intl.NumberFormat('vi-VN', { 
                    style: 'currency', 
                    currency: 'VND' 
                  }).format(order.tong_tien)}
                </span>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="space-y-3">
            <Link
              href="/orders"
              className="w-full btn-secondary text-center block"
            >
              Quay lại danh sách
            </Link>
            {order.trang_thai === 'completed' && (
              <button className="w-full btn-primary">
                Mua lại
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

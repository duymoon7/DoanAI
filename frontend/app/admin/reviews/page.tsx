'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Star, Trash2, MessageSquare } from 'lucide-react';
import toast from 'react-hot-toast';

interface Review {
  id: number;
  san_pham_id: number;
  nguoi_dung_id: number;
  diem_so: number;
  binh_luan: string;
  ngay_tao: string;
  san_pham?: {
    id: number;
    ten: string;
    hinh_anh?: string;
  };
  nguoi_dung?: {
    id: number;
    ho_ten: string;
    email: string;
  };
}

export default function AdminReviewsPage() {
  const router = useRouter();
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>('all');

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
        toast.error('Bạn không có quyền truy cập!');
        router.push('/');
        return;
      }
      
      fetchReviews();
    } catch (error) {
      console.error('Error parsing user data:', error);
      toast.error('Lỗi xác thực');
      router.push('/auth/login');
    }
  }, [router]);

  const fetchReviews = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/danh-gia/all');
      const data = await response.json();
      setReviews(data);
    } catch (error) {
      console.error('Error fetching reviews:', error);
      toast.error('Không thể tải danh sách đánh giá');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Bạn có chắc muốn xóa đánh giá này?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/danh-gia/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to delete review');
      }

      toast.success('Xóa đánh giá thành công');
      fetchReviews();
    } catch (error) {
      console.error('Error deleting review:', error);
      toast.error('Xóa đánh giá thất bại');
    }
  };

  const renderStars = (rating: number) => {
    return (
      <div className="flex items-center space-x-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <Star
            key={star}
            className={`w-4 h-4 ${
              star <= rating
                ? 'fill-yellow-400 text-yellow-400'
                : 'text-gray-300'
            }`}
          />
        ))}
      </div>
    );
  };

  const filteredReviews = filter === 'all'
    ? reviews
    : reviews.filter(review => review.diem_so === parseInt(filter));

  const stats = {
    total: reviews.length,
    star5: reviews.filter(r => r.diem_so === 5).length,
    star4: reviews.filter(r => r.diem_so === 4).length,
    star3: reviews.filter(r => r.diem_so === 3).length,
    star2: reviews.filter(r => r.diem_so === 2).length,
    star1: reviews.filter(r => r.diem_so === 1).length,
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
            <h1 className="text-3xl font-bold">Quản lý đánh giá</h1>
            <p className="text-gray-600 mt-1">Xem và quản lý đánh giá sản phẩm</p>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4 mb-8">
        <div className="card p-4">
          <div className="text-sm text-gray-600 mb-1">Tổng đánh giá</div>
          <div className="text-2xl font-bold">{stats.total}</div>
        </div>
        <div className="card p-4 border-l-4 border-yellow-500">
          <div className="text-sm text-gray-600 mb-1">5 sao</div>
          <div className="text-2xl font-bold text-yellow-600">{stats.star5}</div>
        </div>
        <div className="card p-4 border-l-4 border-green-500">
          <div className="text-sm text-gray-600 mb-1">4 sao</div>
          <div className="text-2xl font-bold text-green-600">{stats.star4}</div>
        </div>
        <div className="card p-4 border-l-4 border-blue-500">
          <div className="text-sm text-gray-600 mb-1">3 sao</div>
          <div className="text-2xl font-bold text-blue-600">{stats.star3}</div>
        </div>
        <div className="card p-4 border-l-4 border-orange-500">
          <div className="text-sm text-gray-600 mb-1">2 sao</div>
          <div className="text-2xl font-bold text-orange-600">{stats.star2}</div>
        </div>
        <div className="card p-4 border-l-4 border-red-500">
          <div className="text-sm text-gray-600 mb-1">1 sao</div>
          <div className="text-2xl font-bold text-red-600">{stats.star1}</div>
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
          {[5, 4, 3, 2, 1].map((star) => (
            <button
              key={star}
              onClick={() => setFilter(star.toString())}
              className={`px-4 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2 ${
                filter === star.toString()
                  ? 'bg-yellow-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <Star className="w-4 h-4" />
              <span>{star} sao</span>
            </button>
          ))}
        </div>
      </div>

      {/* Reviews List */}
      {filteredReviews.length === 0 ? (
        <div className="card p-12 text-center">
          <MessageSquare className="w-24 h-24 text-gray-300 mx-auto mb-6" />
          <p className="text-gray-600">Không có đánh giá nào</p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredReviews.map((review) => (
            <div key={review.id} className="card p-6 hover:shadow-lg transition-shadow">
              <div className="flex gap-4">
                {/* Product Image */}
                {review.san_pham?.hinh_anh && (
                  <img
                    src={review.san_pham.hinh_anh}
                    alt={review.san_pham.ten}
                    className="w-20 h-20 object-cover rounded-lg"
                  />
                )}
                
                {/* Review Content */}
                <div className="flex-1">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h3 className="font-semibold text-gray-900">
                        {review.san_pham?.ten || `Sản phẩm #${review.san_pham_id}`}
                      </h3>
                      <p className="text-sm text-gray-600">
                        Bởi: {review.nguoi_dung?.ho_ten || `User #${review.nguoi_dung_id}`}
                      </p>
                    </div>
                    <button
                      onClick={() => handleDelete(review.id)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      title="Xóa"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                  
                  <div className="flex items-center space-x-3 mb-2">
                    {renderStars(review.diem_so)}
                    <span className="text-sm text-gray-500">
                      {new Date(review.ngay_tao).toLocaleDateString('vi-VN')}
                    </span>
                  </div>
                  
                  {review.binh_luan && (
                    <p className="text-gray-700 mt-2">{review.binh_luan}</p>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

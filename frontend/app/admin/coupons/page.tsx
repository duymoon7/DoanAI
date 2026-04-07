'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { Plus, Edit2, Trash2, X, Calendar, Percent, DollarSign } from 'lucide-react';

interface Coupon {
  id: number;
  ma_code: string;
  mo_ta: string | null;
  loai_giam: 'percent' | 'fixed';
  gia_tri_giam: number;
  gia_tri_don_toi_thieu: number;
  so_luong: number;
  da_su_dung: number;
  ngay_bat_dau: string | null;
  ngay_ket_thuc: string | null;
  hoat_dong: boolean;
  ngay_tao: string;
}

export default function CouponsManagement() {
  const router = useRouter();
  const [coupons, setCoupons] = useState<Coupon[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingCoupon, setEditingCoupon] = useState<Coupon | null>(null);
  const [formData, setFormData] = useState({
    ma_code: '',
    mo_ta: '',
    loai_giam: 'percent' as 'percent' | 'fixed',
    gia_tri_giam: '',
    gia_tri_don_toi_thieu: '0',
    so_luong: '1',
    ngay_bat_dau: '',
    ngay_ket_thuc: '',
    hoat_dong: true
  });

  useEffect(() => {
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
      
      fetchCoupons();
    } catch (error) {
      console.error('Error:', error);
      router.push('/auth/login');
    }
  }, [router]);

  const fetchCoupons = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/ma-giam-gia');
      const data = await response.json();
      setCoupons(data);
    } catch (error) {
      console.error('Error fetching coupons:', error);
      toast.error('Không thể tải danh sách mã giảm giá');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const token = localStorage.getItem('token');
    if (!token) {
      toast.error('Vui lòng đăng nhập lại!');
      router.push('/auth/login');
      return;
    }

    try {
      const payload = {
        ma_code: formData.ma_code.toUpperCase(),
        mo_ta: formData.mo_ta || null,
        loai_giam: formData.loai_giam,
        gia_tri_giam: parseFloat(formData.gia_tri_giam),
        gia_tri_don_toi_thieu: parseFloat(formData.gia_tri_don_toi_thieu),
        so_luong: parseInt(formData.so_luong),
        ngay_bat_dau: formData.ngay_bat_dau || null,
        ngay_ket_thuc: formData.ngay_ket_thuc || null,
        hoat_dong: formData.hoat_dong
      };

      const url = editingCoupon
        ? `http://localhost:8000/api/ma-giam-gia/${editingCoupon.id}`
        : 'http://localhost:8000/api/ma-giam-gia';
      
      const method = editingCoupon ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        if (response.status === 401) {
          toast.error('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại!');
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          router.push('/auth/login');
          return;
        }
        const error = await response.json();
        throw new Error(error.detail || 'Có lỗi xảy ra');
      }

      toast.success(editingCoupon ? 'Cập nhật thành công!' : 'Tạo mã giảm giá thành công!');
      setShowModal(false);
      resetForm();
      fetchCoupons();
    } catch (error: any) {
      console.error('Error:', error);
      toast.error(error.message || 'Có lỗi xảy ra');
    }
  };

  const handleEdit = (coupon: Coupon) => {
    setEditingCoupon(coupon);
    setFormData({
      ma_code: coupon.ma_code,
      mo_ta: coupon.mo_ta || '',
      loai_giam: coupon.loai_giam,
      gia_tri_giam: coupon.gia_tri_giam.toString(),
      gia_tri_don_toi_thieu: coupon.gia_tri_don_toi_thieu.toString(),
      so_luong: coupon.so_luong.toString(),
      ngay_bat_dau: coupon.ngay_bat_dau ? coupon.ngay_bat_dau.split('T')[0] : '',
      ngay_ket_thuc: coupon.ngay_ket_thuc ? coupon.ngay_ket_thuc.split('T')[0] : '',
      hoat_dong: coupon.hoat_dong
    });
    setShowModal(true);
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Bạn có chắc muốn xóa mã giảm giá này?')) return;

    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');
    
    if (!token || !userStr) {
      toast.error('Vui lòng đăng nhập lại!');
      router.push('/auth/login');
      return;
    }
    
    const user = JSON.parse(userStr);
    if (user.vai_tro !== 'admin') {
      toast.error('Chỉ Admin mới có quyền xóa!');
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/ma-giam-gia/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.status === 401) {
        toast.error('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại!');
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        router.push('/auth/login');
        return;
      }

      if (!response.ok) throw new Error('Xóa thất bại');

      toast.success('Xóa thành công!');
      fetchCoupons();
    } catch (error) {
      console.error('Error:', error);
      toast.error('Không thể xóa mã giảm giá');
    }
  };

  const resetForm = () => {
    setFormData({
      ma_code: '',
      mo_ta: '',
      loai_giam: 'percent',
      gia_tri_giam: '',
      gia_tri_don_toi_thieu: '0',
      so_luong: '1',
      ngay_bat_dau: '',
      ngay_ket_thuc: '',
      hoat_dong: true
    });
    setEditingCoupon(null);
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(value);
  };

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return 'Không giới hạn';
    return new Date(dateStr).toLocaleDateString('vi-VN');
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-24 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold">Quản lý mã giảm giá</h1>
        <button
          onClick={() => {
            resetForm();
            setShowModal(true);
          }}
          className="btn-primary flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Tạo mã mới
        </button>
      </div>

      {/* Coupons List */}
      <div className="space-y-4">
        {coupons.length === 0 ? (
          <div className="card p-8 text-center text-gray-500">
            Chưa có mã giảm giá nào
          </div>
        ) : (
          coupons.map((coupon) => (
            <div key={coupon.id} className="card p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-2xl font-bold text-primary">{coupon.ma_code}</span>
                    <span className={`px-3 py-1 rounded-full text-sm ${
                      coupon.hoat_dong ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                    }`}>
                      {coupon.hoat_dong ? 'Hoạt động' : 'Tạm dừng'}
                    </span>
                  </div>
                  
                  {coupon.mo_ta && (
                    <p className="text-gray-600 mb-3">{coupon.mo_ta}</p>
                  )}
                  
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <span className="text-gray-500">Giảm giá:</span>
                      <div className="font-semibold flex items-center gap-1">
                        {coupon.loai_giam === 'percent' ? (
                          <>
                            <Percent className="w-4 h-4" />
                            {coupon.gia_tri_giam}%
                          </>
                        ) : (
                          <>
                            <DollarSign className="w-4 h-4" />
                            {formatCurrency(coupon.gia_tri_giam)}
                          </>
                        )}
                      </div>
                    </div>
                    
                    <div>
                      <span className="text-gray-500">Đơn tối thiểu:</span>
                      <div className="font-semibold">{formatCurrency(coupon.gia_tri_don_toi_thieu)}</div>
                    </div>
                    
                    <div>
                      <span className="text-gray-500">Số lượng:</span>
                      <div className="font-semibold">
                        {coupon.da_su_dung}/{coupon.so_luong}
                      </div>
                    </div>
                    
                    <div>
                      <span className="text-gray-500">Thời hạn:</span>
                      <div className="font-semibold text-xs">
                        {formatDate(coupon.ngay_bat_dau)} - {formatDate(coupon.ngay_ket_thuc)}
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="flex gap-2 ml-4">
                  <button
                    onClick={() => handleEdit(coupon)}
                    className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                    title="Chỉnh sửa"
                  >
                    <Edit2 className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => handleDelete(coupon.id)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Xóa"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold">
                  {editingCoupon ? 'Chỉnh sửa mã giảm giá' : 'Tạo mã giảm giá mới'}
                </h2>
                <button
                  onClick={() => {
                    setShowModal(false);
                    resetForm();
                  }}
                  className="p-2 hover:bg-gray-100 rounded-lg"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">
                    Mã code <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.ma_code}
                    onChange={(e) => setFormData({ ...formData, ma_code: e.target.value.toUpperCase() })}
                    className="input"
                    placeholder="VD: SUMMER2024"
                    required
                    minLength={3}
                    maxLength={50}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Mô tả</label>
                  <textarea
                    value={formData.mo_ta}
                    onChange={(e) => setFormData({ ...formData, mo_ta: e.target.value })}
                    className="input"
                    rows={2}
                    placeholder="Mô tả về mã giảm giá"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Loại giảm giá <span className="text-red-500">*</span>
                    </label>
                    <select
                      value={formData.loai_giam}
                      onChange={(e) => setFormData({ ...formData, loai_giam: e.target.value as 'percent' | 'fixed' })}
                      className="input"
                      required
                    >
                      <option value="percent">Phần trăm (%)</option>
                      <option value="fixed">Số tiền cố định (VNĐ)</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Giá trị giảm <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="number"
                      value={formData.gia_tri_giam}
                      onChange={(e) => setFormData({ ...formData, gia_tri_giam: e.target.value })}
                      className="input"
                      placeholder={formData.loai_giam === 'percent' ? '10' : '50000'}
                      required
                      min="0"
                      step={formData.loai_giam === 'percent' ? '1' : '1000'}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Giá trị đơn tối thiểu</label>
                    <input
                      type="number"
                      value={formData.gia_tri_don_toi_thieu}
                      onChange={(e) => setFormData({ ...formData, gia_tri_don_toi_thieu: e.target.value })}
                      className="input"
                      placeholder="0"
                      min="0"
                      step="1000"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Số lượng <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="number"
                      value={formData.so_luong}
                      onChange={(e) => setFormData({ ...formData, so_luong: e.target.value })}
                      className="input"
                      placeholder="1"
                      required
                      min="1"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Ngày bắt đầu</label>
                    <input
                      type="date"
                      value={formData.ngay_bat_dau}
                      onChange={(e) => setFormData({ ...formData, ngay_bat_dau: e.target.value })}
                      className="input"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">Ngày kết thúc</label>
                    <input
                      type="date"
                      value={formData.ngay_ket_thuc}
                      onChange={(e) => setFormData({ ...formData, ngay_ket_thuc: e.target.value })}
                      className="input"
                    />
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    id="hoat_dong"
                    checked={formData.hoat_dong}
                    onChange={(e) => setFormData({ ...formData, hoat_dong: e.target.checked })}
                    className="w-4 h-4"
                  />
                  <label htmlFor="hoat_dong" className="text-sm font-medium">
                    Kích hoạt mã giảm giá
                  </label>
                </div>

                <div className="flex gap-3 pt-4">
                  <button type="submit" className="btn-primary flex-1">
                    {editingCoupon ? 'Cập nhật' : 'Tạo mã'}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setShowModal(false);
                      resetForm();
                    }}
                    className="btn-secondary flex-1"
                  >
                    Hủy
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Plus, Edit2, Trash2, FolderOpen } from 'lucide-react';
import toast from 'react-hot-toast';

interface Category {
  id: number;
  ten: string;
}

export default function AdminCategoriesPage() {
  const router = useRouter();
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingCategory, setEditingCategory] = useState<Category | null>(null);
  const [formData, setFormData] = useState({ ten: '' });

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
      if (user.vai_tro !== 'admin') {
        toast.error('Bạn không có quyền truy cập!');
        router.push('/');
        return;
      }
      
      fetchCategories();
    } catch (error) {
      console.error('Error parsing user data:', error);
      toast.error('Lỗi xác thực');
      router.push('/auth/login');
    }
  }, [router]);

  const fetchCategories = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/danh-muc');
      const data = await response.json();
      setCategories(data);
    } catch (error) {
      console.error('Error fetching categories:', error);
      toast.error('Không thể tải danh sách danh mục');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.ten.trim()) {
      toast.error('Vui lòng nhập tên danh mục');
      return;
    }

    try {
      const url = editingCategory
        ? `http://localhost:8000/api/danh-muc/${editingCategory.id}`
        : 'http://localhost:8000/api/danh-muc';
      
      const method = editingCategory ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to save category');
      }

      toast.success(editingCategory ? 'Cập nhật danh mục thành công' : 'Thêm danh mục thành công');
      setShowModal(false);
      setEditingCategory(null);
      setFormData({ ten: '' });
      fetchCategories();
    } catch (error) {
      console.error('Error saving category:', error);
      toast.error('Lưu danh mục thất bại');
    }
  };

  const handleEdit = (category: Category) => {
    setEditingCategory(category);
    setFormData({ ten: category.ten });
    setShowModal(true);
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Bạn có chắc muốn xóa danh mục này?')) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/danh-muc/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete category');
      }

      toast.success('Xóa danh mục thành công');
      fetchCategories();
    } catch (error) {
      console.error('Error deleting category:', error);
      toast.error('Xóa danh mục thất bại');
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingCategory(null);
    setFormData({ ten: '' });
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
            <h1 className="text-3xl font-bold">Quản lý danh mục</h1>
            <p className="text-gray-600 mt-1">Quản lý danh mục sản phẩm</p>
          </div>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="btn-primary flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>Thêm danh mục</span>
        </button>
      </div>

      {/* Categories List */}
      {categories.length === 0 ? (
        <div className="card p-12 text-center">
          <FolderOpen className="w-24 h-24 text-gray-300 mx-auto mb-6" />
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Chưa có danh mục nào
          </h2>
          <button
            onClick={() => setShowModal(true)}
            className="btn-primary inline-flex items-center space-x-2"
          >
            <Plus className="w-5 h-5" />
            <span>Thêm danh mục đầu tiên</span>
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {categories.map((category) => (
            <div key={category.id} className="card p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {category.ten}
                  </h3>
                  <p className="text-sm text-gray-600">ID: {category.id}</p>
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleEdit(category)}
                    className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                    title="Sửa"
                  >
                    <Edit2 className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => handleDelete(category.id)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Xóa"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h2 className="text-2xl font-bold mb-4">
              {editingCategory ? 'Sửa danh mục' : 'Thêm danh mục mới'}
            </h2>
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Tên danh mục
                </label>
                <input
                  type="text"
                  value={formData.ten}
                  onChange={(e) => setFormData({ ten: e.target.value })}
                  className="input"
                  placeholder="Nhập tên danh mục"
                  required
                />
              </div>
              <div className="flex space-x-3">
                <button type="submit" className="btn-primary flex-1">
                  {editingCategory ? 'Cập nhật' : 'Thêm'}
                </button>
                <button
                  type="button"
                  onClick={handleCloseModal}
                  className="btn-secondary flex-1"
                >
                  Hủy
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

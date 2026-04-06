'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { ArrowLeft, Search, Users, Shield, User, Mail, Calendar } from 'lucide-react';
import Link from 'next/link';

interface UserData {
  id: number;
  email: string;
  ho_ten: string;
  vai_tro: 'admin' | 'manager' | 'user';
  ngay_tao: string;
}

export default function AdminUsersPage() {
  const router = useRouter();
  const [users, setUsers] = useState<UserData[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRole, setFilterRole] = useState<string>('all');

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
      
      fetchUsers();
    } catch (error) {
      toast.error('Lỗi xác thực');
      router.push('/auth/login');
    }
  }, [router]);

  const fetchUsers = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/nguoi-dung');
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
      toast.error('Không thể tải danh sách người dùng');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateRole = async (userId: number, newRole: 'admin' | 'manager' | 'user') => {
    // Lấy thông tin user hiện tại
    const currentUser = users.find(u => u.id === userId);
    
    // Không cho phép thay đổi vai trò của Admin
    if (currentUser?.vai_tro === 'admin') {
      toast.error('Không thể thay đổi vai trò của Quản trị viên!');
      return;
    }
    
    if (!confirm(`Bạn có chắc muốn đổi vai trò người dùng này thành ${
      newRole === 'admin' ? 'Quản trị viên' : 
      newRole === 'manager' ? 'Quản lý' : 'Người dùng'
    }?`)) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/nguoi-dung/${userId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vai_tro: newRole }),
      });

      if (!response.ok) throw new Error('Failed to update role');

      toast.success('Cập nhật vai trò thành công');
      fetchUsers();
    } catch (error) {
      toast.error('Lỗi khi cập nhật vai trò');
    }
  };

  const handleDeleteUser = async (userId: number) => {
    // Lấy thông tin user
    const user = users.find(u => u.id === userId);
    
    // Không cho phép xóa Admin
    if (user?.vai_tro === 'admin') {
      toast.error('Không thể xóa tài khoản Quản trị viên!');
      return;
    }
    
    if (!confirm('Bạn có chắc muốn xóa người dùng này?')) return;

    try {
      const response = await fetch(`http://localhost:8000/api/nguoi-dung/${userId}`, {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error('Failed to delete');

      toast.success('Xóa người dùng thành công');
      fetchUsers();
    } catch (error) {
      toast.error('Lỗi khi xóa người dùng');
    }
  };

  const filteredUsers = users.filter(user => {
    const matchesSearch = 
      user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.ho_ten.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesRole = filterRole === 'all' || user.vai_tro === filterRole;
    
    return matchesSearch && matchesRole;
  });

  const stats = {
    total: users.length,
    admins: users.filter(u => u.vai_tro === 'admin').length,
    managers: users.filter(u => u.vai_tro === 'manager').length,
    users: users.filter(u => u.vai_tro === 'user').length,
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
            <h1 className="text-3xl font-bold">Quản lý người dùng</h1>
            <p className="text-gray-600 mt-1">{users.length} người dùng</p>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="card p-4 border-l-4 border-blue-500">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-gray-600 mb-1">Tổng người dùng</div>
              <div className="text-2xl font-bold">{stats.total}</div>
            </div>
            <Users className="w-10 h-10 text-blue-500" />
          </div>
        </div>
        <div className="card p-4 border-l-4 border-purple-500">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-gray-600 mb-1">Quản trị viên</div>
              <div className="text-2xl font-bold text-purple-600">{stats.admins}</div>
            </div>
            <Shield className="w-10 h-10 text-purple-500" />
          </div>
        </div>
        <div className="card p-4 border-l-4 border-orange-500">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-gray-600 mb-1">Quản lý</div>
              <div className="text-2xl font-bold text-orange-600">{stats.managers}</div>
            </div>
            <Shield className="w-10 h-10 text-orange-500" />
          </div>
        </div>
        <div className="card p-4 border-l-4 border-green-500">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-gray-600 mb-1">Người dùng</div>
              <div className="text-2xl font-bold text-green-600">{stats.users}</div>
            </div>
            <User className="w-10 h-10 text-green-500" />
          </div>
        </div>
      </div>

      {/* Search & Filter */}
      <div className="card p-4 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Tìm kiếm theo email hoặc tên..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>
          <select
            value={filterRole}
            onChange={(e) => setFilterRole(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
          >
            <option value="all">Tất cả vai trò</option>
            <option value="admin">Quản trị viên</option>
            <option value="manager">Quản lý</option>
            <option value="user">Người dùng</option>
          </select>
        </div>
      </div>

      {/* Users Table */}
      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Họ tên</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vai trò</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ngày tạo</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Thao tác</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {filteredUsers.map((user) => (
                <tr key={user.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm text-gray-900">#{user.id}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-gradient-to-br from-primary to-primary-dark rounded-full flex items-center justify-center text-white font-bold">
                        {user.ho_ten.charAt(0).toUpperCase()}
                      </div>
                      <div className="text-sm font-medium text-gray-900">{user.ho_ten}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-2 text-sm text-gray-900">
                      <Mail className="w-4 h-4 text-gray-400" />
                      <span>{user.email}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      user.vai_tro === 'admin'
                        ? 'bg-purple-100 text-purple-800'
                        : user.vai_tro === 'manager'
                        ? 'bg-orange-100 text-orange-800'
                        : 'bg-green-100 text-green-800'
                    }`}>
                      {user.vai_tro === 'admin' ? 'Quản trị viên' : 
                       user.vai_tro === 'manager' ? 'Quản lý' : 'Người dùng'}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-2 text-sm text-gray-500">
                      <Calendar className="w-4 h-4" />
                      <span>{new Date(user.ngay_tao).toLocaleDateString('vi-VN')}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex items-center justify-end space-x-2">
                      {user.vai_tro === 'admin' ? (
                        // Admin không thể thay đổi vai trò
                        <span className="px-3 py-1 text-xs bg-gray-100 text-gray-500 rounded cursor-not-allowed">
                          Không thể thay đổi
                        </span>
                      ) : (
                        <select
                          value={user.vai_tro}
                          onChange={(e) => handleUpdateRole(user.id, e.target.value as 'admin' | 'manager' | 'user')}
                          className="px-3 py-1 text-xs border border-gray-300 rounded focus:ring-2 focus:ring-primary"
                        >
                          <option value="admin">Quản trị viên</option>
                          <option value="manager">Quản lý</option>
                          <option value="user">Người dùng</option>
                        </select>
                      )}
                      
                      {user.vai_tro === 'admin' ? (
                        // Admin không thể xóa
                        <button
                          disabled
                          className="px-3 py-1 text-xs bg-gray-200 text-gray-400 rounded cursor-not-allowed"
                          title="Không thể xóa Quản trị viên"
                        >
                          Xóa
                        </button>
                      ) : (
                        <button
                          onClick={() => handleDeleteUser(user.id)}
                          className="px-3 py-1 text-xs bg-red-500 text-white rounded hover:bg-red-600"
                        >
                          Xóa
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredUsers.length === 0 && (
          <div className="text-center py-12">
            <Users className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-600">Không tìm thấy người dùng nào</p>
          </div>
        )}
      </div>
    </div>
  );
}

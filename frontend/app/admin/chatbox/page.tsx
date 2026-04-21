'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface ChatMessage {
  id: number;
  user: {
    id: number | null;
    name: string;
    email: string;
  };
  message: string;
  response: string;
  created_at: string;
}

interface ChatStats {
  total_messages: number;
  unique_users: number;
  guest_messages: number;
  recent_messages_7days: number;
  top_users: Array<{
    id: number;
    name: string;
    email: string;
    message_count: number;
  }>;
  messages_by_day: Array<{
    date: string;
    count: number;
  }>;
}

interface ChatConfig {
  ai_provider: string;
  openai_configured: boolean;
  gemini_configured: boolean;
  openai_key_preview: string;
  gemini_key_preview: string;
}

export default function ChatboxManagement() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<'stats' | 'history' | 'config'>('stats');
  
  // Stats
  const [stats, setStats] = useState<ChatStats | null>(null);
  const [loadingStats, setLoadingStats] = useState(true);
  
  // History
  const [history, setHistory] = useState<ChatMessage[]>([]);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [totalMessages, setTotalMessages] = useState(0);
  const [page, setPage] = useState(0);
  const [limit] = useState(20);
  
  // Config
  const [config, setConfig] = useState<ChatConfig | null>(null);
  const [loadingConfig, setLoadingConfig] = useState(false);
  
  // Selected message for detail view
  const [selectedMessage, setSelectedMessage] = useState<ChatMessage | null>(null);

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    if (!token || !user) {
      router.push('/auth/login');
      return;
    }
    
    const userData = JSON.parse(user);
    if (userData.vai_tro !== 'admin') {
      alert('Bạn không có quyền truy cập trang này!');
      router.push('/');
      return;
    }
    
    fetchStats();
  }, [router]);

  const fetchStats = async () => {
    setLoadingStats(true);
    try {
      const response = await fetch('http://localhost:8000/admin/chatbox/stats');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoadingStats(false);
    }
  };

  const fetchHistory = async (pageNum: number = 0) => {
    setLoadingHistory(true);
    try {
      const skip = pageNum * limit;
      const response = await fetch(
        `http://localhost:8000/admin/chatbox/history?skip=${skip}&limit=${limit}`
      );
      const data = await response.json();
      setHistory(data.data);
      setTotalMessages(data.total);
      setPage(pageNum);
    } catch (error) {
      console.error('Error fetching history:', error);
    } finally {
      setLoadingHistory(false);
    }
  };

  const fetchConfig = async () => {
    setLoadingConfig(true);
    try {
      const response = await fetch('http://localhost:8000/admin/chatbox/config');
      const data = await response.json();
      setConfig(data.config);
    } catch (error) {
      console.error('Error fetching config:', error);
    } finally {
      setLoadingConfig(false);
    }
  };

  const handleClearHistory = async () => {
    if (!confirm('Bạn có chắc muốn xóa TOÀN BỘ lịch sử chat? Hành động này không thể hoàn tác!')) {
      return;
    }
    
    try {
      const response = await fetch('http://localhost:8000/admin/chatbox/clear', {
        method: 'DELETE',
      });
      const data = await response.json();
      alert(data.message);
      fetchStats();
      if (activeTab === 'history') {
        fetchHistory(0);
      }
    } catch (error) {
      console.error('Error clearing history:', error);
      alert('Có lỗi xảy ra khi xóa lịch sử chat');
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('vi-VN');
  };

  const totalPages = Math.ceil(totalMessages / limit);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Quản Lý Chatbox AI</h1>
          <p className="text-gray-600">Quản lý cấu hình và lịch sử chat với AI</p>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow mb-6">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              <button
                onClick={() => {
                  setActiveTab('stats');
                  fetchStats();
                }}
                className={`px-6 py-4 text-sm font-medium border-b-2 ${
                  activeTab === 'stats'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                📊 Thống Kê
              </button>
              <button
                onClick={() => {
                  setActiveTab('history');
                  fetchHistory(0);
                }}
                className={`px-6 py-4 text-sm font-medium border-b-2 ${
                  activeTab === 'history'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                💬 Lịch Sử Chat
              </button>
              <button
                onClick={() => {
                  setActiveTab('config');
                  fetchConfig();
                }}
                className={`px-6 py-4 text-sm font-medium border-b-2 ${
                  activeTab === 'config'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                ⚙️ Cấu Hình
              </button>
            </nav>
          </div>
        </div>

        {/* Stats Tab */}
        {activeTab === 'stats' && (
          <div>
            {loadingStats ? (
              <div className="text-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">Đang tải thống kê...</p>
              </div>
            ) : stats ? (
              <div className="space-y-6">
                {/* Overview Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                  <div className="bg-white p-6 rounded-lg shadow">
                    <div className="text-sm text-gray-600 mb-1">Tổng Tin Nhắn</div>
                    <div className="text-3xl font-bold text-blue-600">{stats.total_messages}</div>
                  </div>
                  <div className="bg-white p-6 rounded-lg shadow">
                    <div className="text-sm text-gray-600 mb-1">Người Dùng</div>
                    <div className="text-3xl font-bold text-green-600">{stats.unique_users}</div>
                  </div>
                  <div className="bg-white p-6 rounded-lg shadow">
                    <div className="text-sm text-gray-600 mb-1">Tin Nhắn Khách</div>
                    <div className="text-3xl font-bold text-purple-600">{stats.guest_messages}</div>
                  </div>
                  <div className="bg-white p-6 rounded-lg shadow">
                    <div className="text-sm text-gray-600 mb-1">7 Ngày Gần Đây</div>
                    <div className="text-3xl font-bold text-orange-600">{stats.recent_messages_7days}</div>
                  </div>
                </div>

                {/* Top Users */}
                <div className="bg-white p-6 rounded-lg shadow">
                  <h2 className="text-xl font-bold mb-4">Top Người Dùng Chat Nhiều Nhất</h2>
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tên</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Số Tin Nhắn</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {stats.top_users.map((user, index) => (
                          <tr key={user.id}>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="flex items-center">
                                <div className="flex-shrink-0 h-8 w-8 bg-blue-100 rounded-full flex items-center justify-center">
                                  <span className="text-blue-600 font-bold">{index + 1}</span>
                                </div>
                                <div className="ml-4">
                                  <div className="text-sm font-medium text-gray-900">{user.name}</div>
                                </div>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{user.email}</td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className="px-3 py-1 inline-flex text-sm leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                {user.message_count} tin nhắn
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* Messages by Day */}
                <div className="bg-white p-6 rounded-lg shadow">
                  <h2 className="text-xl font-bold mb-4">Tin Nhắn Theo Ngày (7 Ngày Gần Đây)</h2>
                  <div className="space-y-2">
                    {stats.messages_by_day.map((day) => (
                      <div key={day.date} className="flex items-center">
                        <div className="w-32 text-sm text-gray-600">{day.date}</div>
                        <div className="flex-1">
                          <div className="bg-blue-200 h-8 rounded" style={{ width: `${(day.count / Math.max(...stats.messages_by_day.map(d => d.count))) * 100}%` }}>
                            <div className="px-3 py-1 text-sm font-medium text-blue-900">{day.count} tin nhắn</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : null}
          </div>
        )}

        {/* History Tab */}
        {activeTab === 'history' && (
          <div>
            <div className="bg-white rounded-lg shadow mb-6 p-4 flex justify-between items-center">
              <div className="text-sm text-gray-600">
                Tổng: <span className="font-bold">{totalMessages}</span> tin nhắn
              </div>
              <button
                onClick={handleClearHistory}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
              >
                🗑️ Xóa Toàn Bộ Lịch Sử
              </button>
            </div>

            {loadingHistory ? (
              <div className="text-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">Đang tải lịch sử...</p>
              </div>
            ) : (
              <>
                <div className="bg-white rounded-lg shadow overflow-hidden">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Người Dùng</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tin Nhắn</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Phản Hồi</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Thời Gian</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Hành Động</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {history.map((msg) => (
                        <tr key={msg.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-medium text-gray-900">{msg.user.name}</div>
                            <div className="text-sm text-gray-500">{msg.user.email}</div>
                          </td>
                          <td className="px-6 py-4">
                            <div className="text-sm text-gray-900 max-w-xs truncate">{msg.message}</div>
                          </td>
                          <td className="px-6 py-4">
                            <div className="text-sm text-gray-500 max-w-xs truncate">{msg.response || 'Chưa có phản hồi'}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {formatDate(msg.created_at)}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm">
                            <button
                              onClick={() => setSelectedMessage(msg)}
                              className="text-blue-600 hover:text-blue-900"
                            >
                              Xem Chi Tiết
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* Pagination */}
                {totalPages > 1 && (
                  <div className="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6 mt-4 rounded-lg shadow">
                    <div className="flex-1 flex justify-between sm:hidden">
                      <button
                        onClick={() => fetchHistory(page - 1)}
                        disabled={page === 0}
                        className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
                      >
                        Trước
                      </button>
                      <button
                        onClick={() => fetchHistory(page + 1)}
                        disabled={page >= totalPages - 1}
                        className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
                      >
                        Sau
                      </button>
                    </div>
                    <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
                      <div>
                        <p className="text-sm text-gray-700">
                          Hiển thị <span className="font-medium">{page * limit + 1}</span> đến{' '}
                          <span className="font-medium">{Math.min((page + 1) * limit, totalMessages)}</span> trong{' '}
                          <span className="font-medium">{totalMessages}</span> kết quả
                        </p>
                      </div>
                      <div>
                        <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                          <button
                            onClick={() => fetchHistory(page - 1)}
                            disabled={page === 0}
                            className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                          >
                            ‹
                          </button>
                          {[...Array(totalPages)].map((_, i) => (
                            <button
                              key={i}
                              onClick={() => fetchHistory(i)}
                              className={`relative inline-flex items-center px-4 py-2 border text-sm font-medium ${
                                i === page
                                  ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                                  : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                              }`}
                            >
                              {i + 1}
                            </button>
                          ))}
                          <button
                            onClick={() => fetchHistory(page + 1)}
                            disabled={page >= totalPages - 1}
                            className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                          >
                            ›
                          </button>
                        </nav>
                      </div>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {/* Config Tab */}
        {activeTab === 'config' && (
          <div>
            {loadingConfig ? (
              <div className="text-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">Đang tải cấu hình...</p>
              </div>
            ) : config ? (
              <div className="space-y-6">
                <div className="bg-white p-6 rounded-lg shadow">
                  <h2 className="text-xl font-bold mb-4">Cấu Hình AI Provider</h2>
                  
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        AI Provider Hiện Tại
                      </label>
                      <div className="flex items-center space-x-4">
                        <span className={`px-4 py-2 rounded-lg font-medium ${
                          config.ai_provider === 'openai' 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          OpenAI {config.ai_provider === 'openai' && '✓'}
                        </span>
                        <span className={`px-4 py-2 rounded-lg font-medium ${
                          config.ai_provider === 'gemini' 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          Google Gemini {config.ai_provider === 'gemini' && '✓'}
                        </span>
                      </div>
                    </div>

                    <div className="border-t pt-4">
                      <h3 className="text-lg font-medium mb-3">Trạng Thái API Keys</h3>
                      
                      <div className="space-y-3">
                        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                          <div>
                            <div className="font-medium">OpenAI API Key</div>
                            <div className="text-sm text-gray-600">{config.openai_key_preview}</div>
                          </div>
                          <div>
                            {config.openai_configured ? (
                              <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                                ✓ Đã cấu hình
                              </span>
                            ) : (
                              <span className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium">
                                ✗ Chưa cấu hình
                              </span>
                            )}
                          </div>
                        </div>

                        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                          <div>
                            <div className="font-medium">Google Gemini API Key</div>
                            <div className="text-sm text-gray-600">{config.gemini_key_preview}</div>
                          </div>
                          <div>
                            {config.gemini_configured ? (
                              <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                                ✓ Đã cấu hình
                              </span>
                            ) : (
                              <span className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium">
                                ✗ Chưa cấu hình
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="border-t pt-4">
                      <h3 className="text-lg font-medium mb-3">Hướng Dẫn Cấu Hình</h3>
                      <div className="bg-blue-50 p-4 rounded-lg">
                        <p className="text-sm text-blue-900 mb-2">
                          Để thay đổi cấu hình AI, cập nhật file <code className="bg-blue-100 px-2 py-1 rounded">.env</code> trong thư mục gốc:
                        </p>
                        <pre className="bg-blue-100 p-3 rounded text-sm overflow-x-auto">
{`# Chọn provider: openai hoặc gemini
AI_PROVIDER=openai

# OpenAI API Key
OPENAI_API_KEY=sk-your-key-here

# Google Gemini API Key  
GEMINI_API_KEY=your-gemini-key-here`}
                        </pre>
                        <p className="text-sm text-blue-900 mt-2">
                          Sau khi cập nhật, khởi động lại backend để áp dụng thay đổi.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ) : null}
          </div>
        )}

        {/* Message Detail Modal */}
        {selectedMessage && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-2xl w-full max-h-[80vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-xl font-bold">Chi Tiết Tin Nhắn</h3>
                  <button
                    onClick={() => setSelectedMessage(null)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    ✕
                  </button>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <div className="text-sm font-medium text-gray-500 mb-1">Người dùng</div>
                    <div className="text-gray-900">{selectedMessage.user.name}</div>
                    <div className="text-sm text-gray-500">{selectedMessage.user.email}</div>
                  </div>
                  
                  <div>
                    <div className="text-sm font-medium text-gray-500 mb-1">Thời gian</div>
                    <div className="text-gray-900">{formatDate(selectedMessage.created_at)}</div>
                  </div>
                  
                  <div>
                    <div className="text-sm font-medium text-gray-500 mb-1">Tin nhắn</div>
                    <div className="bg-blue-50 p-4 rounded-lg text-gray-900 whitespace-pre-wrap">
                      {selectedMessage.message}
                    </div>
                  </div>
                  
                  <div>
                    <div className="text-sm font-medium text-gray-500 mb-1">Phản hồi từ AI</div>
                    <div className="bg-gray-50 p-4 rounded-lg text-gray-900 whitespace-pre-wrap">
                      {selectedMessage.response || 'Chưa có phản hồi'}
                    </div>
                  </div>
                </div>
                
                <div className="mt-6 flex justify-end">
                  <button
                    onClick={() => setSelectedMessage(null)}
                    className="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300"
                  >
                    Đóng
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

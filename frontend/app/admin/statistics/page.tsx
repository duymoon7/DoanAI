'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  ShoppingCart, 
  Package, 
  Users,
  Calendar,
  Download,
  RefreshCw
} from 'lucide-react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart
} from 'recharts';

interface RevenueData {
  current_month: number;
  previous_month: number;
  change_percent: number;
  month: number;
  year: number;
}

interface OrderStatusData {
  status: string;
  count: number;
  label: string;
}

interface TopProduct {
  id: number;
  name: string;
  price: number;
  image: string;
  total_sold: number;
  total_revenue: number;
}

interface DashboardStats {
  revenue: RevenueData;
  orders: {
    completed_count: number;
    total_count: number;
  };
  order_status_chart: OrderStatusData[];
  top_selling_products: TopProduct[];
  summary: {
    total_products: number;
    total_users: number;
    total_orders: number;
  };
}

interface MonthlyRevenue {
  year: number;
  month: number;
  revenue: number;
  order_count: number;
  month_name: string;
}

interface RevenueStats {
  total_revenue: number;
  average_order_value: number;
  total_discount: number;
  by_status: any[];
  monthly_revenue: MonthlyRevenue[];
}

// Colors for charts
const COLORS = {
  pending: '#FCD34D',
  completed: '#10B981',
  cancelled: '#EF4444',
  primary: '#3B82F6',
  secondary: '#8B5CF6',
  accent: '#F59E0B'
};

const PIE_COLORS = ['#10B981', '#FCD34D', '#EF4444', '#3B82F6', '#8B5CF6'];

export default function StatisticsPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [revenueStats, setRevenueStats] = useState<RevenueStats | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    // Check authentication
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
      
      fetchStatistics();
    } catch (error) {
      console.error('Error:', error);
      toast.error('Lỗi xác thực');
      router.push('/auth/login');
    }
  }, [router]);

  const fetchStatistics = async () => {
    try {
      const token = localStorage.getItem('token');
      
      // Fetch dashboard stats
      const dashboardResponse = await fetch('http://localhost:8000/api/statistics/dashboard', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!dashboardResponse.ok) {
        throw new Error('Failed to fetch dashboard statistics');
      }

      const dashboardData = await dashboardResponse.json();
      setStats(dashboardData);

      // Fetch revenue stats for charts
      const revenueResponse = await fetch('http://localhost:8000/api/statistics/revenue', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (revenueResponse.ok) {
        const revenueData = await revenueResponse.json();
        setRevenueStats(revenueData);
      }
    } catch (error) {
      console.error('Error fetching statistics:', error);
      toast.error('Không thể tải thống kê');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    setRefreshing(true);
    fetchStatistics();
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(amount);
  };

  const getMonthName = (month: number) => {
    const months = [
      'Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6',
      'Tháng 7', 'Tháng 8', 'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12'
    ];
    return months[month - 1];
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  // Custom tooltip for charts
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 rounded-lg shadow-lg border border-gray-200">
          <p className="font-semibold text-gray-800 mb-2">{label}</p>
          {payload.map((entry: any, index: number) => {
            const entryName = String(entry.name || entry.dataKey || '');
            const shouldFormatCurrency = 
              entryName.toLowerCase().includes('doanh thu') || 
              entryName.toLowerCase().includes('revenue') ||
              entryName === 'total_revenue';
            
            return (
              <p key={index} className="text-sm" style={{ color: entry.color }}>
                {entry.name || entry.dataKey}: {shouldFormatCurrency
                  ? formatCurrency(entry.value) 
                  : entry.value}
              </p>
            );
          })}
        </div>
      );
    }
    return null;
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-8"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-32 bg-gray-200 rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center text-gray-600">
          Không có dữ liệu thống kê
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold mb-2">Báo cáo thống kê</h1>
          <p className="text-gray-600">Tổng quan kinh doanh và hiệu suất</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={handleRefresh}
            disabled={refreshing}
            className="btn btn-secondary flex items-center gap-2"
          >
            <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
            Làm mới
          </button>
          <button
            onClick={() => toast.success('Tính năng export đang phát triển')}
            className="btn btn-primary flex items-center gap-2"
          >
            <Download className="w-4 h-4" />
            Export PDF
          </button>
        </div>
      </div>

      {/* Revenue Card - Doanh thu tháng hiện tại */}
      <div className="card p-6 mb-6 bg-gradient-to-br from-blue-500 to-blue-600 text-white">
        <div className="flex items-center justify-between mb-4">
          <div>
            <p className="text-blue-100 text-sm mb-1">Doanh thu {getMonthName(stats.revenue.month)}</p>
            <p className="text-4xl font-bold">{formatCurrency(stats.revenue.current_month)}</p>
          </div>
          <DollarSign className="w-16 h-16 text-blue-200" />
        </div>
        
        <div className="flex items-center gap-2 text-sm">
          {stats.revenue.change_percent >= 0 ? (
            <>
              <TrendingUp className="w-4 h-4" />
              <span>+{stats.revenue.change_percent.toFixed(2)}%</span>
            </>
          ) : (
            <>
              <TrendingDown className="w-4 h-4" />
              <span>{stats.revenue.change_percent.toFixed(2)}%</span>
            </>
          )}
          <span className="text-blue-100">so với tháng trước</span>
        </div>
        
        <div className="mt-4 pt-4 border-t border-blue-400">
          <p className="text-blue-100 text-sm">
            Tháng trước: {formatCurrency(stats.revenue.previous_month)}
          </p>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm mb-1">Đơn hàng hoàn thành</p>
              <p className="text-3xl font-bold">{stats.orders.completed_count}</p>
            </div>
            <ShoppingCart className="w-12 h-12 text-green-500" />
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm mb-1">Tổng đơn hàng</p>
              <p className="text-3xl font-bold">{stats.summary.total_orders}</p>
            </div>
            <Calendar className="w-12 h-12 text-blue-500" />
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm mb-1">Sản phẩm</p>
              <p className="text-3xl font-bold">{stats.summary.total_products}</p>
            </div>
            <Package className="w-12 h-12 text-purple-500" />
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm mb-1">Khách hàng</p>
              <p className="text-3xl font-bold">{stats.summary.total_users}</p>
            </div>
            <Users className="w-12 h-12 text-yellow-500" />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Pie Chart - Order Status */}
        <div className="card p-6">
          <h2 className="text-xl font-semibold mb-4">Trạng thái đơn hàng</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={stats.order_status_chart}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ label, percent }) => `${label}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="count"
              >
                {stats.order_status_chart.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={COLORS[entry.status as keyof typeof COLORS] || PIE_COLORS[index % PIE_COLORS.length]} 
                  />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
          
          {/* Status breakdown */}
          <div className="mt-4 space-y-2">
            {stats.order_status_chart.map((item) => {
              const percentage = (item.count / stats.summary.total_orders) * 100;
              return (
                <div key={item.status} className="flex items-center justify-between text-sm">
                  <span className={`px-3 py-1 rounded-full font-medium ${getStatusColor(item.status)}`}>
                    {item.label}
                  </span>
                  <span className="text-gray-600">
                    {item.count} đơn ({percentage.toFixed(1)}%)
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Quick Stats */}
        <div className="card p-6">
          <h2 className="text-xl font-semibold mb-4">Thống kê nhanh</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gradient-to-r from-green-50 to-green-100 rounded-lg">
              <span className="text-gray-700 font-medium">Tỷ lệ hoàn thành</span>
              <span className="text-2xl font-bold text-green-600">
                {((stats.orders.completed_count / stats.summary.total_orders) * 100).toFixed(1)}%
              </span>
            </div>
            <div className="flex items-center justify-between p-4 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg">
              <span className="text-gray-700 font-medium">Giá trị đơn TB</span>
              <span className="text-2xl font-bold text-blue-600">
                {formatCurrency(stats.revenue.current_month / (stats.orders.completed_count || 1))}
              </span>
            </div>
            <div className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg">
              <span className="text-gray-700 font-medium">Sản phẩm / Đơn</span>
              <span className="text-2xl font-bold text-purple-600">
                {(stats.top_selling_products.reduce((sum, p) => sum + p.total_sold, 0) / (stats.orders.completed_count || 1)).toFixed(1)}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Monthly Revenue Chart */}
      {revenueStats && revenueStats.monthly_revenue && revenueStats.monthly_revenue.length > 0 && (
        <div className="card p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Doanh thu 12 tháng gần nhất</h2>
          <ResponsiveContainer width="100%" height={350}>
            <AreaChart
              data={[...revenueStats.monthly_revenue].reverse()}
              margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
            >
              <defs>
                <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={COLORS.primary} stopOpacity={0.8}/>
                  <stop offset="95%" stopColor={COLORS.primary} stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="month_name" 
                tick={{ fontSize: 12 }}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis 
                tick={{ fontSize: 12 }}
                tickFormatter={(value) => `${(value / 1000000).toFixed(0)}M`}
              />
              <Tooltip content={<CustomTooltip />} />
              <Area 
                type="monotone" 
                dataKey="revenue" 
                stroke={COLORS.primary} 
                fillOpacity={1} 
                fill="url(#colorRevenue)"
                name="Doanh thu"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Top Products Bar Chart */}
      <div className="card p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Top 10 sản phẩm bán chạy (Biểu đồ)</h2>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart
            data={stats.top_selling_products}
            margin={{ top: 20, right: 30, left: 20, bottom: 100 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="name" 
              angle={-45}
              textAnchor="end"
              height={120}
              tick={{ fontSize: 11 }}
              interval={0}
            />
            <YAxis 
              yAxisId="left"
              orientation="left"
              stroke={COLORS.secondary}
              tick={{ fontSize: 12 }}
            />
            <YAxis 
              yAxisId="right"
              orientation="right"
              stroke={COLORS.primary}
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => `${(value / 1000000).toFixed(0)}M`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Bar 
              yAxisId="left"
              dataKey="total_sold" 
              fill={COLORS.secondary}
              name="Số lượng bán"
              radius={[8, 8, 0, 0]}
            />
            <Bar 
              yAxisId="right"
              dataKey="total_revenue" 
              fill={COLORS.primary}
              name="Doanh thu"
              radius={[8, 8, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Top Selling Products */}
      <div className="card p-6">
        <h2 className="text-xl font-semibold mb-4">Top 10 sản phẩm bán chạy</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-3 px-4">STT</th>
                <th className="text-left py-3 px-4">Sản phẩm</th>
                <th className="text-right py-3 px-4">Giá</th>
                <th className="text-right py-3 px-4">Đã bán</th>
                <th className="text-right py-3 px-4">Doanh thu</th>
              </tr>
            </thead>
            <tbody>
              {stats.top_selling_products.map((product, index) => (
                <tr key={product.id} className="border-b hover:bg-gray-50">
                  <td className="py-3 px-4">
                    <span className={`inline-flex items-center justify-center w-8 h-8 rounded-full ${
                      index === 0 ? 'bg-yellow-100 text-yellow-800' :
                      index === 1 ? 'bg-gray-100 text-gray-800' :
                      index === 2 ? 'bg-orange-100 text-orange-800' :
                      'bg-blue-50 text-blue-800'
                    } font-semibold`}>
                      {index + 1}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-3">
                      {product.image && (
                        <img
                          src={product.image}
                          alt={product.name}
                          className="w-12 h-12 object-cover rounded"
                        />
                      )}
                      <span className="font-medium">{product.name}</span>
                    </div>
                  </td>
                  <td className="py-3 px-4 text-right">{formatCurrency(product.price)}</td>
                  <td className="py-3 px-4 text-right">
                    <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                      {product.total_sold}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right font-semibold text-green-600">
                    {formatCurrency(product.total_revenue)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

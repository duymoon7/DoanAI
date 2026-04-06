'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Mail, Lock, Eye, EyeOff } from 'lucide-react';
import toast from 'react-hot-toast';
import { login } from '@/lib/api';

export default function LoginPage() {
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        try {
            // Call login API
            const response = await login({
                email: formData.email,
                mat_khau: formData.password,
            });

            // Save token to localStorage
            localStorage.setItem('token', response.access_token);
            localStorage.setItem('user', JSON.stringify(response.user));

            toast.success(`Chào mừng ${response.user.ho_ten}!`);
            
            // Redirect to home after 1 second using window.location
            setTimeout(() => {
                window.location.href = '/';
            }, 1000);

        } catch (error: any) {
            console.error('Login error:', error);
            
            if (error.response?.data?.detail) {
                toast.error(error.response.data.detail);
            } else if (error.response?.status === 401) {
                toast.error('Email hoặc mật khẩu không đúng!');
            } else {
                toast.error('Đăng nhập thất bại. Vui lòng thử lại!');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gray-50">
            <div className="max-w-md w-full">
                {/* Header */}
                <div className="text-center mb-8">
                    <div className="w-16 h-16 bg-gradient-to-br from-primary to-primary-dark rounded-xl flex items-center justify-center mx-auto mb-4">
                        <span className="text-white font-bold text-2xl">E</span>
                    </div>
                    <h2 className="text-3xl font-bold text-gray-900">Đăng nhập</h2>
                    <p className="text-gray-600 mt-2">
                        Chào mừng bạn quay trở lại!
                    </p>
                </div>

                {/* Form */}
                <div className="card p-8">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {/* Email */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Email
                            </label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                                <input
                                    type="email"
                                    required
                                    value={formData.email}
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    className="input pl-10"
                                    placeholder="your@email.com"
                                    disabled={loading}
                                />
                            </div>
                        </div>

                        {/* Password */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Mật khẩu
                            </label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                                <input
                                    type={showPassword ? 'text' : 'password'}
                                    required
                                    value={formData.password}
                                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                    className="input pl-10 pr-10"
                                    placeholder="••••••••"
                                    disabled={loading}
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                                    disabled={loading}
                                >
                                    {showPassword ? (
                                        <EyeOff className="w-5 h-5" />
                                    ) : (
                                        <Eye className="w-5 h-5" />
                                    )}
                                </button>
                            </div>
                        </div>

                        {/* Remember & Forgot */}
                        <div className="flex items-center justify-between">
                            <label className="flex items-center space-x-2 cursor-pointer">
                                <input
                                    type="checkbox"
                                    className="rounded text-primary focus:ring-primary"
                                    disabled={loading}
                                />
                                <span className="text-sm text-gray-700">Ghi nhớ đăng nhập</span>
                            </label>
                            <Link
                                href="/auth/forgot-password"
                                className="text-sm text-primary hover:text-primary-dark font-medium"
                            >
                                Quên mật khẩu?
                            </Link>
                        </div>

                        {/* Submit */}
                        <button 
                            type="submit" 
                            className="w-full btn-primary"
                            disabled={loading}
                        >
                            {loading ? 'Đang xử lý...' : 'Đăng nhập'}
                        </button>
                    </form>

                    {/* Register Link */}
                    <p className="text-center text-sm text-gray-600 mt-6">
                        Chưa có tài khoản?{' '}
                        <Link
                            href="/auth/register"
                            className="text-primary hover:text-primary-dark font-medium"
                        >
                            Đăng ký ngay
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}

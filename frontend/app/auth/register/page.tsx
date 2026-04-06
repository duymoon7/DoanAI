'use client';

import { useState, useMemo } from 'react';
import Link from 'next/link';
import { Mail, Lock, Eye, EyeOff, User, Check, X } from 'lucide-react';
import toast from 'react-hot-toast';
import { register } from '@/lib/api';

export default function RegisterPage() {
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        confirmPassword: '',
    });

    // Password validation rules
    const passwordValidation = useMemo(() => {
        const password = formData.password;
        return {
            minLength: password.length >= 8,
            hasUppercase: /[A-Z]/.test(password),
            hasNumber: /\d/.test(password),
        };
    }, [formData.password]);

    const isPasswordValid = useMemo(() => {
        return passwordValidation.minLength && 
               passwordValidation.hasUppercase && 
               passwordValidation.hasNumber;
    }, [passwordValidation]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        // Validate password strength
        if (!isPasswordValid) {
            toast.error('Mật khẩu không đủ mạnh! Vui lòng kiểm tra các yêu cầu.');
            return;
        }

        // Validate passwords match
        if (formData.password !== formData.confirmPassword) {
            toast.error('Mật khẩu xác nhận không khớp!');
            return;
        }

        setLoading(true);

        try {
            // Call register API
            await register({
                email: formData.email,
                mat_khau: formData.password,
                ho_ten: formData.name,
            });

            toast.success('Đăng ký thành công! Đang chuyển đến trang đăng nhập...');
            
            // Redirect to login after 1.5 seconds using window.location
            setTimeout(() => {
                window.location.href = '/auth/login';
            }, 1500);

        } catch (error: any) {
            console.error('Register error:', error);
            
            if (error.response?.data?.detail) {
                toast.error(error.response.data.detail);
            } else if (error.response?.status === 400) {
                toast.error('Email đã được sử dụng!');
            } else {
                toast.error('Đăng ký thất bại. Vui lòng thử lại!');
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
                    <h2 className="text-3xl font-bold text-gray-900">Đăng ký</h2>
                    <p className="text-gray-600 mt-2">
                        Tạo tài khoản mới để bắt đầu mua sắm
                    </p>
                </div>

                {/* Form */}
                <div className="card p-8">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {/* Name */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Họ và tên
                            </label>
                            <div className="relative">
                                <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                                <input
                                    type="text"
                                    required
                                    value={formData.name}
                                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                    className="input pl-10"
                                    placeholder="Nguyễn Văn A"
                                    disabled={loading}
                                />
                            </div>
                        </div>

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
                                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                                </button>
                            </div>
                            
                            {/* Password Requirements */}
                            {formData.password && (
                                <div className="mt-3 space-y-2">
                                    <p className="text-xs font-medium text-gray-700">Yêu cầu mật khẩu:</p>
                                    <div className="space-y-1">
                                        <div className="flex items-center space-x-2">
                                            {passwordValidation.minLength ? (
                                                <Check className="w-4 h-4 text-green-500" />
                                            ) : (
                                                <X className="w-4 h-4 text-red-500" />
                                            )}
                                            <span className={`text-xs ${passwordValidation.minLength ? 'text-green-600' : 'text-gray-600'}`}>
                                                Ít nhất 8 ký tự
                                            </span>
                                        </div>
                                        <div className="flex items-center space-x-2">
                                            {passwordValidation.hasUppercase ? (
                                                <Check className="w-4 h-4 text-green-500" />
                                            ) : (
                                                <X className="w-4 h-4 text-red-500" />
                                            )}
                                            <span className={`text-xs ${passwordValidation.hasUppercase ? 'text-green-600' : 'text-gray-600'}`}>
                                                Ít nhất 1 chữ hoa
                                            </span>
                                        </div>
                                        <div className="flex items-center space-x-2">
                                            {passwordValidation.hasNumber ? (
                                                <Check className="w-4 h-4 text-green-500" />
                                            ) : (
                                                <X className="w-4 h-4 text-red-500" />
                                            )}
                                            <span className={`text-xs ${passwordValidation.hasNumber ? 'text-green-600' : 'text-gray-600'}`}>
                                                Ít nhất 1 số
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Confirm Password */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Xác nhận mật khẩu
                            </label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                                <input
                                    type={showConfirmPassword ? 'text' : 'password'}
                                    required
                                    value={formData.confirmPassword}
                                    onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                                    className="input pl-10 pr-10"
                                    placeholder="••••••••"
                                    disabled={loading}
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                                    disabled={loading}
                                >
                                    {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                                </button>
                            </div>
                            {/* Password Match Indicator */}
                            {formData.confirmPassword && (
                                <div className="mt-2 flex items-center space-x-2">
                                    {formData.password === formData.confirmPassword ? (
                                        <>
                                            <Check className="w-4 h-4 text-green-500" />
                                            <span className="text-xs text-green-600">Mật khẩu khớp</span>
                                        </>
                                    ) : (
                                        <>
                                            <X className="w-4 h-4 text-red-500" />
                                            <span className="text-xs text-red-600">Mật khẩu không khớp</span>
                                        </>
                                    )}
                                </div>
                            )}
                        </div>

                        {/* Terms */}
                        <label className="flex items-start space-x-2 cursor-pointer">
                            <input
                                type="checkbox"
                                required
                                className="rounded text-primary focus:ring-primary mt-1"
                                disabled={loading}
                            />
                            <span className="text-sm text-gray-700">
                                Tôi đồng ý với{' '}
                                <Link href="/terms" className="text-primary hover:text-primary-dark">
                                    Điều khoản dịch vụ
                                </Link>{' '}
                                và{' '}
                                <Link href="/privacy" className="text-primary hover:text-primary-dark">
                                    Chính sách bảo mật
                                </Link>
                            </span>
                        </label>

                        {/* Submit */}
                        <button 
                            type="submit" 
                            className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                            disabled={loading || !isPasswordValid || formData.password !== formData.confirmPassword}
                        >
                            {loading ? 'Đang xử lý...' : 'Đăng ký'}
                        </button>
                    </form>

                    {/* Login Link */}
                    <p className="text-center text-sm text-gray-600 mt-6">
                        Đã có tài khoản?{' '}
                        <Link
                            href="/auth/login"
                            className="text-primary hover:text-primary-dark font-medium"
                        >
                            Đăng nhập ngay
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}

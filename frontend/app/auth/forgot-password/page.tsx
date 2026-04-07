'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Mail, Lock, Eye, EyeOff, ArrowLeft, Check, X } from 'lucide-react';
import toast from 'react-hot-toast';
import { useRouter } from 'next/navigation';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function ForgotPasswordPage() {
    const router = useRouter();
    const [step, setStep] = useState<'email' | 'reset'>('email');
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [formData, setFormData] = useState({
        email: '',
        newPassword: '',
        confirmPassword: '',
    });

    // Password validation
    const passwordValidation = {
        minLength: formData.newPassword.length >= 8,
        hasUppercase: /[A-Z]/.test(formData.newPassword),
        hasNumber: /\d/.test(formData.newPassword),
    };

    const isPasswordValid = passwordValidation.minLength && 
                           passwordValidation.hasUppercase && 
                           passwordValidation.hasNumber;

    const handleCheckEmail = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        try {
            // API_URL already includes /api, so just add the endpoint path
            const response = await axios.get(`${API_URL}/nguoi-dung/check-email/${encodeURIComponent(formData.email)}`);
            
            if (response.data.exists) {
                setStep('reset');
                toast.success('Email hợp lệ! Vui lòng nhập mật khẩu mới.');
            } else {
                toast.error('Email không tồn tại trong hệ thống!');
            }
        } catch (error: any) {
            console.error('Check email error:', error);
            toast.error('Email không tồn tại trong hệ thống!');
        } finally {
            setLoading(false);
        }
    };

    const handleResetPassword = async (e: React.FormEvent) => {
        e.preventDefault();

        // Validate password
        if (!isPasswordValid) {
            toast.error('Mật khẩu không đủ mạnh! Vui lòng kiểm tra các yêu cầu.');
            return;
        }

        // Validate passwords match
        if (formData.newPassword !== formData.confirmPassword) {
            toast.error('Mật khẩu xác nhận không khớp!');
            return;
        }

        setLoading(true);

        try {
            // API_URL already includes /api
            await axios.post(`${API_URL}/auth/reset-password`, {
                email: formData.email,
                new_password: formData.newPassword,
            });

            // Clear any existing session
            localStorage.removeItem('token');
            localStorage.removeItem('user');

            toast.success('Đặt lại mật khẩu thành công! Vui lòng đăng nhập lại.');
            
            setTimeout(() => {
                router.push('/auth/login');
            }, 2000);

        } catch (error: any) {
            console.error('Reset password error:', error);
            
            if (error.response?.data?.detail) {
                toast.error(error.response.data.detail);
            } else {
                toast.error('Đặt lại mật khẩu thất bại. Vui lòng thử lại!');
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
                    <h2 className="text-3xl font-bold text-gray-900">Quên mật khẩu</h2>
                    <p className="text-gray-600 mt-2">
                        {step === 'email' 
                            ? 'Nhập email để đặt lại mật khẩu'
                            : 'Nhập mật khẩu mới của bạn'
                        }
                    </p>
                </div>

                {/* Form */}
                <div className="card p-8">
                    {step === 'email' ? (
                        <form onSubmit={handleCheckEmail} className="space-y-6">
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
                                        placeholder="        quynhhuong@gmail.com"
                                        disabled={loading}
                                    />
                                </div>
                            </div>

                            {/* Submit */}
                            <button 
                                type="submit" 
                                className="w-full btn-primary"
                                disabled={loading}
                            >
                                {loading ? 'Đang kiểm tra...' : 'Tiếp tục'}
                            </button>
                        </form>
                    ) : (
                        <form onSubmit={handleResetPassword} className="space-y-6">
                            {/* New Password */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Mật khẩu mới
                                </label>
                                <div className="relative">
                                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                                    <input
                                        type={showPassword ? 'text' : 'password'}
                                        required
                                        value={formData.newPassword}
                                        onChange={(e) => setFormData({ ...formData, newPassword: e.target.value })}
                                        className="input pl-10 pr-10"
                                        placeholder="        ••••••••"
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
                                {formData.newPassword && (
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
                                        placeholder="        ••••••••"
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
                                        {formData.newPassword === formData.confirmPassword ? (
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

                            {/* Submit */}
                            <button 
                                type="submit" 
                                className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                                disabled={loading || !isPasswordValid || formData.newPassword !== formData.confirmPassword}
                            >
                                {loading ? 'Đang xử lý...' : 'Đặt lại mật khẩu'}
                            </button>

                            {/* Back */}
                            <button
                                type="button"
                                onClick={() => setStep('email')}
                                className="w-full text-sm text-gray-600 hover:text-gray-900 flex items-center justify-center space-x-2"
                                disabled={loading}
                            >
                                <ArrowLeft className="w-4 h-4" />
                                <span>Quay lại</span>
                            </button>
                        </form>
                    )}

                    {/* Login Link */}
                    <p className="text-center text-sm text-gray-600 mt-6">
                        Nhớ mật khẩu?{' '}
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

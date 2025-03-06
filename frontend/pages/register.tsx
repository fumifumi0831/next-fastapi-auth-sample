import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useAuth } from '../contexts/AuthContext';
import Link from 'next/link';

interface RegisterForm {
  email: string;
  password: string;
  confirmPassword: string;
}

export default function Register() {
  const { register: registerUser } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const { 
    register, 
    handleSubmit, 
    watch, 
    formState: { errors } 
  } = useForm<RegisterForm>();

  const onSubmit = async (data: RegisterForm) => {
    try {
      // エラーステートをリセット
      setError(null);

      // パスワード一致の再確認
      if (data.password !== data.confirmPassword) {
        setError('パスワードが一致しません');
        return;
      }

      // ユーザー登録処理
      await registerUser(data.email, data.password);
    } catch (err: any) {
      // エラーハンドリング
      const errorMessage = err.response?.data?.detail || '登録に失敗しました';
      setError(errorMessage);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            アカウント登録
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            または{' '}
            <Link href="/login" className="font-medium text-indigo-600 hover:text-indigo-500">
              ログインはこちら
            </Link>
          </p>
        </div>
        
        {/* エラーメッセージ */}
        {error && (
          <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-6">
          <div className="rounded-md shadow-sm -space-y-px">
            {/* メールアドレス入力 */}
            <div>
              <label htmlFor="email" className="sr-only">メールアドレス</label>
              <input
                {...register('email', { 
                  required: 'メールアドレスは必須です',
                  pattern: {
                    value: /^\S+@\S+$/i,
                    message: '正しいメールアドレスを入力してください'
                  }
                })}
                id="email"
                type="email"
                autoComplete="email"
                placeholder="メールアドレス"
                className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
                  errors.email ? 'border-red-500' : 'border-gray-300'
                } placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
              />
              {errors.email && (
                <p className="text-red-500 text-xs mt-1">{errors.email.message}</p>
              )}
            </div>

            {/* パスワード入力 */}
            <div>
              <label htmlFor="password" className="sr-only">パスワード</label>
              <input
                {...register('password', { 
                  required: 'パスワードは必須です',
                  minLength: {
                    value: 8,
                    message: 'パスワードは8文字以上必要です'
                  },
                  validate: (value) => {
                    // パスワードの複雑性チェック
                    const hasUpperCase = /[A-Z]/.test(value);
                    const hasLowerCase = /[a-z]/.test(value);
                    const hasNumber = /[0-9]/.test(value);
                    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(value);

                    if (!hasUpperCase) return '大文字を含めてください';
                    if (!hasLowerCase) return '小文字を含めてください';
                    if (!hasNumber) return '数字を含めてください';
                    if (!hasSpecialChar) return '特殊文字を含めてください';

                    return true;
                  }
                })}
                id="password"
                type="password"
                autoComplete="new-password"
                placeholder="パスワード"
                className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
                  errors.password ? 'border-red-500' : 'border-gray-300'
                } placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
              />
              {errors.password && (
                <p className="text-red-500 text-xs mt-1">{errors.password.message}</p>
              )}
            </div>

            {/* パスワード確認 */}
            <div>
              <label htmlFor="confirmPassword" className="sr-only">パスワード（確認）</label>
              <input
                {...register('confirmPassword', { 
                  required: 'パスワード（確認）は必須です',
                  validate: (value) => 
                    value === watch('password') || 'パスワードが一致しません'
                })}
                id="confirmPassword"
                type="password"
                autoComplete="new-password"
                placeholder="パスワード（確認）"
                className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
                  errors.confirmPassword ? 'border-red-500' : 'border-gray-300'
                } placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
              />
              {errors.confirmPassword && (
                <p className="text-red-500 text-xs mt-1">{errors.confirmPassword.message}</p>
              )}
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              登録
            </button>
          </div>
        </form>

        {/* パスワード要件の説明 */}
        <div className="text-sm text-gray-600 text-center">
          <p>パスワードは以下の要件を満たす必要があります：</p>
          <ul className="list-disc list-inside">
            <li>8文字以上</li>
            <li>大文字を含む</li>
            <li>小文字を含む</li>
            <li>数字を含む</li>
            <li>特殊文字を含む</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

// クライアントサイドでのみレンダリング
Register.requireAuth = false;

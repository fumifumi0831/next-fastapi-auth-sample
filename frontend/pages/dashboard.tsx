import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useRouter } from 'next/router';
import axios from 'axios';

export default function Dashboard() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [protectedData, setProtectedData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // 認証されていない場合はログインページにリダイレクト
    if (!user) {
      router.push('/login');
      return;
    }

    // 保護されたエンドポイントからデータを取得
    const fetchProtectedData = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('トークンが見つかりません');
        }

        const response = await axios.get('http://localhost:8000/protected', {
          headers: { Authorization: `Bearer ${token}` }
        });

        setProtectedData(response.data);
        setLoading(false);
      } catch (err: any) {
        // エラーハンドリング
        setError(err.response?.data?.detail || 'データの取得に失敗しました');
        setLoading(false);

        // トークンエラーの場合はログアウト
        if (err.response?.status === 401) {
          logout();
        }
      }
    };

    fetchProtectedData();
  }, [user, router, logout]);

  // ローディング中
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-indigo-500 mx-auto"></div>
          <p className="mt-4 text-indigo-600">読み込み中...</p>
        </div>
      </div>
    );
  }

  // エラー発生
  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">エラー: </strong>
          <span className="block sm:inline">{error}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="absolute inset-0 bg-gradient-to-r from-indigo-700 to-purple-500 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <div className="max-w-md mx-auto">
            <div className="divide-y divide-gray-200">
              <div className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                <h2 className="text-3xl font-extrabold text-center text-gray-900">
                  ダッシュボード
                </h2>
                
                {/* ユーザー情報 */}
                <div className="bg-gray-50 p-4 rounded-md">
                  <p className="text-sm text-gray-600">メールアドレス:</p>
                  <p className="font-semibold text-indigo-600">{user?.email}</p>
                </div>

                {/* 保護されたデータ */}
                <div className="bg-gray-50 p-4 rounded-md">
                  <p className="text-sm text-gray-600">メッセージ:</p>
                  <p className="font-semibold">{protectedData?.message}</p>
                </div>
              </div>
              
              <div className="pt-4 text-base leading-6 font-bold sm:text-lg sm:leading-7">
                <button
                  onClick={logout}
                  className="w-full rounded-md bg-red-600 px-4 py-2 text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
                >
                  ログアウト
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// 認証が必要なページ
Dashboard.requireAuth = true;

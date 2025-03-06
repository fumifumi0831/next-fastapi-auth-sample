import Link from 'next/link';
import { useAuth } from '../contexts/AuthContext';

export default function Home() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="max-w-md w-full bg-white shadow-md rounded-lg p-8 text-center">
        <h1 className="text-3xl font-bold mb-6 text-gray-800">
          認証デモアプリケーション
        </h1>

        {user ? (
          // ログイン済みの場合
          <div>
            <p className="text-lg mb-4 text-gray-600">
              こんにちは、<span className="font-semibold text-indigo-600">{user.email}</span> さん
            </p>
            <div className="space-y-4">
              <Link href="/dashboard" className="block w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700 transition">
                ダッシュボードへ
              </Link>
            </div>
          </div>
        ) : (
          // 未ログインの場合
          <div className="space-y-4">
            <Link href="/login" className="block w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700 transition">
              ログイン
            </Link>
            <Link href="/register" className="block w-full bg-gray-200 text-gray-800 py-2 rounded-md hover:bg-gray-300 transition">
              新規登録
            </Link>
          </div>
        )}

        <div className="mt-6 text-sm text-gray-500">
          <p>認証デモアプリケーションへようこそ</p>
          <p>セキュリティ機能を備えた認証システムのサンプルです</p>
        </div>
      </div>
    </div>
  );
}

// 認証不要なページ
Home.requireAuth = false;

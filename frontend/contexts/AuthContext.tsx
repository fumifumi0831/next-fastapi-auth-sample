import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';

// 型定義
interface User {
  id: number;
  email: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  // バックエンドのベースURL
  const API_BASE_URL = 'http://localhost:8000';

  useEffect(() => {
    // 初期化時にトークンの検証
    const token = localStorage.getItem('token');
    if (token) {
      validateToken(token);
    }
  }, []);

  const validateToken = async (token: string) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/protected`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      // ユーザー情報を設定
      setUser({
        id: response.data.user.id,
        email: response.data.user.email
      });
    } catch {
      // トークンが無効な場合はログアウト
      logout();
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/login`, { email, password });
      
      // トークンを保存
      localStorage.setItem('token', response.data.access_token);
      
      // トークンを検証してユーザー情報を取得
      await validateToken(response.data.access_token);
      
      // ダッシュボードにリダイレクト
      router.push('/dashboard');
    } catch (error: any) {
      // エラーハンドリング
      console.error('ログインエラー', error.response?.data);
      throw error;
    }
  };

  const register = async (email: string, password: string) => {
    try {
      await axios.post(`${API_BASE_URL}/register`, { email, password });
      
      // 登録後にログインページへリダイレクト
      router.push('/login');
    } catch (error: any) {
      console.error('登録エラー', error.response?.data);
      throw error;
    }
  };

  const logout = () => {
    // トークンを削除
    localStorage.removeItem('token');
    
    // ユーザー情報をリセット
    setUser(null);
    
    // ログインページにリダイレクト
    router.push('/login');
  };

  return (
    <AuthContext.Provider 
      value={{ 
        user, 
        login, 
        register, 
        logout, 
        isAuthenticated: !!user 
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// カスタムフック
export const useAuth = () => useContext(AuthContext);

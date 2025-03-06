# Next.js + FastAPI Authentication Demo

## プロジェクト概要
このプロジェクトは、Next.jsとFastAPIを使用した自前の認証システムのデモンストレーションです。

## 機能
- ユーザー登録
- ログイン
- ログアウト
- 認証が必要なダッシュボード

## セットアップ

### バックエンド
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windowsの場合は `venv\Scripts\activate`
pip install -r requirements.txt
python main.py
```

### フロントエンド
```bash
cd frontend
npm install
npm run dev
```

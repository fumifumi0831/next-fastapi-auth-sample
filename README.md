# 🔐 Next.js + FastAPI 認証デモアプリケーション

## 📝 プロジェクト概要

このプロジェクトは、Next.js (TypeScript) とFastAPIを使用した、セキュリティを重視した認証システムのデモンストレーションです。7つの重要なセキュリティ対策を実装しています。

## ✨ 主な機能

- ユーザー登録
- ログイン/ログアウト
- 認証が必要なダッシュボード
- 包括的なセキュリティ対策

## 🛡️ セキュリティ対策

### 1. パスワード保護
- bcryptによる安全なパスワードハッシュ化
- 複雑なパスワード要件の検証
  - 最小8文字
  - 大文字、小文字、数字、特殊文字を含む

### 2. トークン管理
- JWTによる安全な認証
- アクセストークンとリフレッシュトークン
- トークンの有効期限管理

### 3. ブルートフォース攻撃対策
- ログイン試行回数の制限
- IPアドレスベースのロックアウト
- 指数関数的バックオフ戦略

### 4. XSS (クロスサイトスクリプティング) 対策
- 入力値のサニタイズ
- セキュリティヘッダーの設定
- コンテンツセキュリティポリシー

### 5. CSRF (クロスサイトリクエストフォージェリ) 対策
- CSRFトークンの生成と検証
- Cookieのセキュア設定

### 6. 安全な通信
- CORS設定
- セキュリティヘッダーの追加
- HTTPSを考慮した設計

### 7. データベースセキュリティ
- 最小権限の原則
- パラメータ化クエリ
- ユーザーテーブルでの追加のセキュリティ情報管理

## 🚀 技術スタック

### バックエンド
- FastAPI
- SQLAlchemy
- SQLite
- Python-jose (JWT)
- Passlib (パスワードハッシュ)

### フロントエンド
- Next.js
- TypeScript
- Tailwind CSS
- Axios
- React Hook Form

## 📦 インストール方法

### 前提条件
- Python 3.8+
- Node.js 14+
- pip
- npm

### バックエンドのセットアップ

1. リポジトリをクローン
```bash
git clone https://github.com/fumifumi0831/next-fastapi-auth-sample.git
cd next-fastapi-auth-sample/backend
```

2. 仮想環境の作成と有効化
```bash
# Windowsの場合
python -m venv venv
venv\Scripts\activate

# Mac/Linuxの場合
python3 -m venv venv
source venv/bin/activate
```

3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

4. サーバーの起動
```bash
python main.py
```

### フロントエンドのセットアップ

1. 別のターミナルで以下を実行
```bash
cd ../frontend
npm install
npm run dev
```

## 🖥️ アプリケーションへのアクセス

- バックエンド: `http://localhost:8000`
- フロントエンド: `http://localhost:3000`

## 🧪 テスト

### バックエンドテスト
```bash
# バックエンドディレクトリで
pytest
```

### フロントエンドテスト
```bash
# フロントエンドディレクトリで
npm test
```

## 🔒 本番環境への注意点

- 環境変数の適切な管理
- 本番用のシークレットキーの使用
- HTTPS環境での運用
- 継続的なセキュリティアップデート

## 🤝 コントリビューション

1. フォーク
2. フィーチャーブランチの作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下で提供されています。詳細は `LICENSE` ファイルを参照してください。

## 💡 免責事項

このデモアプリケーションは教育目的で作成されています。本番環境での使用には、さらなるセキュリティ強化と専門家のレビューが必要です。

## 🌟 サポート

問題や機能リクエストがある場合は、GitHubの Issues セクションに投稿してください。

---

🔐 セキュリティは継続的な学習と改善の旅です。常に最新の知識とベストプラクティスを学び続けましょう！

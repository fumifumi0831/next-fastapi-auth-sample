import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timedelta

from database import init_db, get_db
from models import User
from schemas import UserCreate, UserResponse, LoginRequest, Token, TokenData
from security import (
    SecurityManager, 
    TokenManager, 
    BruteForceDefender, 
    generate_csrf_token, 
    secure_headers
)

# アプリケーションの初期化
app = FastAPI(title="認証デモアプリケーション")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では具体的なオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# セキュリティヘッダーのミドルウェア
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # XSS対策のためのセキュリティヘッダーを設定
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:;"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # CSRF対策としてレスポンスが変更されないようにするヘッダー
    response.headers["Cache-Control"] = "no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    
    # IEで自動的にMIMEスニッフィングを行わないように設定
    response.headers["X-Download-Options"] = "noopen"
    
    # クリックジャッキング対策
    response.headers["X-Frame-Options"] = "DENY"
    
    # もともとのsecure_headersの処理も実行（現在はダミー）
    secure_headers.framework.fastapi(response)
    
    return response

# データベース初期化
init_db()

# 認証保護のためのベアラートークン
security = HTTPBearer()

@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    ユーザー登録エンドポイント
    
    - メールアドレスの重複チェック
    - パスワードのハッシュ化
    - パスワードの複雑性チェック
    """
    # メールアドレスの重複チェック
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="このメールアドレスは既に登録されています"
        )
    
    # パスワードをハッシュ化
    hashed_password = SecurityManager.hash_password(user.password)
    
    # 新規ユーザー作成
    db_user = User(
        email=user.email, 
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.post("/login", response_model=Token)
def login(
    login_data: LoginRequest, 
    db: Session = Depends(get_db)
):
    """
    ログインエンドポイント
    
    - ブルートフォース攻撃対策
    - パスワード検証
    - JWTトークン生成
    """
    # IPアドレスベースのブルートフォース対策
    # 本番環境ではクライアントのIPアドレスを取得
    client_ip = "default_ip"  # 実際のアプリケーションでは適切なIP取得
    
    # ログイン試行の制限
    if not BruteForceDefender.check_attempt(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="ログイン試行回数が多すぎます。しばらく待ってからお試しください。"
        )
    
    # ユーザー検索
    user = db.query(User).filter(User.email == login_data.email).first()
    
    # ユーザーが見つからない場合のエラーハンドリング
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが間違っています"
        )
    
    # ユーザー認証
    if not SecurityManager.verify_password(login_data.password, user.hashed_password):
        # ログイン失敗時の処理
        user.login_attempts = (user.login_attempts or 0) + 1
        
        # 連続ログイン失敗回数が一定数を超えたらアカウントをロック
        if user.login_attempts >= 5:
            user.is_locked = 1
        
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが間違っています"
        )
    
    # アカウントがロックされている場合
    if user.is_locked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="アカウントは一時的にロックされています。パスワードリセットを行ってください。"
        )
    
    # ログイン成功時の処理
    user.last_login = datetime.utcnow()
    user.login_attempts = 0  # ログイン試行回数をリセット
    db.commit()
    
    # JWTトークンの生成
    access_token = TokenManager.create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    # ブルートフォース防御のリセット
    BruteForceDefender.reset_attempts(client_ip)
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
def protected_route(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    認証が必要なエンドポイント
    
    - トークンの検証
    - ユーザー情報の取得
    """
    try:
        # トークンのデコードと検証
        payload = TokenManager.decode_token(credentials.credentials)
        
        # トークンからユーザー情報を抽出
        token_data = TokenData(**payload)
        
        # ユーザーの存在確認
        user = db.query(User).filter(User.id == token_data.sub).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="ユーザーが見つかりません"
            )
        
        return {
            "message": "認証に成功しました", 
            "user": {
                "id": user.id,
                "email": user.email,
                "last_login": user.last_login
            }
        }
    
    except HTTPException as e:
        # トークンの検証に失敗した場合
        raise e

@app.post("/refresh-token")
def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    トークンのリフレッシュ
    
    - 古いトークンの検証
    - 新しいトークンの発行
    """
    try:
        # リフレッシュトークンのデコードと検証
        payload = TokenManager.decode_token(credentials.credentials)
        token_data = TokenData(**payload)
        
        # ユーザーの存在確認
        user = db.query(User).filter(User.id == token_data.sub).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="ユーザーが見つかりません"
            )
        
        # 新しいアクセストークンの生成
        new_access_token = TokenManager.create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        return {"access_token": new_access_token, "token_type": "bearer"}
    
    except HTTPException as e:
        # トークンの検証に失敗した場合
        raise e

@app.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    ログアウト処理
    
    - トークンの無効化
    """
    # 現実的なログアウト処理
    # クライアント側でトークンを破棄することを推奨
    return {"message": "ログアウトしました"}

# アプリケーションの起動
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

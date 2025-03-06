import os
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import ValidationError
# セキュリティヘッダー関連のインポートを一時的にコメントアウト
# from secure import SecureHeaders

# 1. パスワード保護: 強力なハッシュ化コンテキスト
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# セキュリティ設定
SECRET_KEY = os.urandom(32)  # 暗号学的に安全なランダムキー
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

class SecurityManager:
    @staticmethod
    def hash_password(password: str) -> str:
        """
        パスワードをセキュアにハッシュ化
        ソルトは自動生成され、bcryptに組み込まれる
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        パスワードの検証
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def validate_password(password: str) -> bool:
        """
        パスワードの複雑性チェック
        - 最小8文字
        - 大文字、小文字、数字、特殊文字を含む
        """
        # パスワードの複雑性規則
        if len(password) < 8:
            return False
        
        # 大文字、小文字、数字、特殊文字のチェック
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        
        return True

class TokenManager:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        アクセストークンの生成
        """
        to_encode = data.copy()
        
        # トークンの有効期限設定
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        
        # JWTトークンの生成
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """
        リフレッシュトークンの生成
        """
        return TokenManager.create_access_token(
            data, 
            expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )

    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        """
        トークンの検証と復号
        """
        try:
            # トークンをデコードし、検証
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="トークンが無効です")

class BruteForceDefender:
    """
    ブルートフォース攻撃対策
    """
    _attempts: Dict[str, Dict[str, Any]] = {}
    MAX_ATTEMPTS = 5
    LOCKOUT_DURATION = timedelta(minutes=15)

    @classmethod
    def check_attempt(cls, identifier: str) -> bool:
        """
        ログイン試行の検証
        """
        now = datetime.utcnow()
        attempt = cls._attempts.get(identifier, {
            "count": 0,
            "last_attempt": now
        })

        # ロックアウト期間中かチェック
        if (attempt["count"] >= cls.MAX_ATTEMPTS and 
            now - attempt["last_attempt"] < cls.LOCKOUT_DURATION):
            return False

        # 試行回数を更新
        updated_attempt = {
            "count": (
                1 if now - attempt["last_attempt"] > cls.LOCKOUT_DURATION 
                else attempt["count"] + 1
            ),
            "last_attempt": now
        }

        cls._attempts[identifier] = updated_attempt
        return True

    @classmethod
    def reset_attempts(cls, identifier: str):
        """
        ログイン成功時に試行回数をリセット
        """
        if identifier in cls._attempts:
            del cls._attempts[identifier]

# XSS対策用のセキュアヘッダー (一時的にモックオブジェクトを作成)
class DummySecureHeaders:
    def __init__(self):
        pass
    
    @property
    def framework(self):
        return self
    
    def fastapi(self, response):
        # 何もしない、プレースホルダーとして機能
        pass

secure_headers = DummySecureHeaders()

# CSRF対策用のトークン生成
def generate_csrf_token() -> str:
    """
    CSRFトークンの生成
    """
    return os.urandom(32).hex()

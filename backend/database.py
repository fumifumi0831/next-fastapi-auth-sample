from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

# データベース接続URL (SQLite)
DATABASE_URL = "sqlite:///./auth_demo.db"

# データベースエンジンの作成
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # SQLiteの制限を回避
)

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラスの作成
Base = declarative_base()

# ユーザーモデル
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    login_attempts = Column(Integer, default=0)
    is_locked = Column(Integer, default=0)

# データベース初期化関数
def init_db():
    """
    データベースとテーブルを初期化する
    """
    Base.metadata.create_all(bind=engine)

# データベースセッション取得関数
def get_db() -> Session:
    """
    データベースセッションを取得する
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

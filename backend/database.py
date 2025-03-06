from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

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

# データベース初期化関数
def init_db():
    """
    データベースとテーブルを初期化する
    """
    # この時点でmodelsをインポートするとmodels.pyから循環インポートを避けられる
    from models import User  # Userモデルをここでインポート
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

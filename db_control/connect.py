from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from pathlib import Path

# .envファイルを読み込む
base_path = Path(__file__).parents[1]  # backendディレクトリへのパス
env_path = base_path / '.env'
load_dotenv(dotenv_path=env_path)

# データベース接続情報を取得
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
SSL_CA = os.getenv('DB_SSL_CA')  # SSL証明書のパスを取得

# SQLAlchemy用の接続URL
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemyのengineを作成（SSL設定あり）
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl_ca": SSL_CA
    },
    echo=True,
    pool_pre_ping=True
)

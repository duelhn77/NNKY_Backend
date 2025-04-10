<<<<<<< HEAD
# from sqlalchemy import create_engine
# # import sqlalchemy

# import os
# # uname() error回避
# import platform
# print("platform:", platform.uname())


# main_path = os.path.dirname(os.path.abspath(__file__))
# path = os.chdir(main_path)
# print("path:", path)
# engine = create_engine("sqlite:///CRM.db", echo=True)

from sqlalchemy import create_engine
import os
from pathlib import Path
from dotenv import load_dotenv
import pymysql

# 環境変数の読み込み
base_path = Path(__file__).parents[1] #backendディレクトリへのパス
env_path = base_path / '.env'
load_dotenv(dotenv_path=env_path)

# データベース接続情報
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

#SSL証明書のパス
ssl_cert = str('DigiCertGlobalRootCA.crt.pem')
=======
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

# データベース接続情報を取得
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
SSL_CA = os.getenv('DB_SSL_CA')

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

# import mysql.connector
# import os
# from dotenv import load_dotenv

# load_dotenv()  # .envファイルを読み込む

# conn = mysql.connector.connect(
#     host=os.getenv("DB_HOST"),
#     user=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASSWORD"),
#     database=os.getenv("DB_NAME"),
#     ssl_ca=os.getenv("DB_SSL_CA")  # 必要であれば
# )

# print("✅ MySQL接続に成功しました！")
# conn.close()



# # from sqlalchemy import create_engine
# # # import sqlalchemy

# # import os
# # # uname() error回避
# # import platform
# # print("platform:", platform.uname())


# # main_path = os.path.dirname(os.path.abspath(__file__))
# # path = os.chdir(main_path)
# # print("path:", path)
# # engine = create_engine("sqlite:///CRM.db", echo=True)

# # from sqlalchemy import create_engine
# # import os
# # from pathlib import Path
# # from dotenv import load_dotenv
# # import pymysql

# # # 環境変数の読み込み
# # base_path = Path(__file__).parents[1] #backendディレクトリへのパス
# # env_path = base_path / '.env'
# # load_dotenv(dotenv_path=env_path)

# # # データベース接続情報
# # DB_USER = os.getenv('DB_USER')
# # DB_PASSWORD = os.getenv('DB_PASSWORD')
# # DB_HOST = os.getenv('DB_HOST')
# # DB_PORT = os.getenv('DB_PORT')
# # DB_NAME = os.getenv('DB_NAME')

# # #SSL証明書のパス
# # ssl_cert = str('DigiCertGlobalRootCA.crt.pem')
>>>>>>> 833bd91cf8beac673089f9c71f655bbafb675be2

# MySQLのURL構築
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# エンジンの作成
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl":{
            "ssl_ca":ssl_cert
        }
    },
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600
)

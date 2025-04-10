# db_control/auth.py

from passlib.context import CryptContext

# パスワードハッシュの設定（bcryptを使用）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ハッシュ化関数
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 照合関数
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

from datetime import datetime, timedelta
from jose import JWTError, jwt

# JWT設定
SECRET_KEY = "your_secret_key"  # 環境変数などで管理するのがベター
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# JWTトークン作成
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# JWTトークン検証
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

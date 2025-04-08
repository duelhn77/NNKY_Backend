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

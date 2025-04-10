from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_control.connect_MySQL import get_db
from db_control import crud
from pydantic import BaseModel, EmailStr
from datetime import date
from passlib.hash import bcrypt

router = APIRouter()

# リクエストボディ用のスキーマ定義
class UserCreate(BaseModel):
    name: str
    name_kana: str
    email: EmailStr
    password: str
    birth_date: date

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # 既に存在するメールアドレスか確認
    existing = db.query(crud.User).filter(crud.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="このメールアドレスは既に登録されています。")

    new_user = crud.create_user(
        db=db,
        name=user.name,
        name_kana=user.name_kana,
        email=user.email,
        password=user.password,
        birth_date=user.birth_date
    )
    return {"message": "ユーザー登録が完了しました。", "user_id": new_user.user_id}

# ログイン時の入力用スキーマ
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# @router.post("/login")
# def login_user(login: LoginRequest, db: Session = Depends(get_db)):
#     # DBからユーザーを検索
#     user = db.query(crud.User).filter(crud.User.email == login.email).first()
#     if not user:
#         raise HTTPException(status_code=401, detail="メールアドレスが登録されていません。")

#     # パスワード照合
#     if not bcrypt.verify(login.password, user.password):
#         raise HTTPException(status_code=401, detail="パスワードが間違っています。")

#     return {"message": "ログイン成功", "user_id": user.user_id}

@router.post("/login")
def login_user(login: LoginRequest, db: Session = Depends(get_db)):
    print(f"🌐 ログイン試行 Email: {login.email}")

    user = db.query(crud.User).filter(crud.User.email == login.email).first()
    if not user:
        print("🚫 該当するユーザーが見つかりません")
        raise HTTPException(status_code=401, detail="メールアドレスが登録されていません。")

    print(f"✅ ユーザー発見: {user.email}")
    print(f"🔐 入力PW: {login.password}")
    print(f"🔐 登録PW(ハッシュ): {user.password}")

    if not bcrypt.verify(login.password, user.password):
        print("🚫 パスワードが一致しません")
        raise HTTPException(status_code=401, detail="パスワードが間違っています。")

    print("🎉 ログイン成功")
    return {"message": "ログイン成功", "user_id": user.user_id}


from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db_control import auth  # JWT発行関数がここにある
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(crud.User).filter(crud.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="メールアドレスが登録されていません。")

    if not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="パスワードが間違っています。")

    # JWT発行
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from db_control import auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends

# 🔹 レスポンスモデル（返したいユーザー情報の定義）
class UserResponse(BaseModel):
    user_id: int
    name: str
    name_kana: str
    email: str
    birth_date: date

    class Config:
        from_attributes = True

# 🔐 拡張した /me
@router.get("/me", response_model=UserResponse)
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = auth.verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # 🔍 DBから該当ユーザーを取得
    user = db.query(crud.User).filter(crud.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


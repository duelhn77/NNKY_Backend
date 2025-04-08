from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_control.connect_MySQL import get_db
from db_control import crud
from pydantic import BaseModel, EmailStr
from datetime import date

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

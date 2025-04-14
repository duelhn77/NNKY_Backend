from pydantic import BaseModel  # 追加
from typing import List  # 追加
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db_control.connect_MySQL import get_db  # データベース接続用
from db_control import crud  # 既存のCRUD操作を使う
from db_control.mymodels import Partner  # 正しいパスでインポート

router = APIRouter()

# パートナー取得用のレスポンススキーマ
class PartnerResponse(BaseModel):  # BaseModelの追加
    partner_id: int
    partner_name: str  # 修正: partner_name → name

    class Config:
        orm_mode = True  # SQLAlchemyのモデルをPydanticモデルに変換

# パートナー一覧取得API
@router.get("/partners", response_model=List[PartnerResponse])
def get_partners(db: Session = Depends(get_db)):
    # パートナーの全データを取得
    partners = db.query(Partner).all()
    return partners


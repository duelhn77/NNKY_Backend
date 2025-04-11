from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db_control.connect_MySQL import get_db
from db_control import crud  # 既存のCRUD操作を使用
from pydantic import BaseModel
from typing import List  # 追加するインポート


router = APIRouter()

# プレ診断作成用の入力スキーマ
class PreSurveyCreate(BaseModel):
    reservation_id: int
    age_group: str
    item_preparation: bool
    concern_parts: str
    troubles: str
    past_experience: str
    consultation_goal: str
    free_comment: str

# プレ診断情報を取得するレスポンス用のスキーマ
class PreSurveyResponse(BaseModel):
    survey_id: int
    reservation_id: int
    age_group: str
    item_preparation: bool
    concern_parts: str
    troubles: str
    past_experience: str
    consultation_goal: str
    free_comment: str

    class Config:
        orm_mode = True

# プレ診断作成API
@router.post("/presurveys", response_model=PreSurveyResponse)
def create_presurvey(
    presurvey: PreSurveyCreate, db: Session = Depends(get_db)
):
    new_presurvey = crud.create_presurvey(
        db=db,
        reservation_id=presurvey.reservation_id,
        age_group=presurvey.age_group,
        item_preparation=presurvey.item_preparation,
        concern_parts=presurvey.concern_parts,
        troubles=presurvey.troubles,
        past_experience=presurvey.past_experience,
        consultation_goal=presurvey.consultation_goal,
        free_comment=presurvey.free_comment
    )
    if not new_presurvey:
        raise HTTPException(status_code=400, detail="Failed to create presurvey.")
    return new_presurvey

# プレ診断一覧取得API
@router.get("/presurveys", response_model=List[PreSurveyResponse])
def get_presurveys(db: Session = Depends(get_db)):
    presurveys = crud.get_presurveys(db)
    return presurveys

# プレ診断IDで1件取得API
@router.get("/presurveys/{survey_id}", response_model=PreSurveyResponse)
def get_presurvey(survey_id: int, db: Session = Depends(get_db)):
    presurvey = crud.get_presurvey_by_id(db, survey_id)
    if not presurvey:
        raise HTTPException(status_code=404, detail="Presurvey not found.")
    return presurvey

# プレ診断更新API
@router.put("/presurveys/{survey_id}", response_model=PreSurveyResponse)
def update_presurvey(
    survey_id: int, 
    presurvey: PreSurveyCreate, 
    db: Session = Depends(get_db)
):
    updated_presurvey = crud.update_presurvey(
        db=db,
        survey_id=survey_id,
        age_group=presurvey.age_group,
        item_preparation=presurvey.item_preparation,
        concern_parts=presurvey.concern_parts,
        troubles=presurvey.troubles,
        past_experience=presurvey.past_experience,
        consultation_goal=presurvey.consultation_goal,
        free_comment=presurvey.free_comment
    )
    if not updated_presurvey:
        raise HTTPException(status_code=404, detail="Presurvey not found.")
    return updated_presurvey

# プレ診断削除API
@router.delete("/presurveys/{survey_id}")
def delete_presurvey(survey_id: int, db: Session = Depends(get_db)):
    deleted_presurvey_id = crud.delete_presurvey(db, survey_id)
    if not deleted_presurvey_id:
        raise HTTPException(status_code=404, detail="Presurvey not found.")
    return {"message": f"Presurvey {survey_id} deleted"}

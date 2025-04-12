from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db_control.connect_MySQL import get_db  # データベース接続用
from db_control import crud  # 既存のCRUD操作を使う
from db_control.mymodels import Course  # 正しいパスでインポート

router = APIRouter()

# コース作成用のスキーマ
class CourseCreate(BaseModel):
    course_name: str
    description: str

# コース取得用のレスポンススキーマ
class CourseResponse(BaseModel):
    course_id: int
    course_name: str
    description: str

    class Config:
        orm_mode = True  # SQLAlchemyのモデルをPydanticモデルに変換

# コース作成API
@router.post("/courses", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    # 新しいコースのインスタンスを作成
    new_course = Course(
        course_name=course.course_name,
        description=course.description
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)  # 新しく追加されたコース情報を反映
    return new_course  # 作成したコースを返す

# コース一覧取得API
@router.get("/courses", response_model=List[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    # コースの全データを取得
    return db.query(Course).all()

from pydantic import BaseModel
from datetime import datetime
from typing import List

# コース作成用のスキーマ
class CourseCreate(BaseModel):
    course_name: str
    description: str  # ここでdescriptionを追加

# コース取得用のレスポンススキーマ
class CourseResponse(BaseModel):
    course_id: int
    course_name: str

    class Config:
        orm_mode = True  # SQLAlchemyのモデルをPydanticモデルに変換


# スケジュール作成用のスキーマ
class ScheduleCreate(BaseModel):
    course_id: int
    start_time: datetime  # datetime型で受け取る
    end_time: datetime
    reservation_status: str
    partner_id: int

# スケジュール取得用のレスポンススキーマ
class ScheduleResponse(BaseModel):
    schedule_id: int
    course_id: int
    start_time: datetime  # datetime型に変更
    end_time: datetime
    reservation_status: str
    partner_id: int

    class Config:
        orm_mode = True  # SQLAlchemyのモデルをPydanticモデルに変換


# パートナー取得用のレスポンススキーマ
class PartnerResponse(BaseModel):  # PartnerResponseクラスを追加
    partner_id: int
    name: str  # partner_name → nameに変更

    class Config:
        orm_mode = True  # SQLAlchemyのモデルをPydanticモデルに変換

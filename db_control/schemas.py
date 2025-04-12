from pydantic import BaseModel
from datetime import datetime
from typing import List

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

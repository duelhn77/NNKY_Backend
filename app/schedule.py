from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db_control.connect_MySQL import get_db  # データベース接続用
from db_control import crud  # 既存のCRUD操作を使う
from pydantic import BaseModel
from typing import List
# app/schedule.py のインポート部分を修正
from db_control.schemas import ScheduleCreate, ScheduleResponse
from db_control.mymodels import Schedule


router = APIRouter()

# スケジュール作成API
@router.post("/schedules", response_model=ScheduleResponse)
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    new_schedule = Schedule(
        course_id=schedule.course_id,
        start_time=schedule.start_time,
        end_time=schedule.end_time,
        reservation_status=schedule.reservation_status,
        partner_id=schedule.partner_id
    )
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)  # 新しく追加されたスケジュール情報を反映
    return new_schedule  # 作成したスケジュールを返す

# スケジュール一覧取得API
@router.get("/schedules", response_model=List[ScheduleResponse])
def get_schedules(db: Session = Depends(get_db)):
    return db.query(Schedule).all()

# スケジュールIDで1件取得API
@router.get("/schedules/{schedule_id}", response_model=ScheduleResponse)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(Schedule).filter(Schedule.schedule_id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found.")
    return schedule

class ScheduleUpdateStatus(BaseModel):
    reservation_status: str  # 例: 'open' or 'booked'

@router.put("/schedules/{schedule_id}")
def update_schedule_status(
    schedule_id: int,
    status: ScheduleUpdateStatus,
    db: Session = Depends(get_db)
):
    schedule = db.query(Schedule).filter(Schedule.schedule_id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found.")

    schedule.reservation_status = status.reservation_status
    db.commit()
    db.refresh(schedule)
    return {"message": "Schedule status updated", "schedule_id": schedule_id}
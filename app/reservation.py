from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db_control.connect_MySQL import get_db
from db_control import crud  # 既存のCRUD操作を使用
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse

router = APIRouter()

# 予約作成用の入力スキーマ
class ReservationCreate(BaseModel):
    user_id: int
    schedule_id: int
    consultation_style: str

# 予約情報を取得するレスポンス用スキーマ
class ReservationResponse(BaseModel):
    reservation_id: int
    user_id: int
    schedule_id: int
    consultation_style: str

    class Config:
        orm_mode = True

# 予約作成API
@router.post("/reservations", response_model=ReservationResponse)
def create_reservation(
    reservation: ReservationCreate, db: Session = Depends(get_db)
):
    new_reservation = crud.create_reservation(
        db=db,
        user_id=reservation.user_id,
        schedule_id=reservation.schedule_id,
        consultation_style=reservation.consultation_style,
    )
    if not new_reservation:
        raise HTTPException(status_code=400, detail="Failed to create reservation.")
    return new_reservation

@router.options("/{rest_of_path:path}")
async def options_handler():
    return JSONResponse(status_code=200)

# 予約一覧取得API
@router.get("/reservations", response_model=List[ReservationResponse])
def get_reservations(db: Session = Depends(get_db)):
    reservations = crud.get_reservations(db)
    return reservations

# 予約IDで1件取得API
@router.get("/reservations/{reservation_id}", response_model=ReservationResponse)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = crud.get_reservation_by_id(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found.")
    return reservation

# 予約更新API
@router.put("/reservations/{reservation_id}", response_model=ReservationResponse)
def update_reservation(
    reservation_id: int, 
    schedule_id: int, 
    consultation_style: str, 
    db: Session = Depends(get_db)
):
    updated_reservation = crud.update_reservation(
        db=db,
        reservation_id=reservation_id,
        schedule_id=schedule_id,
        consultation_style=consultation_style
    )
    if not updated_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found.")
    return updated_reservation

# 予約削除API
@router.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    deleted_reservation_id = crud.delete_reservation(db, reservation_id)
    if not deleted_reservation_id:
        raise HTTPException(status_code=404, detail="Reservation not found.")
    return {"message": f"Reservation {reservation_id} deleted"}

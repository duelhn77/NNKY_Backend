import platform
from sqlalchemy import create_engine, insert, delete, update, select
from sqlalchemy.orm import sessionmaker
import json
import pandas as pd
from passlib.hash import bcrypt
from db_control.connect import engine
from db_control.mymodels import Customers, User, Reservation  # Reservationテーブルをインポート
from sqlalchemy.orm import Session
from datetime import date


# Frontendとのつなぎ込みで追加（4/10 なりさん）
def find_user_by_email(email):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        user = session.query(User).filter(User.email == email).first()
        return user
    finally:
        session.close()

def create_user(db: Session, name: str, name_kana: str, email: str, password: str, birth_date: date):
    hashed_password = bcrypt.hash(password)  # ✅ここでハッシュ化！
    new_user = User(
        name=name,
        name_kana=name_kana,
        email=email,
        password=hashed_password,
        birth_date=birth_date
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def myinsert(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    query = insert(mymodel).values(values)
    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()

    # セッションを閉じる
    session.close()
    return "inserted"


def myselect(mymodel, customer_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(mymodel).filter(mymodel.customer_id == customer_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = query.all()
        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = []
        for customer_info in result:
            result_dict_list.append({
                "customer_id": customer_info.customer_id,
                "customer_name": customer_info.customer_name,
                "age": customer_info.age,
                "gender": customer_info.gender
            })
        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")

    # セッションを閉じる
    session.close()
    return result_json


def myselectAll(mymodel):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = select(mymodel)
    try:
        # トランザクションを開始
        with session.begin():
            df = pd.read_sql_query(query, con=engine)
            result_json = df.to_json(orient='records', force_ascii=False)

    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        result_json = None

    # セッションを閉じる
    session.close()
    return result_json


def myupdate(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    customer_id = values.pop("customer_id")

    query = update(mymodel).where(mymodel.customer_id == customer_id).values(values)
    try:
        # トランザクションを開始
        with session.begin():
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()
    # セッションを閉じる
    session.close()
    return "put"


def mydelete(mymodel, customer_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = delete(mymodel).where(mymodel.customer_id == customer_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()

    # セッションを閉じる
    session.close()
    return customer_id + " is deleted"


# 追加した予約関連の操作

# 予約作成
def create_reservation(db: Session, user_id: int, schedule_id: int, consultation_style: str):
    new_reservation = Reservation(
        user_id=user_id,
        schedule_id=schedule_id,
        consultation_style=consultation_style
    )
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation

# 予約一覧取得
def get_reservations(db: Session):
    return db.query(Reservation).all()

# 予約IDで予約を取得
def get_reservation_by_id(db: Session, reservation_id: int):
    return db.query(Reservation).filter(Reservation.reservation_id == reservation_id).first()

# 予約更新
def update_reservation(db: Session, reservation_id: int, schedule_id: int, consultation_style: str):
    reservation = db.query(Reservation).filter(Reservation.reservation_id == reservation_id).first()
    if reservation:
        reservation.schedule_id = schedule_id
        reservation.consultation_style = consultation_style
        db.commit()
        db.refresh(reservation)
        return reservation
    return None

# 予約削除
def delete_reservation(db: Session, reservation_id: int):
    reservation = db.query(Reservation).filter(Reservation.reservation_id == reservation_id).first()
    if reservation:
        db.delete(reservation)
        db.commit()
        return reservation_id
    return None

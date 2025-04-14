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

from db_control.mymodels import QuickDiagnosis
import sqlalchemy
from db_control.mymodels import Presurvey



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

# プレ診断作成
def create_pre_survey(db: Session, reservation_id: int, age_group: str, item_preparation: bool, concern_parts: str, troubles: str, past_experience: str, consultation_goal: str, free_comment: str):
    new_pre_survey = Presurvey(
        reservation_id=reservation_id,
        age_group=age_group,
        item_preparation=item_preparation,
        concern_parts=concern_parts,
        troubles=troubles,
        past_experience=past_experience,
        consultation_goal=consultation_goal,
        free_comment=free_comment
    )
    db.add(new_pre_survey)
    db.commit()
    db.refresh(new_pre_survey)
    return new_pre_survey

# プレ診断取得
def get_pre_survey_by_reservation_id(db: Session, reservation_id: int):
    return db.query(Presurvey).filter(Presurvey.reservation_id == reservation_id).first()

# プレ診断更新
def update_pre_survey(db: Session, survey_id: int, age_group: str, item_preparation: bool, concern_parts: str, troubles: str, past_experience: str, consultation_goal: str, free_comment: str):
    pre_survey = db.query(Presurvey).filter(Presurvey.survey_id == survey_id).first()
    if pre_survey:
        pre_survey.age_group = age_group
        pre_survey.item_preparation = item_preparation
        pre_survey.concern_parts = concern_parts
        pre_survey.troubles = troubles
        pre_survey.past_experience = past_experience
        pre_survey.consultation_goal = consultation_goal
        pre_survey.free_comment = free_comment
        db.commit()
        db.refresh(pre_survey)
        return pre_survey
    return None

# プレ診断削除
def delete_pre_survey(db: Session, survey_id: int):
    pre_survey = db.query(Presurvey).filter(Presurvey.survey_id == survey_id).first()
    if pre_survey:
        db.delete(pre_survey)
        db.commit()
        return survey_id
    return None

# 追加: プレ診断作成
def create_presurvey(db: Session, reservation_id: int, age_group: str, item_preparation: bool, concern_parts: str,
                     troubles: str, past_experience: str, consultation_goal: str, free_comment: str):
    new_presurvey = Presurvey(
        reservation_id=reservation_id,
        age_group=age_group,
        item_preparation=item_preparation,
        concern_parts=concern_parts,
        troubles=troubles,
        past_experience=past_experience,
        consultation_goal=consultation_goal,
        free_comment=free_comment
    )
    db.add(new_presurvey)
    db.commit()
    db.refresh(new_presurvey)
    return new_presurvey

# 追加: プレ診断情報取得
def get_presurveys(db: Session):
    return db.query(Presurvey).all()

# 追加: プレ診断IDでプレ診断を取得
def get_presurvey_by_id(db: Session, survey_id: int):
    return db.query(Presurvey).filter(Presurvey.survey_id == survey_id).first()

# 追加: プレ診断更新
def update_presurvey(db: Session, survey_id: int, age_group: str, item_preparation: bool, concern_parts: str,
                     troubles: str, past_experience: str, consultation_goal: str, free_comment: str):
    presurvey = db.query(Presurvey).filter(Presurvey.survey_id == survey_id).first()
    if presurvey:
        presurvey.age_group = age_group
        presurvey.item_preparation = item_preparation
        presurvey.concern_parts = concern_parts
        presurvey.troubles = troubles
        presurvey.past_experience = past_experience
        presurvey.consultation_goal = consultation_goal
        presurvey.free_comment = free_comment
        db.commit()
        db.refresh(presurvey)
        return presurvey
    return None

# 追加: プレ診断削除
def delete_presurvey(db: Session, survey_id: int):
    presurvey = db.query(Presurvey).filter(Presurvey.survey_id == survey_id).first()
    if presurvey:
        db.delete(presurvey)
        db.commit()
        return survey_id
    return None

# ✅ なりさん追加（4/13）
def create_quick_diagnosis(db: Session, user_id: int, result_summary: str):
    new_diagnosis = QuickDiagnosis(
        user_id=user_id,
        result_summary=result_summary
    )
    db.add(new_diagnosis)
    db.commit()
    db.refresh(new_diagnosis)
    return new_diagnosis

from sqlalchemy import Column, String, Integer, Text, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

# Baseをインポート
Base = declarative_base()

# Userモデル
class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    name_kana = Column(String)
    email = Column(String, unique=True)  # ここはemailでログイン
    password = Column(String)
    birth_date = Column(Date)  # 'Date'型を使う

    # 予約情報とのリレーション
    reservations = relationship("Reservation", back_populates="user")

# コースモデル
class Course(Base):
    __tablename__ = 'course'
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(255))
    # description = Column(Text)  # この行を削除しました

    # スケジュール情報とのリレーション
    schedules = relationship("Schedule", back_populates="course")  # back_populatesで反対側のリレーションを指定

# パートナー（例）
class Partner(Base):
    __tablename__ = 'partner'
    partner_id = Column(Integer, primary_key=True)
    partner_name = Column(String(255))

    # スケジュール情報とのリレーション
    schedules = relationship("Schedule", back_populates="partner")  # back_populatesで反対側のリレーションを指定

# 予約モデル
class Reservation(Base):
    __tablename__ = 'reservation'
    reservation_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    schedule_id = Column(Integer, ForeignKey('schedule.schedule_id'))
    consultation_style = Column(String(255))

    user = relationship("User", back_populates="reservations")
    presurveys = relationship("Presurvey", back_populates="reservation")

# プレ診断モデル
class Presurvey(Base):
    __tablename__ = 'presurvey'
    survey_id = Column(Integer, primary_key=True, autoincrement=True)
    reservation_id = Column(Integer, ForeignKey('reservation.reservation_id'))
    age_group = Column(String(255))
    item_preparation = Column(Boolean)
    concern_parts = Column(Text)
    troubles = Column(Text)
    past_experience = Column(Text)
    consultation_goal = Column(Text)
    free_comment = Column(Text)

    reservation = relationship("Reservation", back_populates="presurveys")

# スケジュールモデル（修正）
class Schedule(Base):
    __tablename__ = 'schedule'
    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('course.course_id'))  # コースID
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    reservation_status = Column(String(20))  # 例: 'open', 'closed', 'booked' など
    partner_id = Column(Integer, ForeignKey('partner.partner_id'))  # パートナーID

    # リレーション
    course = relationship("Course", back_populates="schedules")  # Courseとのリレーション
    partner = relationship("Partner", back_populates="schedules")  # Partnerとのリレーション

# その他のモデル（Customers, Items, Purchases, PurchaseDetails）も同様に定義されている
class Customers(Base):
    __tablename__ = 'customers'
    customer_id = Column(String(10), primary_key=True)
    customer_name = Column(String(100))
    age = Column(Integer)
    gender = Column(String(10))

class Items(Base):
    __tablename__ = 'items'
    item_id = Column(String(10), primary_key=True)
    item_name = Column(String(100))
    price = Column(Integer)

class Purchases(Base):
    __tablename__ = 'purchases'
    purchase_id = Column(String(10), primary_key=True)
    customer_id = Column(String(10))
    purchase_date = Column(String(10))

class PurchaseDetails(Base):
    __tablename__ = 'purchase_details'
    detail_id = Column(String(10), primary_key=True)
    purchase_id = Column(String(10))
    item_id = Column(String(10))
    quantity = Column(Integer)

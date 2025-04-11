from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    name_kana = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    birth_date = Column(Date)

    # 予約情報とのリレーション
    reservations = relationship("Reservation", back_populates="user")

class Reservation(Base):
    __tablename__ = 'reservation'
    reservation_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    schedule_id = Column(Integer)
    consultation_style = Column(String(255))

    # 予約情報に紐づくユーザー情報
    user = relationship("User", back_populates="reservations")

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

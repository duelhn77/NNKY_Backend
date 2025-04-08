# from sqlalchemy import String, Integer
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# # from datetime import datetime


# class Base(DeclarativeBase):
#     pass


# class Customers(Base):
#     __tablename__ = 'customers'
#     customer_id: Mapped[str] = mapped_column(String(10), primary_key=True)
#     customer_name: Mapped[str] = mapped_column(String(100))
#     age: Mapped[int] = mapped_column(Integer)
#     gender: Mapped[str] = mapped_column(String(10))


# class Items(Base):
#     __tablename__ = 'items'
#     item_id: Mapped[str] = mapped_column(String(10), primary_key=True)
#     item_name: Mapped[str] = mapped_column(String(100))
#     price: Mapped[int] = mapped_column(Integer)


# class Purchases(Base):
#     __tablename__ = 'purchases'
#     purchase_id: Mapped[str] = mapped_column(String(10), primary_key=True)
#     customer_id: Mapped[str] = mapped_column(String(10))
#     purchase_date: Mapped[str] = mapped_column(String(10))


# class PurchaseDetails(Base):
#     __tablename__ = 'purchase_details'
#     detail_id: Mapped[str] = mapped_column(String(10), primary_key=True)
#     purchase_id: Mapped[str] = mapped_column(String(10))
#     item_id: Mapped[str] = mapped_column(String(10))
#     quantity: Mapped[int] = mapped_column(Integer)

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    name_kana = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    birth_date = Column(Date)

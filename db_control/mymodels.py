# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from datetime import datetime


# class Base(DeclarativeBase):
#     pass


# class Customers(Base):
#     __tablename__ = 'customers'
#     customer_id: Mapped[str] = mapped_column(primary_key=True)
#     customer_name: Mapped[str] = mapped_column()
#     age: Mapped[int] = mapped_column()
#     gender: Mapped[str] = mapped_column()


# class Items(Base):
#     __tablename__ = 'items'
#     item_id: Mapped[str] = mapped_column(primary_key=True)
#     item_name: Mapped[str] = mapped_column()
#     price: Mapped[int] = mapped_column()


# class Purchases(Base):
#     __tablename__ = 'purchases'
#     purchase_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     purchase_name: Mapped[str] = mapped_column(ForeignKey("customers.customer_id"))
#     date: Mapped[datetime] = mapped_column()


# class PurchaseDetails(Base):
#     __tablename__ = 'purchase_details'
#     purchase_id: Mapped[int] = mapped_column(ForeignKey("purchases.purchase_id"), primary_key=True)
#     item_name: Mapped[str] = mapped_column(ForeignKey("items.item_id"), primary_key=True)
#     quantity: Mapped[int] = mapped_column()

from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import declarative_base
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
from sqlalchemy.orm import MappedColumn, mapped_column
from models.base import Base
from sqlalchemy import Column, ForeignKey, Integer

class Subscription(Base):
    __tablename__ = "subscriptions"
    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)
    user_id: Column[int] = Column(Integer, ForeignKey("users.id"))
    currency_id: Column[int] = Column(Integer, ForeignKey("currencies.id"))


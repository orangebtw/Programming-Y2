from models.base import Base
from sqlalchemy import Column, ForeignKey, Integer

class Subscription(Base):
    __tablename__ = "subscriptions"
    user_id: Column[int] = Column(Integer, ForeignKey("users.id"), primary_key=True)
    currency_id: Column[int] = Column(Integer, ForeignKey("currencies.id"), primary_key=True)


from models.base import Base
from sqlalchemy import Column, String, Integer

class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String)

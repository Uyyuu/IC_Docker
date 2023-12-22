from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .database import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, index=True)
    # authenticated = Column(BOOLEAN, server_default=DefaultClause("false"))

class PredResult(Base):
    __tablename__ = 'pred_result'
    pred_id = Column(Integer, primary_key=True, index=True)
    pred = Column(String)
    date = Column(DateTime, index=True)
    image_path = Column(String)
    caption = Column(String, nullable=True, default=None)
    user_id = Column(Integer, ForeignKey(User.user_id, ondelete='SET NULL'), nullable=False)
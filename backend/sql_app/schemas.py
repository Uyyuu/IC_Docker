import datetime
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str 
    hashed_password: str

class User(UserCreate):
    user_id: int

    class Config:
        orm_mode = True

class PredResultRegister(BaseModel):
    pred: str
    image_path: str
    user_id: int
    caption: Optional[str] = None

class PredResultCreate(PredResultRegister):
    date: datetime.date


class PredResult(PredResultCreate):
    pred_id: int
    
    class Config:
        orm_mode=True
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

class GetPredResult(BaseModel):
    start_number: int
    data_num: int
    user_id: int
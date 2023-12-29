from fastapi import APIRouter, Depends

from typing import List

import sql_app as sq
from sql_app import dps
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/users/create/", response_model=sq.schemas.User, tags=['Users'])
def user_create(user: sq.schemas.UserCreate, db: Session = Depends(dps.get_db)):
    return sq.crud.create_user(db=db, user=user)

@router.get("/users/get/info/", response_model=List[sq.schemas.User], tags=['Users'])
def users_ifno(skip: int = 0, limit: int = 100, db: Session = Depends(dps.get_db)):
    users = sq.crud.get_users(db, skip=skip, limit=limit)
    return users
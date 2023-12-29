from fastapi import FastAPI

from api import auth, pred, user

import sql_app as sq
from sql_app.database import engine


sq.models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(pred.router)
app.include_router(user.router)

# 通信の確認
@app.get('/')
def conect_check():
    return {'message':'Success!'}











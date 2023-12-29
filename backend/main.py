from fastapi import FastAPI, UploadFile, Depends
import auth

from typing import List, Annotated, Optional
import datetime

import torch
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
from CNN_model.model import CNN, DataTransform

import io
from PIL import Image 

import sql_app as sq
from sql_app import dps
from sql_app.database import SessionLocal, engine
from sqlalchemy.orm import Session
from auth import oauth2_scheme


sq.models.Base.metadata.create_all(bind=engine)


# 正解ラベル
classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

n_output: int = len(classes)  
n_hidden: int = 128  

#DataTransformのインスタンス化
transform = DataTransform()
#ネットワークのインスタンス化         
net = CNN(n_output=n_output, n_hidden=n_hidden)
#学習済みパラメータのロード cpuの記述必要
net.load_state_dict(torch.load('model_ver2.0.pth', map_location=torch.device('cpu')))

app = FastAPI()

app.include_router(auth.router)

# 通信の確認
@app.get('/')
def conect_check():
    return {'message':'Success!',}

@app.post("/users/create/", response_model=sq.schemas.User, tags=['Users'])
def user_create(user: sq.schemas.UserCreate, db: Session = Depends(dps.get_db)):
    return sq.crud.create_user(db=db, user=user)

@app.get("/users/get/info/", response_model=List[sq.schemas.User], tags=['Users'])
def users_ifno(skip: int = 0, limit: int = 100, db: Session = Depends(dps.get_db)):
    users = sq.crud.get_users(db, skip=skip, limit=limit)
    return users

async def pred_register(db: Session, pred: str, image_path: str, user_id: int, caption: Optional[str] = None):
    data = sq.schemas.PredResultCreate(
        date = datetime.date.today(),
        pred = pred,
        image_path = image_path,
        user_id = user_id,
        caption=caption
    )
    register_data = sq.crud.create_pred_result(db=db, pred_result=data)
    return register_data

# @app.get("/predictions/history/", response_model=List[sq.schemas.PredResult])
# async def get_pred_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     pred_results = sq.crud.get_pred_results(db, skip=skip, limit=limit)
#     return pred_results

@app.post("/predictions/get/histories/", response_model=List[sq.schemas.PredResult], tags=['Predicitions'])
async def get_pred_history(get_pred: sq.schemas.GetPredResult, db: Session = Depends(dps.get_db)):
    return sq.crud.get_pred_results_by_user_id(db, user_id=get_pred.user_id, skip=get_pred.start_number, limit=get_pred.data_num)
    

# POSTリクエストに対して推論結果を返す
@app.post('/predictions/', tags=['Predicitions'])
async def predict(token: Annotated[str, Depends(oauth2_scheme)], upload_file: UploadFile = (...), db: Session = Depends(dps.get_db)):
    #画像読み込みの処理いまいち理解できてない
    contents = await upload_file.read()
    input = Image.open(io.BytesIO(contents)).convert("RGB")
    input = transform(input)
    input = input.unsqueeze(0)

    print("Input Tensor Size:", input.size())

    #推論モード
    net.eval()

    with torch.no_grad():
        output = net(input)
    
    predicted_class = torch.argmax(output, dim=1)

    return {'result_class': classes[predicted_class]}

@app.post('/predictions/register/', response_model=sq.schemas.PredResult, tags=['Predicitions'])
async def regster_pred_log(pred_result: sq.schemas.PredResultRegister, db: Session = Depends(dps.get_db)):
    # awaitつけたらエラー出なかった
    registre_data = await pred_register(db=db, pred=pred_result.pred, image_path=pred_result.image_path, user_id=pred_result.user_id, caption=pred_result.caption)
    return registre_data

@app.delete('/predctions/delete/{item_id}', tags=['Predictions'])
async def delete_log(item_id: int, db: Session = Depends(dps.get_db)):
    delete_data = sq.crud.delete_predcit_history(db=db, item_id=item_id)
    return delete_data

@app.put('/predictions/update/{item_id}', tags=['Predictions'])
async def update_log(item_id: int, caption: str, db: Session = Depends(dps.get_db)):
    update_data = sq.crud.update_predict_history(db=db, item_id=item_id, caption=caption)
    return update_data


# #アップロードされた画像ファイル名を返すエンドポイントの作成
# @app.post('/uploadfile')
# async def uploadfile(upload_file: UploadFile = (...)):
#     return {
#         'filename': upload_file.filename
#     }

# fastapi-login

# from fastapi.security import OAuth2PasswordRequestForm
# from fastapi_login.exceptions import InvalidCredentialsException
# from fastapi_login import LoginManager
# import os
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import JSONResponse
# from fastapi import status, Request

# SECRET = os.urandom(24).hex()

# manager = LoginManager(SECRET, token_url = '/login')

# @manager.user_loader()
# def load_user(username: str, db: Session = Depends(get_db) ):
#     user = sq.crud.get_user_by_username(username=username, db=db)
#     return user

# @app.post('/login')
# def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     username = data.username
#     password = data.password

#     user = load_user(username=username, db=db)  # we are using the same function to retrieve the user
#     if not user:
#         raise InvalidCredentialsException  # you can also use your own HTTPException
#     elif password != user.password:
#         raise InvalidCredentialsException
    
#     access_token = manager.create_access_token(
#         data=dict(sub=username)
#     )
#     return {'access_token': access_token, 'token_type': 'bearer'}

# @app.exception_handler(RequestValidationError)
# async def handler(request:Request, exc:RequestValidationError):
#     print(exc)
#     return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)








from fastapi import APIRouter, UploadFile, Depends
from . import auth

from typing import List, Annotated, Optional
import datetime

import torch
# import torchvision.transforms as transforms
# import torch.nn as nn
# import torch.nn.functional as F
from CNN_model.model import CNN, DataTransform

import io
from PIL import Image 

import sql_app as sq
from sql_app import dps
from sqlalchemy.orm import Session

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

router = APIRouter()

def pred_register(db: Session, pred: str, image_path: str, user_id: int, caption: Optional[str] = None):
    data = sq.schemas.PredResultCreate(
        date = datetime.date.today(),
        pred = pred,
        image_path = image_path,
        user_id = user_id,
        caption=caption
    )
    register_data = sq.crud.create_pred_result(db=db, pred_result=data)
    return register_data

@router.post("/predictions/get/histories/", response_model=List[sq.schemas.PredResult], tags=['Predicitions'])
def get_pred_history(get_pred: sq.schemas.GetPredResult, db: Session = Depends(dps.get_db)):
    return sq.crud.get_pred_results_by_user_id(db, user_id=get_pred.user_id, skip=get_pred.start_number, limit=get_pred.data_num)
    

# POSTリクエストに対して推論結果を返す
@router.post('/predictions/', tags=['Predicitions'])
async def predict(token: Annotated[str, Depends(auth.oauth2_scheme)], upload_file: UploadFile = (...), db: Session = Depends(dps.get_db)):
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

@router.post('/predictions/register/', response_model=sq.schemas.PredResult, tags=['Predicitions'])
def regster_pred_log(pred_result: sq.schemas.PredResultRegister, db: Session = Depends(dps.get_db)):
    registre_data = pred_register(db=db, pred=pred_result.pred, image_path=pred_result.image_path, user_id=pred_result.user_id, caption=pred_result.caption)
    return registre_data

@router.delete('/predctions/delete/{item_id}', tags=['Predictions'])
def delete_log(item_id: int, db: Session = Depends(dps.get_db)):
    delete_data = sq.crud.delete_predcit_history(db=db, item_id=item_id)
    return delete_data

@router.put('/predictions/update/{item_id}', tags=['Predictions'])
def update_log(item_id: int, caption: str, db: Session = Depends(dps.get_db)):
    update_data = sq.crud.update_predict_history(db=db, item_id=item_id, caption=caption)
    return update_data

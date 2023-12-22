from sqlalchemy.orm import Session
from . import models,schemas
from passlib.context import CryptContext
from fastapi import HTTPException, status


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# パスワードのハッシュ化
def get_password_hash(password):
    return pwd_context.hash(password)


# ユーザー一覧取得
def get_users(db: Session, skip: int=0, limit: int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

# usernameからユーザー情報を取得
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# user_idから予測結果の履歴を取得
def get_pred_results_by_user_id(db: Session, user_id: int, skip: int=0, limit=10):
    existing_data = db.query(models.PredResult).filter(models.PredResult.user_id == user_id).offset(skip).limit(limit).all()
    # if existing_data is Noneだとエラー返さない．おそらくNoneではなくリストになってるから
    if len(existing_data) == 0:
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="履歴はありません．"
               )
    return existing_data

# 予測履歴の削除
def delete_predcit_history(db: Session, item_id: int):
    delet_data = db.query(models.PredResult).filter(models.PredResult.pred_id == item_id).first()
    db.delete(delet_data)
    db.commit()
    return delet_data

# キャプションのアップデート
def update_predict_history(db: Session, item_id: int, caption: str):
    update_data: schemas.PredResult = db.query(models.PredResult).filter(models.PredResult.pred_id == item_id).first()
    update_data.caption = caption
    db.commit()
    return update_data

# ユーザー登録
def create_user(db: Session, user: schemas.UserCreate):
    existing_user = get_user_by_username(db=db, username=user.username)
    if existing_user:
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="すでに使われているユーザー名です．別の名前で登録してください"
               )
    db_user = models.User(username = user.username, hashed_password=get_password_hash(user.hashed_password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 予測結果の登録
def create_pred_result(db: Session, pred_result: schemas.PredResultCreate):
    db_pred_result = models.PredResult(
        date = pred_result.date,
        pred = pred_result.pred,
        image_path = pred_result.image_path,
        caption = pred_result.caption,
        user_id = pred_result.user_id
    )
    db.add(db_pred_result)
    db.commit()
    db.refresh(db_pred_result)
    return db_pred_result

#  予測結果の取得
# def get_pred_results(db:Session, skip: int=0, limit=10):
#     existing_data = db.query(models.PredResult).offset(skip).limit(limit).all()
#     if len(existing_data) == 0:
#         raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail="履歴はありません．"
#                )
#     return existing_data
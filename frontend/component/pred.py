import streamlit as st
import requests
import json
import os
from typing import Optional 

# 画像の予測結果，画像のファイルパスを返す
def pred(url: str, headers: str, image_path: str):
    with st.form(key='pred'):

        uploaded_file = st.file_uploader("Choose a file...", type=["jpg", "png", "jpeg"])

        submit_button = st.form_submit_button(label='予測')

        if uploaded_file is None:
            return None, None
        
        if submit_button:
            st.image(uploaded_file, caption="アップロードされた画像", use_column_width=True)

            files = {'upload_file': (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}
            res = requests.post(url=url, files=files, headers=headers)
            result = res.json()

            image_path = os.path.join(image_path, uploaded_file.name)

            with open(image_path, 'wb') as f:
                f.write(uploaded_file.read())

            if res.status_code == 200:
                st.success(f"予測結果は {result['result_class']} ")
            else:
                st.error(f"Error uploading file: {res.status_code}")

            return res,image_path
       

# 画像の予測結果のログを返す
def pred_result(url: str, headers: str):
    with st.form(key='get_pred_result'):
        start_number: int = st.number_input('取得する最初のデータ',min_value=0, value=0)
        data_num: int = st.number_input('取得するデータの個数',min_value=1, value=10, max_value=20)
        data = {
            'start_number': start_number,
            'data_num': data_num,
            'user_id': st.session_state.user_id
        }

        submit_button = st.form_submit_button(label='決定')

        if submit_button:
            res = requests.post(
                url = url,
                data = json.dumps(data)
            )
            if res.status_code == 200:
                st.success('予測履歴を取得して表示')
                st.json(res.json())

            return res

# 画像の予測結果を登録
def register_pred_result(url: str, pred: str, image_path: str, user_id: int, caption: Optional[str] = None):
    data = {
        'pred': pred,
        'image_path': image_path,
        'user_id': user_id,
        'caption': caption
    }
    res = requests.post(
        url=url,
        data = json.dumps(data)
    )

    if res.status_code == 200:
        st.success('登録しました')
    else:
        st.error('登録失敗しました')

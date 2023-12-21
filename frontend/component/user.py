import streamlit as st
import requests
import json

def login(url: str):
    # st.title("ログイン画面")

    with st.form(key='login'):
        username: str = st.text_input('ユーザー名', max_chars=12)
        password: str = st.text_input('パスワード', type='password')
        # ログインのリクエストの時はjsonにしない(form data)
        data = {
            'username': username,
            'password': password
        }
        submit_button = st.form_submit_button(label='ログイン')

    res = None

    if submit_button:
        url = url
        res = requests.post(
                url,
                data = data
            )
        if res.status_code == 200:
            st.success('ログイン成功')
            # st.json(res.json())
        else:
            st.error('ログイン失敗')
    
    return res
    
def create_user(url: str):
    # st.title('ユーザ登録画面')
    with st.form(key='user_register'):
        username: str = st.text_input('ユーザー名', max_chars=12)
        password: str = st.text_input('パスワード', type='password')
        data = {
            'username': username,
            'hashed_password': password
        }
        submit_button = st.form_submit_button(label='登録')
    
    res = None

    if submit_button:
        url = url
        res = requests.post(
                url,
                data = json.dumps(data)
            )
        if res.status_code == 200:
            st.success('ユーザー登録完了')
    
    return res

def get_current_user_id(url: str, headers: str):
    res = requests.get(
        url=url,
        headers=headers
    )

    return res
import streamlit as st
from component.user import login, create_user, get_current_user_id
from component.pred import pred, pred_result, register_pred_result
from component.session import page_change_to_pred_log, logout, login2create_user, create_user2login
import pandas as pd

if "token" not in st.session_state:
    st.session_state.token = None

if "is_login" not in st.session_state:
    st.session_state.is_login = True 

if "pred_class" not in st.session_state:
    st.session_state.pred_class = None

if "image_path" not in st.session_state:
    st.session_state.image_path = None

url_login = 'http://api:8080/login/'
url_create_user = 'http://api:8080/users/create/'
url_pred = 'http://api:8080/predictions/'
url_pred_result = 'http://api:8080/predictions/get/histories/'
url_pred_register = 'http://api:8080/predictions/register/'
url_get_user_id = 'http://api:8080/users/get/user_id/'

IMG_PATH = './Images'

if st.session_state.token is None and st.session_state.is_login == True:
    st.title('ログイン')

    res = login(url = url_login)

    button_create_user = st.button('新規ユーザー登録', on_click=login2create_user)

    if button_create_user:
        st.session_state.is_login = False
    
    if res is not None:
        if res.status_code == 200:
            st.session_state.token = res.json()
            st.button('アプリへ移動')
        else:
            st.session_state.token = None

elif st.session_state.token is None and st.session_state.is_login == False:
    st.title('新規ユーザー登録')

    res = create_user(url = url_create_user)

    if res is not None:
        if res.status_code == 400:
            error_message = res.json()['detail']
            st.error(error_message)

        elif res.status_code == 200:
            st.session_state.is_login = True
            
            username = res.json()['username']
            st.success(f"ユーザー名：{username}")
        
        st.button('ログイン画面へ', on_click=create_user2login)
    
elif st.session_state.token is not None:
    st.title('アプリ画面')
    page = st.sidebar.selectbox('ページを選択',['画像予測','予測履歴'], key='page')
    st.sidebar.button('ログアウト', on_click=logout)

    st.session_state.headers = {'Authorization':f'Bearer {st.session_state.token["access_token"]}'}

    user_id = get_current_user_id(url=url_get_user_id, headers=st.session_state.headers).json()['user_id']
    st.session_state.user_id = user_id

    if page == '画像予測':
        st.subheader('画像分類')

        # pred()をif文で分岐させたらformが消えちゃう
        # ここどうにかしないと，予想だけど，結果を登録ボタン押した時にスクリプト再実行されておかしくなってる気がする．on_clickとかで設定すればいい？

        if st.session_state.pred_class is None:
            res, st.session_state.image_path = pred(url = url_pred, headers=st.session_state.headers, image_path=IMG_PATH)

            if res is not None:
                st.session_state.pred_class = res.json()['result_class']
        
        if st.session_state.pred_class is not None:
            caption: str = st.text_input('画像に対するキャプション(任意)')
            pred_reg_button = st.button('予測結果を登録')

            if pred_reg_button:
                if st.session_state.pred_class is None:
                    st.error('登録内容がありません')
                else:
                    register_pred_result(
                        url=url_pred_register, 
                        pred=st.session_state.pred_class,
                        image_path=st.session_state.image_path,
                        user_id=st.session_state.user_id,
                        caption=caption
                    )
                    st.session_state.pred_class = None
                    st.session_state.image_path = None
                    # st.session_state.caption = None
                
                st.button('推論結果を見る', on_click=page_change_to_pred_log)
                st.button('もう一度画像を入力')
                
    elif page == '予測履歴':
        st.subheader('予測履歴')

        res = pred_result(url=url_pred_result, headers=st.session_state.headers)

        if res is not None:
            if res.status_code == 400:
                error_message = res.json()['detail']
                st.error(error_message)
            
            elif res.status_code == 200:
                pred_results = res.json()

                df = pd.DataFrame(pred_results)

                # 選択した列だけ表示
                selected_columns = ["date", "pred", "caption", "image_path","pred_id"]
                df_selected = df[selected_columns]

                df_selected.index = range(1, len(df_selected) + 1)

                st.data_editor(
                    df_selected,
                    column_config={
                        "caption": st.column_config.TextColumn(
                            width = "large"
                        ),
                        "image_path": st.column_config.ImageColumn(
                            "Preview Image", help="Streamlit app preview screenshots"
                        ),
                    },
                    disabled=["date", "pred", "caption"],
                    hide_index=True,
                )

    

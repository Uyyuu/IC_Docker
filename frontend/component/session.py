import streamlit as st

# ページ遷移の管理
def page_change_to_pred_log():
    st.session_state.page = '予測履歴'

def login2create_user():
    st.session_state.is_login = False

def create_user2login():
    st.session_state.is_login = True

def logout():
    st.session_state.token = None
    # st.rerun() ←いらない
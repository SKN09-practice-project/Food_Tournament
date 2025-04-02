import streamlit as st

for key in list(st.session_state.keys()):
    del st.session_state[key]

st.set_page_config(page_title="🍽️ 음식 이상형 월드컵", page_icon="🥘")

st.title("🏠 음식 월드컵 시작하기")

round_options = [4, 8, 16]
selected_round = st.selectbox("플레이할 라운드를 선택하세요:", round_options)

if st.button("게임 시작"):
    st.session_state.round = selected_round
    st.session_state.winner = {}

    st.switch_page("pages/main.py")



    

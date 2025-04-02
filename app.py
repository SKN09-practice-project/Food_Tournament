import streamlit as st

st.set_page_config(page_title="🍽️ 음식 이상형 월드컵", page_icon="🥘")

st.title("🏠 음식 월드컵 시작하기")

# ✅ 선택 라운드
round_options = [4, 8, 16]
selected_round = st.selectbox("플레이할 라운드를 선택하세요:", round_options)

# ✅ 게임 시작 버튼
if st.button("게임 시작"):
    # ✅ 세션 전부 초기화
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    # ✅ 선택된 라운드만 다시 세팅
    st.session_state.round = selected_round
    st.switch_page("pages/main.py")

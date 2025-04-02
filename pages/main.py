import streamlit as st
import random
from game_logic import create_brackets, match_candidates
import time
import os

# 이미지 폴더 설정
image_folder = "food_images"
image_files = [f for f in os.listdir(image_folder) if f.endswith(".jpg")]

candidates = [
    {"name": os.path.splitext(img)[0], "image": f"{image_folder}/{img}"}
    for img in image_files
]

# 라운드 수 확인 (없으면 안내)
if "round" not in st.session_state:
    st.warning("홈 화면에서 라운드를 먼저 선택해 주세요.")
    st.stop()

round_num = st.session_state.round

# 초기 세션 상태 설정
if "bracket" not in st.session_state:
    st.session_state.bracket = create_brackets(round_num, candidates)
    st.session_state.matchups = match_candidates(st.session_state.bracket)
    st.session_state.round_index = 0
    st.session_state.selected = []
    st.session_state.current_round = round_num

# 라운드명 설정
st.session_state.current_round_name = (
    "결승전" if st.session_state.current_round == 2 else f"{st.session_state.current_round}강"
)

st.subheader(f"{st.session_state.current_round_name} - {st.session_state.round_index + 1}번째 경기")

# 경기 진행
if st.session_state.round_index < len(st.session_state.matchups):
    pair = st.session_state.matchups[st.session_state.round_index]
    col1, col2 = st.columns(2)

    def select_winner(winner):
        st.session_state.selected.append(winner)
        st.session_state.round_index += 1

        # 현재 라운드 종료 시
        if st.session_state.round_index >= len(st.session_state.matchups):
            if len(st.session_state.selected) == 1:
                # ✅ 결승전 끝나면 바로 결과 페이지로 전환
                st.session_state.bracket = st.session_state.selected
                st.session_state.winner = st.session_state.selected[0]
                st.switch_page("pages/game_result.py")

            else:
                # 다음 라운드 세팅
                st.session_state.bracket = st.session_state.selected
                st.session_state.matchups = match_candidates(st.session_state.bracket)
                st.session_state.selected = []
                st.session_state.round_index = 0
                st.session_state.current_round //= 2

        time.sleep(0.3)
        st.rerun()

    # 왼쪽 음식
    with col1:
        st.image(pair[0]['image'], use_container_width=True)
        if st.button(pair[0]['name']):
            select_winner(pair[0])

    # 오른쪽 음식 (있을 경우만)
    if len(pair) > 1:
        with col2:
            st.image(pair[1]['image'], use_container_width=True)
            if st.button(pair[1]['name']):
                select_winner(pair[1])

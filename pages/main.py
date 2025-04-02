import streamlit as st
import random
from game_logic import create_brackets, match_candidates
import time 
import os


# food_images 폴더 경로
image_folder = "food_images"

# 이미지 파일 목록 가져오기
image_files = [f for f in os.listdir(image_folder) if f.endswith(".jpg")]

# candidates 리스트 생성
candidates = [
    {"name": os.path.splitext(img)[0], "image": f"{image_folder}/{img}"}
    for img in image_files
]

# 예시 라운드 수 선택 
round_num = st.session_state.round 



# 세션 초기화 
if "bracket" not in st.session_state:
    st.session_state.bracket = create_brackets(round_num, candidates)
    st.session_state.matchups = match_candidates(st.session_state.bracket)
    st.session_state.round_index = 0
    st.session_state.selected = []
    st.session_state.current_round = round_num
    st.session_state.current_round_name = f"{round_num}강"

# 현재 라운드 정보 업데이트
st.session_state.current_round_name = "결승전" if st.session_state.current_round == 2 else f"{st.session_state.current_round}강"

st.subheader(f"{st.session_state.current_round_name} - {st.session_state.round_index + 1}번째 경기")


# 경기 진행
if st.session_state.round_index < len(st.session_state.matchups):
    pair = st.session_state.matchups[st.session_state.round_index]
    col1, col2 = st.columns(2)

    def select_winner(winner):
        st.session_state.selected.append(winner)
        st.session_state.round_index += 1

        if st.session_state.round_index >= len(st.session_state.matchups):  # 라운드 종료 시
            if len(st.session_state.selected) == 1:  
                st.session_state.bracket = st.session_state.selected

            else: 
                st.session_state.bracket = st.session_state.selected
                st.session_state.matchups = match_candidates(st.session_state.bracket)
                st.session_state.selected = []
                st.session_state.round_index = 0
                st.session_state.current_round //= 2  # 다음 라운드로 이동
        
        time.sleep(0.3)  
        st.rerun()

    # 왼쪽 후보
    with col1:
        st.image(pair[0]['image'], use_container_width=True)
        if st.button(pair[0]['name']):
            select_winner(pair[0])

    # 오른쪽 후보 
    if len(pair) > 1:
        with col2:
            st.image(pair[1]['image'], use_container_width=True)
            if st.button(pair[1]['name']):
                select_winner(pair[1])

# {st.session_state.bracket[0]['name']} # 최종 우승 
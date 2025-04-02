import streamlit as st
import random
from game_logic import create_brackets, match_candidates
import time 

# 예시 이미지들 
candidates = [
    {"name": "피자", "image": "https://cdn.pixabay.com/photo/2023/07/20/19/42/flower-8140215_1280.jpg"},
    {"name": "버거", "image": "https://images.pexels.com/photos/68507/spring-flowers-flowers-collage-floral-68507.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"},
    {"name": "1", "image": "https://cdn.pixabay.com/photo/2023/07/20/19/42/flower-8140215_1280.jpg"},
    {"name": "2", "image": "https://images.pexels.com/photos/68507/spring-flowers-flowers-collage-floral-68507.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"},
    {"name": "3", "image": "https://cdn.pixabay.com/photo/2023/07/20/19/42/flower-8140215_1280.jpg"},
    {"name": "4", "image": "https://images.pexels.com/photos/68507/spring-flowers-flowers-collage-floral-68507.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"},
    {"name": "5", "image": "https://cdn.pixabay.com/photo/2023/07/20/19/42/flower-8140215_1280.jpg"},
    {"name": "6", "image": "https://images.pexels.com/photos/68507/spring-flowers-flowers-collage-floral-68507.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"},
    {"name": "7", "image": "https://cdn.pixabay.com/photo/2023/07/20/19/42/flower-8140215_1280.jpg"},
    {"name": "8", "image": "https://images.pexels.com/photos/68507/spring-flowers-flowers-collage-floral-68507.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"},
    {"name": "9", "image": "https://images.pexels.com/photos/68507/spring-flowers-flowers-collage-floral-68507.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"},
    {"name": "10", "image": "https://cdn.pixabay.com/photo/2023/07/20/19/42/flower-8140215_1280.jpg"}
] # 12개


# 예시 라운드 수 선택 
round_num = 4  # 초기 라운드 (4강)



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
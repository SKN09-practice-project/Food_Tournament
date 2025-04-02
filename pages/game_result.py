import streamlit as st
from PIL import Image
import os
import json

# 📁 랭킹 데이터 불러오기
def load_ranking_from_file(filename="ranking_data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# 💾 랭킹 데이터 저장하기
def save_ranking_to_file(data, filename="ranking_data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 🖼️ 이미지 로딩 함수 (예외 처리 포함)
def load_image_with_fallback(image_path, fallback_text="이미지를 불러올 수 없습니다."):
    try:
        image = Image.open(image_path)
        st.image(image, use_container_width=True)
    except Exception:
        st.warning(fallback_text)

# 🔁 다시하기 버튼 동작 (세션 초기화)
def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.switch_page("app.py")

# ✅ 우승자 정보 확인
if "winner" not in st.session_state or not st.session_state.winner:
    st.warning("최종 우승자 정보가 없습니다. 게임을 먼저 진행해주세요.")
    if st.button("🏠 홈으로 가기"):
        st.switch_page("app.py")
    st.stop()

# 📌 winner 정보 추출
winner = st.session_state.winner
winner_name = winner["name"]
image_path = winner.get("image", "")  # image_url → image로 키 맞춤

# 🏆 결과 출력
st.title("🍽️ 최종 결과")
st.subheader("🎉 당신의 최애 음식은...")
st.markdown(f"## 🏆 **{winner_name}** 입니다!")
load_image_with_fallback(image_path)

# 📊 랭킹 업데이트 (중복 방지)
if "ranking_updated" not in st.session_state:
    ranking = load_ranking_from_file()
    
    if winner_name in ranking:
        ranking[winner_name]["count"] += 1
    else:
        ranking[winner_name] = {
            "count": 1,
            "image_url": image_path
        }

    save_ranking_to_file(ranking)
    st.session_state.ranking_updated = True  # ✅ 중복 저장 방지용 플래그

# 버튼 영역
col1, col2 = st.columns(2)
with col1:
    if st.button("🔁 다시 하기"):
        reset_game()

with col2:
    if st.button("📊 랭킹 보기"):
        st.switch_page("pages/rank_result.py")

import streamlit as st
from PIL import Image
from pathlib import Path
import json

def load_ranking_from_file(filename="ranking_data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_ranking_to_file(data, filename="ranking_data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_image_with_fallback(image_url, fallback_text="이미지를 불러올 수 없습니다."):
    try:
        image = Image.open(Path(image_url))
        st.image(image, use_container_width=True)
    except Exception:
        st.warning(fallback_text)


def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.switch_page("app.py")


if "winner" not in st.session_state:
    st.session_state.winner = {
        "name": "떡볶이",
        "image_url": "./img/떡볶이.png"
    }

winner = st.session_state.winner

st.title("🍽️ 최종 결과")
st.subheader("🎉 당신의 최애 음식은...")
st.markdown(f"## 🏆 **{winner['name']}** 입니다!")

load_image_with_fallback(winner.get("image_url", ""))

ranking = load_ranking_from_file()
winner_name = winner["name"]
image_url = winner.get("image_url", "")

if winner_name in ranking:
    ranking[winner_name]["count"] += 1
else:
    ranking[winner_name] = {
        "count": 1,
        "image_url": image_url
    }

save_ranking_to_file(ranking)


col1, col2 = st.columns(2)

with col1:
    if st.button("🔁 다시 하기"):
        reset_game()

with col2:
    if st.button("📊 랭킹 보기"):
        st.switch_page("pages/rank_result.py")
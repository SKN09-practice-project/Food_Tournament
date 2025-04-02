import streamlit as st
from PIL import Image
from pathlib import Path

if "winner" not in st.session_state:
    st.session_state.winner = {
        "name": "떡볶이",
        "image_url": "./img/떡볶이.png"
    }

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

winner = st.session_state.winner

st.title("🍽️ 최종 결과")
st.subheader("🎉 당신의 최애 음식은...")
st.markdown(f"## 🏆 **{winner['name']}** 입니다!")

load_image_with_fallback(winner.get("image_url", ""))

if st.button("🔁 다시 하기"):
    reset_game()

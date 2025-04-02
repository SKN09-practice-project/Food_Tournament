import streamlit as st
import json
import os
from PIL import Image

# JSON 파일 로드
json_file_path = "food_name_image_pairs.json"

if os.path.exists(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as file:
        food_image_list = json.load(file)
else:
    st.error(f"JSON 파일을 찾을 수 없습니다: {json_file_path}")
    st.stop()

# '햄버거' 항목 찾기
hamburger_entry = next((item for item in food_image_list if item["name"] == "햄버거"), None)

if hamburger_entry:
    image_path = hamburger_entry["image"]
    # 이미지 파일이 존재하는지 확인 후 표시
    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, caption="햄버거", use_column_width=True)
    else:
        st.error(f"이미지 파일을 찾을 수 없습니다: {image_path}")
else:
    st.error("JSON 데이터에 '햄버거' 항목이 없습니다.")

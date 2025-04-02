import streamlit as st
import streamlit.components.v1 as components
import base64
import json
from math import ceil

def image_to_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

def load_ranking_from_file(filename="ranking_data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

col_title, col_home = st.columns([6, 1])
with col_title:
    st.title("🏆 음식 인기 순위표")
with col_home:
    st.page_link("app.py", label=" ", icon="🏠", use_container_width=True)


ranking = load_ranking_from_file()

if not ranking:
    st.warning("랭킹 데이터가 없습니다. 게임을 먼저 진행해 주세요.")
    st.stop()

sorted_items = sorted(ranking.items(), key=lambda x: x[1]["count"], reverse=True)

ITEMS_PER_PAGE = 5
total_items = len(sorted_items)
total_pages = ceil(total_items / ITEMS_PER_PAGE)

if "current_page" not in st.session_state:
    st.session_state.current_page = 1

page = st.session_state.current_page
start = (page - 1) * ITEMS_PER_PAGE
end = start + ITEMS_PER_PAGE
paginated_items = sorted_items[start:end]

total_count = sum([v["count"] for _, v in ranking.items()])
start_rank = start + 1
end_rank = min(end, total_items)

st.markdown(f"### 🧾 음식 순위 ({start_rank}위 ~ {end_rank}위)")

table_html = f"""
<style>
table {{
  width: 100%;
  border-collapse: collapse;
}}
th, td {{
  padding: 10px;
  text-align: center;
  border: 1px solid #ddd;
}}
img {{
  width: 70px;
  border-radius: 8px;
}}
</style>
<table>
<tr>
  <th>순위</th>
  <th>이미지</th>
  <th>이름</th>
  <th>선택 횟수</th>
  <th>비율</th>
</tr>
"""

for i, (name, data) in enumerate(paginated_items, start=start + 1):
    count = data["count"]
    percent = (count / total_count) * 100
    img_base64 = image_to_base64(data["image_url"])
    img_html = f'<img src="data:image/png;base64,{img_base64}">' if img_base64 else "❌"
    bar_html = f"""
    <div style='background:#eee; width:100px; margin:auto;'>
      <div style='background:#ff6b6b; width:{percent:.1f}%; padding:2px; color:white; font-size:12px;'>
        {percent:.1f}%
      </div>
    </div>
    """

    table_html += f"""
    <tr>
        <td>{i}</td>
        <td>{img_html}</td>
        <td><b>{name}</b></td>
        <td>{count}</td>
        <td>{bar_html}</td>
    </tr>
    """

table_html += "</table>"

components.html(table_html, height=650, scrolling=True)

col1, col_spacer, col2 = st.columns([1, 5, 1])
with col1:
    st.button("⬅️ 이전", disabled=(page <= 1), on_click=lambda: st.session_state.__setitem__('current_page', page - 1))
with col2:
    st.button("다음 ➡️", disabled=(page >= total_pages), on_click=lambda: st.session_state.__setitem__('current_page', page + 1))

st.markdown(f"<div style='text-align: center; color: gray; font-size: 14px;'>페이지 {page} / {total_pages}</div>", unsafe_allow_html=True)

if st.button("🏠 홈으로 가기"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.switch_page("app.py")
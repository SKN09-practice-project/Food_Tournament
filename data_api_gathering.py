import requests
import os
import json
from urllib.parse import quote
from dotenv import load_dotenv

# .env 파일에서 API 키 로드
load_dotenv()
API_KEY = os.getenv("PIXABAY_API_KEY")

# 이미지 저장 디렉토리 생성
save_dir = "food_images"
os.makedirs(save_dir, exist_ok=True)

# 필터링 함수: 태그에 음식 관련 키워드 포함 여부 확인
def is_food_image(hit):
    tags = hit.get("tags", "").lower()
    return any(word in tags for word in ["food", "meal", "dish", "cuisine", "lunch", "dinner", "breakfast"])

food_pairs = [
    # 기존 목록 (디저트 제외)
    ("피자", "Pizza"),
    ("햄버거", "Burger"),
    ("파스타", "Pasta"),
    ("스테이크", "Steak"),
    ("초밥", "Sushi"),
    ("타코", "Tacos"),
    ("라자냐", "Lasagna"),
    ("치킨 윙", "Chicken Wings"),
    ("샌드위치", "Sandwich"),
    ("핫도그", "Hot Dog"),
    ("파에야", "Paella"),
    ("부리토", "Burrito"),
    ("치킨 커리", "Chicken Curry"),
    ("팟타이", "Pad Thai"),
    ("쌀국수", "Pho"),
    ("딤섬", "Dim Sum"),
    ("훠궈", "Hot Pot"),
    ("스시 롤", "Sushi Roll"),
    ("타코야키", "Takoyaki"),
    ("야키소바", "Yakisoba"),
    ("텐동", "Tendon"),
    ("나시고랭", "Nasi Goreng"),
    ("미고랭", "Mie Goreng"),
    ("사테이", "Satay"),
    ("그린 커리", "Green Curry"),
    ("레드 커리", "Red Curry"),
    ("마살라 도사", "Masala Dosa"),
    ("팔라펠", "Falafel"),
    ("케밥", "Kebab"),
    ("무사카", "Moussaka"),
    ("차우멘", "Chow Mein"),
    ("볶음밥", "Fried Rice"),
    ("카르보나라", "Carbonara"),
    ("볼로네제", "Bolognese"),
    ("리조또", "Risotto"),
    # 추가된 한식 및 아시아 요리
    ("비빔밥", "Bibimbap"),
    ("떡볶이", "Tteokbokki"),
    ("잡채", "Japchae"),
    ("김밥", "Kimbap"),
    ("해물파전", "Haemul Pajeon"),
    ("감자탕", "Gamjatang"),
    ("부대찌개", "Budae Jjigae"),
    ("갈비찜", "Galbijjim"),
    ("닭갈비", "Dak Galbi"),
    ("오징어볶음", "Ojingeo Bokkeum")
]


food_data = []

for kor_name, eng_query in food_pairs:
    query = quote(eng_query)
    url = f"https://pixabay.com/api/?key={API_KEY}&q={query}&image_type=photo&category=food&per_page=5"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"[❌] {kor_name}: API 요청 실패 (status: {response.status_code})")
            continue

        res = response.json()
        hits = res.get('hits', [])

        # 음식 관련 태그만 필터링
        food_hits = [hit for hit in hits if is_food_image(hit)]

        if food_hits:
            image_url = food_hits[0]['webformatURL']
            image_data = requests.get(image_url).content

            filename = os.path.join(save_dir, f"{kor_name}.jpg")
            with open(filename, "wb") as f:
                f.write(image_data)

            food_data.append({
                "name": kor_name,
                "image": filename
            })

            print(f"[✔] {kor_name} 저장 완료: {image_url}")
        else:
            print(f"[✘] {kor_name}: 음식 관련 이미지 없음")

    except Exception as e:
        print(f"[⚠] {kor_name} 에러: {e}")

# JSON으로 저장
with open("food_name_image_pairs.json", "w", encoding="utf-8") as f:
    json.dump(food_data, f, ensure_ascii=False, indent=2)

print("\n[📁] food_name_image_pairs.json 저장 완료 ✅")

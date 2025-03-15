import json
import os
from data.stringify import stringify

# JSON 디렉토리 설정
JSON_DIR = "json"
JSON_FILE = os.path.join(JSON_DIR, "news_data.json")

# 디렉토리가 없으면 생성
if not os.path.exists(JSON_DIR):
    os.makedirs(JSON_DIR)

# json 포맷으로 저장 (하나의 파일에 배열 형태로 저장)
def json_save(news_list):
    if not news_list:  # 뉴스가 없을 경우 경고 메시지 출력
        print("⚠️ json 변환할 크롤링된 뉴스가 없습니다.")
        return

    print("\n📢 JSON 변환 시작...")

    # 기존 파일이 있다면 데이터 로드 (새로운 뉴스와 합치기 위해)
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)  # 기존 데이터 불러오기
                if not isinstance(existing_data, list):  # 기존 데이터가 리스트가 아니면 초기화
                    existing_data = []
            except json.JSONDecodeError:
                existing_data = []  # 파일이 비어있거나 오류가 있을 경우 초기화
    else:
        existing_data = []  # 파일이 없으면 새로운 리스트 생성

    # 새로운 뉴스 데이터를 변환하여 기존 데이터와 합치기
    new_data = [stringify(news) for news in news_list]
    all_data = existing_data + new_data  # 기존 데이터 + 새로운 데이터

    # JSON 파일로 저장
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    print(f"\n✅ JSON 파일 저장 완료: {JSON_FILE}")
    print(f"📝 총 {len(all_data)}개의 뉴스 기사가 저장되었습니다.")

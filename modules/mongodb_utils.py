from pymongo import MongoClient, ASCENDING

# MongoDB 연결 및 데이터베이스 선택
mongo_client = MongoClient("mongodb://localhost:27017/") # 로컬 MongoDB 서버에 연결
mongo_db = mongo_client["rappit_news_db"] # 사용할 데이터베이스

# 두 버전의 컬렉션 정의
raw_collection = mongo_db["news_articles_raw"] # 가공 전 원본 뉴스 데이터를 저장할 컬렉션
indexed_collection = mongo_db["news_articles_indexed"] # 정제 및 인덱싱된 뉴스 데이터를 저장할 컬렉션

# 인덱스 설정 (indexed 컬렉션에만 적용)
indexed_collection.create_index("url", unique=True) # URL 중복 방지를 위한 유일 인덱스
indexed_collection.create_index([("press.name", ASCENDING)]) # 언론사명 기준 오름차순 정렬 인덱스
indexed_collection.create_index([("published_at", ASCENDING)]) # 발행일 기준 오름차순 정렬 인덱스
indexed_collection.create_index([("categories", ASCENDING)]) # 카테고리(섹션) 기준 정렬 인덱스

# MongoDB 저장 함수 (두 컬렉션에 저장)
def save_to_mongodb(
    news_list # 크롤링한 뉴스 객체 리스트
):
    # 저장할 뉴스가 없을 경우 메시지 출력 후 종료
    if not news_list:
        print("⛔ 저장할 뉴스 데이터가 없습니다.")
        return

    raw_count = 0 # news_articles_raw에 저장된 뉴스 개수
    indexed_count = 0 # news_articles_indexed에 저장된 뉴스 개수

    # 크롤링한 뉴스 리스트를 반복
    for news in news_list:
        doc = news.to_dict() # News 객체를 딕셔너리 형태로 변환

        # 중복 URL 방지 (indexed 컬렉션 기준으로 중복 체크) 
        if indexed_collection.find_one({"url": news.url}):
            continue

        try:
            raw_collection.insert_one(doc) # news_articles_raw 컬렉션에 뉴스 문서를 저장 (원본 그대로 저장)
            indexed_collection.insert_one(doc) # news_articles_indexed 커렉션에 뉴스 문서를 저장 (검색 및 정렬 최적화를 위해 인덱스 적용)
            raw_count += 1 # raw 저장 카운터 증가
            indexed_count += 1 # indexed 저장 카운터 증가
        except Exception as e:
            print(f"❌ 뉴스 저장 실패: {e}") # 저장 실패 시 예외 메시지 출력

    # 저장 결과 춫력
    print(f"✅ news_articles_raw: {raw_count}개 저장 완료") 
    print(f"✅ news_articles_indexed: {indexed_count}개 저장 완료")

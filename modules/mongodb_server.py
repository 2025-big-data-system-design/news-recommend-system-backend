from pymongo import MongoClient, ASCENDING

# MongoDB 연결 및 컬렉션 선택
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["rappit_news_db"]

# 두 버전의 컬렉션
raw_collection = mongo_db["news_articles_raw"]
indexed_collection = mongo_db["news_articles_indexed"]

# 🔑 인덱스 설정 (indexed 컬렉션에만 적용)
indexed_collection.create_index("url", unique=True)
indexed_collection.create_index([("press.name", ASCENDING)])
indexed_collection.create_index([("published_at", ASCENDING)])
indexed_collection.create_index([("categories", ASCENDING)])

# MongoDB 저장 함수 (두 컬렉션에 저장)
def save_to_mongodb(news_list):
    if not news_list:
        print("⛔ 저장할 뉴스 데이터가 없습니다.")
        return

    raw_count = 0
    indexed_count = 0

    for news in news_list:
        doc = news.to_dict()

        # ⛔ 중복 URL 방지 (indexed 컬렉션 기준)
        if indexed_collection.find_one({"url": news.url}):
            continue

        try:
            raw_collection.insert_one(doc)       # 정제되지 않은 원본 저장
            indexed_collection.insert_one(doc)   # 인덱스 최적화된 컬렉션 저장
            raw_count += 1
            indexed_count += 1
        except Exception as e:
            print(f"❌ 뉴스 저장 실패: {e}")

    print(f"✅ news_articles_raw: {raw_count}개 저장 완료")
    print(f"✅ news_articles_indexed: {indexed_count}개 저장 완료")

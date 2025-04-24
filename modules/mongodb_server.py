# MongoDB 관련 import
from pymongo import MongoClient # MongoDB 클라이언트 객체 생성용 import

# MongoDB 초기화
mongo_client = MongoClient("mongodb://localhost:27017/") # MongoDB 클라이언트 생성 (로컬 MongoDB 서버에 연결)
mongo_db = mongo_client["rappit_news_db"] # 사용할 데이터베이스 선택 (news_crawler_db가 없으면 자동으로 생성)
news_collection = mongo_db["news_articles"] # 사용할 컬렉션 선택 (news_article가 없으면 자동으로 생성)

# MongoDB에 저장하는 함수 (중복 URL 방지, to_dict() 사용)
def save_to_mongodb(news_list):
    if not news_list:
        print("⛔ 저장할 뉴스 데이터가 없습니다.")
        return

    inserted_count = 0  # 저장된 뉴스 수 카운트용

    for news in news_list:
        # 뉴스 URL이 이미 존재하는지 확인
        if news_collection.find_one({"url": news.url}):
            continue  # 이미 저장된 뉴스는 skip

        try:
            news_dict = news.to_dict()  # ✅ 클래스 내 to_dict 메서드 사용
            news_collection.insert_one(news_dict)
            inserted_count += 1
        except Exception as e:
            print(f"❌ 뉴스 저장 실패: {e}")

    print(f"✅ MongoDB에 새 뉴스 {inserted_count}개 저장 완료!")


from pymongo import MongoClient

# MongoDB 클라이언트 연결
client = MongoClient("mongodb://localhost:27017/big_data")  # 로컬 MongoDB 연결
db = client["crawler"]  # 사용할 데이터베이스
collection = db["article"]  # 저장할 컬렉션(테이블)

# JSON 데이터를 MongoDB에 삽입
collection.insert_one(news_json)

print("✅ MongoDB에 뉴스 데이터 저장 완료!")

# MongoDB 관련 라이브러리
from pymongo import MongoClient # MongoDB 데이터베이스 연결

# MongoDB 연결 및 데이터베이스 선택
mongo_client = MongoClient("mongodb://localhost:27017/") # 로컬 MongoDB 서버에 연결
mongo_db = mongo_client["rappit_news_db"] # 사용할 데이터베이스

# 사용할 컬렉션 선택
raw_collection = mongo_db["news_articles_raw"] # 인덱싱되지 않은 컬렉션
indexed_collection = mongo_db["news_articles_indexed"] # 인덱싱된 컬렉션
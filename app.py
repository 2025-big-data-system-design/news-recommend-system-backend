# 기본 라이브러리
import time # API 요청 처리 소요 시간을 측정하기 위해 사용

# Flask 관련 라이브러리 
from flask import Flask, jsonify, request # Flask 웹 서버를 생성하고, JSON 응답 및 HTTP 요청 파라미터를 처리하기 위해 사용

# MongoDB 관련 라이브러리
from pymongo import MongoClient # MongoDB 데이터베이스 연결
from bson import ObjectId # MongoDB의 ObjectId를 문자열로 변환하여 JSON 직렬화 시 사용

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

# MongoDB 연결 및 데이터베이스 선택
mongo_client = MongoClient("mongodb://localhost:27017/") # 로컬 MongoDB 서버에 연결
mongo_db = mongo_client["rappit_news_db"] # 사용할 데이터베이스

raw_collection = mongo_db["news_articles_raw"] # 인덱싱되지 않은 컬렉션
indexed_collection = mongo_db["news_articles_indexed"] # 인덱싱된 컬렉션

# ObjectId를 문자열로 변환
def serialize_doc(
    doc # MongoDB에서 조회한 단일 문서 (dict 형태)
):
    doc["_id"] = str(doc["_id"]) # _id 필드를 문자열로 변환
    return doc # 변환된 문서를 반환

# news_articles_raw 컬렉션의 모든 뉴스 문서를 조회
@app.route("/api/news/raw/all", methods=["GET"])
def get_all_news_raw():
    start_time = time.time() # API 요청 처리 시작 시간 기록

    # news_articles_raw 컬렉션에서 모든 문서를 조회
    news_list = list(raw_collection.find()) 
    
    # 조회한 문서들의 ObjectId를 문자열로 반환
    serialized = [serialize_doc(doc) for doc in news_list] 

    # API 처리 소요 시간을 밀리초(ms) 단위로 계산
    elapsed = round((time.time() - start_time) * 1000, 2)  
    
    return jsonify({
        "count": len(serialized), # 반환한 뉴스 문서 수
        "elapsed_ms": elapsed, # 조회 처리 시간
        "data": serialized # 변환된 뉴스 문서 리스트
    })

# news_articles_raw 컬렉션의 뉴스 문서를 페이지 단위로 조회
@app.route("/api/news/raw", methods=["GET"])
def get_news_raw_by_page():
    try:
        # 요청 쿼리 파라미터에서 page 번호를 가져오고, 기본값은 1로 설정
        page = int(request.args.get("page", 1))
        # 요청 쿼리 파라미터에서 페이지당 문서 수(size)를 가져오고, 기본값은 10으로 설정
        size = int(request.args.get("size", 10))
        if page < 1 or size < 1:
            raise ValueError # page나 size가 1 미만이면 잘못된 요청으로 판단

        start_time = time.time() # API 요청 처리 시작 시간 기록

        skip = (page - 1) * size # 건너뛸 문서 수 계산
        
        # news_articles_raw 컬렉션에서 페이지 범위에 맞게 문서 조회
        news_list = list(raw_collection.find().skip(skip).limit(size)) 
        
        # 조회된 문서들의 ObjectId를 문자열로 변환
        serialized = [serialize_doc(doc) for doc in news_list]
        
        # API 처리 소요 시간을 밀리초(ms) 단위로 계산
        elapsed = round((time.time() - start_time) * 1000, 2)
        return jsonify({
            "count": len(serialized), # 변환된 뉴스 문서 수
            "elapsed_ms": elapsed, # 조회 처리 시간
            "data": serialized # 변환된 뉴스 문서 리스트
        })
    except ValueError:
        # page나 size가 유효하지 않다고 에러 응답
        return jsonify({"error": "Invalid 'page' or 'size' parameter"}), 400

# news_articles_indexed 컬렉션의 모든 뉴스 문서를 조회
@app.route("/api/news/indexed/all", methods=["GET"])
def get_all_news_indexed():
    start_time = time.time() # API 요청 처리시작 시간 기록

    # news_articles_indexed 컬렉션에서 모든 문서를 조회
    news_list = list(indexed_collection.find())
    
    # 조회한 문서들의 ObjectId를 문자열로 변환
    serialized = [serialize_doc(doc) for doc in news_list]

    # API 처리 소요 시간을 밀리초(ms) 단위로 계산
    elapsed = round((time.time() - start_time) * 1000, 2)
    return jsonify({
        "count": len(serialized), # 반환된 뉴스 문서 수
        "elapsed_ms": elapsed, # 조회 처리 시간
        "data": serialized # 변환된 뉴스 문서 리스트
    })

# news_articles_indexed 컬렉션의 뉴스 문서를 페이지 단위로 조회
@app.route("/api/news/indexed", methods=["GET"])
def get_news_indexed_by_page():
    try:
        # 요청 쿼리 파라미터에서 page 번호를 가져오고, 기본값은 1로 설정
        page = int(request.args.get("page", 1))
        # 요청 쿼리 파라미터에서 페이지당 문서 수(size)를 가져오고, 기본값은 10으로 설정
        size = int(request.args.get("size", 10))
        
        if page < 1 or size < 1: # page나 size가 1 미만이면
            raise ValueError # 잘못된 요청으로 판단

        start_time = time.time() # API 요청 처리 시작 시간을 기록

        skip = (page - 1) * size # 건너뛸 문서 수 계산
        
        # news_articles_indexed 컬렉션에서 페이지 범위에 맞게 문서 조회
        news_list = list(indexed_collection.find().skip(skip).limit(size))
        # 조회한 문서들의 ObjectId를 문자열로 변환
        serialized = [serialize_doc(doc) for doc in news_list]

        # API 처리 소요 시간을 밀리초(ms) 단위로 계산
        elapsed = round((time.time() - start_time) * 1000, 2)
        return jsonify({
            "count": len(serialized), # 반환된 뉴스 문서 수 
            "elapsed_ms": elapsed, # 조회 처리 시간
            "data": serialized # 변환된 뉴스 문서 리스트
        })
    except ValueError:
        return jsonify({"error": "Invalid 'page' or 'size' parameter"}), 400

# 언론사 이름 필드를 기준으로 각각의 처리 성능 비교
@app.route("/api/news/perf/press", methods=["GET"])
def compare_press_query_perf():
    # 요청 쿼리 파라미터에서 언론사명(name)을 가져옴
    press_name = request.args.get("name", None) 
    if not press_name: # 언론사명이 없는 경우
        # 에러 반환
        return jsonify({"error": "Query parameter 'name' is required"}), 400

    # raw 컬렉션의 검색 및 처리 시간 측정
    start_raw = time.time() # raw 조회 시간 기록
    raw_result = list(raw_collection.find({"press.name": press_name})) # news_articles_raw 컬렉션에서 press.name 조건으로 조회
    raw_elapsed = round((time.time() - start_raw) * 1000, 2) # raw 컬렉션 처리 소요 시간을 밀리초(ms)로 계산

    # indexed 컬렉션의 검색 및 처리 시간 측정
    start_idx = time.time() # indexed 조회 시간 기록
    idx_result = list(indexed_collection.find({"press.name": press_name})) # news_articles_indexed 컬렉션에서 press.name 조건으로 조회
    idx_elapsed = round((time.time() - start_idx) * 1000, 2) # indexed 컬렉션 처리 소요 시간을 밀리초(ms)로 계산

    # raw vs indexed 결과를 JSON 형태로 비교 반환
    return jsonify({
        "query": {"press.name": press_name}, # 사용된 쿼리 조건
        "raw": {
            "count": len(raw_result), # raw 컬렉션에서 조회된 문서 수
            "elapsed_ms": raw_elapsed # raw 컬렉션 조회 소요 시간 (ms)
        },
        "indexed": {
            "count": len(idx_result), # indexed 컬렉션에서 조회된 문서 수
            "elapsed_ms": idx_elapsed # indexed 컬렉션 조회 소요 시간
        }
    })
    
if __name__ == "__main__":
    app.run(debug=True)

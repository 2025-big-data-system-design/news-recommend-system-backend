# 기본 라이브러리
import time # API 요청 처리 소요 시간을 측정하기 위해 사용

# Flask 관련 라이브러리 
from flask import Blueprint, jsonify, request # Flask 웹 서버를 생성하고, JSON 응답 및 HTTP 요청 파라미터를 처리하기 위해 사용

# 내부 모듈 import
from db import raw_collection
from utils.serialize import serialize_doc

# Blueprint 생성
raw_news_bp = Blueprint('raw_news', __name__, url_prefix='/api/news/raw')

# news_articles_raw 컬렉션의 모든 뉴스 문서를 조회
# ex) http://localhost:5000/api/news/raw/all
@raw_news_bp.route("/all", methods=["GET"])
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
# ex) http://localhost:5000/api/news/raw?page=1&size=100
@raw_news_bp.route("", methods=["GET"])
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

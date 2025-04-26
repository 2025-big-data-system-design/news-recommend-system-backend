# 기본 라이브러리
import time # API 요청 처리 소요 시간을 측정하기 위해 사용

# Flask 관련 라이브러리 
from flask import Blueprint, jsonify, request # Flask 웹 서버를 생성하고, JSON 응답 및 HTTP 요청 파라미터를 처리하기 위해 사용

# 내부 모듈 import
from db import indexed_collection
from utils.serialize import serialize_doc

# Blueprint 생성
indexed_news_bp = Blueprint('indexed_news', __name__, url_prefix='/api/news/indexed')

# news_articles_indexed 컬렉션의 모든 뉴스 문서를 조회
# ex) http://localhost:5000/api/news/indexed/all
@indexed_news_bp.route("/all", methods=["GET"])
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
# ex) http://localhost:5000/api/news/indexed?page=1&size=100
@indexed_news_bp.route("", methods=["GET"])
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
    
# 뉴스 필터링 및 검색 API
# ex) http://localhost:5000/api/news/indexed/search?page=1&size=10&sortOption=최신순&selectedCategory=IT/과학&selectedPress=조선일보,중앙일보&query=인공지능&queryMode=title_content
@indexed_news_bp.route("/search", methods=["GET"])
def search_news_indexed():
    try:
        # 쿼리 파라미터 파싱
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 10))
        sort_option = request.args.get("sortOption", "최신순")
        selected_category = request.args.get("selectedCategory", "전체")
        selected_press = request.args.get("selectedPress", "") # 쉼표로 구분된 문자열
        query = request.args.get("query", "")
        query_mode = request.args.get("queryMode", "title_content")

        if page < 1 or size < 1:
            raise ValueError

        # MongoDB 검색 조건 준비
        filter_query = {}

        # 카테고리 필터링
        if selected_category and selected_category != "전체":
            filter_query["categories"] = selected_category

        # 언론사 필터링
        if selected_press:
            press_list = selected_press.split(",")
            filter_query["press.name"] = {"$in": press_list}

        # 키워드 검색 (제목, 내용 포함 설정)
        if query:
            if query_mode == "title":
                filter_query["title"] = {"$regex": query, "$options": "i"}
            elif query_mode == "content":
                filter_query["content.text"] = {"$regex": query, "$options": "i"}
            else:  # title_content
                filter_query["$or"] = [
                    {"title": {"$regex": query, "$options": "i"}},
                    {"content.text": {"$regex": query, "$options": "i"}}
                ]

        # 정렬 옵션 설정
        sort_field = "published_at" # 기본은 최신순
        sort_order = -1 # 내림차순
        if sort_option == "최신순":
            sort_field = "published_at"
            sort_order = -1
        elif sort_option == "오래된순":
            sort_field = "published_at"
            sort_order = 1
        # (필요하면 나중에 인기순 같은 것도 추가 가능)

        start_time = time.time()

        skip = (page - 1) * size

        # MongoDB 쿼리 실행
        cursor = indexed_collection.find(filter_query).sort(sort_field, sort_order).skip(skip).limit(size)
        news_list = list(cursor)

        serialized = [serialize_doc(doc) for doc in news_list]
        elapsed = round((time.time() - start_time) * 1000, 2)

        # 총 개수 (필터링된 전체 수)
        total_count = indexed_collection.count_documents(filter_query)

        return jsonify({
            "count": len(serialized),
            "total": total_count,
            "elapsed_ms": elapsed,
            "data": serialized
        })

    except ValueError:
        return jsonify({"error": "Invalid 'page' or 'size' parameter"}), 400

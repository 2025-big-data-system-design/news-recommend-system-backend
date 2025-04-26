# 기본 라이브러리
import time # API 요청 처리 소요 시간을 측정하기 위해 사용

# Flask 관련 라이브러리
from flask import Blueprint, jsonify # Flask Blueprint, JSON 응답

# 내부 모듈 import
from db import indexed_collection # 인덱싱된 뉴스 컬렉션 사용

# Blueprint 생성
category_bp = Blueprint('category', __name__, url_prefix='/api/category')

# news_articles_indexed 컬렉션에서 카테고리 목록 조회
# ex) http://localhost:5000/api/category/all
@category_bp.route("/all", methods=["GET"])
def get_all_categories():
    start_time = time.time() # API 요청 처리 시작 시간 기록

    # aggregate 파이프라인 정의
    pipeline = [
        {
            "$group": {
                "_id": "$categories", # ✅ 뉴스 문서의 categories 배열 기준으로 그룹화
            }
        },
        {
            "$unwind": "$_id" # ✅ 배열 풀어헤치기
        },
        {
            "$group": {
                "_id": "$_id" # ✅ 개별 카테고리로 다시 그룹화
            }
        },
        {
            "$project": {
                "_id": 0,
                "name": "$_id" # ✅ _id → name으로 변환
            }
        },
        {
            "$sort": {
                "name": 1 # 이름 오름차순 정렬
            }
        }
    ]

    category_list = list(indexed_collection.aggregate(pipeline)) # Aggregate 쿼리 실행

    elapsed = round((time.time() - start_time) * 1000, 2) # API 처리 소요 시간

    return jsonify({
        "count": len(category_list), # 반환된 카테고리 수
        "elapsed_ms": elapsed, # 처리 시간
        "data": category_list # 카테고리 목록
    })

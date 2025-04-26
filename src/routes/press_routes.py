# 기본 라이브러리
import time # API 요청 처리 소요 시간을 측정하기 위해 사용

# Flask 관련 라이브러리
from flask import Blueprint, jsonify # Flask Blueprint, JSON 응답

# 내부 모듈 import
from db import indexed_collection # 인덱싱된 뉴스 컬렉션 사용
from utils.serialize import serialize_doc # 필요하면 (안 써도 됨)

# Blueprint 생성
press_bp = Blueprint('press', __name__, url_prefix='/api/press')

# news_articles_indexed 컬렉션에서 언론사 목록 조회
# ex) http://localhost:5000/api/press/all
@press_bp.route("/all", methods=["GET"])
def get_all_press_info():
    start_time = time.time() # API 요청 처리 시작 시간 기록

    # aggregate 파이프라인 정의
    pipeline = [
        {
            "$group": {
                "_id": "$press.name", # 언론사 이름을 기준으로 그룹화
                "logo": {"$first": "$press.logo"} # 언론사 로고는 첫 번째 값 사용
            }
        },
        {
            "$project": {
                "_id": 0, # _id 제거
                "name": "$_id", # _id를 name으로 치환
                "logo": 1 # 로고 포함
            }
        },
        {
            "$sort": {
                "name": 1 # 이름 오름차순 정렬
            }
        }
    ]

    press_list = list(indexed_collection.aggregate(pipeline)) # Aggregate 쿼리 실행

    elapsed = round((time.time() - start_time) * 1000, 2) # API 처리 소요 시간

    return jsonify({
        "count": len(press_list), # 반환된 언론사 수
        "elapsed_ms": elapsed, # 처리 시간
        "data": press_list # 언론사 목록
    })

# MongoDB 관련 라이브러리
from bson import ObjectId # MongoDB의 ObjectId를 문자열로 변환하여 JSON 직렬화 시 사용

# ObjectId를 문자열로 변환
def serialize_doc(
    doc # MongoDB에서 조회한 단일 문서 (dict 형태)
):
    doc["_id"] = str(doc["_id"]) # _id 필드를 문자열로 변환
    return doc # 변환된 문서를 반환

# 기본 라이브러리
import re # 정규 표현식을 사용하여 텍스트 전처리 수행
import os, sys, json

# 텍스트 처리 및 머신러닝 모듈
from sklearn.feature_extraction.text import TfidfVectorizer # TfidVectorization: TF-IDF 벡터화를 수행하여 키워드 추출

# 한글 형태소 분석 모듈
from konlpy.tag import Okt # 한글 형태소 분석기 (명사 추출 수행)

# 현재 파일 기준으로 data 폴더의 절대 경로를 추가
current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일이 위치한 디렉토리
parent_dir = os.path.dirname(current_dir)  # 상위 디렉토리 (프로젝트 루트)
data_path = os.path.join(parent_dir, "data")  # data 폴더 경로
model_path = os.path.join(parent_dir, "models") # model 폴더 경로로
json_path = os.path.join(parent_dir, "json", "news_data.json")  # JSON 파일 경로

sys.path.append(data_path)  # data 폴더를 Python 모듈 검색 경로에 추가
sys.path.append(model_path) # model 폴더를 aPython 모듈 검색 경로에 추가

# 프로젝트 내 데이터 모듈
from sample_news import sample_news  # 샘플 뉴스 객체 가져오기
from stopwords import STOPWORDS  # 불용어 리스트 불러오기

# JSON 파일 로드 함수
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)  # JSON 파일을 파이썬 객체로 변환
    return data

# 한글 형태소 분석기 객체 생성
okt = Okt()

# 텍스트 전처리
def preprocess_text(text):
    text = re.sub(r"[^가-힣\s]", "", text)  # 한글과 공백 이외의 문자 제거
    words = okt.nouns(text)  # 명사 추출

    # 불용어 및 한 글자 단어 제거
    filtered_words = [word for word in words if len(word) > 1 and word not in STOPWORDS]

    return " ".join(filtered_words)  # 공백으로 연결된 문자열 반환 (TF-IDF에서 사용하기 위함)

# TF-IDF를 이용하여 키워드 추출
def extract_keywords(
    text, # 입력 테스트 (뉴스 기사 본문)
    top_n=10 # 상위 몇 개의 키워드를 추출할지 결정
):
    processed_text = preprocess_text(text)  # 텍스트 전처리

    # 벡터라이저 초기화 및 TF-IDF 벡터 변환
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([processed_text])
    
    # 각 단어의 TF-IDF 점수 가져오기
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    # TF-IDF 점수가 높은 순서대로 정렬
    keyword_scores = sorted(zip(feature_names, scores), key=lambda x: x[1], reverse=True)

    # 상위 top_n개의 키워드 추출
    keywords = [word for word, score in keyword_scores[:top_n]]

    return keywords # 중요 키워드 리스트 반환

# 샘플 뉴스 본문에서 키워드 추출
# keywords = extract_keywords(sample_news.content, top_n=10)

# # 결과 출력
# print("🔥 중요 키워드 (TF-IDF 기준 상위 10개):")
# print(keywords)

# JSON 파일 불러오기
news_data = load_json(json_path)

# 각 뉴스 기사에서 중요 키워드 추출 (최대 5개 뉴스만 테스트)
for i, doc in enumerate(news_data):
    keywords = extract_keywords(doc["content"], top_n=15)
    print(f"\n🔥 뉴스 중요 키워드드 {i+1} 키워드: {keywords}")



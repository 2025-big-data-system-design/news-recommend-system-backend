# 기본 라이브러리
import re # 정규 표현식을 사용하여 텍스트 전처리 수행

# 텍스트 처리 및 머신러닝 모듈
from sklearn.feature_extraction.text import TfidfVectorizer # TfidVectorization: TF-IDF 벡터화를 수행하여 키워드 추출

from data.stopwords import STOPWORDS

# 한글 형태소 분석 모듈
from konlpy.tag import Okt # 한글 형태소 분석기 (명사 추출 수행)

from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

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

def summarize_news(text, max_length=512, summary_length=100):
    # KoBART 모델 로드
    tokenizer = PreTrainedTokenizerFast.from_pretrained("digit82/kobart-summarization")
    model = BartForConditionalGeneration.from_pretrained("digit82/kobart-summarization")
    
    # 입력 텍스트 토큰화
    inputs = tokenizer([text], max_length=max_length, return_tensors="pt", truncation=True)

    # 요약 생성
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=summary_length,
        min_length=30,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )

    # 디코딩하여 텍스트로 반환
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
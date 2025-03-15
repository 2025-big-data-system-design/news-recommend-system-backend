# 기본 라이브러리
import time # 크롤링 시 페이지 로딩을 기다리기 위해 사용

# Seleniu 관련 모듈
from selenium.webdriver.common.by import By # 웹 요소를 선택할 때 사용 (CSS Selector 등)

# 프로젝트 내 모듈
from modules.webdriver import create_webdriver # Selenium WebDriver를 생성하는 함수
from data.config import CATEGORY_URLS # 뉴스 카테고리별 URL을 설정한 설정 파일
from modules.extractor import ( # 데이터 추출 함수 (크롤링한 웹페이지에서 특정 데이터를 추출)
    extract_news_title, # 뉴스 제목
    extract_news_content, # 뉴스 본문 내용 추출
    extract_press_name, # 언론사(신문사) 이름 추출
    extract_news_date, # 뉴스 발행 날짜 추출
    extract_reporter_name,  # 기자 이름 추출
    extract_thumbnail # 뉴스 썸네일 이미지 URL 추출
)

# 데이터 모델 모듈
from models.news import News # 크롤링한 뉴스 정보를 객체로 관리하는 클래스

# 출력 관련 모듈 (크롤링된 뉴스 정보를 보기 쉽게 출력)
from modules.printer import (
    print_news_details, # 크롤링한 뉴스 링크 목록 출력
    print_news_links # 크롤링한 뉴스 기사 상세 정보 출력 
)

def crawl_all_news_links(
    max_links=30 # 각 카테고리별 최대 크롤링할 뉴스 링크 개수
):
    all_news_links = {} # 모든 뉴스 링크를 저장할 딕셔너리
    total_news_cnt = 0 # 전체 크롤링된 뉴스 개수

    # 1차 카테고리(primary_category)를 반복하며, 하위 2차 카테고리(secondary) 카테고리까지 해당하는 뉴스 링크 크롤링
    # "정치" (1차 카테고리) → "메인", "국회", "청와대" (2차 카테고리)
    for primary_category, secondary_categories in CATEGORY_URLS.items():  
        primary_category_news_cnt = 0 # 현재 1차 카테고리에서 크롤링된 뉴스 개수 

        # 각 2차 카테고리(secondary_category)를 순회하며 뉴스 링크를 크롤링
        for secondary_category, url in secondary_categories.items():
            if secondary_category == "메인": # 메인 카테고리의 경우, 헤드라인 뉴스 크롤링 실행
                news_links = crawl_headline_news_links(primary_category, max_links)
            else: # 그 외의 카테고리인 경우 크롤링 패스 (추후 수정)
                news_links = []

            # 크롤링된 뉴스 링크를 딕셔너리에 저장
            all_news_links[f"{primary_category} > {secondary_category}"] = news_links
            secondary_category_news_cnt = len(news_links) # 현재 2차 카테고리에서 크롤링된 뉴스 개수
            primary_category_news_cnt += secondary_category_news_cnt # 1차 카테고리에서 크롤링된 뉴스 개수 업데이트
            total_news_cnt += secondary_category_news_cnt # 전체 뉴스 개수 업데이트

            # 뉴스 크롤링 완료 메시지 출력
            print(f"✅ {primary_category} > {secondary_category} 뉴스 {secondary_category_news_cnt}개 크롤링 완료!") 

        # 특정 1차 카테고리에 해당하는 뉴스 개수 출력
        print(f"\n📊 {primary_category} 카테고리 총 {primary_category_news_cnt}개 크롤링 완료!\n" + "=" * 60)

    # 전체 뉴스 개수 출력
    print(f"\n🎯 총 {total_news_cnt}개의 뉴스 링크 크롤링 완료!\n" + "=" * 60)

    return all_news_links # 크롤링된 뉴스 링크 딕셔너리 반환

# 주어진 1차 카테고리의 메인에서 헤드라인 뉴스 링크를 크롤링
def crawl_headline_news_links(
    primary_category, 
    max_links=30 # 각 카테고리별 최대 크롤링할 뉴스 링크 개수
):
    # 주어진 1차 카테고리가 CATEGORY_URLS에 존재하는지 확인
    if primary_category not in CATEGORY_URLS:
        print(f"❌ {primary_category} 카테고리는 존재하지 않습니다.")
        return []
    
    driver = create_webdriver() # 웹 드라이버 생성
    news_links = [] # 크롤링된 뉴스 링크 리스트
    
    try:
        category_url = CATEGORY_URLS[primary_category]["메인"] # 해당 1차 카테고리의 "메인" URL 가져오기
        print(f"🔍 {primary_category} 헤드라인 뉴스 크롤링 중...") 
        driver.get(category_url) # 페이지 이동
        time.sleep(3) # 페이지 로딩 대기
        
        # 헤드라인 뉴스 기사 링크 가져오기
        news_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/mnews/article/']")
        for news in news_elements:
            link = news.get_attribute("href") # 해당 뉴스 기사 요소의 href 속성 추출
            # 뉴스 댓글 URL은 제외하고 뉴스 기사 URL인지 확인
            if link and link.startswith("https://n.news.naver.com/mnews/article/") and "comment" not in link:
                if link not in news_links: # 중복 링크 방지
                    news_links.append(link) # 뉴스 링크 리스트에 추가

            if len(news_links) >= max_links:  # 최대 크롤링 개수를 초과하면 종료
                break
        
    finally:
        driver.quit() # 웹 드라이버 종료
        
    return news_links # 크롤링된 뉴스 링크 리스트 반환

# 여러 개의 뉴스 기사에서 상세 정보를 크롤링
def crawl_multiple_news_details(news_urls):
    driver = create_webdriver() # 웹 드라이버 생성
    all_news_details = [] # 뉴스 정보 저장 리스트

    try:
        # 입력된 뉴스 URL 리스트를 순회하며 크롤링
        for url in news_urls:
            driver.get(url) # 해당 뉴스 페이지로 이동
            
            # 뉴스 기사 주요 정보 추출
            news_title = extract_news_title(driver) # 제목 추출
            news_content = extract_news_content(driver) # 본문 내용 추출
            press_name = extract_press_name(driver) # 신문사 이름 추출
            news_date = extract_news_date(driver) # 뉴스 작성 날짜 추출
            reporter_name = extract_reporter_name(driver) # 기자 이름 추출
            thumbnail = extract_thumbnail(driver) # 썸네일 이미지 URL 추출
            
            # 크롤링한 데이터를 기반으로 News 객체 생성
            news = News(url, news_title, news_content, press_name, news_date, reporter_name, thumbnail)
            all_news_details.append(news) # 뉴스 정보 리스트에 추가
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}") # 오류 발생 시 메시지 출력
    finally:
        driver.quit() # 웹 드라이버 종료

    return all_news_details  # 크롤링된 뉴스 객체 리스트 반환
        
if __name__ == "__main__":
    # 1. 모든 카테고리에서 뉴스 링크 크롤링
    news_links = crawl_all_news_links(max_links=1) # 각 카테고리별 최대 1개의 뉴스 링크 크롤링 (테스트용)
    print_news_links(news_links) # 크롤링된 뉴스 링크 목록 출력

    # 2. 크롤링한 뉴스 링크들을 이용해 뉴스 상세 정보 가져오기
    all_links = [link for links in news_links.values() for link in links] # 크롤링된 모든 뉴스 링크를 리스트로 반환
    if all_links: # 크롤링된 뉴스 링크가 비어있지 않은 경우
        print("\n📰 뉴스 기사 상세 정보 크롤링 중...")
        news_details = crawl_multiple_news_details(all_links) # 뉴스 상세 정보 크롤링 수행
        print_news_details(news_details) # 크롤링된 뉴스 기사 정보를 출력
    else: # 크롤링된 뉴스 링크가 없을 경우 경고 메시지 출력
        print("⚠️ 크롤링된 뉴스 링크가 없습니다.")
# Selenium 관련 모듈
from selenium.webdriver.common.by import By # 웹 요소를 CSS Selector 등으로 선택할 때 사용

# 정규 표현식 관련 모듈
import re # 이메일 등 텍스트에서 패턴 기반 추출을 위해 사용

# 주어진 CSS 선택자로 요소의 텍스트를 추출
def extract_element_text(
    driver, # Selenium WebDriver 객체
    selector, # CSS 선택자 문자열 (ex. div.title)
    default="값 없음" # 요소가 없을 경우 반환할 기본값
):
    try: 
        # 해당 selector에 해당하는 요소를 찾기
        element = driver.find_element(By.CSS_SELECTOR, selector)
        
        # 요소가 존재하면 텍스트를 반환, 없으면 기본값 반환
        return element.text if element else default
    
    except Exception:
        # 예외 발생시 (요소 없음, DOM 접근 오류 등) 기본값 반환
        return default
    
# 주어진 CSS 선택자로 요소의 특정 속성을 추출
def extract_element_attribute(
    driver, # Selenium Webdriver 객체
    selector, # CSS 선택자 문자열
    attribute, # 추출할 속성 이름 
    default="값 없음" # 요소나 속성이 없을 경우 기본값
):
    try:
        # 해당 selector에 해당하는 요소를 찾기
        element = driver.find_element(By.CSS_SELECTOR, selector)
        # 요소가 존재하면 속성 값 반환, 없으면 기본 값 반환
        return element.get_attribute(attribute) if element else default
    except Exception:
        # 예외 발생 (요소 없음, 속성 없음, DOM 오류 등) 기본값 반환
        return default
    
# 제목 추출 (단순 값)
def extract_news_title(
    driver # Seleniuum WebDriver 객체
):
    # 뉴스 제목을 CSS 선택지로 추출, 없을 경우 "제목 없음" 반환
    return extract_element_text(driver, "h2.media_end_head_headline > span", "제목 없음")

# 요약문(리드) 추출 (단순 값)
def extract_news_summary(
    driver # Selenium WebDriver 객체
):
    # 요약문(기사 서두에 있는 요약)을 CSS 선택자를 추출, 없을 경우 "요약 없음" 반환
    return extract_element_text(driver, "strong.media_end_summary", "요약 없음")

# 본문 내용 추출 (기사 본문의 HTML, 텍스트, 문단 리스트)
def extract_news_content(
    driver # Selenium WebDriver 객체
):
    # 본문 영역의 HTML을 그대로 추출
    html = extract_element_attribute(driver, "article#dic_area", "innerHTML", "")
    # 본문 영역의 텍스트만 추출
    text = extract_element_text(driver, "article#dic_area", "본문 없음")
    
    # 텍스트를 줄바꿈 기준으로 문단 단위로 분리한 리스트 생성
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    
    return {
        "html": html, # 본문 HTML 원본
        "text": text, # 전체 텍스트 내용
        "paragraphs": paragraphs # 문단 리스트
    }

# 언론사 정보 추출 (언론사의 이름과 로고)
def extract_press_info(
    driver # Selenium WebDriver 객체
):
    # 언론사 이름을 먼저 'title' 속성에서 추출
    name = extract_element_attribute(driver, "img.media_end_head_top_logo_img", "title", None)
    
    # 'title' 속성이 없는 경우 'alt' 속성을 대신 사용
    if not name:
        name = extract_element_attribute(driver, "img.media_end_head_top_logo_img", "alt", "신문사 없음")
    
    # 언론사 로고 이미지의 src 속성 추출 (로고 URL)
    logo = extract_element_attribute(driver, "img.media_end_head_top_logo_img", "src", "")
    return {
        "name": name, # 언론사 이름 (예: 중앙일보, KBS)
        "logo": logo # 언론사 로고 이미지 URL
    }

# 기자 정보 추출 (기자 이름, 이메일, 프로필 정보)
def extract_reporter_info(
    driver # Selenium WebDriver 객체
):
    # 기자 이름 추출 (em 태그에서 기자 이름이 포함된 텍스트 추출)
    name = extract_element_text(driver, "em.media_end_head_journalist_name", "기자 없음")
    
    # 기자 이메일 추출 (이메일은 일반적으로 'span.byline_s' 내부에 포함)
    email = extract_element_text(driver, "span.byline_s", "")  # 이메일 전체 문자열 추출
    
    # 정규 표현식을 사용하여 이메일 형식만 추출
    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email)
    email = email_match.group() if email_match else "이메일 없음" # 유효한 이메일이 없으면 기본값
    
    # 기사 프로필 이미지 URL 추출
    profile = extract_element_attribute(driver, ".media_journalistcard_summary_photo_inner_img", "src", "")
    
    # 추출한 정보를 딕셔너리 형태로 변환
    return {
        "name": name, # 기자 이름
        "email": email, # 기자 이메일
        "profile_image": profile # 기자 프로필 이미지 URL
    }

# 대표 이미지(썸네일) 추출 (단순 값)
def extract_thumbnail(
    driver # Selenium WebDriver 객체
):
    # 뉴스 본문 내 이미지 요소 중 가장 대표적인 이미지를 선택해서 src 속성 값을 반환
    return extract_element_attribute(driver, "div.newsct_body img", "src", "이미지 없음")

# 뉴스 발행일 추출 (텍스트)
def extract_news_date(
    driver # Selenium WebDriver 객체
):
    # 발행일 텍스트를 추출 (예: "2025.04.24. 오후 9:21")
    return extract_element_text(driver, "span.media_end_head_info_datestamp_time", "날짜 없음")

# 카테고리 태그 추출 (값 배열)
def extract_categories(
    driver # Selenium WebDriver 객체
):
    try:
        # 카테고리 태그에 해당하는 모든 요소를 선택
        elements = driver.find_elements(By.CSS_SELECTOR, ".media_end_categorize_item")
        # 텍스트가 비어있지 않은 항목만 리스트로 변환
        return [el.text.strip() for el in elements if el.text.strip()]
    except Exception:
        # 예외 발생 시 빈 리스트 반환
        return []
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
def extract_element_attribute(driver, selector, attribute, default="값 없음"):
    try:
        element = driver.find_element(By.CSS_SELECTOR, selector)
        return element.get_attribute(attribute) if element else default
    except Exception:
        return default
    
# 제목 추출 (단순 값)
def extract_news_title(driver):
    return extract_element_text(driver, "h2.media_end_head_headline > span", "제목 없음")

# 요약문(리드) 추출 (단순 값)
def extract_news_summary(driver):
    return extract_element_text(driver, "strong.media_end_summary", "요약 없음")

# 본문 내용 추출 (문서형: HTML, 텍스트, 문단 리스트, 개체명은 추후 NLP에서 추출)
def extract_news_content(driver):
    html = extract_element_attribute(driver, "article#dic_area", "innerHTML", "")
    text = extract_element_text(driver, "article#dic_area", "본문 없음")
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    # entities는 나중에 NLP로 처리, 일단 빈 리스트
    return {
        "html": html,
        "text": text,
        "paragraphs": paragraphs,
        "entities": []
    }

# 언론사 정보 추출 (문서형: name + logo)
def extract_press_info(driver):
    name = extract_element_attribute(driver, "img.media_end_head_top_logo_img", "title", None)
    if not name:
        name = extract_element_attribute(driver, "img.media_end_head_top_logo_img", "alt", "신문사 없음")
    logo = extract_element_attribute(driver, "img.media_end_head_top_logo_img", "src", "")
    return {
        "name": name,
        "logo": logo
    }

# 기자 정보 추출 (문서형: name + 이메일 + 프로필 이미지)
def extract_reporter_info(driver):
    name = extract_element_text(driver, "em.media_end_head_journalist_name", "기자 없음")
    email = extract_element_text(driver, "span.byline_s", "")  # 정규식으로 후처리 필요
    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email)
    email = email_match.group() if email_match else "이메일 없음"
    profile = extract_element_attribute(driver, ".media_journalistcard_summary_photo_inner_img", "src", "")
    return {
        "name": name,
        "email": email,
        "profile_image": profile
    }

# 대표 이미지(썸네일) 추출 (단순 값)
def extract_thumbnail(driver):
    return extract_element_attribute(driver, "div.newsct_body img", "src", "이미지 없음")

# 발행일 추출 (단순 값 - ISO 형식으로 변환 가능)
def extract_news_date(driver):
    return extract_element_text(driver, "span.media_end_head_info_datestamp_time", "날짜 없음")

# 카테고리 태그 추출 (값 배열)
def extract_categories(driver):
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, ".media_end_categorize_item")
        return [el.text.strip() for el in elements if el.text.strip()]
    except Exception:
        return []
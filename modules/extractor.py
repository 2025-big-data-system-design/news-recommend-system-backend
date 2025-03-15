from selenium.webdriver.common.by import By

# 주어진 CSS 선택자로 요소의 텍스트를 추출
def extract_element_text(driver, selector, default="값 없음"):
    try: 
        element = driver.find_element(By.CSS_SELECTOR, selector)
        return element.text if element else default
    except Exception:
        return default
    
# 주어진 CSS 선택자로 요소의 특정 속성을 추출
def extract_element_attribute(driver, selector, attribute, default="값 없음"):
    try:
        element = driver.find_element(By.CSS_SELECTOR, selector)
        return element.get_attribute(attribute) if element else default
    except Exception:
        return default
    
# 뉴스 제목 추출
def extract_news_title(driver):
    return extract_element_text(driver, "h2.media_end_head_headline > span", "제목 없음")

# 뉴스 본문 내용 추출
def extract_news_content(driver):
    return extract_element_text(driver, "article#dic_area", "본문 없음")

# 신문사(언론사) 추출 
def extract_press_name(driver):
    press_name = extract_element_attribute(driver, "img.media_end_head_top_logo_img", "title", None)
    if not press_name:  # title이 없으면 alt 속성을 사용
        press_name = extract_element_attribute(driver, "img.media_end_head_top_logo_img", "alt", "신문사 없음")
    return press_name

# 뉴스 입력 시간 추출
def extract_news_date(driver):
    return extract_element_text(driver, "span.media_end_head_info_datestamp_time", "날짜 없음")
    
# 기자 이름 추출
def extract_reporter_name(driver):
    return extract_element_text(driver, "em.media_end_head_journalist_name", "기자 없음")
    
# 대표 이미지(썸네일) 추출
def extract_thumbnail(driver):
    return extract_element_attribute(driver, "div.newsct_body img", "src", "이미지 없음")
    
# Selenium 관련 모듈 임포트
from selenium import webdriver # Selenium 웹드라이버
from selenium.webdriver.chrome.service import Service # ChromeService 서비스 관리
from selenium.webdriver.chrome.options import Options # 크롬 옵션 설정
from data.config import CHROMEDRIVER_PATH

def configure_chrome_options():
    # Selenium 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless") # 브라우저 창을 열지 않고 실행
    chrome_options.add_argument("--disable-gpu") # GPU 가속 비활성화
    chrome_options.add_argument("--no-sandbox") # 보안 샌드박스를 비활성화
    chrome_options.add_argument("--disable-dev-shm-usage") # 크롬 크래시 방지
    
    # ChromeDriver 로그 숨기기
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    return chrome_options

def create_webdriver():
    chrome_options = configure_chrome_options()
    
    # 웹드라이버 실행
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver
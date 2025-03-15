# config.py

# 크롬 드라이버 경로 설정
CHROMEDRIVER_PATH = "drivers/chromedriver.exe"

# 네이버 뉴스 카테고리 및 서브 카테고리 URL 목록
CATEGORY_URLS = {
    "정치": {
        "메인": "https://news.naver.com/section/100",
        "대통령실": "https://news.naver.com/breakingnews/section/100/264",
        "국회/정당": "https://news.naver.com/breakingnews/section/100/265",
        "북한": "https://news.naver.com/breakingnews/section/100/268",
        "행정": "https://news.naver.com/breakingnews/section/100/266",
        "국방/외교": "https://news.naver.com/breakingnews/section/100/267",
        "정치일반": "https://news.naver.com/breakingnews/section/100/269",
    },
    "경제": {
        "메인": "https://news.naver.com/section/101",
        "금융": "https://news.naver.com/breakingnews/section/101/259",
        "증권": "https://news.naver.com/breakingnews/section/101/258",
        "산업/재계": "https://news.naver.com/breakingnews/section/101/261",
        "중기/벤처": "https://news.naver.com/breakingnews/section/101/771",
        "부동산": "https://news.naver.com/breakingnews/section/101/260",
        "글로벌 경제": "https://news.naver.com/breakingnews/section/101/262",
        "생활경제": "https://news.naver.com/breakingnews/section/101/310",
        "경제 일반": "https://news.naver.com/breakingnews/section/101/263",
    },
    "사회": {
        "메인": "https://news.naver.com/section/102",
        "사건사고": "https://news.naver.com/breakingnews/section/102/249",
        "교육": "https://news.naver.com/breakingnews/section/102/250",
        "노동": "https://news.naver.com/breakingnews/section/102/251",
        "언론": "https://news.naver.com/breakingnews/section/102/254",
        "환경": "https://news.naver.com/breakingnews/section/102/252",
        "인권/복지": "https://news.naver.com/breakingnews/section/102/59",
        "식품/의료": "https://news.naver.com/breakingnews/section/102/255",
        "지역": "https://news.naver.com/breakingnews/section/102/256",
        "인물": "https://news.naver.com/breakingnews/section/102/276",
        "사회 일반": "https://news.naver.com/breakingnews/section/102/257",
    },
    "생활/문화": {
        "메인": "https://news.naver.com/section/103",
        "건강정보": "https://news.naver.com/breakingnews/section/103/241",
        "자동차/시승기": "https://news.naver.com/breakingnews/section/103/239",
        "도로/교통": "https://news.naver.com/breakingnews/section/103/240",
        "여행/레저": "https://news.naver.com/breakingnews/section/103/237",
        "음식/맛집": "https://news.naver.com/breakingnews/section/103/238",
        "패션/뷰티": "https://news.naver.com/breakingnews/section/103/376",
        "공연/전시": "https://news.naver.com/breakingnews/section/103/242",
        "책": "https://news.naver.com/breakingnews/section/103/243",
        "종교": "https://news.naver.com/breakingnews/section/103/244",
        "날씨": "https://news.naver.com/breakingnews/section/103/248",
        "생활문화 일반": "https://news.naver.com/breakingnews/section/103/245",
    },
    "IT/과학": {
        "메인": "https://news.naver.com/section/105",
        "모바일": "https://news.naver.com/breakingnews/section/105/226",
        "인터넷/SNS": "https://news.naver.com/breakingnews/section/105/227",
        "통신/뉴미디어": "https://news.naver.com/breakingnews/section/105/230",
        "IT 일반": "https://news.naver.com/breakingnews/section/105/732",
        "보안/해킹": "https://news.naver.com/breakingnews/section/105/283",
        "컴퓨터": "https://news.naver.com/breakingnews/section/105/229",
        "게임/리뷰": "https://news.naver.com/breakingnews/section/105/228",
        "과학 일반": "https://news.naver.com/breakingnews/section/105/326",
    },
    "세계": {
        "메인": "https://news.naver.com/section/104",
        "아시아/호주": "https://news.naver.com/breakingnews/section/104/231",
        "미국/중남미": "https://news.naver.com/breakingnews/section/104/232",
        "유럽": "https://news.naver.com/breakingnews/section/104/233",
        "중동/아프리카": "https://news.naver.com/breakingnews/section/104/234",
        "세계 일반": "https://news.naver.com/breakingnews/section/104/322",
    },
}

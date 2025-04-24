class News:
    def __init__(
        self,
        url: str, # 뉴스 기사 URL
        title: str, # 뉴스 제목
        summary: str, # 뉴스 요약문
        content: dict, # 뉴스 본문 관련 정보 (html, text, paragraphs, entites)
        press: dict, # 언론사 정보 (name, logo)
        reporter: dict, # 기자 정보 (name, email, profile_image)
        thumbnail: str, # 뉴스에 삽입된 대표 이미지 URL
        published_at, # 뉴스 발행 시각
        categories: list, # 기사에 태그된 카테고리 목록
        keywords: list = None # 중요 키워드 리스트 (TF-IDF 기반 추출)
    ):
        self.url = url # 뉴스 기사 URL
        self.title = title # 뉴스 제목
        self.summary = summary # 뉴스 요약문
        self.content = content # 뉴스 본문 관련 정보
        self.press = press # 언론사 정보
        self.reporter = reporter # 기자 정보
        self.thumbnail = thumbnail # 뉴스에 삽입된 대표 이미지 URL 
        self.published_at = published_at # 뉴스 발행 시각
        self.categories = categories # 기사에 태그된 카테고리 목록
        self.keywords = keywords if keywords else [] # 중요 키워드 리스트 (기본값을 빈 리스트로 설정)

    # 뉴스 제목, URL, 언론사 이름, 기자 이름, 발행일을 요약적으로 표시
    def __repr__(self):
        return (
            # 뉴스 제목과 URL
            f"News(title='{self.title}', url='{self.url}', " 
            # 언론사와 기자 이름
            f"press='{self.press.get('name')}', reporter='{self.reporter.get('name')}', "
            # 발행일
            f"published_at='{self.published_at}')"
        )

    # News 객체를 딕셔너리 형태로 변환
    def to_dict(self):
        return {
            "url": self.url, # 뉴스 기사 URL
            "title": self.title, # 뉴스 제목
            "summary": self.summary, # 뉴스 요약문
            "content": self.content, # 뉴스 본문 관련 정보 (html, text, paragraphs, entites)
            "press": self.press, # 언론사 정보 (name, logo)
            "reporter": self.reporter, # 기자 정보 (name, email, profile_image)
            "thumbnail": self.thumbnail, # 뉴스에 삽입된 대표 이미지 URL
            "published_at": self.published_at, # 뉴스 발행 시각
            "categories": self.categories, # 기사에 태그된 카테고리 목록
            "keywords": self.keywords # 중요 키워드 리스트
        }
class News:
    # 뉴스 기사 초기화
    def __init__(self, url, title, content, press, date, reporter, thumbnail):
        self.url = url # 기사 URL
        self.title = title # 기사 제목
        self.content = content # 기사 본문 내용
        self.press = press # 신문사 (언론사) 이름
        self.date = date # 기사 입력 날짜
        self.reporter = reporter # 기자 이름
        self.thumbnail = thumbnail # 기사 대표 이미지
    
    # 뉴스 기사 문자열 표현
    # 본문은 길어질 수 있으므로 30자까지만 출력
    def __repr__(self):
        return (f"News(url='{self.url}', title='{self.title}', content='{self.content[:30]}...', " 
                f"press='{self.press}', date='{self.date}', reporter='{self.reporter}', thumbnail='{self.thumbnail}')")
    
    # 뉴스 기사 딕셔너리 표현
    def to_dict(self):
        return {
            "url": self.url,
            "title": self.title,
            "content": self.content, 
            "press": self.press,
            "date": self.date,
            "reporter": self.reporter,
            "thumbnail": self.thumbnail
        }

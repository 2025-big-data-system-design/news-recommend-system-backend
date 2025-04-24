class News:
    def __init__(
        self,
        url: str,
        title: str,
        summary: str,
        content: dict,          # html, text, paragraphs[], entities[]
        press: dict,            # name, logo
        reporter: dict,         # name, email, profile_image
        thumbnail: str,
        published_at,           # datetime 형식
        categories: list        # 문자열 리스트
    ):
        self.url = url
        self.title = title
        self.summary = summary
        self.content = content
        self.press = press
        self.reporter = reporter
        self.thumbnail = thumbnail
        self.published_at = published_at
        self.categories = categories

    def __repr__(self):
        return (
            f"News(title='{self.title}', url='{self.url}', "
            f"press='{self.press.get('name')}', reporter='{self.reporter.get('name')}', "
            f"published_at='{self.published_at}')"
        )

    def to_dict(self):
        return {
            "url": self.url,
            "title": self.title,
            "summary": self.summary,
            "content": self.content,
            "press": self.press,
            "reporter": self.reporter,
            "thumbnail": self.thumbnail,
            "published_at": self.published_at,
            "categories": self.categories
        }

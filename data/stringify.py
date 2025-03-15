# 뉴스 객체를 JSON 형식으로 변환하는 함수
def stringify(news):
    return {
        "url": news.url,
        "title": news.title,
        "content": news.content,
        "press": news.press,
        "date": news.date,
        "reporter": news.reporter,
        "thumbnail": news.thumbnail,
    }
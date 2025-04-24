# 크롤링된 뉴스 링크를 출력
def print_news_links(news_links):
    print("\n🔗 크롤링된 뉴스 링크 목록:")
    for category, links in news_links.items():
        print(f"\n📌 {category}:") # 카테고리별 출력
        for link in links:
            print(f"   - {link}") # 크롤링된 뉴스 링크 출력

    print("\n🎉 모든 뉴스 링크 크롤링 완료!") # 완료 메시지 출력
    
# 크롤링된 뉴스 기사 정보를 출력
def print_news_details(news_list):
    if not news_list:  # 뉴스가 없을 경우 경고 메시지 출력
        print("⚠️ 크롤링된 뉴스가 없습니다.")
        return

    print("\n📢 크롤링된 뉴스 기사 정보:")
    for news in news_list:
        print("=" * 60)
        print(f"🔗 기사 링크: {news.url}")                    # 뉴스 URL 출력
        print(f"📰 제목: {news.title}")                      # 뉴스 제목 출력
        print(f"📝 요약문: {news.summary}")                 # 뉴스 요약 출력
        print(f"📜 본문 내용 일부: {news.content['text'][:60]}...")  # 본문 텍스트 일부 출력
        print(f"🔠 문단 수: {len(news.content['paragraphs'])}")     # 문단 수 출력
        print(f"🔎 개체명 수: {len(news.content['entities'])}")     # 개체명 수 출력
        print(f"🏢 언론사: {news.press['name']}")           # 언론사 이름 출력
        print(f"🖼️ 로고: {news.press['logo']}")            # 언론사 로고 출력
        print(f"🧑 기자: {news.reporter['name']}")          # 기자 이름 출력
        print(f"📧 이메일: {news.reporter['email']}")       # 기자 이메일 출력
        print(f"🖼️ 프로필 이미지: {news.reporter['profile_image']}")  # 프로필 이미지 출력
        print(f"📅 발행일: {news.published_at}")            # 발행 날짜 출력
        print(f"🖼️ 썸네일 이미지: {news.thumbnail}")        # 썸네일 이미지 출력
        print(f"🏷️ 카테고리: {', '.join(news.categories)}")  # 카테고리 출력
        print(f"🔑 키워드: {', '.join(news.keywords)}") # 키워드 출력
        print("=" * 60 + "\n")

    print("\n🎉 모든 뉴스 기사 정보 크롤링 완료!")  # 완료 메시지 출력
        
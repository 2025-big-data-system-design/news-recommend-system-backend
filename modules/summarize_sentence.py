from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
import torch

# KoBART 모델 로드
tokenizer = PreTrainedTokenizerFast.from_pretrained("digit82/kobart-summarization")
model = BartForConditionalGeneration.from_pretrained("digit82/kobart-summarization")

def summarize_news(text, max_length=512, summary_length=100):
    # 입력 텍스트 토큰화
    inputs = tokenizer([text], max_length=max_length, return_tensors="pt", truncation=True)

    # 요약 생성
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=summary_length,
        min_length=30,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )

    # 디코딩하여 텍스트로 반환
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# 테스트용 한국어 뉴스 기사
news_article = """
17일 렉서스코리아 LX 700h 공식 출시\n렉서스코리아는 플래그십 스포츠유틸리티차량(SUV) '디 올 뉴 LX 700h(THE ALL-NEW LX 700h)'를 17일 국내 시장에 출시했다.\n\n이번에 렉서스가 선보이는 LX 700h 4세대 모델은 기존 LX의 신뢰성, 내구성, 오프로드 주행 성능을 계승하면서도, 새롭게 개발된 병렬 하이브리드 시스템과 개량된 'GA-F 플랫폼'을 도입해 정교한 드라이빙 성능을 구현했다.\n\n렉서스 디 올 뉴 LX 700h 4인승 VIP 트림. 렉서스코리아 제공\n\n\n렉서스는 신형 LX 700h에 새로운 병렬 하이브리드 시스템을 탑재했다. 3.5ℓ V6 트윈 터보 엔진과 10단 자동 변속기 사이에 클러치가 포함된 모터 제너레이터(MG)를 배치했다. 이를 통해 엔진과 모터의 강력한 출력과 토크를 효과적으로 노면에 전달하며 주행 상황에 따라 엔진 단독 또는 모터 단독 주행을 최적의 방식으로 자동 제어할 수 있게 했다.\n\n또한 발전기(얼터네이터)와 스타터를 기본 장착해 하이브리드 시스템이 정지하더라도 엔진만으로 비상 주행이 가능하도록 설계했다. 엔진 차량과 동등한 도하 성능(700㎜)을 확보하기 위해 하이브리드 메인 배터리에 새로운 방수 구조를 적용했다.\n\nLX 700h에는 개량된 'GA-F 플랫폼'을 적용해 저중심화, 경량화, 차체 강성 향상 등 차량의 기본 성능을 한층 강화했다. 내연기관 모델과 동일한 최저 지상고를 유지하는 한편, 스페어 타이어의 위치를 조정해 오프로드 성능과 정비 편의성을 균형 있게 개선했다.\n\n렉서스는 LX 700h에 라디에이터 서포트 주변의 강성을 보강하고 패치 형태의 보강재를 추가해 조향 응답성을 향상시켰다. '전자제어 가변 서스펜션(AVS·Adaptive Variable Suspension)'은 액추에이터의 밸브 구조를 새롭게 설계해 거친 노면에서도 감쇠력을 부드럽게 조절할 수 있게 했다.\n\n외관 디자인은 '품격 있는 세련미'라는 익스테리어 디자인 테마를 바탕으로 최고의 오프로드 성능을 계승하면서도 도심에서도 강렬한 존재감을 발휘할 수 있도록 설계됐다. 인테리어는 직선적인 수평 디자인을 유지해 넓은 개방감을 강조하며, 거친 도로에서도 안정적인 균형감을 느낄 수 있도록 설계됐다.\n\n특히 시트에 세미아닐린 가죽을 사용해 탑승자의 피로도를 최소화할 수 있도록 설계됐다. 1열 시트는 승객의 신장 차이와 관계없이 편안한 착석감을 제공하는 헤드레스트 디자인과 마사지 기능이 포함된 '리프레시 시트' 옵션을 탑재했다.\n\n렉서스 디 올 뉴 LX 700h 5인승 오버트레일 트림. 렉서스코리아 제공\n\n\n4인승 VIP 그레이드는 탑승자가 최고급 라운지에 있는 듯한 경험을 누릴 수 있도록 설계했다. 독립된 2열 뒷좌석 시트는 대형 헤드레스트와 리프레시 시트 기능을 갖췄으며, 뒷좌석 우측에는 '오토만' 기능이 적용돼 신체의 특정 부위에 전해지는 압력 없이 사람의 몸이 자유로워지는 무중력 자세를 구현한다.\n\n아울러 업그레이드된 안전사양 '렉서스 세이프티 시스템 플러스'와 인포테인먼트 시스템 '렉서스 커넥트' 그리고 안드로이드 오토와 애플 카플레이가 전 트림에 기본 제공된다. 또한 360도 서라운드 사운드를 구현하는 25개 스피커를 탑재한 마크 레빈슨 사운드 시스템이 기본 장착돼 있다.\n\n렉서스 LX 700h의 가격은 ▲4인승 VIP 1억9457만원 ▲5인승 오버트레일 1억6587만원 ▲7인승 럭셔리 1억6797만원이다(부가세 포함, 개별소비세 3.5%).
"""

# 요약 실행
summary = summarize_news(news_article)
print("📌 요약 결과:")
print(summary)

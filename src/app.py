# 기본 라이브러리
from flask import Flask # Flask 웹 서버 생성

# Blueprint import
from routes.raw_news_routes import raw_news_bp
from routes.indexed_news_routes import indexed_news_bp
from routes.press_routes import press_bp
from routes.category_routes import category_bp # ✅ 카테고리 라우터 추가

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

# Blueprint 등록
app.register_blueprint(raw_news_bp)
app.register_blueprint(indexed_news_bp)
app.register_blueprint(press_bp)
app.register_blueprint(category_bp) # ✅ 카테고리 블루프린트 등록

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

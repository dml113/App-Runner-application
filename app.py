from flask import Flask

# Flask 애플리케이션 생성
app = Flask(__name__)

# 기본 경로("/")로 들어오는 요청에 대한 응답
@app.route('/')
def hello():
    return "Hello, World!"

# 애플리케이션 실행
if __name__ == '__main__':
    # 디버그 모드에서 실행
    app.run(debug=True)

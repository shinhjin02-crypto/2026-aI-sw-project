from flask import Flask, render_template, redirect, request
from dotenv import load_dotenv
import os
import requests

load_dotenv()

client_id = os.getenv('NAVER_CLIENT_ID')
client_secret = os.getenv('NAVER_CLIENT_SECRET')
callback_uri = os.getenv('NAVER_REDIRECT_URI')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/naver/callback')
def naver_callback():
    code = request.args.get("code")
    state = request.args.get('state') #내가 준 값이 맞는지 봐야하는데, 오늘은 귀찮아서 안함

    #이 코드를 들고 네이버한테 "니가 준거 맞냐고 물어보러 간다"
    token_url = (
        f"https://nid.naver.com/oauth2.0/token?"
        f"grant_type=authorization_code&client_id={client_id}"
        f"&redirect_url={callback_uri}&state=HELLO"
    )

    token_response = requests.get(token_url).json()
    access_token = token_response.get("access_token")
    print(access_token)

    #나와 저 사용자에 대한 검증이 끝나서, 나는 네이버와 대화할 수 있는 인증토큰 (access_token)을 받아왔음.
    #이제 이걸로, 우리 고갱님의 정보를 물어본다...
    
    #그럼 필수동의 항목은 다 받아올 수 있고, 선택 동의 항목은 사용자가 동의하고 가입했다면 받아오고 아니면 네이버가 안줌

    return "인증은 일단 성공, 당신이 누군지 몰라도 네이버 다녀온건 확인했음"

@app.route('/login')
def naver_login():

    auto_url = (
        f"https://nid.naver.com/oauth2.0/authorize?"
        f"response_type=code&client_id={client_id}"
        f"&redirect_uri={callback_uri}&state=HELLO"
    )

    return redirect(auto_url)

if __name__ == '__main__':
    app.run(debug=True)
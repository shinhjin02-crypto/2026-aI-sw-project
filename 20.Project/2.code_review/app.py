from flask import Flask, send_from_directory, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import requests
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

app = Flask(__name__, static_folder="public") #static폴더를 public 으로 쓸 때 해줘야함


def convert_github_to_raw(url):
    if "github.com" in url and "/blob/" in url:
        raw_url = url.replace("github.com", "raw.githubusercontent.com")
        raw_url = raw_url.replace("/blob/", "/")
        return raw_url

    return url


@app.route('/')
def index():
    return send_from_directory("public", "index.html")


@app.route('/api/codecheck', methods=['POST'])
def code_check():

    #데이터를 JSON 형태로 받아온다
    #chatgpt API를 받아온다.
    #응답을 받아와서 반환한다

    data = request.get_json()

    #사용자가 입력한 github URL
    url = data.get('url')

    #github URL -> RAW URL 변환
    raw_url = convert_github_to_raw(url)

    #실제 소스코드 가져오기
    resp = requests.get(raw_url)

    if resp.status_code != 200:
        return jsonify({
            "result": "소스코드를 가져오지 못했습니다."
        })

    #github raw 코드 내용
    code = resp.text

    prompt = (
        "다음 소스코드를 보고 취약점을 분석하시오.\n"
        "각 취약점에 대해 해당 코드의 라인 번호, 코드 스니펫, 취약점 설명과 개선 방안을 간단하게 설명하시오. 주석은 무시해도 됩니다.\n\n"
        "소스코드:\n"
        "-------------------\n"
        f"{code}\n"
        "-------------------\n"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "너는 코드 보안 분석 전문가야."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content

    return jsonify({
        "result": result
    })


if __name__ == '__main__':
    app.run(debug=True)
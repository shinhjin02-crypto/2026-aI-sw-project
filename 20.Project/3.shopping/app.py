from flask import Flask, send_from_directory, jsonify, request
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__, static_folder="public")

reviews = []

# ------------------
# API 라우팅
# ------------------
@app.route('/api/reviews', methods=['POST'])
def add_review():
    data = request.get_json()

    rating = data.get('rating')
    comment = data.get('comment')

    if not rating or not comment:
        return jsonify({'message': '평점과 후기를 입력해주세요.'}), 400

    review = {
        'rating': int(rating),
        'comment': comment
    }

    reviews.append(review)

    return jsonify({
        'message': '리뷰 저장 완료',
        'reviews': reviews
    })


@app.route('/api/reviews', methods=['GET'])
def get_review():
    return jsonify(reviews)


@app.route('/api/ai-summary', methods=['GET'])
def get_ai_summary():
    if len(reviews) == 0:
        return jsonify({
            'summary': '현재는 리뷰가 없습니다.',
            'average_rating': 'N/A'
        })

    comments = "\n".join([f"- 평점 {r['rating']}점: {r['comment']}" for r in reviews])
    average_rating = sum([r['rating'] for r in reviews]) / len(reviews)

    prompt = f"""
        다음 쇼핑몰 상품 리뷰들을 보고 핵심 내용을 짧게 요약해줘.

        조건:
        - 고객들이 좋게 본 점
        - 아쉽게 본 점
        - 전체적인 분위기
        - 2~3문장으로 요약

        리뷰 목록:
        {comments}
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    summary = response.output_text

    return jsonify({
        'summary': summary,
        'average_rating': round(average_rating, 1)
    })

# ------------------
# 웹 서비스 라우팅
# ------------------
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
# 1. openai 관련 라이브러리를 다 불러온다 (dotenv, openai 등등)
# 2. OOO 페이지 (우리의 최종 페이지) 에서 채팅창 FE 를 만든다.
# 3-1. 그 FORM의 입력값을 BE에서 POST로 받아서, chatgpt API 호출한다. (그냥 아무말이나 해도 됨.)
# 3-2. 응답 받아서 다시 프런트엔드에 반환해서 결과 출력한다. (추가: 복습을 원하면 이런데서 SSE 구현해봐도 됨)
# 4. 그럼 이제, 진짜 우리의 이 상황 (학년, 커리큐럼) 에 대해서 영어로 대화를 하도록 만든다.
# 5. [추가] 메모리를 통해서 대화 내용 컨텍스트를 기억하게 한다."	...				 

from flask import Flask, render_template, request
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

app = Flask(__name__)

chat_memory=[]

#각 학년별 커리큘럼 데이터
curriculums = {
    #key=[value]
    1: ['기초 인사', '간단한 문장', '동물 이름'],
    2: ['학교 생활', '가족 소개', '자기 소개'],
    3: ['취미와 운동', '날씨 묘사', '간단한 이야기'],
    4: ['쇼핑과 가격', '음식 주문', '여행 이야기'],
    5: ['역사와 문화', '과학과 자연', '사회 이슈'],
    6: ['미래 계획', '진로 탐색', '세계 여행'],
}

grade_rules = {
        1: """
    - 아주 짧은 영어 문장으로 말해.
    - 한글 설명을 많이 섞어줘.
    - 단어 위주로 알려줘.
    - 예문은 1개만 줘.
    """,
        2: """
    - 짧은 영어 문장으로 말해.
    - 쉬운 단어를 사용해.
    - 한글 설명을 함께 해줘.
    - 예문은 1~2개 줘.
    """,
        3: """
    - 쉬운 영어 문장으로 대화해.
    - 간단한 질문도 같이 해줘.
    - 어려운 표현은 한국어로 설명해.
    """,
        4: """
    - 영어 비율을 조금 더 높여줘.
    - 문장 패턴을 알려줘.
    - 학생이 따라 말할 수 있는 예문을 줘.
    """,
        5: """
    - 영어로 먼저 설명하고, 필요한 부분만 한국어로 설명해.
    - 문법 포인트를 1개 포함해.
    - 예문과 짧은 연습문제를 줘.
    """,
        6: """
    - 최대한 영어로 대화해.
    - 중학교 준비 수준의 표현도 조금 포함해.
    - 문법 설명과 응용 예문을 포함해.
    """
}

@app.route('/test-ai')
def test_ai():
    response = client.responses.create(
        model = "gpt-4o-mini",
        input = "안녕? 너는 10년차 영어 강사야."
    )
    answer = response.output_text

    return answer

@app.route('/chat', methods=['POST'])
def chat():

    global chat_memory

    user_message = request.form.get('message')
    grade = request.form.get('grade')
    curriculum_title = request.form.get('curriculum_title')

    grade = int(grade)

    # 현재 학년 규칙만 가져오기
    rule = grade_rules.get(
        grade,
        "학생 수준에 맞게 쉽게 설명해."
    )

    system_prompt = f"""
        너는 초등학교 {grade}학년 학생을 가르치는 친절한 영어 선생님이야.

        현재 수업 주제는 "{curriculum_title}" 이야.
        반드시 이 주제와 관련된 영어 대화를 해야 해.

        출력 형식 규칙:
        1. Markdown 문법을 절대 사용하지 마.
        2. **굵게**, ##제목, - 목록, ```코드블록을 쓰지 마.
        3. 일반 문장으로만 답해.
        4. 줄바꿈은 짧게만 사용해.

        학년별 규칙:
        {rule}

        주제별 대화 규칙:
        1. 학생의 질문이 다른 내용이어도 "{curriculum_title}" 주제로 자연스럽게 연결해.
        2. "{curriculum_title}"와 관련된 단어를 2개 이상 알려줘.
        3. "{curriculum_title}"와 관련된 쉬운 영어 예문을 1개 이상 말해줘.
        4. 학생이 대답할 수 있는 짧은 영어 질문을 마지막에 1개 해줘.
        5. 완전히 관련 없는 질문이면 짧게 답한 뒤 다시 "{curriculum_title}" 수업으로 돌아와.
        6. 실제 영어 선생님처럼 자연스럽게 대화해.
        7. 매번 같은 형식으로 답하지 마.
        8. 꼭 단어/예문/질문을 모두 넣지 않아도 돼.
        9. 친구처럼 부드럽게 이어서 대화해.
        10. 초등학생과 대화하듯 밝고 따뜻하게 말해.

        학생의 말:
        {user_message}
    """

    chat_memory.append({
        "role": "user",
        "content": user_message
    })

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ] + chat_memory

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    ai_answer = response.choices[0].message.content

    chat_memory.append({
        "role": "assistant",
        "content": ai_answer
    })

    return ai_answer

@app.route('/')
def home():
    return render_template('home.html', grades=curriculums.keys())

@app.route('/grade/<int:grade>')
def grade(grade):
    if grade in curriculums:
        curriculums_index = list(enumerate(curriculums[grade]))
        return render_template('grade.html', grade=grade, grades=curriculums.keys(),
        curriculums=curriculums_index)
    return "해당 학년은 존재하지 않습니다", 404

@app.route('/grade/<int:grade>/curriculum/<int:curriculum_id>')
def curriculum(grade, curriculum_id):
    if grade in curriculums and 0 <= curriculum_id < len(curriculums[grade]):
        curriculum_title = curriculums[grade][curriculum_id]
        return render_template('curriculum.html', grade=grade, grades=curriculums.keys(),
        curriculum_title=curriculum_title)
    return "해당 학년은 존재하지 않습니다.", 404

if __name__ == '__main__':
    app.run(debug=True)

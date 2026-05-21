#강사님거 보고 다시하기
import requests
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

messages = [
    {
        'role': 'system',
        'content': '너는 나와 잘 놀아주는 친구야.'
    }
]

def ask_chatbot(user_input):
    global messages

    messages.append({
        'role': 'user',
        'content': user_input
    })

    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            json={
                'model': 'gpt-3.5-turbo',
                'messages': messages,
                'temperature': 1.0,
                'max_tokens': 1000
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {openai_api_key}'
            }
        )

        data = response.json()

        final_response = data['choices'][0]['message']['content']

        messages.append({
            'role': 'assistant',
            'content': final_response
        })

        # 시스템 메시지 + 최근 대화 20개만 유지
        messages = [messages[0]] + messages[-20:]

        return final_response

    except Exception as e:
        print('오류:', e)
        return '오류가 발생했습니다.'


while True:
    user_input = input("\n당신의 질문: ").strip()

    if user_input.lower() in ['quit', 'exit', '종료', '끝']:
        print("대화를 종료합니다. 안녕히계세요.")
        break

    print("대화를 생성중입니다. 잠시만 기다려 주세요....")
    print("챗봇응답:", ask_chatbot(user_input))
    print('-' * 60)
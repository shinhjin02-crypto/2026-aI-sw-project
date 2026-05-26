import os
import requests
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {openai_api_key}'
}

# ---------------- 첫 번째 질문 ----------------

user_input = "대한민국의 수도는 어디야?"

response = requests.post(
    # 'https://api.openai.com/v1/completions'
    'https://api.openai.com/v1/responses',

    headers=headers,

    json={
        'model': 'gpt-4o-mini',
        'input': user_input
    }
)

data = response.json()

print(data)
print('-' * 30)

answer = data['output'][0]['content'][0]['text']
print('응답:', answer)
print('응답ID: ', data['id'])

# 다음 대화를 위해 response_id 저장
response_id = data['id']

# ---------------- 두 번째 질문 ----------------

user_input = "그 도시의 인구는 몇이야?"

response = requests.post(
    # 'https://api.openai.com/v1/completions'
    'https://api.openai.com/v1/responses',

    headers=headers,

    json={
        'model': 'gpt-4o-mini',
        'input': user_input,
        'previous_response_id': response_id
    }
)

data = response.json()

print(data)
print('-' * 30)

answer = data['output'][0]['content'][0]['text']
print('응답:', answer)
print('응답ID: ', data['id'])

# 다시 최신 response_id 저장
response_id = data['id']

# ---------------- 세 번째 질문 ----------------

user_input = "그 도시에서 가볼만한 곳 추천해줘"

response = requests.post(
    # 'https://api.openai.com/v1/completions'
    'https://api.openai.com/v1/responses',

    headers=headers,

    json={
        'model': 'gpt-4o-mini',
        'input': user_input,
        'previous_response_id': response_id
    }
)

data = response.json()

print(data)
print('-' * 30)

answer = data['output'][0]['content'][0]['text']
print('응답:', answer)
print('응답ID: ', data['id'])
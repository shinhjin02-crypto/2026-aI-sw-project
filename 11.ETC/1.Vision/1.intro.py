# 방법
# 1. 사진을 직접 올린다 (base64 인코딩)
# 2. 이미지 URL을 주고 읽어가려고 한다.

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTM4MdAX00sEHSQNxcF9csoD54ip6EvR3NujA&s'

response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages= [
        {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': '이 이미지를 한국어로 설명해줘'},
                {'type': 'image_url', 'image_url': {'url': image_url}} # <- 이줄이 핵심
            ]
        }
    ]
)

print(response.choices[0].message.content)
# 텍스트를 기반으로 이미지를 생성...(GAN)

# 구버전 모델이 dall-e => dall-e-2 => ?
# gpt-image-1.5 또는 gpt-image-2

import os
import base64

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

prompt = "토끼가 거북이 등에 올라타서 바다를 여행하는 모습, 수채화, 수많은 별이 떠있는 밤하늘"

result = client.images.generate(
    model="gpt-image-1",
    prompt = prompt,
    size = '1024x1024',
    quality='medium' # low / medium / high / auto
)

# image-2
# 4k 까지 지원함 (4096), 16:9 비율도 생성 가능
# 빠진 단점 하나는, 투명 배경 못만듦... 투명 배경은 1.5 기능임...

b64 = result.data[0].b64_json
with open('output.png', 'wb') as f:
    f.write(base64.b64decode(b64))

print('저장 완료')
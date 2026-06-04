import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

text = "안녕하세요. 오늘은 OpenAI 음성 합성 기능을 테스트하고 있습니다. 한국어 발음과 억양이 얼마나 자연스러운지 확인해 보겠습니다."

response = client.audio.speech.create(
    model='tts-1',
    voice = 'alloy',
    input = text
)

response.write_to_file('output.mp3')
print('저장완료')
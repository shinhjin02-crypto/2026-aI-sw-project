import os
import base64

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def transcribe_audio(file):
    with open(file, "rb") as af:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=af,
            response_format="text",
            language="ko"
        )
    return transcript

result = transcribe_audio("sample.mp3")
print("결과: ", result)
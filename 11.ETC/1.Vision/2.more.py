import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

#image_path = "11.ETC/1.Vision/canva_dog.webp"
image_path = "11.ETC/1.Vision/summer.webp"


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def ask_about_image(question, b64):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/webp;base64,{b64}"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content


questions = [
    "이미지에 있는 한글 글자를 다 읽어줘",
    "해당 이미지에 사용된 주요 색상을 알려줘",
    "이미지의 전체 분위기를 한 문장으로 표현하면?"
]

b64 = encode_image(image_path)

for q in questions:
    print("-" * 50)
    print(f"질문: {q}")
    print(f"답변: {ask_about_image(q, b64)}")
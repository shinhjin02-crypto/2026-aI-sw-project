import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

city_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'population': {'type': 'integer'},
        'area_km2': {'type': 'number'},
    },
    'required': ['name', 'population', 'area_km2'],
    'additionalProperties': False,
}

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {'role': 'system', 'content': '질문에 대해 JSON으로만 답변하시오.'},
        {'role': 'user', 'content': '서울의 인구와 면적을 알려주시오.'},
    ],
    response_format={
        'type': 'json_schema',  # 출력 결과가 아래 정의한 나만의 스키마로 주도록 요청
        'json_schema': {
            'name': 'city_info',  # 내가 정의하는 이름
            'strict': True,       # 엄격하게 따라라
            'schema': city_schema
        }
    }
)

answer = response.choices[0].message.content
#print(answer)

data = json.loads(answer)
print(
    f"도시의 이름: {data['name']} "
    f"- 인구: {data['population']:,}명, "
    f"면적: {data['area_km2']}km2"
)
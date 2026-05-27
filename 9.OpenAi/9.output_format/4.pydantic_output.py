import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from pydantic import BaseModel

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class CityInfo(BaseModel):
    name: str
    population: int
    area_km2: float

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

response = client.chat.completions.parse(
    model='gpt-4o-mini',
    messages=[
        {'role': 'system', 'content': '질문에 대해 JSON으로만 답변하시오.'},
        {'role': 'user', 'content': '서울의 인구와 면적을 알려주시오.'},
    ],
    response_format=CityInfo
)

answer = response.choices[0].message.parsed
data = answer
#print(answer)
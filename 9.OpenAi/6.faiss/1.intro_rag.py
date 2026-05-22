#pip install faiss-cpu

from dotenv import load_dotenv
import os

from openai import OpenAI

import faiss
import numpy as np

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

#우리의 문장 데이터
documents = [
    "한국소프트웨어저작권협회는 SPC 라는 약자를 가지고 있고, 다양한 국내 기업의 SW 라이선스와 저작권을 다루는 곳입니다.",
    "홍길동은 2020년 1월 1일 생으로, 강원도 설빙산에서 태어났고 그곳에서 호랑이를 잡아먹으며 성장하였습니다.",
    "Python은 개발 언어 중에 가장 쉽다고 하는데, 그렇게 쉬운 언어는 아닙니다."
]

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    # print(response)
    return np.array(response.data[0].embedding, dtype="float32")

#print(get_embedding(documents))

index = faiss.IndexFlatL2(1536) #OPENAI로 임베딩 하면 1536차원

doc_embeddings = np.array(
    [get_embedding(doc) for doc in documents],
    dtype="float32"
)

index.add(doc_embeddings)       # 나온 숫자값을 벡터 DB에 넣는다

# 사용자의 질문을 받아서 우리의 백터 DB에 물어본다
def rag_query(user_query):

    query_embedding = get_embedding(user_query)

    #벡터 DB에서 질문 (user_query)의 숫자값과 가장 가까운거 k=1개를 반환하시오.
    _, indices = index.search(
        np.array([query_embedding], dtype="float32"),
        k=1
    )

    # 나온 숫자값을 벡터 DB에 넣는다
    retrieved_doc = documents[indices[0][0]]

    prompt = f""" 
    너는 문서 기반 답변 어시스턴트다.

    규칙:
    1. 반드시 관련자료에 있는 내용만 사용해서 답변한다.
    2. 질문과 관련 없는 내용은 절대 추측해서 답변하지 않는다.
    3. 관련자료만으로 답변할 수 없으면 친절하게 부족하다고 말한다.
    4. 사용자는 관련자료를 볼 수 없으므로 "자료에 따르면", "문서에 따르면" 같은 표현은 사용하지 않는다.
    5. 답변은 자연스럽고 친절한 말투와 뿌잉뿌잉하게 작성한다.
    6. 필요하면 가벼운 이모티콘은 사용할 수 있지만 과하지 않게 한다.
    

    사용자의 질문: {user_query}

    관련자료: {retrieved_doc}
    """

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 친절한 AI도우미 입니다."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

#query = "홍길동은 누구인가요?"
#query = "파이썬은 어떤 언어인가요?"
query = "오늘 저녁 뭐 먹을까?"

result = rag_query(query)

print(result)
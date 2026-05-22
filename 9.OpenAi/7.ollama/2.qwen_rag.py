# pip install faiss-cpu
# pip install openai python-dotenv requests

from dotenv import load_dotenv
import os
import requests

from openai import OpenAI

import faiss
import numpy as np

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

MODEL_NAME = "qwen2.5:1.5b"
# MODEL_NAME = "exone3.5:2.4b"

# 우리의 문장 데이터
documents = [
    "한국소프트웨어저작권협회는 SPC 라는 약자를 가지고 있고, 다양한 국내 기업의 SW 라이선스와 저작권을 다루는 곳입니다.",
    "홍길동은 2020년 1월 1일 생으로, 강원도 설빙산에서 태어났고 그곳에서 호랑이를 잡아먹으며 성장하였습니다.",
    "Python은 개발 언어 중에 가장 쉽다고 하는데, 그렇게 쉬운 언어는 아닙니다."
]

# Qwen에게 질문하는 함수
def ask_qwen(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    return data['response']


# 문장을 숫자 벡터로 바꾸는 함수
def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    # print(response)
    return np.array(response.data[0].embedding, dtype="float32")


# OPENAI로 임베딩 하면 1536차원
index = faiss.IndexFlatL2(1536)

# 문서들을 전부 임베딩해서 벡터 DB에 넣는다
doc_embeddings = np.array([get_embedding(doc) for doc in documents], dtype="float32")
index.add(doc_embeddings)


# 사용자의 질문을 받아서 우리의 벡터 DB에 물어본다
def rag_query(user_query):

    query_embedding = get_embedding(user_query)

    # 벡터 DB에서 질문(user_query)의 숫자값과 가장 가까운 거 k=1개를 반환하시오.
    distance, indices = index.search(
        np.array([query_embedding], dtype="float32"), k=1
    )

    retrieved_doc = documents[indices[0][0]]

    # 거리 측정된 걸 유사도 점수로 변환
    true_distance = np.sqrt(distance[0][0])
    similarity_score = 1 / (1 + true_distance)

    #print("\n=== 유사도 점수 ===")
    #print(f"검색된 문서: {retrieved_doc}")
    #print(f"유사도 점수: {similarity_score:.3f}")
#
    print(">>>>>>>")
    print("질문과 가까운 벡터 인덱스:", indices[0][0], ",", "그 거리:", distance[0][0])
    print("<<<<<<<")

    # similarity_score는 높을수록 비슷한 것
    # 그러므로 0.40보다 낮으면 관련 없는 질문으로 판단
    if similarity_score < 0.40:
        return "해당 내용은 적합한 답변을 찾을 수 없습니다."

    prompt = f"""
        너는 문서 기반 답변 어시스턴트다.

        규칙:
        1. 반드시 관련자료에 있는 내용만 사용해서 답변한다.
        2. 질문과 관련 없는 내용은 절대 추측해서 답변하지 않는다.
        3. 관련자료만으로 답변할 수 없으면 친절하게 부족하다고 말한다.
        4. 사용자는 관련자료를 볼 수 없으므로 "자료에 따르면", "문서에 따르면" 같은 표현은 사용하지 않는다.
        5. 답변은 자연스럽고 친절하게 작성한다.
        6. 필요하면 가벼운 이모티콘은 사용할 수 있지만 과하지 않게 한다.

        사용자의 질문: {user_query}

        관련자료: {retrieved_doc}
        """

    # 여기서 OpenAI GPT가 아니라 로컬 Qwen에게 최종 답변을 맡김
    response = ask_qwen(prompt)

    return response


while True:
    query = input("\n나: ")

    if query.lower() == "exit":
        print("종료합니다.")
        break

    result = rag_query(query)
    print("응답:", result)
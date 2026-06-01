# 표준 LCEL 로 RAG 모델을 구현하기

import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()

# 1. 벡터 스토어(DB) 정의하기
DB_DIR = "./chroma_db"
COLLECTION_NAME = "my_rag"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=DB_DIR
)

if store._collection.count() == 0:
    docs = (
        TextLoader("./10.LangChain/7.RAG/3.store/nvme.txt", encoding="utf-8").load()
        + TextLoader("./10.LangChain/7.RAG/3.store/hbm.txt", encoding="utf-8").load()
    )

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    ).split_documents(docs)

    for c in chunks:
        c.metadata["source"] = os.path.basename(c.metadata.get("source", "N/A"))

    store.add_documents(chunks)

retriever = store.as_retriever(search_kwargs={"k": 3})

# 2. LLM + 프롬프트 설계하기
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 문서 기반 QA 시스템입니다. 아래 문서만 참고해서 답변하시오.\n\n{context}"),
    ("user", "{question}")
])

# 3. 표준 질의 응답을 위한 파이프라인 설계
def format_docs(docs):
    return "\n\n".join(
        f"[{i}] {d.page_content}"
        for i, d in enumerate(docs, start=1)
    )

def extract_sources(docs):
    seen, sources = set(), []

    for d in docs:
        src = d.metadata.get("source", "N/A")

        if src not in seen:
            seen.add(src)
            sources.append(src)

    return sources

def retrieve_and_split(inputs):
    docs = retriever.invoke(inputs["question"])

    return {
        "question": inputs["question"],
        "context": format_docs(docs),
        "sources": extract_sources(docs)
    }

def append_source(d):
    src_lines = "\n".join(f"- {s}" for s in d["sources"])
    return f"{d['answer']}\n\n참고문서:\n{src_lines}"

chain = (
    RunnableLambda(retrieve_and_split)
    | RunnablePassthrough.assign(answer=prompt | llm | StrOutputParser())
    | RunnableLambda(append_source)
)

# 4. 최종 질문
print(chain.invoke({"question": "NVMe와 HBM의 차이는?"}))
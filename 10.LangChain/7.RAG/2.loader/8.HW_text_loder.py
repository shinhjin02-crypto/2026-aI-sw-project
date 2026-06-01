import os
import shutil
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

DB_DIR = "./10.LangChain/7.RAG/2.loader/chroma_db"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

# 기존 DB 삭제
if os.path.exists(DB_DIR):
    if os.path.isdir(DB_DIR):
        shutil.rmtree(DB_DIR)
    else:
        os.remove(DB_DIR)

def make_collection(file_path, collection_name, source_name):
    docs = TextLoader(file_path, encoding="utf-8").load()

    for doc in docs:
        doc.metadata["source"] = source_name

    chunks = splitter.split_documents(docs)

    store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=DB_DIR
    )

    print(f"{collection_name} 컬렉션 생성 완료")
    print(f"청크 개수: {store._collection.count()}")

    return store


# HBM 컬렉션
hbm_store = make_collection(
    "./10.LangChain/7.RAG/2.loader/hbm.text",
    "hbm_collection",
    "HBM"
)

# NVME 컬렉션
nvme_store = make_collection(
    "./10.LangChain/7.RAG/2.loader/nvme.text",
    "nvme_collection",
    "NVME"
)

# HBM + NVME 통합 컬렉션
hbm_docs = TextLoader(
    "./10.LangChain/7.RAG/2.loader/hbm.text",
    encoding="utf-8"
).load()

nvme_docs = TextLoader(
    "./10.LangChain/7.RAG/2.loader/nvme.text",
    encoding="utf-8"
).load()

for doc in hbm_docs:
    doc.metadata["source"] = "HBM"

for doc in nvme_docs:
    doc.metadata["source"] = "NVME"

all_docs = hbm_docs + nvme_docs
all_chunks = splitter.split_documents(all_docs)

all_store = Chroma.from_documents(
    documents=all_chunks,
    embedding=embeddings,
    collection_name="all_collection",
    persist_directory=DB_DIR
)

print("\nall_collection 생성 완료")
print(f"청크 개수: {all_store._collection.count()}")

# 검색 테스트
question = "HBM과 NVME의 차이점은?"

print("\n[ALL COLLECTION 검색 결과]")

results = all_store.similarity_search(question, k=4)

for i, doc in enumerate(results, start=1):
    print(f"\n[{i}] 출처: {doc.metadata.get('source')}")
    print(doc.page_content[:300])
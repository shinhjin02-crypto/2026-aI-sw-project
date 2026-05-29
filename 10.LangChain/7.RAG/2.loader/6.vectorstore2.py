import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

DB_DIR = "./chroma_db"
COLLECTION_NAME = "coding"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def build_store():
    docs = TextLoader(
        "./10.LangChain/7.RAG/2.loader/hbm.text", encoding="utf-8").load()

    chunks = RecursiveCharacterTextSplitter( chunk_size=500, chunk_overlap=100 ).split_documents(docs)

    store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=DB_DIR
    )

    print(f"새 DB 생성 성공 - {len(chunks)} 청크 저장됨")
    return store


def load_store():
    store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=DB_DIR
    )

    print(f"기존 DB 로딩 성공 - {store._collection.count()} 청크 로딩됨")
    return store


if os.path.exists(DB_DIR) and os.listdir(DB_DIR):
    store = load_store()
else:
    store = build_store()


results = store.similarity_search("HBM이란 무엇인가요?", k=2)

for i, d in enumerate(results, start=1):
    print(f"\n[{i}]")
    print(f" -> {d.page_content[:60]}...")
import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()

DB_DIR = "./chroma_db"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 100)

FILES = [
    "./10.LangChain/7.RAG/3.store/nvme.txt",
    "./10.LangChain/7.RAG/3.store/hbm.txt",
    "./10.LangChain/7.RAG/3.store/cisc2024.pdf"
]

def load_any_docs(path):
   if path.lower().endswith(".pdf"):
      return PyPDFLoader(path).load()
   else:
      return TextLoader(path, encoding="utf-8").load()

def build_document():
   chunks = []
   for path in FILES:
      part = splitter.split_documents(load_any_docs(path))
      for c in part:
         c.metadata["source"] = os.path.basename(path) #통합된 컬렉션 내에서, 문서를 구분하기 위해 각각의 데이터에 메타 데이터를 넣음
      chunks += part
   return Chroma.from_documents(chunks, embeddings, collection_name="unified", persist_directory=DB_DIR)

store = Chroma(collection_name="unified", embedding_function=embeddings, persist_directory=DB_DIR)
if store._collection.count() == 0:
   store = build_document()

print(f"컬렉션 이름: unified, 청크 통합 개수: {store._collection.count()}")

# 쿼리
query = "저장장치 인터페이스 속도는?"
print("질문: ", query)
for d in store.similarity_search(query, k=2):
   print(f"\n---\n[{d.metadata.get('source')}] {d.page_content}")

query = "가장 값싸고 가성비 좋은 패스트푸드는?"
print("질문: ", query)
for d in store.similarity_search(query, k=2):
   print(f"\n---\n[{d.metadata.get('source')}] {d.page_content}")

# 특정 메타데이터를 기반으로만 필터링을 원하면??
results = store.similarity_search(query, k=2, filter={"source": "hbm.txt"})
for d in results:
   print(f"\n---\n{d.page_content}")
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


class VectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()

    def create_vectorstore(self, text_chunks):
        return FAISS.from_texts(texts=text_chunks, embedding=self.embeddings)

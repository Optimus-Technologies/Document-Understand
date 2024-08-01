from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain_core.vectorstores import VectorStoreRetriever
from typing import List

from api_keys import *


class LineTextSplitter:
    def __init__(self, lines_per_chunk):
        self.lines_per_chunk = lines_per_chunk

    def split_documents(self, documents):
        chunks = []
        for doc in documents:
            lines = doc.page_content.split('\n')
            for i in range(0, len(lines), self.lines_per_chunk):
                chunk = '\n'.join(lines[i:i + self.lines_per_chunk])
                chunks.append(Document(page_content=chunk, metadata=doc.metadata))
        return chunks

def retriever(doc_list: List[dict], query: str):
    embeddings = OpenAIEmbeddings()
    documents = []
    embedded_docs = []

    for doc_dict in doc_list:
        for file_name, text in doc_dict.items():
            doc = Document(page_content=text, metadata={"file_name": file_name})
            documents.append(doc)
            
            # Create embedding for each document
            embedding = embeddings.embed_documents([text])[0]
            embedded_docs.append({file_name: embedding})

    vectorstore = FAISS.from_documents(documents, embeddings)
    
    retriever = VectorStoreRetriever(vectorstore=vectorstore, search_type="similarity_score_threshold", search_kwargs={'score_threshold': 0.5})

    # Retrieve results
    results = retriever.invoke(input=query)

    return results


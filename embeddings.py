from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
import os
from langchain_core.vectorstores import VectorStoreRetriever


os.environ["OPENAI_API_KEY"] = "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"
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'


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

def retriever(doc_text: str, query: str):
    with open("documents.txt", 'w') as doc:
        doc.write(doc_text)

    loader = TextLoader("documents.txt")
    documents = loader.load()

    # Check the loaded document length
    print(f"Document length: {len(documents[0].page_content)}")

    # Set lines per chunk to a small value for testing
    text_splitter = LineTextSplitter(lines_per_chunk=10)
    texts = text_splitter.split_documents(documents)
    
    

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)
    
    # Ensure correct configuration for the retriever
    retriever = VectorStoreRetriever(vectorstore=vectorstore, search_type="similarity_score_threshold", search_kwargs={'score_threshold': 0.5})

    # Print query vector for debugging
    query_vector = embeddings.embed_query(query)

    # Retrieve results
    results = retriever.invoke(input=query)
    

    return results


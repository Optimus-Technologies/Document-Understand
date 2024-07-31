import os
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.documents import Document
from typing import List



os.environ["GROQ_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = "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"

# def format_docs(docs: List[Document]):
#     return "\n\n".join(doc.page_content for doc in docs)

# Load, chunk and index the contents of the blog.
def retriever_generator(docs: List[Document], query: str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    for doc in docs:
        splits = text_splitter.split_documents(doc)
        vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever()
    prompt = """You are an assistant for question-answering tasks.\
            Use the following pieces of retrieved context to\
            answer the question. If you don't know the answer, \
            just say that you don't know. Use three sentences\
            maximum and keep the answer concise.
            Question: {question} 
            Context: {context} 
            Answer:"""


    # format_docs(docs)

    llm = ChatGroq(model="llama3-8b-8192")
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    response = rag_chain.invoke(query)
    return response
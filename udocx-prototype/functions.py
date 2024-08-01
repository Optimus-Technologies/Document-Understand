from parser import document_convertor
import model
from embeddings import retriever

def chat_with_data(documents, chat_history, query, category='Agriculture'):
    text_string = ""
    text_list = []
    
    for document in documents:
        file_name = document.name
        ext = document.name.split(".")[1]
        text = document_convertor(ext=ext, document=document)
        text_string += f"\nFilename: {file_name}\nContent:\n{text}\n"
        text_list.append({file_name: text})
    

        text_chunk = ""
    if "total" or "all" in query:
        text_chunk = text_string
        
    else:
        doc_chunk = retriever(doc_list=text_list, query=query)

        for chunk in doc_chunk:
            text_chunk += chunk.page_content

    #Generate answer to question
    
    #Get Chat History
    chat_history = chat_history


    ai_chat_history = ""
    for usr_message, ai_response in chat_history:
        ai_chat_history += f"\nuser_message: {usr_message}\nai_response: {ai_response}\n"


    response = model.extract_info(text=text_chunk, category=category, query=query, chat_history=ai_chat_history)
    

    #suggest followup
    if "total" or "all" in query:
        followups = []
    else:
        followups = model.suggest_followups(text=text_chunk, chat_history=ai_chat_history)

    #Update chat history
    return {
            "status": "OK",
            "followups": followups,
            "answer": response
        }

    


def extract_all_data(documents, category ):
    text_string = ""
    for document in documents:
        file_name = document.name
        ext = document.name.split(".")[1]
        text = document_convertor(ext=ext, document=document)
        text_string += f"\nFilename: {file_name}\nContent:\n{text}\n"
    

    return model.extract_all_key_info(text_string, category)


def summarize_documents(documents, category):
    text_string = ""
    for document in documents:
        file_name = document.name
        ext = document.name.split(".")[1]
        text = document_convertor(ext=ext, document=document)
        text_string += f"\nFilename: {file_name}\nContent:\n{text}\n"
    

    return model.summarizer(text_string, category)
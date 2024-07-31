from fastapi import FastAPI, UploadFile, File, HTTPException, status
import sqlite3
import parser, model
from crud import *
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.documents import Document
from typing import List
from embeddings import retriever

app = FastAPI()

app.add_middleware( CORSMiddleware, 
                   allow_origins=["*"], 
                   allow_credentials=True, 
                   allow_methods=["*"], 
                   allow_headers=["*"],
                   )



@app.post("/key_info/")
async def extract_key_info(category: str, documents: List[UploadFile] = [File(...)]):
    text_string = ""
    for document in documents:
            file_name = document.filename
            ext = document.filename.split(".")[1]
            text = await parser.document_convertor(ext=ext, document=document)
            text_string += f"\nFilename: {file_name}\nContent:\n{text}\n"
    key_info = await model.extract_all_key_info(text=text_string, category=category)
    
    return {"key_info": key_info}


@app.post("/file/")
async def chat_with_data(session_id: int, followup_id: int, category: str, query: str, documents: List[UploadFile] = [File(...)]):
    try:
        texts = []
        text_string = ""
        for document in documents:
            file_name = document.filename
            ext = document.filename.split(".")[1]
            text = await parser.document_convertor(ext=ext, document=document)
            text_string += f"\nFilename: {file_name}\nContent:\n{text}\n"
            texts.append([{file_name: text}])


        doc_chunk: List[Document] = retriever(doc_text=text_string, query=query)

        text_chunk = ""
        for chunk in doc_chunk:
            text_chunk += chunk.page_content

        #Generate answer to question
        
        #Activate chat session
        await activate_session(document=text)

        #Get Chat History
        chat_history = await get_chat_history(session_id=session_id)


        ai_chat_history = ""
        for usr_message, ai_response in chat_history:
            ai_chat_history += f"\nuser_message: {usr_message}\nai_response: {ai_response}\n"


        response = await model.extract_info(text=text_chunk, category=category, query=query, chat_history=ai_chat_history)
        

        #suggest followup
        followups = await model.suggest_followups(text=text_chunk, chat_history=ai_chat_history)

        #Update chat history
        await update_chat_history(session_id=session_id, followup_id=followup_id, user_msg=query, ai_response=response)

        return {
            "status": "OK",
            "followups": followups,
            "answer": response
        }
    except sqlite3.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: str{e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error processing chat str{e}")

@app.get("/{session_id}/chat_history")
async def chat_history(session_id: int):
    try:
        chat_history = await get_chat_history(session_id=session_id)
        if chat_history:
            return {
                "session_id": session_id,
                "chat_history": [{"user_msg": chat[0], "ai_response": chat[1]} for chat in chat_history]
            }
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    except sqlite3.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: str{e}")


@app.delete("/{session_id}/delete_history/{followup_id}")
async def delete_single_history(session_id: int, followup_id: int):
    try:
        return await delete_single_chat_history(session_id=session_id, followup_id=followup_id)
    except sqlite3.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error etr{e}")


@app.delete("/{session_id}/delete_history")
async def delete_hsitory(session_id: int):
    try:
        return await delete_chat_history(session_id=session_id)
    except sqlite3.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error str{e}")
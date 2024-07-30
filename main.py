from fastapi import FastAPI, UploadFile, File, HTTPException, status
import sqlite3
import parser, model
from crud import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware( CORSMiddleware, 
                   allow_origins=["*"], # Allows all origins, you can specify specific domains if needed 
                   allow_credentials=True, 
                   allow_methods=["*"], # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.) 
                   allow_headers=["*"], # Allows all headers 
                   )


# class ChatRequest(BaseModel):
#     query: str
#     session_id: int 

@app.post("/key_info/")
async def extract_key_info(document: UploadFile = File(...)):
    text = await parser.convert_to_text(document=document)
    documents = []
    key_info = await model.extract_key_info(text)
    formatted_key_info = parser.format_output(key_info)
    documents.append(formatted_key_info)

    output_docs = ""
    for doc in documents:
        output_docs = output_docs + doc + "\n" + "="*40 + "\n"


    return {
        "key_info": output_docs
    }


@app.post("/file/")
async def chat_with_data(session_id: int, followup_id: int, query: str, document: UploadFile = File(...)):
    try:
        ext = document.filename.split(".")[1]
        text = await parser.document_convertor(ext=ext, document=document)
        #Activate chat session
        await activate_session(document=text)

        #Get Chat History
        chat_history = await get_chat_history(session_id=session_id)

        #Making the chat history compactible with the model
        ai_chat_history = []
        # for usr_message, ai_response in chat_history:
        #     ai_chat_history.append(model.HumanMessage(content=usr_message))
        #     ai_chat_history.append(model.AIMessage(content=ai_response))

        for usr_message, ai_response in chat_history:
             ai_chat_history.append({"role": "user", "content": usr_message})
             ai_chat_history.append({"role": "user", "content": ai_response})



        response = await model.chat_with_model(query=query, document=text, chat_history=ai_chat_history)
        #response = await model.question_answer(query=query, document=text, chat_history=chat_history)

        #Update chat history
        await update_chat_history(session_id=session_id, followup_id=followup_id, user_msg=query, ai_response=response.content)

        return {
            "status": "OK",
            "answer": response.content
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
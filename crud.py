from database import con, cur


async def activate_session(document: str):
    cur.execute('''
        INSERT OR IGNORE INTO sessions(document)
        VALUES (?)
    ''', (document, ))
    con.commit()
    return 


async def get_chat_history(session_id: int):
    cur.execute('''
        SELECT user_msg, ai_response 
        FROM chat_history
        WHERE session_id=?
    ''', (session_id, ) )
    chat_history = cur.fetchall()
    return chat_history


async def update_chat_history(session_id: int, followup_id: int, user_msg: str, ai_response: str):
    cur.execute('''
        INSERT INTO chat_history (session_id, followup_id, user_msg, ai_response)
        VALUES (?, ?, ?, ?)
    ''', (session_id, followup_id, user_msg, ai_response, ))
    con.commit()
    return


async def delete_single_chat_history(session_id: int, followup_id: int):
    cur.execute('''
        DELETE FROM chat_history
        WHERE session_id=? AND followup_id=?
    ''', (session_id, followup_id, ))
    return {"message": "Followup deleted successfully"}


async def delete_chat_history(session_id: int):
    cur.execute('''
        DELETE FROM chat_history
        WHERE session_id=?
    ''', (session_id, ))
    con.commit()
    return {"message": "Chat history deleted successfully"}
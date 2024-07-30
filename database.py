import sqlite3

con = sqlite3.connect("sessions.db")
cur = con.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS sessions(
            session_id INTEGER PRIMARY KEY,
            document TEXT NOT NULL,
            session_desc TEXT
    )
''')


cur.execute('''
    CREATE TABLE IF NOT EXISTS chat_history(
            followup_id INTEGER NOT NULL,
            session_id INTEGER NOT NULL,
            user_msg TEXT,
            ai_response TEXT,
            PRIMARY KEY(session_id, followup_id),
            FOREIGN KEY(session_id) REFERENCES sessions(id)
    )
''')

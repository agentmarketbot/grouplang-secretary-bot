import sqlite3
from typing import Optional

class Database:
    def __init__(self, db_name='conversations.db'):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    transcription TEXT,
                    summary TEXT
                )
            ''')

    def save_conversation(self, conversation_id: str, transcription: str, summary: str):
        with self.connection:
            self.connection.execute('''
                INSERT INTO conversations (id, transcription, summary)
                VALUES (?, ?, ?)
            ''', (conversation_id, transcription, summary))

    def get_conversation(self, conversation_id: str) -> Optional[dict]:
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM conversations WHERE id = ?', (conversation_id,))
        row = cursor.fetchone()
        if row:
            return {'id': row[0], 'transcription': row[1], 'summary': row[2]}
        return None

import sqlite3
from typing import Optional

class Database:
    def __init__(self, db_name='conversations.db'):
        self.connection = sqlite3.connect(db_name)
        self._create_table()

    def _create_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    transcription TEXT,
                    summary TEXT
                )
            ''')

    def save_conversation(self, conversation_id: str, transcription: str, summary: str):
        with self.connection:
            self.connection.execute('''
                INSERT INTO conversations (conversation_id, transcription, summary)
                VALUES (?, ?, ?)
            ''', (conversation_id, transcription, summary))

    def get_conversation(self, conversation_id: str) -> Optional[dict]:
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT transcription, summary FROM conversations WHERE conversation_id = ?
        ''', (conversation_id,))
        row = cursor.fetchone()
        if row:
            return {'transcription': row[0], 'summary': row[1]}
        return None

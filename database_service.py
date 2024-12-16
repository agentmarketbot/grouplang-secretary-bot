import psycopg2
from config import Config

class DatabaseService:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self._create_conversations_table()

    def _create_conversations_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id SERIAL PRIMARY KEY,
                chat_id BIGINT NOT NULL,
                conversation_id VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def save_conversation(self, chat_id, conversation_id, message):
        self.cursor.execute("""
            INSERT INTO conversations (chat_id, conversation_id, message)
            VALUES (%s, %s, %s)
        """, (chat_id, conversation_id, message))

    def get_conversations(self, chat_id):
        self.cursor.execute("""
            SELECT conversation_id, message, timestamp
            FROM conversations
            WHERE chat_id = %s
            ORDER BY timestamp DESC
        """, (chat_id,))
        return self.cursor.fetchall()

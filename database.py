import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def create_conversations_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS conversations (
            id SERIAL PRIMARY KEY,
            chat_id BIGINT NOT NULL,
            conversation_id VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.cursor.execute(create_table_query)

    def store_conversation(self, chat_id, conversation_id, message):
        insert_query = """
        INSERT INTO conversations (chat_id, conversation_id, message)
        VALUES (%s, %s, %s);
        """
        self.cursor.execute(insert_query, (chat_id, conversation_id, message))

    def get_conversations(self, chat_id):
        select_query = """
        SELECT * FROM conversations WHERE chat_id = %s ORDER BY created_at DESC;
        """
        self.cursor.execute(select_query, (chat_id,))
        return self.cursor.fetchall()

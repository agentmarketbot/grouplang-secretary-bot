import mysql.connector
from config import Config

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        self.cursor = self.connection.cursor()

    def create_conversation(self, conversation_id, text, summary):
        query = "INSERT INTO conversations (conversation_id, text, summary) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (conversation_id, text, summary))
        self.connection.commit()

    def get_conversation(self, conversation_id):
        query = "SELECT text, summary FROM conversations WHERE conversation_id = %s"
        self.cursor.execute(query, (conversation_id,))
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.connection.close()

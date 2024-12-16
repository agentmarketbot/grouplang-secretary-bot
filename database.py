import mysql.connector
from mysql.connector import Error
from config import Config

class MySQLDatabase:
    def __init__(self):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise

    def insert_conversation(self, conversation_id, text, summary):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO conversations (conversation_id, text, summary) VALUES (%s, %s, %s)"
            cursor.execute(query, (conversation_id, text, summary))
            self.connection.commit()
        except Error as e:
            print(f"Error inserting conversation: {e}")
            raise

    def close(self):
        if self.connection.is_connected():
            self.connection.close()

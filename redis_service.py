import redis
from config import Config

class RedisService:
    def __init__(self):
        self.client = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            db=Config.REDIS_DB
        )

    def set_conversation(self, conversation_id: str, data: dict):
        self.client.set(conversation_id, data)

    def get_conversation(self, conversation_id: str) -> dict:
        data = self.client.get(conversation_id)
        return data if data else {}

    def delete_conversation(self, conversation_id: str):
        self.client.delete(conversation_id)

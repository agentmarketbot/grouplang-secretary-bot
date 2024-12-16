from pymongo import MongoClient
from typing import Dict, Any

class MongoDBService:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db['conversations']

    def save_conversation(self, conversation: Dict[str, Any]) -> None:
        self.collection.insert_one(conversation)

    def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        return self.collection.find_one({"conversation_id": conversation_id})

    def update_conversation(self, conversation_id: str, update_data: Dict[str, Any]) -> None:
        self.collection.update_one({"conversation_id": conversation_id}, {"$set": update_data})

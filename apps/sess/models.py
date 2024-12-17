from datetime import datetime
from typing import List

from bson import ObjectId


class Session:
    """会话模型类"""
    def __init__(self, db):
        self.collection = db['sessions']

    def create(self, user_id: str, sess_name: str) -> str:
        """创建新会话"""
        session = {
            "user_id": user_id,
            "sess_name": sess_name,
            "create_at": datetime.utcnow(),
            "update_at": datetime.utcnow()
        }
        result = self.collection.insert_one(session)
        return str(result.inserted_id)

    def get_user_sessions(self, user_id: str) -> List[dict]:
        """获取用户的所有会话"""
        return list(self.collection.find({"user_id": user_id}))

    def verify_ownership(self, sess_id: str, user_id: str) -> bool:
        """验证会话所有权"""
        session = self.collection.find_one({"_id": ObjectId(sess_id)})
        return session and session["user_id"] == user_id


class Chat:
    """聊天消息模型类"""
    def __init__(self, db):
        self.collection = db['chats']

    def create_message(self, sess_id: str, user_id: str, content: str, from_type: str) -> str:
        """创建新消息"""
        chat = {
            "sess_id": ObjectId(sess_id),
            "user_id": user_id,
            "chat_content": content,
            "from": from_type,
            "create_at": datetime.utcnow()
        }
        result = self.collection.insert_one(chat)
        return str(result.inserted_id)

    def get_session_chats(self, sess_id: str) -> List[dict]:
        """获取会话的所有消息"""
        return list(self.collection.find(
            {"sess_id": ObjectId(sess_id)},
            sort=[("create_at", 1)]
        ))

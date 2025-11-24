from app.models.chat_message_model import ChatMessageModel as ChatMessage
from app.db import db
from sqlalchemy.exc import SQLAlchemyError


class ChatService:
    def get_all_messages_by_conversation(self, conversation_id):
        """Lấy tất cả tin nhắn trong 1 conversation"""
        return (
            ChatMessage.query
            .filter_by(conversation_id=conversation_id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )

    def get_message(self, message_id):
        """Lấy 1 tin nhắn theo id"""
        message = ChatMessage.query.get(message_id)
        if not message:
            raise ValueError(f"Message {message_id} không tồn tại")
        return message

    def create_message(self, data):
        """Tạo tin nhắn mới"""
        message = ChatMessage(
            conversation_id=data.get("conversation_id"),
            sender=data.get("sender"),
            user_id=data.get("user_id"),
            message=data.get("message"),
            message_type=data.get("message_type", "text"),
        )
        try:
            db.session.add(message)
            db.session.commit()
            return message
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def update_message(self, message_id, data):
        """Cập nhật tin nhắn"""
        message = self.get_message(message_id)
        for field in ["message", "message_type"]:
            if field in data:
                setattr(message, field, data[field])
        try:
            db.session.commit()
            return message
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def delete_message(self, message_id):
        """Xóa tin nhắn"""
        message = self.get_message(message_id)
        try:
            db.session.delete(message)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

chat_service = ChatService()

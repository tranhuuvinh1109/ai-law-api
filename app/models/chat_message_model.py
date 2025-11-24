from datetime import datetime
from app.db import db

class ChatMessageModel(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.String(100), nullable=False, index=True)  # ID của cuộc trò chuyện (có thể là session)
    sender = db.Column(db.String(50), nullable=False)  # 'user' hoặc 'bot'
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)  # Nếu sender là user, liên kết tới bảng User
    message = db.Column(db.Text, nullable=False)  # Nội dung tin nhắn
    message_type = db.Column(db.String(20), default="text")  # text, image, audio, file...
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ChatMessage {self.sender}: {self.message[:20]}>"

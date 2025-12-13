from app.models.conversation_model import ConversationModel as Conversation
from app.services.chat_service import chat_service
from app.services.ai_usage_service import deduct_user_balance, create_ai_usage
from app.db import db
from datetime import datetime
import uuid
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class ConversationService:
    def get_all(self, user_id):
        return Conversation.query.filter_by(user_id=user_id).order_by(Conversation.updated_at.desc()).all()

    def get(self, conversation_id):
        return Conversation.query.get(conversation_id)

    def create(self, user_id, title=None):
        """Tạo conversation mới với user_id từ token"""
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(
            id=conversation_id,
            user_id=user_id,
            title=title or "Untitled"
        )
        db.session.add(conversation)
        db.session.commit()
        return conversation

    # def ask_ai(self, conversation_id, user_id, message_text):
    #     """
    #     Gửi tin nhắn từ user, fake trả lời AI, lưu cả 2 message
    #     """

    #     # 1️⃣ Lưu message từ user
    #     user_message = chat_service.create_message({
    #         "conversation_id": conversation_id,
    #         "sender_id": user_id,
    #         "message": message_text,
    #         "message_type": "text"
    #     })

    #     # 2️⃣ Fake trả lời từ AI
    #     ai_text = f"Đây là phản hồi giả từ AI cho tin nhắn: '{message_text}'"

    #     # 3️⃣ Lưu message từ AI (sender_id = None vì là bot)
    #     ai_message = chat_service.create_message({
    #         "conversation_id": conversation_id,
    #         "sender_id": None,
    #         "message": ai_text,
    #         "message_type": "text"
    #     })

    #     # 4️⃣ Cập nhật updated_at cho conversation
    #     conv = self.get(conversation_id)
    #     if conv:
    #         conv.updated_at = datetime.utcnow()
    #         db.session.commit()

    #     return ai_message
    def ask_ai(self, conversation_id, user_id, message_text, model=None):
        """
        Gửi message user → gọi GPT → lưu message AI → cập nhật conversation → trả JSON hợp lệ
        Nếu model được cung cấp, sẽ trừ tiền và lưu lịch sử sử dụng AI
        """

        # 1️⃣ Lưu message từ user
        user_message = chat_service.create_message({
            "conversation_id": conversation_id,
            "sender_id": user_id,
            "message": message_text,
            "message_type": "text"
        })

        # 2️⃣ Gọi API GPT để tạo phản hồi
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Bạn là cán bộ tư vấn hành chính Việt Nam. "
                            "Trả lời nhiệt tình, đầy đủ, chính xác theo pháp luật. "
                            "Mọi câu trả lời phải trích dẫn nguồn văn bản pháp luật."
                        )
                    },
                    {"role": "user", "content": message_text}
                ]
            )

            ai_text = response.choices[0].message.content

        except Exception as e:
            ai_text = f"[AI ERROR] {str(e)}"

        # 3️⃣ Lưu message AI (sender_id = None vì là bot)
        ai_message = chat_service.create_message({
            "conversation_id": conversation_id,
            "sender_id": None,
            "message": ai_text,
            "message_type": "text"
        })

        # 4️⃣ Cập nhật updated_at cho conversation
        conv = self.get(conversation_id)
        if conv:
            conv.updated_at = datetime.utcnow()
            db.session.commit()

        # 5️⃣ Nếu có model, trừ tiền và lưu lịch sử sử dụng AI
        if model and not ai_text.startswith("[AI ERROR]"):
            try:
                # Trừ 500 từ balance user
                deduct_user_balance(user_id, 500)

                # Lưu lịch sử sử dụng AI
                create_ai_usage({
                    "user_id": user_id,
                    "conversation_id": conversation_id,
                    "model": model,
                    "tokens_used": len(message_text.split()) + len(ai_text.split()),  # Rough token estimate
                    "cost": 500.0  # Fixed cost as per requirement
                })
            except Exception as deduct_error:
                # Nếu trừ tiền thất bại, ghi log nhưng không làm gián đoạn flow chính
                print(f"Warning: Failed to deduct balance for user {user_id}: {str(deduct_error)}")

        # 6️⃣ Trả JSON chuẩn → tránh lỗi Axios
        return ai_message
        

    def update(self, conversation_id, data):
        conv = self.get(conversation_id)
        if not conv:
            raise ValueError("Conversation not found")
        for field in ["title", "user_id"]:
            if field in data:
                setattr(conv, field, data[field])
        db.session.commit()
        return conv

    def delete(self, conversation_id):
        conv = self.get(conversation_id)
        if not conv:
            raise ValueError("Conversation not found")
        db.session.delete(conv)
        db.session.commit()


conversation_service = ConversationService()

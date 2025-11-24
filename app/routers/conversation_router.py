from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.schemas.chat_schema import ConversationSchema, ConversationUpdateSchema, ChatMessageSchema
from app.services.conversation_service import conversation_service
from app.services.chat_service import chat_service

blp = Blueprint("Conversation", __name__, description="Conversation API")


@blp.route("/conversations")
class ConversationList(MethodView):
    @blp.response(200, ConversationSchema(many=True))
    def get(self):
        """Get all conversations"""
        return conversation_service.get_all()

@blp.route("/conversations/<string:conversation_id>")
class ConversationDetail(MethodView):
    @blp.response(200, ConversationSchema)
    def get(self, conversation_id):
        """Get conversation details by ID"""
        conversation = conversation_service.get(conversation_id)
        if not conversation:
            abort(404, message=f"Conversation {conversation_id} not found")
        return conversation

    @blp.arguments(ConversationUpdateSchema)
    @blp.response(200, ConversationSchema)
    def put(self, data, conversation_id):
        """Update conversation"""
        return conversation_service.update(conversation_id, data)

    @blp.response(204)
    def delete(self, conversation_id):
        """Delete conversation"""
        conversation_service.delete(conversation_id)
        return {}

@blp.route("/conversations/<string:conversation_id>/messages")
class ConversationMessages(MethodView):
    @blp.response(200, ChatMessageSchema(many=True))
    def get(self, conversation_id):
        """Get all messages in a conversation"""
        messages = chat_service.get_all_messages_by_conversation(conversation_id)
        return messages

@blp.route("/conversations/<string:conversation_id>/ask")
class ConversationAskAI(MethodView):
    @blp.arguments(ChatMessageSchema)
    @blp.response(201, ChatMessageSchema)
    def post(self, data, conversation_id):
        """
        User gửi tin nhắn đến AI, fake trả lời từ bot, lưu cả 2 message
        Body:
        {
            "user_id": 1,
            "message": "Nội dung câu hỏi"
        }
        """
        user_id = data.get("user_id")
        message_text = data.get("message")

        if not message_text or not user_id:
            abort(400, message="user_id và message là bắt buộc")

        # Gọi service để fake AI trả lời
        bot_message = conversation_service.ask_ai(
            conversation_id=conversation_id,
            user_id=user_id,
            message_text=message_text
        )

        return bot_message
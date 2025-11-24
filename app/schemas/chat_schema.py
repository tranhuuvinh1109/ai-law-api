from marshmallow import Schema, fields

class ConversationSchema(Schema):
    id = fields.Str()
    user_id = fields.Int()
    title = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class ConversationUpdateSchema(Schema):
    title = fields.Str()
    user_id = fields.Int()

class ChatMessageSchema(Schema):
    id = fields.Int()
    conversation_id = fields.Str()
    sender = fields.Str()
    user_id = fields.Int()
    message = fields.Str()
    message_type = fields.Str()
    created_at = fields.DateTime()

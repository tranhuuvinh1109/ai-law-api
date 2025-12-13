from marshmallow import Schema, fields


class PlainTransactionSchema(Schema):
    """Base transaction schema"""
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    status = fields.Int(required=True)  # 0: pending, 1: completed, 2: failed, 3: cancelled
    amount = fields.Float(required=True)
    payment_method = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    additional_data = fields.Dict(allow_none=True)


class TransactionSchema(PlainTransactionSchema):
    """Full transaction schema with user info"""
    user = fields.Nested("PlainUserSchema", dump_only=True)


class TransactionCreateSchema(Schema):
    """Schema for creating transaction"""
    status = fields.Int(required=True)
    amount = fields.Float(required=True)
    payment_method = fields.Str(required=True)
    additional_data = fields.Dict(allow_none=True)


class TransactionUpdateSchema(Schema):
    """Schema for updating transaction"""
    status = fields.Int(allow_none=True)
    amount = fields.Float(allow_none=True)
    payment_method = fields.Str(allow_none=True)
    additional_data = fields.Dict(allow_none=True)


class TransactionFilterSchema(Schema):
    """Schema for filtering transactions"""
    user_id = fields.Int(allow_none=True)
    status = fields.Int(allow_none=True)
    payment_method = fields.Str(allow_none=True)
    page_size = fields.Int(allow_none=True, default=20)
    page = fields.Int(allow_none=True, default=1)


class TransactionPageSchema(Schema):
    """Schema for paginated transaction results"""
    results = fields.List(fields.Nested(TransactionSchema()))
    total_page = fields.Int()
    total_transactions = fields.Int()

from marshmallow import Schema, fields


class GuestResponseSchema(Schema):
    """Schema for guest user creation response"""
    access_token = fields.Str(required=True, description="JWT access token for guest")
    id = fields.Int(required=True, description="User ID of the guest")
    username = fields.Str(required=True, description="Username of the guest")
    email = fields.Str(required=True, description="Email of the guest")
    user_type = fields.Str(required=True, description="Type of user (always 'guest')")
    expires_in = fields.Int(required=True, description="Token expiration time in seconds")
    message = fields.Str(required=True, description="Success message")
    role = fields.Int(required=True, description="role")


class GuestInfoSchema(Schema):
    """Schema for guest user information"""
    id = fields.Int(required=True, description="User ID")
    username = fields.Str(required=True, description="Username")
    email = fields.Str(required=True, description="Email")
    role = fields.Int(required=True, description="User role")
    block = fields.Bool(required=True, description="Block status")
    time_created = fields.Str(required=True, description="Creation timestamp")
    user_type = fields.Str(required=True, description="Type of user")


class GuestCreateResponseSchema(Schema):
    """Schema for guest creation response"""
    success = fields.Bool(required=True, description="Operation success status")
    data = fields.Nested(GuestResponseSchema, required=True, description="Guest user data")
    message = fields.Str(required=True, description="Response message")


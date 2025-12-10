from flask.views import MethodView
from flask_smorest import Blueprint

from app.schemas.guest_schema import (
    GuestCreateResponseSchema,
    GuestInfoSchema,
    GuestResponseSchema,
)
from app.services import guest_service

blp = Blueprint("Guest", __name__, description="Guest API")


@blp.route("/guest")
class CreateGuest(MethodView):
    @blp.response(201, GuestCreateResponseSchema)
    def post(self):
        """
        Create a new guest user and return access token
        ---
        responses:
          201:
            description: Guest user created successfully
            schema: GuestCreateResponseSchema
          500:
            description: Internal server error
        """
        try:
            guest_data = guest_service.create_guest_user()

            response = {
                "success": True,
                "data": guest_data,
                "message": "Guest user created successfully"
            }

            return response, 201

        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Failed to create guest user: {str(e)}"
            }, 500


@blp.route("/guest/<int:user_id>")
class GuestInfo(MethodView):
    @blp.response(200, GuestInfoSchema)
    def get(self, user_id):
        """
        Get guest user information by ID
        ---
        parameters:
          - name: user_id
            in: path
            type: integer
            required: true
            description: Guest user ID
        responses:
          200:
            description: Guest user information
            schema: GuestInfoSchema
          404:
            description: Guest user not found
          500:
            description: Internal server error
        """
        try:
            guest_info = guest_service.get_guest_user(user_id)

            if not guest_info:
                return {
                    "message": "Guest user not found"
                }, 404

            return guest_info

        except Exception as e:
            return {
                "message": f"Failed to get guest user: {str(e)}"
            }, 500


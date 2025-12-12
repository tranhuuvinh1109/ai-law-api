import logging
import uuid
from datetime import timedelta

from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256

from app.db import db
from app.models.user_model import UserModel

# Create logger for this module
logger = logging.getLogger(__name__)

# Default password for guest users (hashed)
GUEST_PASSWORD = pbkdf2_sha256.hash("guest_password_123")


def create_guest_user():
    """
    Create a new guest user and return access token
    """
    try:
        # Generate unique ID for guest
        guest_id = str(uuid.uuid4())

        # Create guest username and email
        username = f"guest_{guest_id}"
        email = f"guest_{guest_id}@guest.local"

        # Create guest user in database
        guest_user = UserModel(
            username=username,
            email=email,
            password=GUEST_PASSWORD,
            role=3,  # 3: guest role
            block=False
        )

        db.session.add(guest_user)
        db.session.commit()

        # Create access token with user identity
        access_token = create_access_token(
            identity=guest_user.id,
            additional_claims={
                "user_type": "guest",
                "username": username
            },
            expires_delta=timedelta(hours=24)  # Token expires in 24 hours
        )

        logger.info(f"Guest user created successfully! Username: {username}")

        return {
            "access_token": access_token,
            "id": guest_user.id,
            "username": username,
            "email": email,
            "user_type": "guest",
            "expires_in": 86400,  # 24 hours in seconds
            "message": "Guest user created successfully",
            "role": 3
        }

    except Exception as e:
        logger.error(f"Error creating guest user: {str(e)}")
        db.session.rollback()
        raise e


def get_guest_user(user_id):
    """
    Get guest user by ID
    """
    try:
        user = UserModel.query.filter_by(id=user_id, role=3).first()  # role=3 for guests
        if not user:
            return None

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "block": user.block,
            "time_created": user.time_created,
            "user_type": "guest"
        }

    except Exception as e:
        logger.error(f"Error getting guest user: {str(e)}")
        raise e


def cleanup_guest_users():
    """
    Clean up old guest users (optional - for maintenance)
    This could be run periodically to remove old guest accounts
    """
    try:
        # This is just an example - you might want to implement time-based cleanup
        # For now, we'll skip this as guest users are meant to persist
        logger.info("Guest user cleanup skipped - guests are persistent")
        return 0

    except Exception as e:
        logger.error(f"Error cleaning up guest users: {str(e)}")
        raise e


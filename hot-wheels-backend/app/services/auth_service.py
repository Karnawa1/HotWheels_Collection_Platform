"""
Authentication Service
Handles user authentication, registration, and session management
"""

from typing import Optional, Tuple, Dict
from datetime import datetime, timedelta
from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from app import db
from app.models.user import User
from app.models.user_session import UserSession
from app.utils.validators import validate_email, validate_password, validate_username
from app.utils.helpers import hash_token, get_request_ip, get_request_user_agent
from app.utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES
import uuid


class AuthService:
    """
    Authentication service
    Single Responsibility: Handle all authentication-related operations
    """

    @staticmethod
    def register_user(username: str, email: str, password: str, **kwargs) -> Tuple[Optional[User], Optional[str]]:
        """
        Register a new user

        Args:
            username: Username
            email: Email address
            password: Plain text password
            **kwargs: Additional user fields (full_name, country, city, etc.)

        Returns:
            Tuple of (user_object, error_message)
        """
        # Validate inputs
        is_valid, error = validate_username(username)
        if not is_valid:
            return None, error

        is_valid, error = validate_email(email)
        if not is_valid:
            return None, error

        is_valid, error = validate_password(password)
        if not is_valid:
            return None, error

        # Check for duplicates
        if User.query.filter_by(email=email).first():
            return None, ERROR_MESSAGES['DUPLICATE_EMAIL']

        if User.query.filter_by(username=username).first():
            return None, ERROR_MESSAGES['DUPLICATE_USERNAME']

        # Create user
        try:
            user = User(
                username=username,
                email=email,
                **{k: v for k, v in kwargs.items() if k in ['fullname', 'country', 'city', 'bio']}
            )
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            current_app.logger.info(f"New user registered: {username} ({email})")

            return user, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"User registration failed: {str(e)}")
            return None, "Registration failed. Please try again."

    @staticmethod
    def authenticate(email: str, password: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Authenticate user and create session

        Args:
            email: User email
            password: Plain text password

        Returns:
            Tuple of (tokens_dict, error_message)
        """
        # Find user
        user = User.query.filter_by(email=email).first()

        if not user:
            current_app.logger.warning(f"Login attempt with non-existent email: {email}")
            return None, "Invalid email or password"

        # Check if account is active
        if not user.isactive:
            return None, "Account is deactivated"

        # Verify password
        if not user.check_password(password):
            current_app.logger.warning(f"Failed login attempt for user: {email}")
            return None, "Invalid email or password"

        # Create JWT tokens
        try:
            access_token = create_access_token(identity=str(user.userid))
            refresh_token = create_refresh_token(identity=str(user.userid))

            # Create session record
            session = UserSession(
                sessionid=str(uuid.uuid4()),
                userid=user.userid,
                tokenhash=hash_token(access_token),
                ipaddress=get_request_ip(),
                useragent=get_request_user_agent(),
                expiresat=datetime.utcnow() + timedelta(hours=24)
            )

            db.session.add(session)
            user.update_last_login()
            db.session.commit()

            current_app.logger.info(f"User logged in: {user.username}")

            return {
                'accessToken': access_token,
                'refreshToken': refresh_token,
                'user': user.to_dict()
            }, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Authentication error: {str(e)}")
            return None, "Authentication failed"

    @staticmethod
    def logout(user_id: int, token: str) -> Tuple[bool, Optional[str]]:
        """
        Logout user and invalidate session

        Args:
            user_id: User ID
            token: Access token

        Returns:
            Tuple of (success, error_message)
        """
        try:
            token_hash = hash_token(token)

            # Find and delete session
            session = UserSession.query.filter_by(
                userid=user_id,
                tokenhash=token_hash
            ).first()

            if session:
                db.session.delete(session)
                db.session.commit()

            current_app.logger.info(f"User logged out: {user_id}")
            return True, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Logout error: {str(e)}")
            return False, "Logout failed"

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """
        Get user by ID

        Args:
            user_id: User ID

        Returns:
            User object or None
        """
        return User.query.filter_by(userid=user_id, isactive=True).first()

    @staticmethod
    def update_user_profile(user_id: int, **kwargs) -> Tuple[Optional[User], Optional[str]]:
        """
        Update user profile

        Args:
            user_id: User ID
            **kwargs: Fields to update

        Returns:
            Tuple of (user_object, error_message)
        """
        user = User.query.filter_by(userid=user_id).first()

        if not user:
            return None, ERROR_MESSAGES['USER_NOT_FOUND']

        try:
            # Update allowed fields only
            allowed_fields = ['fullname', 'country', 'city', 'bio', 'profileimageurl']

            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    setattr(user, field, value)

            db.session.commit()
            current_app.logger.info(f"User profile updated: {user_id}")

            return user, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Profile update error: {str(e)}")
            return None, "Profile update failed"

    @staticmethod
    def change_password(user_id: int, old_password: str, new_password: str) -> Tuple[bool, Optional[str]]:
        """
        Change user password

        Args:
            user_id: User ID
            old_password: Current password
            new_password: New password

        Returns:
            Tuple of (success, error_message)
        """
        user = User.query.filter_by(userid=user_id).first()

        if not user:
            return False, ERROR_MESSAGES['USER_NOT_FOUND']

        # Verify old password
        if not user.check_password(old_password):
            return False, "Current password is incorrect"

        # Validate new password
        is_valid, error = validate_password(new_password)
        if not is_valid:
            return False, error

        try:
            user.set_password(new_password)

            # Invalidate all existing sessions
            UserSession.query.filter_by(userid=user_id).delete()

            db.session.commit()
            current_app.logger.info(f"Password changed for user: {user_id}")

            return True, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Password change error: {str(e)}")
            return False, "Password change failed"

    @staticmethod
    def cleanup_expired_sessions():
        """
        Remove expired sessions (cron job)
        """
        try:
            expired = UserSession.query.filter(
                UserSession.expiresat < datetime.utcnow()
            ).delete()

            db.session.commit()
            current_app.logger.info(f"Cleaned up {expired} expired sessions")

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Session cleanup error: {str(e)}")
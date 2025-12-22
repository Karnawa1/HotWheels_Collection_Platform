"""
Authentication Routes
User registration, login, logout, and profile management
"""

from flask import Blueprint, request, g
from flask_jwt_extended import jwt_required as jwt_refresh_required
from app.services.auth_service import AuthService
from app.middleware.auth_middleware import jwt_required
from app.utils.helpers import format_success_response, format_error_response
from app.utils.constants import SUCCESS_MESSAGES, ERROR_MESSAGES


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user

    Request Body:
        {
            "username": "string",
            "email": "string",
            "password": "string",
            "full_name": "string" (optional),
            "country": "string" (optional),
            "city": "string" (optional)
        }

    Returns:
        201: User created successfully
        400: Validation error
        409: Email/username already exists
    """
    data = request.get_json()

    # Validate required fields
    required_fields = ['username', 'email', 'password']
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return format_error_response(
            message=f"Missing required fields: {', '.join(missing_fields)}",
            status_code=400
        )

    # Register user
    user, error = AuthService.register_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        fullname=data.get('full_name'),
        country=data.get('country'),
        city=data.get('city'),
        bio=data.get('bio')
    )

    if error:
        return format_error_response(message=error, status_code=400)

    # Auto-login after registration
    result, login_error = AuthService.authenticate(
        email=data['email'],
        password=data['password']
    )

    if login_error:
        # User created but auto-login failed, still return success
        return format_success_response(
            data={'user': user.to_dict()},
            message=SUCCESS_MESSAGES['USER_CREATED'],
            status_code=201
        )

    return format_success_response(
        data=result,
        message=SUCCESS_MESSAGES['USER_CREATED'],
        status_code=201
    )


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT tokens

    Request Body:
        {
            "email": "string",
            "password": "string"
        }

    Returns:
        200: Login successful with tokens
        401: Invalid credentials
    """
    data = request.get_json()

    # Validate required fields
    if not data.get('email') or not data.get('password'):
        return format_error_response(
            message="Email and password are required",
            status_code=400
        )

    # Authenticate
    result, error = AuthService.authenticate(
        email=data['email'],
        password=data['password']
    )

    if error:
        return format_error_response(message=error, status_code=401)

    return format_success_response(
        data=result,
        message=SUCCESS_MESSAGES['LOGIN_SUCCESS'],
        status_code=200
    )


@auth_bp.route('/logout', methods=['POST'])
@jwt_required
def logout():
    """
    Logout user and invalidate session

    Headers:
        Authorization: Bearer <token>

    Returns:
        200: Logout successful
        401: Unauthorized
    """
    token = request.headers.get('Authorization', '').replace('Bearer ', '')

    success, error = AuthService.logout(
        user_id=g.current_user_id,
        token=token
    )

    if error:
        return format_error_response(message=error, status_code=500)

    return format_success_response(
        message=SUCCESS_MESSAGES['LOGOUT_SUCCESS'],
        status_code=200
    )


@auth_bp.route('/me', methods=['GET'])
@jwt_required
def get_current_user():
    """
    Get current authenticated user profile

    Headers:
        Authorization: Bearer <token>

    Returns:
        200: User profile
        401: Unauthorized
    """
    user = g.current_user

    return format_success_response(
        data={'user': user.to_dict()},
        status_code=200
    )


@auth_bp.route('/me', methods=['PUT'])
@jwt_required
def update_profile():
    """
    Update current user profile

    Headers:
        Authorization: Bearer <token>

    Request Body:
        {
            "full_name": "string" (optional),
            "country": "string" (optional),
            "city": "string" (optional),
            "bio": "string" (optional),
            "profile_image_url": "string" (optional)
        }

    Returns:
        200: Profile updated
        401: Unauthorized
        400: Validation error
    """
    data = request.get_json()

    user, error = AuthService.update_user_profile(
        user_id=g.current_user_id,
        **data
    )

    if error:
        return format_error_response(message=error, status_code=400)

    return format_success_response(
        data={'user': user.to_dict()},
        message="Profile updated successfully",
        status_code=200
    )


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required
def change_password():
    """
    Change user password

    Headers:
        Authorization: Bearer <token>

    Request Body:
        {
            "old_password": "string",
            "new_password": "string"
        }

    Returns:
        200: Password changed
        401: Unauthorized
        400: Validation error
    """
    data = request.get_json()

    if not data.get('old_password') or not data.get('new_password'):
        return format_error_response(
            message="Both old and new passwords are required",
            status_code=400
        )

    success, error = AuthService.change_password(
        user_id=g.current_user_id,
        old_password=data['old_password'],
        new_password=data['new_password']
    )

    if error:
        return format_error_response(message=error, status_code=400)

    return format_success_response(
        message="Password changed successfully. Please login again.",
        status_code=200
    )


@auth_bp.route('/refresh', methods=['POST'])
@jwt_refresh_required(refresh=True)
def refresh_token():
    """
    Refresh access token using refresh token

    Headers:
        Authorization: Bearer <refresh_token>

    Returns:
        200: New access token
        401: Invalid refresh token
    """
    from flask_jwt_extended import create_access_token, get_jwt_identity

    try:
        # Get user ID from refresh token (already verified by decorator)
        current_user_id = get_jwt_identity()

        # Create new access token
        new_access_token = create_access_token(identity=current_user_id)

        return format_success_response(
            data={'accessToken': new_access_token},
            message="Token refreshed successfully",
            status_code=200
        )
    except Exception as e:
        return format_error_response(
            message=ERROR_MESSAGES['UNAUTHORIZED'],
            status_code=401
        )
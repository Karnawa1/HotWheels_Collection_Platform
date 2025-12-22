"""
Collections Routes
User collection and wishlist management endpoints
"""

from flask import Blueprint, request, g
from app.services.collection_service import CollectionService
from app.middleware.auth_middleware import jwt_required
from app.utils.helpers import format_success_response, format_error_response
from app.utils.constants import SUCCESS_MESSAGES


collections_bp = Blueprint('collections', __name__)


@collections_bp.route('/', methods=['GET'])
@jwt_required
def get_collection():
    """
    Get current user's collection with filters

    Headers:
        Authorization: Bearer <token>

    Query Parameters:
        page: Page number
        per_page: Items per page
        for_sale: Filter for sale items (true/false)
        for_trade: Filter for trade items (true/false)
        condition: Filter by condition

    Returns:
        200: Paginated collection
        401: Unauthorized
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    filters = {
        'forsale': request.args.get('for_sale', '').lower() == 'true',
        'fortrade': request.args.get('for_trade', '').lower() == 'true',
        'condition': request.args.get('condition')
    }

    # Remove falsy values
    filters = {k: v for k, v in filters.items() if v}

    result = CollectionService.get_user_collection(
        user_id=g.current_user_id,
        page=page,
        per_page=per_page,
        **filters
    )

    return format_success_response(data=result, status_code=200)


@collections_bp.route('/', methods=['POST'])
@jwt_required
def add_to_collection():
    """
    Add a car model to user's collection

    Headers:
        Authorization: Bearer <token>

    Request Body:
        {
            "model_id": integer (required),
            "acquisition_date": "YYYY-MM-DD" (optional),
            "acquisition_price": float (optional),
            "condition": string (optional, default: "Mint"),
            "is_in_package": boolean (optional, default: true),
            "package_condition": string (optional),
            "quantity": integer (optional, default: 1),
            "storage_location": string (optional),
            "notes": string (optional),
            "is_for_trade": boolean (optional, default: false),
            "is_for_sale": boolean (optional, default: false)
        }

    Returns:
        201: Added to collection
        401: Unauthorized
        400: Validation error
        404: Model not found
    """
    data = request.get_json()

    if not data.get('model_id'):
        return format_error_response(
            message="model_id is required",
            status_code=400
        )

    item, error = CollectionService.add_to_collection(
        user_id=g.current_user_id,
        model_id=data['model_id'],
        **{k: v for k, v in data.items() if k != 'model_id'}
    )

    if error:
        return format_error_response(message=error, status_code=400)

    return format_success_response(
        data={'collection_item': item.to_dict(include_relations=True)},
        message=SUCCESS_MESSAGES['COLLECTION_ADDED'],
        status_code=201
    )


@collections_bp.route('/<int:collection_id>', methods=['PUT'])
@jwt_required
def update_collection_item(collection_id):
    """
    Update a collection item

    Headers:
        Authorization: Bearer <token>

    Path Parameters:
        collection_id: Collection item ID

    Request Body:
        {
            "acquisition_price": float (optional),
            "condition": string (optional),
            "is_in_package": boolean (optional),
            "package_condition": string (optional),
            "quantity": integer (optional),
            "storage_location": string (optional),
            "notes": string (optional),
            "is_for_trade": boolean (optional),
            "is_for_sale": boolean (optional)
        }

    Returns:
        200: Item updated
        401: Unauthorized
        404: Item not found
        400: Validation error
    """
    data = request.get_json()

    item, error = CollectionService.update_collection_item(
        collection_id=collection_id,
        user_id=g.current_user_id,
        **data
    )

    if error:
        return format_error_response(message=error, status_code=400)

    return format_success_response(
        data={'collection_item': item.to_dict(include_relations=True)},
        message="Collection item updated successfully",
        status_code=200
    )


@collections_bp.route('/<int:collection_id>', methods=['DELETE'])
@jwt_required
def remove_from_collection(collection_id):
    """
    Remove item from collection

    Headers:
        Authorization: Bearer <token>

    Path Parameters:
        collection_id: Collection item ID

    Returns:
        200: Item removed
        401: Unauthorized
        404: Item not found
    """
    success, error = CollectionService.remove_from_collection(
        collection_id=collection_id,
        user_id=g.current_user_id
    )

    if error:
        return format_error_response(message=error, status_code=404)

    return format_success_response(
        message="Item removed from collection",
        status_code=200
    )


@collections_bp.route('/stats', methods=['GET'])
@jwt_required
def get_collection_stats():
    """
    Get statistics about user's collection

    Headers:
        Authorization: Bearer <token>

    Returns:
        200: Collection statistics
        401: Unauthorized
    """
    stats = CollectionService.get_collection_stats(user_id=g.current_user_id)

    return format_success_response(data={'stats': stats}, status_code=200)


# WISHLIST ENDPOINTS

@collections_bp.route('/wishlist', methods=['GET'])
@jwt_required
def get_wishlist():
    """
    Get current user's wishlist

    Headers:
        Authorization: Bearer <token>

    Query Parameters:
        page: Page number
        per_page: Items per page

    Returns:
        200: Paginated wishlist
        401: Unauthorized
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    result = CollectionService.get_user_wishlist(
        user_id=g.current_user_id,
        page=page,
        per_page=per_page
    )

    return format_success_response(data=result, status_code=200)


@collections_bp.route('/wishlist', methods=['POST'])
@jwt_required
def add_to_wishlist():
    """
    Add a model to user's wishlist

    Headers:
        Authorization: Bearer <token>

    Request Body:
        {
            "model_id": integer (required),
            "priority": integer (optional, 1-5),
            "max_price_willing": float (optional),
            "notes": string (optional)
        }

    Returns:
        201: Added to wishlist
        401: Unauthorized
        400: Validation error
        404: Model not found
    """
    data = request.get_json()

    if not data.get('model_id'):
        return format_error_response(
            message="model_id is required",
            status_code=400
        )

    item, error = CollectionService.add_to_wishlist(
        user_id=g.current_user_id,
        model_id=data['model_id'],
        **{k: v for k, v in data.items() if k != 'model_id'}
    )

    if error:
        return format_error_response(message=error, status_code=400)

    return format_success_response(
        data={'wishlist_item': item.to_dict(include_relations=True)},
        message=SUCCESS_MESSAGES['WISHLIST_ADDED'],
        status_code=201
    )


@collections_bp.route('/wishlist/<int:wishlist_id>', methods=['DELETE'])
@jwt_required
def remove_from_wishlist(wishlist_id):
    """
    Remove item from wishlist

    Headers:
        Authorization: Bearer <token>

    Path Parameters:
        wishlist_id: Wishlist item ID

    Returns:
        200: Item removed
        401: Unauthorized
        404: Item not found
    """
    success, error = CollectionService.remove_from_wishlist(
        wishlist_id=wishlist_id,
        user_id=g.current_user_id
    )

    if error:
        return format_error_response(message=error, status_code=404)

    return format_success_response(
        message="Item removed from wishlist",
        status_code=200
    )
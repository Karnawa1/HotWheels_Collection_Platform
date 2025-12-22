"""
Marketplace Routes
Listings, transactions, and reviews endpoints
"""

from flask import Blueprint, request, g
from app.services.marketplace_service import MarketplaceService
from app.middleware.auth_middleware import jwt_required, optional_jwt
from app.utils.helpers import format_success_response, format_error_response
from app.utils.constants import SUCCESS_MESSAGES


marketplace_bp = Blueprint('marketplace', __name__)


@marketplace_bp.route('/listings', methods=['GET'])
@optional_jwt
def get_listings():
    """
    Get active marketplace listings with filters

    Query Parameters:
        page: Page number
        per_page: Items per page
        model_id: Filter by car model
        listing_type: Filter by type (sale/trade/auction)
        seller_id: Filter by seller
        price_min: Minimum price
        price_max: Maximum price

    Returns:
        200: Paginated listings
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    filters = {
        'model_id': request.args.get('model_id', type=int),
        'listing_type': request.args.get('listing_type'),
        'seller_id': request.args.get('seller_id', type=int),
        'price_min': request.args.get('price_min', type=float),
        'price_max': request.args.get('price_max', type=float)
    }

    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None}

    result = MarketplaceService.get_active_listings(
        page=page,
        per_page=per_page,
        **filters
    )

    return format_success_response(data=result, status_code=200)


@marketplace_bp.route('/listings', methods=['POST'])
@jwt_required
def create_listing():
    """
    Create a new marketplace listing

    Headers:
        Authorization: Bearer <token>

    Request Body:
        {
            "model_id": integer (required),
            "listing_type": string (required, "sale"/"trade"/"auction"),
            "condition": string (required),
            "price": float (required for sales),
            "description": string (optional),
            "collection_item_id": integer (optional),
            "expires_at": datetime (optional)
        }

    Returns:
        201: Listing created
        401: Unauthorized
        400: Validation error
        404: Model not found
    """
    data = request.get_json()

    # Validate required fields
    required = ['model_id', 'listing_type', 'condition']
    missing = [f for f in required if not data.get(f)]

    if missing:
        return format_error_response(
            message=f"Missing required fields: {', '.join(missing)}",
            status_code=400
        )

    listing, error = MarketplaceService.create_listing(
        seller_id=g.current_user_id,
        model_id=data['model_id'],
        listing_type=data['listing_type'],
        condition=data['condition'],
        **{k: v for k, v in data.items() if k not in required}
    )

    if error:
        return format_error_response(message=error, status_code=400)

    return format_success_response(
        data={'listing': listing.to_dict(include_relations=True)},
        message=SUCCESS_MESSAGES['LISTING_CREATED'],
        status_code=201
    )


@marketplace_bp.route('/listings/<int:listing_id>', methods=['GET'])
@optional_jwt
def get_listing(listing_id):
    """
    Get a specific listing by ID

    Path Parameters:
        listing_id: Listing ID

    Returns:
        200: Listing details
        404: Listing not found
    """
    listing = MarketplaceService.get_listing(listing_id, increment_views=True)

    if not listing:
        return format_error_response(
            message="Listing not found",
            status_code=404
        )

    return format_success_response(
        data={'listing': listing.to_dict(include_relations=True)},
        status_code=200
    )


@marketplace_bp.route('/listings/<int:listing_id>', methods=['PUT'])
@jwt_required
def update_listing(listing_id):
    """
    Update a listing (seller only)

    Headers:
        Authorization: Bearer <token>

    Path Parameters:
        listing_id: Listing ID

    Request Body:
        {
            "price": float (optional),
            "description": string (optional),
            "condition": string (optional)
        }

    Returns:
        200: Listing updated
        401: Unauthorized
        403: Not the seller
        404: Listing not found
        400: Validation error
    """
    data = request.get_json()

    listing, error = MarketplaceService.update_listing(
        listing_id=listing_id,
        seller_id=g.current_user_id,
        **data
    )

    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return format_error_response(message=error, status_code=status_code)

    return format_success_response(
        data={'listing': listing.to_dict(include_relations=True)},
        message="Listing updated successfully",
        status_code=200
    )


@marketplace_bp.route('/listings/<int:listing_id>/cancel', methods=['POST'])
@jwt_required
def cancel_listing(listing_id):
    """
    Cancel a listing (seller only)

    Headers:
        Authorization: Bearer <token>

    Path Parameters:
        listing_id: Listing ID

    Returns:
        200: Listing cancelled
        401: Unauthorized
        403: Not the seller
        404: Listing not found
    """
    success, error = MarketplaceService.cancel_listing(
        listing_id=listing_id,
        seller_id=g.current_user_id
    )

    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return format_error_response(message=error, status_code=status_code)

    return format_success_response(
        message="Listing cancelled successfully",
        status_code=200
    )


# TRANSACTION ENDPOINTS

@marketplace_bp.route('/transactions', methods=['POST'])
@jwt_required
def create_transaction():
    """
    Create a transaction (purchase or trade)

    Headers:
        Authorization: Bearer <token>

    Request Body:
        {
            "listing_id": integer (required),
            "payment_method": string (optional)
        }

    Returns:
        201: Transaction created
        401: Unauthorized
        400: Validation error
        404: Listing not found
        409: Cannot buy from yourself
    """
    data = request.get_json()

    if not data.get('listing_id'):
        return format_error_response(
            message="listing_id is required",
            status_code=400
        )

    transaction, error = MarketplaceService.create_transaction(
        listing_id=data['listing_id'],
        buyer_id=g.current_user_id,
        paymentmethod=data.get('payment_method')
    )

    if error:
        # Determine appropriate status code
        if 'not found' in error.lower():
            status_code = 404
        elif 'yourself' in error.lower() or 'not active' in error.lower():
            status_code = 409
        else:
            status_code = 400

        return format_error_response(message=error, status_code=status_code)

    return format_success_response(
        data={'transaction': transaction.to_dict(include_relations=True)},
        message=SUCCESS_MESSAGES['TRANSACTION_COMPLETED'],
        status_code=201
    )


@marketplace_bp.route('/transactions/purchases', methods=['GET'])
@jwt_required
def get_purchases():
    """
    Get current user's purchases

    Headers:
        Authorization: Bearer <token>

    Query Parameters:
        page: Page number
        per_page: Items per page

    Returns:
        200: Paginated purchases
        401: Unauthorized
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    result = MarketplaceService.get_user_transactions(
        user_id=g.current_user_id,
        as_buyer=True,
        page=page,
        per_page=per_page
    )

    return format_success_response(data=result, status_code=200)


@marketplace_bp.route('/transactions/sales', methods=['GET'])
@jwt_required
def get_sales():
    """
    Get current user's sales

    Headers:
        Authorization: Bearer <token>

    Query Parameters:
        page: Page number
        per_page: Items per page

    Returns:
        200: Paginated sales
        401: Unauthorized
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    result = MarketplaceService.get_user_transactions(
        user_id=g.current_user_id,
        as_buyer=False,
        page=page,
        per_page=per_page
    )

    return format_success_response(data=result, status_code=200)


# REVIEW ENDPOINTS

@marketplace_bp.route('/reviews', methods=['POST'])
@jwt_required
def create_review():
    """
    Create a review for a transaction

    Headers:
        Authorization: Bearer <token>

    Request Body:
        {
            "transaction_id": integer (required),
            "reviewee_id": integer (required),
            "rating": integer (required, 1-5),
            "comment": string (optional)
        }

    Returns:
        201: Review created
        401: Unauthorized
        400: Validation error
        404: Transaction not found
        409: Already reviewed
    """
    data = request.get_json()

    required = ['transaction_id', 'reviewee_id', 'rating']
    missing = [f for f in required if f not in data]

    if missing:
        return format_error_response(
            message=f"Missing required fields: {', '.join(missing)}",
            status_code=400
        )

    review, error = MarketplaceService.create_review(
        transaction_id=data['transaction_id'],
        reviewer_id=g.current_user_id,
        reviewee_id=data['reviewee_id'],
        rating=data['rating'],
        comment=data.get('comment')
    )

    if error:
        # Determine status code
        if 'not found' in error.lower():
            status_code = 404
        elif 'already' in error.lower():
            status_code = 409
        else:
            status_code = 400

        return format_error_response(message=error, status_code=status_code)

    return format_success_response(
        data={'review': review.to_dict(include_relations=True)},
        message=SUCCESS_MESSAGES['REVIEW_SUBMITTED'],
        status_code=201
    )
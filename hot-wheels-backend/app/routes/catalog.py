"""
Catalog Routes
Car model catalog, search, and filtering endpoints
"""

from flask import Blueprint, request
from app.services.catalog_service import CatalogService
from app.middleware.auth_middleware import optional_jwt
from app.utils.helpers import format_success_response, format_error_response


catalog_bp = Blueprint('catalog', __name__)


@catalog_bp.route('/models', methods=['GET'])
@optional_jwt
def search_models():
    """
    Search car models with filters

    Query Parameters:
        q: Search query (casting name)
        page: Page number (default: 1)
        per_page: Items per page (default: 20, max: 100)
        year_min: Minimum release year
        year_max: Maximum release year
        rarity: Rarity level
        color: Color filter
        series: Series name filter

    Returns:
        200: Paginated search results
    """
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    # Build filters from query parameters
    filters = {
        'year_min': request.args.get('year_min', type=int),
        'year_max': request.args.get('year_max', type=int),
        'rarity': request.args.get('rarity'),
        'color': request.args.get('color'),
        'series': request.args.get('series')
    }

    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None}

    result = CatalogService.search_models(
        query=query if query else None,
        page=page,
        per_page=per_page,
        **filters
    )

    return format_success_response(data=result, status_code=200)


@catalog_bp.route('/models/<int:model_id>', methods=['GET'])
@optional_jwt
def get_model(model_id):
    """
    Get a specific car model by ID

    Path Parameters:
        model_id: Car model ID

    Returns:
        200: Model details
        404: Model not found
    """
    model = CatalogService.get_model_by_id(model_id, include_relations=True)

    if not model:
        return format_error_response(
            message="Car model not found",
            status_code=404
        )

    return format_success_response(
        data={'model': model.to_dict(include_relations=True)},
        status_code=200
    )


@catalog_bp.route('/models/rare', methods=['GET'])
@optional_jwt
def get_rare_models():
    """
    Get rare and special models (Rare, Chase, Super Treasure Hunt)

    Query Parameters:
        page: Page number
        per_page: Items per page

    Returns:
        200: Paginated rare models
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    result = CatalogService.get_rare_models(page=page, per_page=per_page)

    return format_success_response(data=result, status_code=200)


@catalog_bp.route('/models/recent', methods=['GET'])
@optional_jwt
def get_recent_releases():
    """
    Get recently released models

    Query Parameters:
        year: Year filter (default: current year)
        page: Page number
        per_page: Items per page

    Returns:
        200: Paginated recent models
    """
    year = request.args.get('year', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    result = CatalogService.get_recent_releases(
        year=year,
        page=page,
        per_page=per_page
    )

    return format_success_response(data=result, status_code=200)


@catalog_bp.route('/models/popular', methods=['GET'])
@optional_jwt
def get_popular_models():
    """
    Get most popular models (most collected)

    Query Parameters:
        limit: Number of results (default: 10, max: 50)

    Returns:
        200: List of popular models
    """
    limit = request.args.get('limit', 10, type=int)
    limit = min(limit, 50)  # Cap at 50

    models = CatalogService.get_popular_models(limit=limit)

    return format_success_response(
        data={'models': [m.to_dict() for m in models]},
        status_code=200
    )


@catalog_bp.route('/castings', methods=['GET'])
@optional_jwt
def get_castings():
    """
    Get all castings with pagination

    Query Parameters:
        page: Page number
        per_page: Items per page

    Returns:
        200: Paginated castings
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    result = CatalogService.get_all_castings(page=page, per_page=per_page)

    return format_success_response(data=result, status_code=200)


@catalog_bp.route('/castings/<int:casting_id>', methods=['GET'])
@optional_jwt
def get_casting(casting_id):
    """
    Get a specific casting by ID

    Path Parameters:
        casting_id: Casting ID

    Returns:
        200: Casting details
        404: Casting not found
    """
    casting = CatalogService.get_casting_by_id(casting_id)

    if not casting:
        return format_error_response(
            message="Casting not found",
            status_code=404
        )

    return format_success_response(
        data={'casting': casting.to_dict()},
        status_code=200
    )


@catalog_bp.route('/castings/<int:casting_id>/models', methods=['GET'])
@optional_jwt
def get_casting_models(casting_id):
    """
    Get all models for a specific casting

    Path Parameters:
        casting_id: Casting ID

    Query Parameters:
        page: Page number
        per_page: Items per page

    Returns:
        200: Paginated models for casting
        404: Casting not found
    """
    # Verify casting exists
    casting = CatalogService.get_casting_by_id(casting_id)
    if not casting:
        return format_error_response(
            message="Casting not found",
            status_code=404
        )

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    result = CatalogService.get_models_by_casting(
        casting_id=casting_id,
        page=page,
        per_page=per_page
    )

    return format_success_response(data=result, status_code=200)


@catalog_bp.route('/castings/search', methods=['GET'])
@optional_jwt
def search_castings():
    """
    Search castings by name

    Query Parameters:
        q: Search query
        page: Page number
        per_page: Items per page

    Returns:
        200: Paginated search results
        400: Missing query parameter
    """
    query = request.args.get('q', '').strip()

    if not query:
        return format_error_response(
            message="Search query 'q' is required",
            status_code=400
        )

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    result = CatalogService.search_castings(
        query=query,
        page=page,
        per_page=per_page
    )

    return format_success_response(data=result, status_code=200)


@catalog_bp.route('/series', methods=['GET'])
@optional_jwt
def get_series():
    """
    Get all series with optional year filter

    Query Parameters:
        year: Filter by release year
        page: Page number
        per_page: Items per page

    Returns:
        200: Paginated series
    """
    year = request.args.get('year', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    result = CatalogService.get_all_series(
        year=year,
        page=page,
        per_page=per_page
    )

    return format_success_response(data=result, status_code=200)


@catalog_bp.route('/series/<int:series_id>', methods=['GET'])
@optional_jwt
def get_series_detail(series_id):
    """
    Get a specific series by ID

    Path Parameters:
        series_id: Series ID

    Returns:
        200: Series details
        404: Series not found
    """
    series = CatalogService.get_series_by_id(series_id)

    if not series:
        return format_error_response(
            message="Series not found",
            status_code=404
        )

    return format_success_response(
        data={'series': series.to_dict()},
        status_code=200
    )


@catalog_bp.route('/series/<int:series_id>/models', methods=['GET'])
@optional_jwt
def get_series_models(series_id):
    """
    Get all models for a specific series

    Path Parameters:
        series_id: Series ID

    Query Parameters:
        page: Page number
        per_page: Items per page

    Returns:
        200: Paginated models for series
        404: Series not found
    """
    # Verify series exists
    series = CatalogService.get_series_by_id(series_id)
    if not series:
        return format_error_response(
            message="Series not found",
            status_code=404
        )

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    result = CatalogService.get_models_by_series(
        series_id=series_id,
        page=page,
        per_page=per_page
    )

    return format_success_response(data=result, status_code=200)


@catalog_bp.route('/manufacturers', methods=['GET'])
@optional_jwt
def get_manufacturers():
    """
    Get all manufacturers

    Returns:
        200: List of manufacturers
    """
    manufacturers = CatalogService.get_all_manufacturers()

    return format_success_response(
        data={'manufacturers': [m.to_dict() for m in manufacturers]},
        status_code=200
    )


@catalog_bp.route('/stats', methods=['GET'])
@optional_jwt
def get_catalog_stats():
    """
    Get catalog statistics

    Returns:
        200: Catalog statistics
    """
    stats = CatalogService.get_catalog_stats()

    return format_success_response(data={'stats': stats}, status_code=200)
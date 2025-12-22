"""
Catalog Service
Handles car model catalog, search, and filtering
"""

from typing import Optional, Dict, List
from flask import current_app
from sqlalchemy import and_, or_, func
from app import db
from app.models.car_model import CarModel
from app.models.casting import Casting
from app.models.series import Series
from app.models.manufacturer import Manufacturer
from app.utils.helpers import paginate_query, sanitize_search_query, parse_filters
from app.utils.constants import ERROR_MESSAGES


class CatalogService:
    """
    Catalog service
    Single Responsibility: Handle car model catalog operations
    """

    @staticmethod
    def search_models(query: str = None, page: int = 1, per_page: int = 20, **filters) -> Dict:
        """
        Search car models with filters

        Args:
            query: Search query string
            page: Page number
            per_page: Items per page
            **filters: Additional filters (year, rarity, series, etc.)

        Returns:
            Dictionary with paginated search results
        """
        # Start with base query
        db_query = CarModel.query

        # Text search on casting name
        if query:
            sanitized = sanitize_search_query(query)
            db_query = db_query.join(Casting).filter(
                Casting.castingname.ilike(f'%{sanitized}%')
            )

        # Apply filters
        validated_filters = parse_filters(filters)

        if validated_filters.get('year_min'):
            db_query = db_query.filter(CarModel.releaseyear >= validated_filters['year_min'])

        if validated_filters.get('year_max'):
            db_query = db_query.filter(CarModel.releaseyear <= validated_filters['year_max'])

        if validated_filters.get('rarity'):
            db_query = db_query.filter(CarModel.raritylevel == validated_filters['rarity'])

        if validated_filters.get('color'):
            db_query = db_query.filter(CarModel.color.ilike(f'%{validated_filters["color"]}%'))

        if validated_filters.get('series'):
            db_query = db_query.join(Series).filter(
                Series.seriesname.ilike(f'%{validated_filters["series"]}%')
            )

        # Order by release year (newest first) then by ID
        db_query = db_query.order_by(
            CarModel.releaseyear.desc(),
            CarModel.modelid.desc()
        )

        return paginate_query(db_query, page, per_page)

    @staticmethod
    def get_model_by_id(model_id: int, include_relations: bool = True) -> Optional[CarModel]:
        """
        Get a car model by ID

        Args:
            model_id: Car model ID
            include_relations: Whether to eager load relationships

        Returns:
            CarModel object or None
        """
        if include_relations:
            return CarModel.query.options(
                db.joinedload(CarModel.casting),
                db.joinedload(CarModel.series)
            ).filter_by(modelid=model_id).first()

        return CarModel.query.filter_by(modelid=model_id).first()

    @staticmethod
    def get_models_by_casting(casting_id: int, page: int = 1, per_page: int = 20) -> Dict:
        """
        Get all models for a specific casting

        Args:
            casting_id: Casting ID
            page: Page number
            per_page: Items per page

        Returns:
            Dictionary with paginated models
        """
        query = CarModel.query.filter_by(castingid=casting_id).order_by(
            CarModel.releaseyear.desc()
        )

        return paginate_query(query, page, per_page)

    @staticmethod
    def get_models_by_series(series_id: int, page: int = 1, per_page: int = 20) -> Dict:
        """
        Get all models for a specific series

        Args:
            series_id: Series ID
            page: Page number
            per_page: Items per page

        Returns:
            Dictionary with paginated models
        """
        query = CarModel.query.filter_by(seriesid=series_id).order_by(
            CarModel.releaseyear.desc(),
            CarModel.color
        )

        return paginate_query(query, page, per_page)

    @staticmethod
    def get_rare_models(page: int = 1, per_page: int = 20) -> Dict:
        """
        Get rare and special models

        Args:
            page: Page number
            per_page: Items per page

        Returns:
            Dictionary with paginated rare models
        """
        query = CarModel.query.filter(
            CarModel.raritylevel.in_(['Rare', 'Chase', 'Super Treasure Hunt'])
        ).order_by(CarModel.releaseyear.desc())

        return paginate_query(query, page, per_page)

    @staticmethod
    def get_recent_releases(year: int = None, page: int = 1, per_page: int = 20) -> Dict:
        """
        Get recently released models

        Args:
            year: Optional year filter
            page: Page number
            per_page: Items per page

        Returns:
            Dictionary with paginated recent models
        """
        from datetime import datetime

        if not year:
            year = datetime.now().year

        query = CarModel.query.filter_by(releaseyear=year).order_by(
            CarModel.createdat.desc()
        )

        return paginate_query(query, page, per_page)

    # CASTING METHODS

    @staticmethod
    def get_all_castings(page: int = 1, per_page: int = 50) -> Dict:
        """
        Get all castings

        Args:
            page: Page number
            per_page: Items per page

        Returns:
            Dictionary with paginated castings
        """
        query = Casting.query.order_by(Casting.castingname)

        return paginate_query(query, page, per_page)

    @staticmethod
    def get_casting_by_id(casting_id: int) -> Optional[Casting]:
        """
        Get casting by ID

        Args:
            casting_id: Casting ID

        Returns:
            Casting object or None
        """
        return Casting.query.filter_by(castingid=casting_id).first()

    @staticmethod
    def search_castings(query: str, page: int = 1, per_page: int = 20) -> Dict:
        """
        Search castings by name

        Args:
            query: Search query
            page: Page number
            per_page: Items per page

        Returns:
            Dictionary with paginated castings
        """
        sanitized = sanitize_search_query(query)

        db_query = Casting.query.filter(
            Casting.castingname.ilike(f'%{sanitized}%')
        ).order_by(Casting.castingname)

        return paginate_query(db_query, page, per_page)

    # SERIES METHODS

    @staticmethod
    def get_all_series(year: int = None, page: int = 1, per_page: int = 50) -> Dict:
        """
        Get all series, optionally filtered by year

        Args:
            year: Optional year filter
            page: Page number
            per_page: Items per page

        Returns:
            Dictionary with paginated series
        """
        query = Series.query

        if year:
            query = query.filter_by(releaseyear=year)

        query = query.order_by(Series.releaseyear.desc(), Series.seriesname)

        return paginate_query(query, page, per_page)

    @staticmethod
    def get_series_by_id(series_id: int) -> Optional[Series]:
        """
        Get series by ID

        Args:
            series_id: Series ID

        Returns:
            Series object or None
        """
        return Series.query.filter_by(seriesid=series_id).first()

    # MANUFACTURER METHODS

    @staticmethod
    def get_all_manufacturers() -> List[Manufacturer]:
        """
        Get all manufacturers

        Returns:
            List of Manufacturer objects
        """
        return Manufacturer.query.order_by(Manufacturer.name).all()

    @staticmethod
    def get_manufacturer_by_id(manufacturer_id: int) -> Optional[Manufacturer]:
        """
        Get manufacturer by ID

        Args:
            manufacturer_id: Manufacturer ID

        Returns:
            Manufacturer object or None
        """
        return Manufacturer.query.filter_by(manufacturerid=manufacturer_id).first()

    # STATISTICS METHODS

    @staticmethod
    def get_catalog_stats() -> Dict:
        """
        Get catalog statistics

        Returns:
            Dictionary with statistics
        """
        total_models = CarModel.query.count()
        total_castings = Casting.query.count()
        total_series = Series.query.count()

        # Models by rarity
        rarity_stats = db.session.query(
            CarModel.raritylevel,
            func.count(CarModel.modelid)
        ).group_by(CarModel.raritylevel).all()

        # Models by year (last 5 years)
        from datetime import datetime
        current_year = datetime.now().year

        year_stats = db.session.query(
            CarModel.releaseyear,
            func.count(CarModel.modelid)
        ).filter(
            CarModel.releaseyear >= current_year - 5
        ).group_by(CarModel.releaseyear).order_by(
            CarModel.releaseyear.desc()
        ).all()

        return {
            'total_models': total_models,
            'total_castings': total_castings,
            'total_series': total_series,
            'by_rarity': {rarity: count for rarity, count in rarity_stats},
            'by_year': {year: count for year, count in year_stats}
        }

    @staticmethod
    def get_popular_models(limit: int = 10) -> List[CarModel]:
        """
        Get popular models (most in collections)

        Args:
            limit: Number of models to return

        Returns:
            List of CarModel objects
        """
        from app.models.user import UserCollection

        # Query models with most collection entries
        popular = db.session.query(
            CarModel,
            func.count(UserCollection.collectionid).label('collection_count')
        ).join(
            UserCollection, CarModel.modelid == UserCollection.modelid
        ).group_by(
            CarModel.modelid
        ).order_by(
            func.count(UserCollection.collectionid).desc()
        ).limit(limit).all()

        return [model for model, count in popular]
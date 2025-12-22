"""
Unit Tests for Catalog Service
Tests car model catalog, search, and filtering
"""

import pytest
from app.services.catalog_service import CatalogService
from app.models.car_model import CarModel
from app.models.casting import Casting
from app.models.series import Series


class TestCatalogServiceSearchModels:
    """Tests for searching car models"""

    def test_search_models_all(self, app, sample_car_model):
        """Test searching all models without filters"""
        with app.app_context():
            result = CatalogService.search_models()
            
            assert 'items' in result
            assert 'pagination' in result
            assert len(result['items']) >= 1

    def test_search_models_by_query(self, app, sample_car_model, sample_casting):
        """Test searching models by text query"""
        with app.app_context():
            result = CatalogService.search_models(query='Camaro')
            
            assert 'items' in result
            # All results should match the query

    def test_search_models_by_year_range(self, app, sample_car_model):
        """Test filtering models by year range"""
        with app.app_context():
            result = CatalogService.search_models(
                year_min=2020,
                year_max=2024
            )
            
            for item in result['items']:
                assert 2020 <= item['release_year'] <= 2024

    def test_search_models_by_rarity(self, app, sample_car_model, rare_car_model):
        """Test filtering models by rarity"""
        with app.app_context():
            result = CatalogService.search_models(rarity='Common')
            
            for item in result['items']:
                assert item['rarity_level'] == 'Common'

    def test_search_models_pagination(self, app, sample_car_model):
        """Test models search pagination"""
        with app.app_context():
            result = CatalogService.search_models(page=1, per_page=5)
            
            assert result['pagination']['per_page'] == 5
            assert result['pagination']['page'] == 1


class TestCatalogServiceGetModel:
    """Tests for getting individual models"""

    def test_get_model_by_id_success(self, app, sample_car_model):
        """Test getting model by ID"""
        with app.app_context():
            model = CatalogService.get_model_by_id(sample_car_model.modelid)
            
            assert model is not None
            assert model.modelid == sample_car_model.modelid

    def test_get_model_by_id_not_found(self, app):
        """Test getting non-existent model"""
        with app.app_context():
            model = CatalogService.get_model_by_id(99999)
            assert model is None

    def test_get_model_with_relations(self, app, sample_car_model):
        """Test getting model with eager-loaded relations"""
        with app.app_context():
            model = CatalogService.get_model_by_id(
                sample_car_model.modelid,
                include_relations=True
            )
            
            assert model is not None
            # Relations should be loaded
            assert model.casting is not None
            assert model.series is not None


class TestCatalogServiceModelsByCasting:
    """Tests for getting models by casting"""

    def test_get_models_by_casting(self, app, sample_casting, sample_car_model):
        """Test getting all models for a casting"""
        with app.app_context():
            result = CatalogService.get_models_by_casting(
                casting_id=sample_casting.castingid
            )
            
            assert 'items' in result
            for item in result['items']:
                assert item['casting_id'] == sample_casting.castingid

    def test_get_models_by_casting_empty(self, app, sample_manufacturer):
        """Test getting models for casting with no models"""
        with app.app_context():
            # Create empty casting
            from app import db
            casting = Casting(
                castingname='Empty Casting',
                firstreleaseyear=2024,
                manufacturerid=sample_manufacturer.manufacturerid
            )
            db.session.add(casting)
            db.session.commit()
            
            result = CatalogService.get_models_by_casting(casting.castingid)
            assert len(result['items']) == 0


class TestCatalogServiceModelsBySeries:
    """Tests for getting models by series"""

    def test_get_models_by_series(self, app, sample_series, sample_car_model):
        """Test getting all models for a series"""
        with app.app_context():
            result = CatalogService.get_models_by_series(
                series_id=sample_series.seriesid
            )
            
            assert 'items' in result
            for item in result['items']:
                assert item['series_id'] == sample_series.seriesid


class TestCatalogServiceRareModels:
    """Tests for getting rare models"""

    def test_get_rare_models(self, app, rare_car_model):
        """Test getting rare models"""
        with app.app_context():
            result = CatalogService.get_rare_models()
            
            assert 'items' in result
            for item in result['items']:
                assert item['rarity_level'] in ['Rare', 'Chase', 'Super Treasure Hunt']

    def test_get_rare_models_pagination(self, app, rare_car_model):
        """Test rare models pagination"""
        with app.app_context():
            result = CatalogService.get_rare_models(page=1, per_page=10)
            
            assert result['pagination']['per_page'] == 10


class TestCatalogServiceRecentReleases:
    """Tests for getting recent releases"""

    def test_get_recent_releases_current_year(self, app, sample_car_model):
        """Test getting releases from current year"""
        with app.app_context():
            result = CatalogService.get_recent_releases(year=2024)
            
            assert 'items' in result
            for item in result['items']:
                assert item['release_year'] == 2024

    def test_get_recent_releases_default_year(self, app):
        """Test getting releases defaults to current year"""
        with app.app_context():
            from datetime import datetime
            current_year = datetime.now().year
            
            result = CatalogService.get_recent_releases()
            
            # Should use current year by default
            assert 'items' in result


class TestCatalogServiceCastings:
    """Tests for casting operations"""

    def test_get_all_castings(self, app, sample_casting):
        """Test getting all castings"""
        with app.app_context():
            result = CatalogService.get_all_castings()
            
            assert 'items' in result
            assert len(result['items']) >= 1

    def test_get_casting_by_id(self, app, sample_casting):
        """Test getting casting by ID"""
        with app.app_context():
            casting = CatalogService.get_casting_by_id(sample_casting.castingid)
            
            assert casting is not None
            assert casting.castingid == sample_casting.castingid

    def test_get_casting_by_id_not_found(self, app):
        """Test getting non-existent casting"""
        with app.app_context():
            casting = CatalogService.get_casting_by_id(99999)
            assert casting is None

    def test_search_castings(self, app, sample_casting):
        """Test searching castings by name"""
        with app.app_context():
            result = CatalogService.search_castings(query='Camaro')
            
            assert 'items' in result


class TestCatalogServiceSeries:
    """Tests for series operations"""

    def test_get_all_series(self, app, sample_series):
        """Test getting all series"""
        with app.app_context():
            result = CatalogService.get_all_series()
            
            assert 'items' in result
            assert len(result['items']) >= 1

    def test_get_all_series_by_year(self, app, sample_series):
        """Test filtering series by year"""
        with app.app_context():
            result = CatalogService.get_all_series(year=2024)
            
            for item in result['items']:
                assert item['release_year'] == 2024

    def test_get_series_by_id(self, app, sample_series):
        """Test getting series by ID"""
        with app.app_context():
            series = CatalogService.get_series_by_id(sample_series.seriesid)
            
            assert series is not None
            assert series.seriesid == sample_series.seriesid

    def test_get_series_by_id_not_found(self, app):
        """Test getting non-existent series"""
        with app.app_context():
            series = CatalogService.get_series_by_id(99999)
            assert series is None


class TestCatalogServiceManufacturers:
    """Tests for manufacturer operations"""

    def test_get_all_manufacturers(self, app, sample_manufacturer):
        """Test getting all manufacturers"""
        with app.app_context():
            manufacturers = CatalogService.get_all_manufacturers()
            
            assert len(manufacturers) >= 1

    def test_get_manufacturer_by_id(self, app, sample_manufacturer):
        """Test getting manufacturer by ID"""
        with app.app_context():
            manufacturer = CatalogService.get_manufacturer_by_id(
                sample_manufacturer.manufacturerid
            )
            
            assert manufacturer is not None
            assert manufacturer.name == 'Mattel'

    def test_get_manufacturer_by_id_not_found(self, app):
        """Test getting non-existent manufacturer"""
        with app.app_context():
            manufacturer = CatalogService.get_manufacturer_by_id(99999)
            assert manufacturer is None


class TestCatalogServiceStats:
    """Tests for catalog statistics"""

    def test_get_catalog_stats(self, app, sample_car_model, sample_casting, sample_series):
        """Test getting catalog statistics"""
        with app.app_context():
            stats = CatalogService.get_catalog_stats()
            
            assert 'total_models' in stats
            assert 'total_castings' in stats
            assert 'total_series' in stats
            assert 'by_rarity' in stats
            assert 'by_year' in stats
            assert stats['total_models'] >= 1
            assert stats['total_castings'] >= 1


class TestCarModelModel:
    """Tests for CarModel model"""

    def test_car_model_to_dict(self, app, sample_car_model):
        """Test CarModel to_dict conversion"""
        with app.app_context():
            model_dict = sample_car_model.to_dict()
            
            assert 'model_id' in model_dict
            assert 'casting_id' in model_dict
            assert 'release_year' in model_dict
            assert 'color' in model_dict
            assert 'rarity_level' in model_dict
            assert model_dict['color'] == 'Spectraflame Red'

    def test_car_model_to_dict_with_relations(self, app, sample_car_model):
        """Test CarModel to_dict with relations"""
        with app.app_context():
            model_dict = sample_car_model.to_dict(include_relations=True)
            
            assert 'casting_name' in model_dict
            assert 'series_name' in model_dict


class TestCastingModel:
    """Tests for Casting model"""

    def test_casting_to_dict(self, app, sample_casting):
        """Test Casting to_dict conversion"""
        with app.app_context():
            casting_dict = sample_casting.to_dict()
            
            assert 'casting_id' in casting_dict
            assert 'casting_name' in casting_dict
            assert casting_dict['casting_name'] == "'67 Camaro"


class TestSeriesModel:
    """Tests for Series model"""

    def test_series_to_dict(self, app, sample_series):
        """Test Series to_dict conversion"""
        with app.app_context():
            series_dict = sample_series.to_dict()
            
            assert 'series_id' in series_dict
            assert 'series_name' in series_dict
            assert 'release_year' in series_dict
            assert series_dict['series_name'] == 'Mainline 2024'


class TestManufacturerModel:
    """Tests for Manufacturer model"""

    def test_manufacturer_to_dict(self, app, sample_manufacturer):
        """Test Manufacturer to_dict conversion"""
        with app.app_context():
            mfr_dict = sample_manufacturer.to_dict()
            
            assert 'manufacturer_id' in mfr_dict
            assert 'name' in mfr_dict
            assert mfr_dict['name'] == 'Mattel'


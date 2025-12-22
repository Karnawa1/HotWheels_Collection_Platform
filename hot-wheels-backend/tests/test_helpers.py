"""
Unit Tests for Helpers Module
Tests utility functions
"""

import pytest
from app.utils.helpers import (
    format_error_response,
    format_success_response,
    generate_sku,
    mask_email,
    hash_token,
    generate_token,
    sanitize_search_query,
    parse_filters,
    calculate_offset,
    build_pagination_links
)


class TestFormatErrorResponse:
    """Tests for error response formatting"""

    def test_basic_error_response(self):
        """Test basic error response structure"""
        response, status_code = format_error_response("Test error", 400)
        
        assert status_code == 400
        assert response['success'] is False
        assert response['error'] == "Test error"
        assert 'timestamp' in response

    def test_error_response_with_details(self):
        """Test error response with additional details"""
        details = {'field': 'email', 'reason': 'Invalid format'}
        response, status_code = format_error_response("Validation error", 422, errors=details)
        
        assert status_code == 422
        assert response['details'] == details

    def test_default_status_code(self):
        """Test default status code is 400"""
        response, status_code = format_error_response("Error")
        assert status_code == 400

    def test_server_error_status(self):
        """Test 500 status code"""
        response, status_code = format_error_response("Internal error", 500)
        assert status_code == 500


class TestFormatSuccessResponse:
    """Tests for success response formatting"""

    def test_basic_success_response(self):
        """Test basic success response structure"""
        data = {'user_id': 1, 'username': 'test'}
        response, status_code = format_success_response(data=data)
        
        assert status_code == 200
        assert response['success'] is True
        assert response['data'] == data
        assert 'timestamp' in response

    def test_success_response_with_message(self):
        """Test success response with message"""
        response, status_code = format_success_response(
            data={'id': 1},
            message="Created successfully",
            status_code=201
        )
        
        assert status_code == 201
        assert response['message'] == "Created successfully"

    def test_success_response_no_data(self):
        """Test success response without data"""
        response, status_code = format_success_response(message="Done")
        
        assert response['success'] is True
        assert 'data' not in response or response.get('data') is None
        assert response['message'] == "Done"


class TestGenerateSku:
    """Tests for SKU generation"""

    def test_generate_sku_format(self):
        """Test SKU format"""
        sku = generate_sku("'67 Camaro", "Red", 2024)
        
        assert sku.startswith('HW-2024-')
        assert len(sku) == 16  # HW-YEAR-HASH (HW-2024-XXXXXXXX)

    def test_generate_sku_deterministic(self):
        """Test SKU generation is deterministic"""
        sku1 = generate_sku("Mustang", "Blue", 2023)
        sku2 = generate_sku("Mustang", "Blue", 2023)
        
        assert sku1 == sku2

    def test_generate_sku_unique_for_different_inputs(self):
        """Test different inputs produce different SKUs"""
        sku1 = generate_sku("Camaro", "Red", 2024)
        sku2 = generate_sku("Mustang", "Red", 2024)
        sku3 = generate_sku("Camaro", "Blue", 2024)
        
        assert sku1 != sku2
        assert sku1 != sku3


class TestMaskEmail:
    """Tests for email masking"""

    def test_mask_normal_email(self):
        """Test masking normal email"""
        masked = mask_email('john.doe@example.com')
        
        assert masked == 'joh***@example.com'
        assert '@example.com' in masked

    def test_mask_short_local_part(self):
        """Test masking email with short local part"""
        masked = mask_email('ab@example.com')
        
        assert '@example.com' in masked
        assert 'ab' not in masked or '***' in masked

    def test_mask_empty_email(self):
        """Test masking empty email"""
        masked = mask_email('')
        assert masked == '***@***'

    def test_mask_none_email(self):
        """Test masking None email"""
        masked = mask_email(None)
        assert masked == '***@***'

    def test_mask_invalid_email(self):
        """Test masking invalid email without @"""
        masked = mask_email('invalidemail')
        assert masked == '***@***'


class TestHashToken:
    """Tests for token hashing"""

    def test_hash_token_returns_string(self):
        """Test hash token returns string"""
        hashed = hash_token('test_token')
        
        assert isinstance(hashed, str)
        assert len(hashed) == 64  # SHA-256 produces 64 hex chars

    def test_hash_token_deterministic(self):
        """Test same input produces same hash"""
        hash1 = hash_token('my_token')
        hash2 = hash_token('my_token')
        
        assert hash1 == hash2

    def test_hash_token_different_inputs(self):
        """Test different inputs produce different hashes"""
        hash1 = hash_token('token1')
        hash2 = hash_token('token2')
        
        assert hash1 != hash2


class TestGenerateToken:
    """Tests for token generation"""

    def test_generate_token_returns_string(self):
        """Test generate token returns string"""
        token = generate_token()
        assert isinstance(token, str)

    def test_generate_token_is_random(self):
        """Test generated tokens are unique"""
        tokens = [generate_token() for _ in range(10)]
        unique_tokens = set(tokens)
        
        assert len(unique_tokens) == 10  # All should be unique

    def test_generate_token_length(self):
        """Test token has reasonable length"""
        token = generate_token()
        assert len(token) >= 32  # Should be at least 32 chars


class TestSanitizeSearchQuery:
    """Tests for search query sanitization"""

    def test_sanitize_normal_query(self):
        """Test sanitizing normal search query"""
        sanitized = sanitize_search_query('Camaro 67')
        assert sanitized == 'Camaro 67'

    def test_sanitize_removes_special_chars(self):
        """Test sanitization removes dangerous characters"""
        sanitized = sanitize_search_query("'; DROP TABLE users;--")
        assert ';' not in sanitized
        assert "'" not in sanitized
        assert '--' not in sanitized

    def test_sanitize_allows_alphanumeric(self):
        """Test sanitization allows alphanumeric and basic chars"""
        sanitized = sanitize_search_query('Hot-Wheels_2024')
        assert 'Hot' in sanitized
        assert 'Wheels' in sanitized
        assert '2024' in sanitized

    def test_sanitize_empty_query(self):
        """Test sanitizing empty query"""
        sanitized = sanitize_search_query('')
        assert sanitized == ''

    def test_sanitize_none_query(self):
        """Test sanitizing None query"""
        sanitized = sanitize_search_query(None)
        assert sanitized == ''

    def test_sanitize_limits_length(self):
        """Test sanitization limits query length"""
        long_query = 'a' * 200
        sanitized = sanitize_search_query(long_query)
        assert len(sanitized) <= 100


class TestParseFilters:
    """Tests for filter parsing"""

    def test_parse_year_filters(self):
        """Test parsing year filters"""
        filters = {'year_min': '2020', 'year_max': '2024'}
        parsed = parse_filters(filters)
        
        assert parsed['year_min'] == 2020
        assert parsed['year_max'] == 2024

    def test_parse_price_filters(self):
        """Test parsing price filters"""
        filters = {'price_min': '5.99', 'price_max': '50.00'}
        parsed = parse_filters(filters)
        
        assert parsed['price_min'] == 5.99
        assert parsed['price_max'] == 50.00

    def test_parse_string_filters(self):
        """Test parsing string filters"""
        filters = {'color': 'Red', 'rarity': 'Rare', 'condition': 'Mint'}
        parsed = parse_filters(filters)
        
        assert parsed['color'] == 'Red'
        assert parsed['rarity'] == 'Rare'
        assert parsed['condition'] == 'Mint'

    def test_parse_invalid_year(self):
        """Test parsing invalid year filter"""
        filters = {'year_min': 'invalid'}
        parsed = parse_filters(filters)
        
        assert 'year_min' not in parsed

    def test_parse_empty_filters(self):
        """Test parsing empty filters"""
        parsed = parse_filters({})
        assert parsed == {}

    def test_parse_filters_string_length_limit(self):
        """Test string filters are limited in length"""
        filters = {'color': 'a' * 100}
        parsed = parse_filters(filters)
        
        assert len(parsed['color']) <= 50


class TestCalculateOffset:
    """Tests for offset calculation"""

    def test_calculate_offset_first_page(self):
        """Test offset for first page"""
        offset = calculate_offset(page=1, per_page=20)
        assert offset == 0

    def test_calculate_offset_second_page(self):
        """Test offset for second page"""
        offset = calculate_offset(page=2, per_page=20)
        assert offset == 20

    def test_calculate_offset_tenth_page(self):
        """Test offset for tenth page"""
        offset = calculate_offset(page=10, per_page=20)
        assert offset == 180

    def test_calculate_offset_zero_page(self):
        """Test offset for page 0 (should treat as page 1)"""
        offset = calculate_offset(page=0, per_page=20)
        assert offset == 0

    def test_calculate_offset_negative_page(self):
        """Test offset for negative page (should treat as page 1)"""
        offset = calculate_offset(page=-5, per_page=20)
        assert offset == 0


class TestBuildPaginationLinks:
    """Tests for pagination link building"""

    def test_build_links_middle_page(self):
        """Test building links for middle page"""
        links = build_pagination_links('/api/models', page=5, total_pages=10)
        
        assert links['self'] == '/api/models?page=5'
        assert links['first'] == '/api/models?page=1'
        assert links['last'] == '/api/models?page=10'
        assert links['prev'] == '/api/models?page=4'
        assert links['next'] == '/api/models?page=6'

    def test_build_links_first_page(self):
        """Test building links for first page"""
        links = build_pagination_links('/api/models', page=1, total_pages=10)
        
        assert links['prev'] is None
        assert links['next'] == '/api/models?page=2'

    def test_build_links_last_page(self):
        """Test building links for last page"""
        links = build_pagination_links('/api/models', page=10, total_pages=10)
        
        assert links['prev'] == '/api/models?page=9'
        assert links['next'] is None

    def test_build_links_single_page(self):
        """Test building links when only one page"""
        links = build_pagination_links('/api/models', page=1, total_pages=1)
        
        assert links['prev'] is None
        assert links['next'] is None
        assert links['first'] == links['last']


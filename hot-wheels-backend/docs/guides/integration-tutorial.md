# Integration Tutorial: Building a Hot Wheels Collection Manager

This step-by-step tutorial walks you through building a complete integration with the Hot Wheels Collector API. By the end, you'll have a working application that can:

1. Authenticate users
2. Browse the Hot Wheels catalog
3. Manage a personal collection
4. Create marketplace listings
5. Complete transactions

## Prerequisites

- Python 3.8+ or Node.js 16+
- Basic understanding of REST APIs
- Code editor of your choice

## Tutorial Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    INTEGRATION ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌─────────────────┐                      ┌─────────────────┐          │
│   │  Your           │                      │  Hot Wheels     │          │
│   │  Application    │ ◄──── HTTP/REST ───► │  Collector API  │          │
│   └────────┬────────┘                      └────────┬────────┘          │
│            │                                        │                    │
│            │                                        │                    │
│   ┌────────▼────────┐                      ┌────────▼────────┐          │
│   │  • Auth Module  │                      │  • PostgreSQL   │          │
│   │  • Catalog View │                      │  • Redis Cache  │          │
│   │  • Collection   │                      │  • JWT Auth     │          │
│   │  • Marketplace  │                      │                 │          │
│   └─────────────────┘                      └─────────────────┘          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Part 1: Setup and Configuration

### Python Setup

```bash
# Create project directory
mkdir hotwheels-integration
cd hotwheels-integration

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install requests python-dotenv
```

### Configuration File

Create `.env`:

```env
API_BASE_URL=https://api.hotwheels-collector.com/api/v1
# For local development:
# API_BASE_URL=http://localhost:5000/api/v1
```

### Base API Client

Create `hotwheels_client.py`:

```python
"""
Hot Wheels Collector API Client
A complete Python client for the Hot Wheels Collector API
"""

import os
import requests
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()


class HotWheelsAPIError(Exception):
    """Custom exception for API errors"""
    def __init__(self, message: str, status_code: int, error_data: dict = None):
        self.message = message
        self.status_code = status_code
        self.error_data = error_data or {}
        super().__init__(self.message)


class HotWheelsClient:
    """
    Client for the Hot Wheels Collector API
    
    Usage:
        client = HotWheelsClient()
        client.login("email@example.com", "password")
        models = client.search_models(query="Camaro")
    """
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv('API_BASE_URL')
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: dict = None,
        params: dict = None,
        auth_required: bool = False
    ) -> dict:
        """Make an HTTP request to the API"""
        
        url = f"{self.base_url}{endpoint}"
        headers = {}
        
        if auth_required:
            if not self.access_token:
                raise HotWheelsAPIError("Authentication required", 401)
            headers['Authorization'] = f'Bearer {self.access_token}'
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers
            )
            
            response_data = response.json()
            
            if not response_data.get('success', False):
                error_msg = response_data.get('error', {}).get('message', 'Unknown error')
                raise HotWheelsAPIError(error_msg, response.status_code, response_data)
            
            return response_data
            
        except requests.exceptions.RequestException as e:
            raise HotWheelsAPIError(f"Request failed: {str(e)}", 0)
    
    # ==================== Authentication ====================
    
    def register(
        self,
        username: str,
        email: str,
        password: str,
        full_name: str = None,
        country: str = None,
        city: str = None
    ) -> dict:
        """
        Register a new user account
        
        Args:
            username: Unique username (3-50 chars)
            email: Valid email address
            password: Password (min 8 chars)
            full_name: Optional full name
            country: Optional country
            city: Optional city
            
        Returns:
            User data dictionary
        """
        data = {
            'username': username,
            'email': email,
            'password': password
        }
        if full_name:
            data['full_name'] = full_name
        if country:
            data['country'] = country
        if city:
            data['city'] = city
            
        response = self._make_request('POST', '/auth/register', data=data)
        return response['data']['user']
    
    def login(self, email: str, password: str) -> dict:
        """
        Login and store authentication tokens
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Token data dictionary
        """
        data = {'email': email, 'password': password}
        response = self._make_request('POST', '/auth/login', data=data)
        
        self.access_token = response['data']['access_token']
        self.refresh_token = response['data'].get('refresh_token')
        
        return response['data']
    
    def logout(self) -> bool:
        """Logout and clear tokens"""
        self._make_request('POST', '/auth/logout', auth_required=True)
        self.access_token = None
        self.refresh_token = None
        return True
    
    def get_current_user(self) -> dict:
        """Get the current authenticated user's profile"""
        response = self._make_request('GET', '/auth/me', auth_required=True)
        return response['data']['user']
    
    def update_profile(self, **kwargs) -> dict:
        """
        Update user profile
        
        Kwargs:
            full_name, country, city, bio, profile_image_url
        """
        response = self._make_request('PUT', '/auth/me', data=kwargs, auth_required=True)
        return response['data']['user']
    
    # ==================== Catalog ====================
    
    def search_models(
        self,
        query: str = None,
        page: int = 1,
        per_page: int = 20,
        year_min: int = None,
        year_max: int = None,
        rarity: str = None,
        color: str = None,
        series: str = None
    ) -> dict:
        """
        Search car models with filters
        
        Args:
            query: Search term (matches casting name)
            page: Page number (default 1)
            per_page: Items per page (max 100)
            year_min: Minimum release year
            year_max: Maximum release year
            rarity: Rarity level filter
            color: Color filter
            series: Series name filter
            
        Returns:
            Dict with 'models' list and 'pagination' info
        """
        params = {'page': page, 'per_page': per_page}
        if query:
            params['q'] = query
        if year_min:
            params['year_min'] = year_min
        if year_max:
            params['year_max'] = year_max
        if rarity:
            params['rarity'] = rarity
        if color:
            params['color'] = color
        if series:
            params['series'] = series
            
        response = self._make_request('GET', '/catalog/models', params=params)
        return response['data']
    
    def get_model(self, model_id: int) -> dict:
        """Get a specific car model by ID"""
        response = self._make_request('GET', f'/catalog/models/{model_id}')
        return response['data']['model']
    
    def get_rare_models(self, page: int = 1, per_page: int = 20) -> dict:
        """Get rare and special models"""
        params = {'page': page, 'per_page': per_page}
        response = self._make_request('GET', '/catalog/models/rare', params=params)
        return response['data']
    
    def get_popular_models(self, limit: int = 10) -> List[dict]:
        """Get most popular models"""
        params = {'limit': min(limit, 50)}
        response = self._make_request('GET', '/catalog/models/popular', params=params)
        return response['data']['models']
    
    def get_castings(self, page: int = 1, per_page: int = 50) -> dict:
        """Get all castings with pagination"""
        params = {'page': page, 'per_page': per_page}
        response = self._make_request('GET', '/catalog/castings', params=params)
        return response['data']
    
    def search_castings(self, query: str, page: int = 1, per_page: int = 20) -> dict:
        """Search castings by name"""
        params = {'q': query, 'page': page, 'per_page': per_page}
        response = self._make_request('GET', '/catalog/castings/search', params=params)
        return response['data']
    
    def get_series(self, year: int = None, page: int = 1, per_page: int = 50) -> dict:
        """Get all series with optional year filter"""
        params = {'page': page, 'per_page': per_page}
        if year:
            params['year'] = year
        response = self._make_request('GET', '/catalog/series', params=params)
        return response['data']
    
    def get_catalog_stats(self) -> dict:
        """Get catalog statistics"""
        response = self._make_request('GET', '/catalog/stats')
        return response['data']['stats']
    
    # ==================== Collections ====================
    
    def get_collection(
        self,
        page: int = 1,
        per_page: int = 20,
        for_sale: bool = None,
        for_trade: bool = None,
        condition: str = None
    ) -> dict:
        """
        Get user's collection with optional filters
        
        Args:
            page: Page number
            per_page: Items per page
            for_sale: Filter for sale items
            for_trade: Filter for trade items
            condition: Filter by condition
        """
        params = {'page': page, 'per_page': per_page}
        if for_sale is not None:
            params['for_sale'] = str(for_sale).lower()
        if for_trade is not None:
            params['for_trade'] = str(for_trade).lower()
        if condition:
            params['condition'] = condition
            
        response = self._make_request('GET', '/collections', params=params, auth_required=True)
        return response['data']
    
    def add_to_collection(
        self,
        model_id: int,
        condition: str = 'Mint',
        is_in_package: bool = True,
        acquisition_price: float = None,
        acquisition_date: str = None,
        quantity: int = 1,
        storage_location: str = None,
        notes: str = None,
        is_for_trade: bool = False,
        is_for_sale: bool = False
    ) -> dict:
        """
        Add a car model to user's collection
        
        Args:
            model_id: ID of the car model
            condition: Condition level (Mint, Near Mint, etc.)
            is_in_package: Whether item is in original packaging
            acquisition_price: Price paid for the item
            acquisition_date: Date acquired (YYYY-MM-DD)
            quantity: Number of items
            storage_location: Where item is stored
            notes: Additional notes
            is_for_trade: Mark as available for trade
            is_for_sale: Mark as for sale
        """
        data = {
            'model_id': model_id,
            'condition': condition,
            'is_in_package': is_in_package,
            'quantity': quantity,
            'is_for_trade': is_for_trade,
            'is_for_sale': is_for_sale
        }
        if acquisition_price:
            data['acquisition_price'] = acquisition_price
        if acquisition_date:
            data['acquisition_date'] = acquisition_date
        if storage_location:
            data['storage_location'] = storage_location
        if notes:
            data['notes'] = notes
            
        response = self._make_request('POST', '/collections', data=data, auth_required=True)
        return response['data']['collection_item']
    
    def update_collection_item(self, collection_id: int, **kwargs) -> dict:
        """Update a collection item"""
        response = self._make_request(
            'PUT', f'/collections/{collection_id}',
            data=kwargs, auth_required=True
        )
        return response['data']['collection_item']
    
    def remove_from_collection(self, collection_id: int) -> bool:
        """Remove an item from collection"""
        self._make_request('DELETE', f'/collections/{collection_id}', auth_required=True)
        return True
    
    def get_collection_stats(self) -> dict:
        """Get collection statistics"""
        response = self._make_request('GET', '/collections/stats', auth_required=True)
        return response['data']['stats']
    
    # ==================== Wishlist ====================
    
    def get_wishlist(self, page: int = 1, per_page: int = 20) -> dict:
        """Get user's wishlist"""
        params = {'page': page, 'per_page': per_page}
        response = self._make_request('GET', '/collections/wishlist', params=params, auth_required=True)
        return response['data']
    
    def add_to_wishlist(
        self,
        model_id: int,
        priority: int = 3,
        max_price_willing: float = None,
        notes: str = None
    ) -> dict:
        """Add a model to wishlist"""
        data = {'model_id': model_id, 'priority': priority}
        if max_price_willing:
            data['max_price_willing'] = max_price_willing
        if notes:
            data['notes'] = notes
            
        response = self._make_request('POST', '/collections/wishlist', data=data, auth_required=True)
        return response['data']['wishlist_item']
    
    def remove_from_wishlist(self, wishlist_id: int) -> bool:
        """Remove item from wishlist"""
        self._make_request('DELETE', f'/collections/wishlist/{wishlist_id}', auth_required=True)
        return True
    
    # ==================== Marketplace ====================
    
    def get_listings(
        self,
        page: int = 1,
        per_page: int = 20,
        model_id: int = None,
        listing_type: str = None,
        seller_id: int = None,
        price_min: float = None,
        price_max: float = None
    ) -> dict:
        """Get marketplace listings with filters"""
        params = {'page': page, 'per_page': per_page}
        if model_id:
            params['model_id'] = model_id
        if listing_type:
            params['listing_type'] = listing_type
        if seller_id:
            params['seller_id'] = seller_id
        if price_min:
            params['price_min'] = price_min
        if price_max:
            params['price_max'] = price_max
            
        response = self._make_request('GET', '/marketplace/listings', params=params)
        return response['data']
    
    def create_listing(
        self,
        model_id: int,
        listing_type: str,
        condition: str,
        price: float = None,
        description: str = None,
        collection_item_id: int = None
    ) -> dict:
        """
        Create a new marketplace listing
        
        Args:
            model_id: ID of the car model
            listing_type: 'sale', 'trade', or 'auction'
            condition: Condition level
            price: Price (required for sales)
            description: Listing description
            collection_item_id: Link to collection item
        """
        data = {
            'model_id': model_id,
            'listing_type': listing_type,
            'condition': condition
        }
        if price:
            data['price'] = price
        if description:
            data['description'] = description
        if collection_item_id:
            data['collection_item_id'] = collection_item_id
            
        response = self._make_request('POST', '/marketplace/listings', data=data, auth_required=True)
        return response['data']['listing']
    
    def get_listing(self, listing_id: int) -> dict:
        """Get a specific listing"""
        response = self._make_request('GET', f'/marketplace/listings/{listing_id}')
        return response['data']['listing']
    
    def cancel_listing(self, listing_id: int) -> bool:
        """Cancel a listing"""
        self._make_request('POST', f'/marketplace/listings/{listing_id}/cancel', auth_required=True)
        return True
    
    def create_transaction(self, listing_id: int, payment_method: str = None) -> dict:
        """Create a transaction (purchase)"""
        data = {'listing_id': listing_id}
        if payment_method:
            data['payment_method'] = payment_method
            
        response = self._make_request('POST', '/marketplace/transactions', data=data, auth_required=True)
        return response['data']['transaction']
    
    def get_purchases(self, page: int = 1, per_page: int = 20) -> dict:
        """Get user's purchase history"""
        params = {'page': page, 'per_page': per_page}
        response = self._make_request('GET', '/marketplace/transactions/purchases', params=params, auth_required=True)
        return response['data']
    
    def get_sales(self, page: int = 1, per_page: int = 20) -> dict:
        """Get user's sales history"""
        params = {'page': page, 'per_page': per_page}
        response = self._make_request('GET', '/marketplace/transactions/sales', params=params, auth_required=True)
        return response['data']
    
    def create_review(
        self,
        transaction_id: int,
        reviewee_id: int,
        rating: int,
        comment: str = None
    ) -> dict:
        """Create a review for a transaction"""
        data = {
            'transaction_id': transaction_id,
            'reviewee_id': reviewee_id,
            'rating': rating
        }
        if comment:
            data['comment'] = comment
            
        response = self._make_request('POST', '/marketplace/reviews', data=data, auth_required=True)
        return response['data']['review']
```

## Part 2: Example Usage

Create `example_usage.py`:

```python
"""
Example usage of the Hot Wheels API Client
"""

from hotwheels_client import HotWheelsClient, HotWheelsAPIError


def main():
    # Initialize client
    client = HotWheelsClient()
    
    try:
        # ==================== Authentication ====================
        print("=" * 50)
        print("AUTHENTICATION")
        print("=" * 50)
        
        # Register (uncomment if new user)
        # user = client.register(
        #     username="my_collector",
        #     email="collector@example.com",
        #     password="SecureP@ss123",
        #     full_name="John Collector"
        # )
        # print(f"Registered: {user['username']}")
        
        # Login
        tokens = client.login("collector@example.com", "SecureP@ss123")
        print(f"✓ Logged in successfully")
        print(f"  Token expires in: {tokens['expires_in']} seconds")
        
        # Get profile
        user = client.get_current_user()
        print(f"  User: {user['username']} ({user['role']})")
        
        # ==================== Catalog Browsing ====================
        print("\n" + "=" * 50)
        print("CATALOG")
        print("=" * 50)
        
        # Get catalog stats
        stats = client.get_catalog_stats()
        print(f"✓ Catalog stats:")
        print(f"  Total models: {stats.get('total_models', 'N/A')}")
        print(f"  Total castings: {stats.get('total_castings', 'N/A')}")
        
        # Search for Camaros
        results = client.search_models(query="Camaro", per_page=5)
        print(f"\n✓ Search results for 'Camaro':")
        for model in results.get('models', []):
            print(f"  - {model.get('casting_name', 'Unknown')} ({model['color']}) - {model['release_year']}")
        
        # Get rare models
        rare = client.get_rare_models(per_page=3)
        print(f"\n✓ Rare models:")
        for model in rare.get('models', [])[:3]:
            print(f"  - {model.get('casting_name', 'Unknown')} - {model.get('rarity_level', 'Unknown')}")
        
        # ==================== Collection Management ====================
        print("\n" + "=" * 50)
        print("COLLECTION")
        print("=" * 50)
        
        # Get collection stats
        coll_stats = client.get_collection_stats()
        print(f"✓ Collection stats:")
        print(f"  Total items: {coll_stats.get('total_items', 0)}")
        print(f"  Total value: ${coll_stats.get('total_value', 0):.2f}")
        
        # Get collection
        collection = client.get_collection(per_page=5)
        print(f"\n✓ My collection ({collection.get('pagination', {}).get('total', 0)} items):")
        for item in collection.get('items', [])[:5]:
            car = item.get('car_model', {})
            print(f"  - {car.get('casting_name', 'Unknown')} - {item['condition']}")
        
        # Add to collection (if model exists)
        if results.get('models'):
            first_model = results['models'][0]
            try:
                new_item = client.add_to_collection(
                    model_id=first_model['model_id'],
                    condition='Mint',
                    is_in_package=True,
                    acquisition_price=1.29,
                    notes="Found at Target"
                )
                print(f"\n✓ Added to collection: {new_item['collection_id']}")
            except HotWheelsAPIError as e:
                if "already" in str(e.message).lower():
                    print(f"\n✓ Model already in collection")
                else:
                    raise
        
        # ==================== Marketplace ====================
        print("\n" + "=" * 50)
        print("MARKETPLACE")
        print("=" * 50)
        
        # Get active listings
        listings = client.get_listings(per_page=5)
        print(f"✓ Active listings ({listings.get('pagination', {}).get('total', 0)} total):")
        for listing in listings.get('listings', [])[:5]:
            car = listing.get('car_model', {})
            price = listing.get('price')
            price_str = f"${price:.2f}" if price else "Trade"
            print(f"  - {car.get('casting_name', 'Unknown')} - {listing['condition']} - {price_str}")
        
        # ==================== Logout ====================
        print("\n" + "=" * 50)
        client.logout()
        print("✓ Logged out successfully")
        
    except HotWheelsAPIError as e:
        print(f"\n✗ API Error: {e.message} (Status: {e.status_code})")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


if __name__ == "__main__":
    main()
```

## Part 3: Advanced Patterns

### Automatic Token Refresh

```python
import time
import jwt

class HotWheelsClientWithAutoRefresh(HotWheelsClient):
    """Client with automatic token refresh"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token_expiry = None
    
    def login(self, email: str, password: str) -> dict:
        result = super().login(email, password)
        
        # Decode token to get expiry
        try:
            payload = jwt.decode(
                self.access_token,
                options={"verify_signature": False}
            )
            self.token_expiry = payload.get('exp')
        except:
            # Default to 24 hours if can't decode
            self.token_expiry = time.time() + 86400
        
        return result
    
    def _ensure_valid_token(self):
        """Refresh token if expired or about to expire"""
        if not self.access_token:
            raise HotWheelsAPIError("Not authenticated", 401)
        
        # Refresh if expiring in next 5 minutes
        if self.token_expiry and time.time() > (self.token_expiry - 300):
            self._refresh_token()
    
    def _refresh_token(self):
        """Refresh the access token"""
        if not self.refresh_token:
            raise HotWheelsAPIError("No refresh token available", 401)
        
        headers = {'Authorization': f'Bearer {self.refresh_token}'}
        response = self.session.post(
            f"{self.base_url}/auth/refresh",
            headers=headers
        )
        data = response.json()
        
        if data.get('success'):
            self.access_token = data['data']['access_token']
            # Update expiry
            try:
                payload = jwt.decode(
                    self.access_token,
                    options={"verify_signature": False}
                )
                self.token_expiry = payload.get('exp')
            except:
                self.token_expiry = time.time() + 86400
    
    def _make_request(self, *args, auth_required=False, **kwargs):
        if auth_required:
            self._ensure_valid_token()
        return super()._make_request(*args, auth_required=auth_required, **kwargs)
```

### Batch Operations

```python
class CollectionBatchManager:
    """Manage batch collection operations"""
    
    def __init__(self, client: HotWheelsClient):
        self.client = client
    
    def add_multiple(self, items: list) -> dict:
        """
        Add multiple items to collection
        
        Args:
            items: List of dicts with model_id and optional fields
            
        Returns:
            Dict with 'success' and 'failed' lists
        """
        results = {'success': [], 'failed': []}
        
        for item in items:
            try:
                result = self.client.add_to_collection(**item)
                results['success'].append({
                    'model_id': item['model_id'],
                    'collection_id': result['collection_id']
                })
            except HotWheelsAPIError as e:
                results['failed'].append({
                    'model_id': item['model_id'],
                    'error': e.message
                })
        
        return results

# Usage
batch_manager = CollectionBatchManager(client)
items_to_add = [
    {'model_id': 1, 'condition': 'Mint'},
    {'model_id': 2, 'condition': 'Near Mint'},
    {'model_id': 3, 'condition': 'Good'}
]
results = batch_manager.add_multiple(items_to_add)
print(f"Added: {len(results['success'])}, Failed: {len(results['failed'])}")
```

## Part 4: Error Handling Best Practices

```python
def robust_api_call(client, operation, *args, max_retries=3, **kwargs):
    """
    Make an API call with automatic retry on transient errors
    """
    last_error = None
    
    for attempt in range(max_retries):
        try:
            return operation(*args, **kwargs)
            
        except HotWheelsAPIError as e:
            last_error = e
            
            # Don't retry client errors
            if 400 <= e.status_code < 500:
                raise
            
            # Retry server errors
            if e.status_code >= 500:
                print(f"Server error, retrying ({attempt + 1}/{max_retries})...")
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            
            raise
    
    raise last_error


# Usage
try:
    models = robust_api_call(
        client,
        client.search_models,
        query="Mustang",
        max_retries=3
    )
except HotWheelsAPIError as e:
    if e.status_code == 401:
        print("Please login again")
    elif e.status_code == 404:
        print("Resource not found")
    elif e.status_code == 429:
        print("Rate limited - please wait")
    else:
        print(f"Error: {e.message}")
```

## Summary

You've now learned how to:

1. ✅ Set up a Python API client
2. ✅ Authenticate and manage tokens
3. ✅ Browse the Hot Wheels catalog
4. ✅ Manage personal collections
5. ✅ Interact with the marketplace
6. ✅ Handle errors gracefully
7. ✅ Implement advanced patterns

## Next Steps

- [API Reference](../reference/api-overview.md) - Complete endpoint documentation
- [Best Practices](../advanced/best-practices.md) - Production-ready patterns
- [Error Handling](../reference/error-codes.md) - Comprehensive error guide

---

*Need help? Contact support@hotwheels-collector.com*


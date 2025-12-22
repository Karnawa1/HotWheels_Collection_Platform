# API Best Practices

This guide covers best practices for integrating with the Hot Wheels Collector API in production environments.

## Authentication Best Practices

### Token Management

```python
class TokenManager:
    """Secure token management"""
    
    def __init__(self):
        self._access_token = None
        self._refresh_token = None
        self._expiry = None
    
    def store_tokens(self, access_token: str, refresh_token: str, expires_in: int):
        """Store tokens securely"""
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._expiry = time.time() + expires_in
    
    def is_token_valid(self) -> bool:
        """Check if access token is valid (with 5-min buffer)"""
        if not self._access_token:
            return False
        return time.time() < (self._expiry - 300)  # 5-minute buffer
    
    def get_access_token(self) -> str:
        """Get access token, refreshing if needed"""
        if not self.is_token_valid():
            self._refresh()
        return self._access_token
    
    def _refresh(self):
        """Refresh the access token"""
        # Implementation
        pass
    
    def clear(self):
        """Clear all tokens on logout"""
        self._access_token = None
        self._refresh_token = None
        self._expiry = None
```

### Security Recommendations

| Practice | Description |
|----------|-------------|
| Use HTTPS | Always use TLS encryption |
| Secure storage | Never store tokens in localStorage |
| Token refresh | Refresh before expiration |
| Logout properly | Call logout endpoint |
| Rotate secrets | Periodically change credentials |

## Request Optimization

### Pagination

Always use pagination for list endpoints:

```python
def fetch_all_items(client, endpoint, page_size=50):
    """Fetch all items with pagination"""
    all_items = []
    page = 1
    
    while True:
        response = client.get(endpoint, params={
            'page': page,
            'per_page': page_size
        })
        
        items = response['data']['items']
        all_items.extend(items)
        
        pagination = response['data']['pagination']
        if not pagination['has_next']:
            break
        
        page += 1
    
    return all_items
```

### Caching

Implement client-side caching for read-heavy data:

```python
import time
from functools import lru_cache

class CachedAPIClient:
    def __init__(self, client):
        self.client = client
        self._cache = {}
        self._cache_ttl = {}
    
    def get_model(self, model_id: int, ttl: int = 300):
        """Get model with caching"""
        cache_key = f"model:{model_id}"
        
        if cache_key in self._cache:
            if time.time() < self._cache_ttl[cache_key]:
                return self._cache[cache_key]
        
        # Fetch fresh data
        model = self.client.get_model(model_id)
        
        # Cache it
        self._cache[cache_key] = model
        self._cache_ttl[cache_key] = time.time() + ttl
        
        return model
    
    def invalidate(self, cache_key: str = None):
        """Invalidate cache"""
        if cache_key:
            self._cache.pop(cache_key, None)
            self._cache_ttl.pop(cache_key, None)
        else:
            self._cache.clear()
            self._cache_ttl.clear()
```

### Batch Operations

Group related operations when possible:

```python
async def add_multiple_to_collection(items: list):
    """Add multiple items efficiently"""
    results = {'success': [], 'failed': []}
    
    # Use asyncio for parallel requests
    async with aiohttp.ClientSession() as session:
        tasks = [
            add_item_async(session, item)
            for item in items
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
    
    for item, response in zip(items, responses):
        if isinstance(response, Exception):
            results['failed'].append({
                'model_id': item['model_id'],
                'error': str(response)
            })
        else:
            results['success'].append(response)
    
    return results
```

## Error Handling

### Comprehensive Error Handler

```python
class APIErrorHandler:
    """Centralized error handling"""
    
    @staticmethod
    def handle(error: APIError, context: dict = None):
        """Handle API errors with appropriate actions"""
        
        handlers = {
            'UNAUTHORIZED': APIErrorHandler._handle_auth,
            'TOKEN_EXPIRED': APIErrorHandler._handle_token_expired,
            'RATE_LIMIT_EXCEEDED': APIErrorHandler._handle_rate_limit,
            'VALIDATION_ERROR': APIErrorHandler._handle_validation,
            'NOT_FOUND': APIErrorHandler._handle_not_found,
        }
        
        handler = handlers.get(error.code, APIErrorHandler._handle_generic)
        return handler(error, context)
    
    @staticmethod
    def _handle_auth(error, context):
        # Log user out, redirect to login
        return {'action': 'logout', 'redirect': '/login'}
    
    @staticmethod
    def _handle_token_expired(error, context):
        # Try to refresh token
        return {'action': 'refresh_token'}
    
    @staticmethod
    def _handle_rate_limit(error, context):
        # Extract wait time, schedule retry
        wait_time = context.get('retry_after', 60)
        return {'action': 'wait', 'seconds': wait_time}
    
    @staticmethod
    def _handle_validation(error, context):
        # Return field errors for form display
        return {'action': 'show_errors', 'fields': error.details}
    
    @staticmethod
    def _handle_not_found(error, context):
        return {'action': 'redirect', 'to': '/not-found'}
    
    @staticmethod
    def _handle_generic(error, context):
        # Log and show generic message
        logger.error(f"API Error: {error.code} - {error.message}")
        return {'action': 'show_error', 'message': error.message}
```

### Retry Logic

```python
import time
import random
from typing import Callable, TypeVar

T = TypeVar('T')

def retry_with_backoff(
    func: Callable[[], T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True
) -> T:
    """
    Execute function with exponential backoff retry
    
    Args:
        func: Function to execute
        max_retries: Maximum number of retries
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        jitter: Add randomness to delay
    """
    last_error = None
    
    for attempt in range(max_retries + 1):
        try:
            return func()
        
        except APIError as e:
            last_error = e
            
            # Don't retry client errors (except rate limits)
            if 400 <= e.status < 500 and e.code != 'RATE_LIMIT_EXCEEDED':
                raise
            
            if attempt == max_retries:
                raise
            
            # Calculate delay
            delay = min(base_delay * (2 ** attempt), max_delay)
            
            if jitter:
                delay = delay * (0.5 + random.random())
            
            logger.info(f"Retry {attempt + 1}/{max_retries} in {delay:.2f}s")
            time.sleep(delay)
    
    raise last_error
```

## Rate Limiting

### Client-Side Throttling

```python
import time
from collections import deque
from threading import Lock

class RateLimiter:
    """Client-side rate limiter"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = deque()
        self.lock = Lock()
    
    def acquire(self, timeout: float = None) -> bool:
        """
        Acquire permission to make a request
        
        Returns:
            True if request allowed, False if timed out
        """
        start_time = time.time()
        
        while True:
            with self.lock:
                now = time.time()
                
                # Remove old requests
                while self.requests and self.requests[0] < now - self.window_seconds:
                    self.requests.popleft()
                
                # Check if we can make a request
                if len(self.requests) < self.max_requests:
                    self.requests.append(now)
                    return True
            
            # Check timeout
            if timeout is not None and time.time() - start_time >= timeout:
                return False
            
            # Wait before retrying
            time.sleep(0.1)
    
    def wait_time(self) -> float:
        """Get time until next request slot"""
        with self.lock:
            if len(self.requests) < self.max_requests:
                return 0
            
            oldest = self.requests[0]
            return max(0, oldest + self.window_seconds - time.time())

# Usage
rate_limiter = RateLimiter(max_requests=100, window_seconds=60)

def make_request():
    if rate_limiter.acquire(timeout=30):
        return client.get('/catalog/models')
    else:
        raise Exception("Rate limit timeout")
```

## Data Validation

### Input Validation

```python
from dataclasses import dataclass
from typing import Optional
import re

@dataclass
class CollectionItemInput:
    """Validated collection item input"""
    model_id: int
    condition: str = 'Mint'
    is_in_package: bool = True
    acquisition_price: Optional[float] = None
    quantity: int = 1
    
    VALID_CONDITIONS = ['Mint', 'Near Mint', 'Excellent', 'Good', 'Fair', 'Poor']
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        errors = []
        
        if self.model_id <= 0:
            errors.append("model_id must be positive")
        
        if self.condition not in self.VALID_CONDITIONS:
            errors.append(f"condition must be one of: {self.VALID_CONDITIONS}")
        
        if self.acquisition_price is not None and self.acquisition_price < 0:
            errors.append("acquisition_price cannot be negative")
        
        if self.quantity < 1:
            errors.append("quantity must be at least 1")
        
        if errors:
            raise ValueError("; ".join(errors))
    
    def to_dict(self):
        data = {
            'model_id': self.model_id,
            'condition': self.condition,
            'is_in_package': self.is_in_package,
            'quantity': self.quantity
        }
        if self.acquisition_price is not None:
            data['acquisition_price'] = self.acquisition_price
        return data

# Usage
try:
    item = CollectionItemInput(
        model_id=1,
        condition='Mint',
        acquisition_price=4.99
    )
    client.add_to_collection(**item.to_dict())
except ValueError as e:
    print(f"Validation error: {e}")
```

## Logging

### Structured Logging

```python
import logging
import json
from datetime import datetime

class APILogger:
    """Structured API logging"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def request(self, method: str, endpoint: str, **kwargs):
        """Log API request"""
        self._log('INFO', 'api_request', {
            'method': method,
            'endpoint': endpoint,
            **kwargs
        })
    
    def response(self, status: int, duration_ms: float, **kwargs):
        """Log API response"""
        level = 'INFO' if status < 400 else 'WARNING' if status < 500 else 'ERROR'
        self._log(level, 'api_response', {
            'status': status,
            'duration_ms': round(duration_ms, 2),
            **kwargs
        })
    
    def error(self, error_code: str, message: str, **kwargs):
        """Log API error"""
        self._log('ERROR', 'api_error', {
            'error_code': error_code,
            'message': message,
            **kwargs
        })
    
    def _log(self, level: str, event: str, data: dict):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'event': event,
            **data
        }
        getattr(self.logger, level.lower())(json.dumps(log_entry))

# Usage
api_logger = APILogger('hotwheels_api')

start_time = time.time()
api_logger.request('GET', '/catalog/models', params={'q': 'Camaro'})

response = client.search_models(query='Camaro')

api_logger.response(
    status=200,
    duration_ms=(time.time() - start_time) * 1000,
    result_count=len(response['models'])
)
```

## Testing

### Mock API Client

```python
from unittest.mock import Mock

class MockHotWheelsClient:
    """Mock client for testing"""
    
    def __init__(self):
        self.search_models = Mock(return_value={
            'models': [
                {'model_id': 1, 'casting_name': "'67 Camaro", 'color': 'Red'}
            ],
            'pagination': {'total': 1, 'page': 1}
        })
        
        self.add_to_collection = Mock(return_value={
            'collection_id': 1,
            'model_id': 1,
            'condition': 'Mint'
        })
        
        self.create_listing = Mock(return_value={
            'listing_id': 1,
            'status': 'active'
        })

# Usage in tests
def test_add_to_collection():
    client = MockHotWheelsClient()
    
    result = client.add_to_collection(model_id=1, condition='Mint')
    
    assert result['collection_id'] == 1
    client.add_to_collection.assert_called_once_with(
        model_id=1, condition='Mint'
    )
```

## Production Checklist

### Before Deployment

- [ ] **Authentication**: Implement secure token storage
- [ ] **Error Handling**: Comprehensive error handler
- [ ] **Rate Limiting**: Client-side throttling
- [ ] **Retry Logic**: Exponential backoff with jitter
- [ ] **Logging**: Structured request/response logging
- [ ] **Caching**: Appropriate cache strategy
- [ ] **Validation**: Input validation on all requests
- [ ] **Testing**: Unit and integration tests
- [ ] **Monitoring**: Error rate and latency tracking

### Configuration

```python
# config.py
class APIConfig:
    BASE_URL = os.getenv('API_BASE_URL', 'https://api.hotwheels-collector.com/api/v1')
    TIMEOUT = int(os.getenv('API_TIMEOUT', 30))
    MAX_RETRIES = int(os.getenv('API_MAX_RETRIES', 3))
    RATE_LIMIT = int(os.getenv('API_RATE_LIMIT', 100))
    CACHE_TTL = int(os.getenv('API_CACHE_TTL', 300))
```

---

**Next:** [Rate Limiting](rate-limiting.md) | [Versioning](versioning.md)


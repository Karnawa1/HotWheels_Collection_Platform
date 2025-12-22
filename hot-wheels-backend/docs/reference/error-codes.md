# Error Handling Documentation

This document provides comprehensive information about error handling in the Hot Wheels Collector API.

## Error Response Format

All errors follow a consistent JSON format:

```json
{
  "success": false,
  "error": {
    "message": "Human-readable error description",
    "code": "ERROR_CODE"
  }
}
```

## Error Categories

### Authentication Errors (4xx)

| HTTP Code | Error Code | Message | Description | Recovery |
|-----------|------------|---------|-------------|----------|
| 400 | VALIDATION_ERROR | Missing required fields: email, password | Request validation failed | Fix request body |
| 400 | INVALID_EMAIL | Invalid email format | Email format incorrect | Use valid email |
| 400 | INVALID_PASSWORD | Password must be at least 8 characters | Password too short | Use longer password |
| 401 | UNAUTHORIZED | Authentication required | No token provided | Login first |
| 401 | INVALID_TOKEN | Token is invalid or malformed | JWT validation failed | Re-login |
| 401 | TOKEN_EXPIRED | Token has expired | Access token expired | Refresh token |
| 401 | INVALID_CREDENTIALS | Invalid email or password | Login failed | Check credentials |
| 401 | ACCOUNT_DISABLED | Account is deactivated | Account disabled | Contact support |
| 403 | FORBIDDEN | Access forbidden | Insufficient permissions | Check user role |
| 409 | DUPLICATE_EMAIL | Email already registered | Email exists | Use different email |
| 409 | DUPLICATE_USERNAME | Username already taken | Username exists | Use different username |

### Resource Errors (4xx)

| HTTP Code | Error Code | Message | Description | Recovery |
|-----------|------------|---------|-------------|----------|
| 404 | NOT_FOUND | Resource not found | Requested resource missing | Check resource ID |
| 404 | USER_NOT_FOUND | User not found | User doesn't exist | Verify user ID |
| 404 | MODEL_NOT_FOUND | Car model not found | Model doesn't exist | Check model ID |
| 404 | LISTING_NOT_FOUND | Listing not found | Listing doesn't exist | Check listing ID |
| 404 | COLLECTION_NOT_FOUND | Collection item not found | Item doesn't exist | Check collection ID |
| 404 | TRANSACTION_NOT_FOUND | Transaction not found | Transaction missing | Check transaction ID |

### Business Logic Errors (4xx)

| HTTP Code | Error Code | Message | Description | Recovery |
|-----------|------------|---------|-------------|----------|
| 400 | INVALID_YEAR | Year must be 1968 or later | Invalid year value | Use year >= 1968 |
| 400 | INVALID_PRICE | Price must be greater than 0 | Invalid price | Use positive price |
| 400 | INVALID_RATING | Rating must be between 1 and 5 | Rating out of range | Use 1-5 |
| 400 | INVALID_CONDITION | Invalid condition level | Wrong condition value | Use valid condition |
| 400 | INVALID_RARITY | Invalid rarity level | Wrong rarity value | Use valid rarity |
| 400 | INVALID_LISTING_TYPE | Invalid listing type | Wrong type value | Use sale/trade/auction |
| 409 | SELF_TRANSACTION | Cannot purchase from yourself | Self-purchase attempt | Buy from another user |
| 409 | LISTING_NOT_ACTIVE | Listing is not active | Listing unavailable | Find another listing |
| 409 | ALREADY_EXISTS | Item already exists | Duplicate creation | Use existing item |
| 409 | ALREADY_REVIEWED | Already reviewed this transaction | Duplicate review | N/A |
| 409 | INSUFFICIENT_QUANTITY | Insufficient quantity available | Not enough stock | Reduce quantity |

### Rate Limiting (429)

| HTTP Code | Error Code | Message | Description | Recovery |
|-----------|------------|---------|-------------|----------|
| 429 | RATE_LIMIT_EXCEEDED | Rate limit exceeded. Try again in X seconds | Too many requests | Wait and retry |

### Server Errors (5xx)

| HTTP Code | Error Code | Message | Description | Recovery |
|-----------|------------|---------|-------------|----------|
| 500 | INTERNAL_ERROR | An unexpected error occurred | Server error | Retry later |
| 503 | SERVICE_UNAVAILABLE | Service temporarily unavailable | Server overloaded | Retry later |

## Error Handling Best Practices

### Client-Side Error Handling

```javascript
async function apiCall(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, options);
    const data = await response.json();
    
    if (!data.success) {
      throw new APIError(data.error.message, data.error.code, response.status);
    }
    
    return data;
  } catch (error) {
    if (error instanceof APIError) {
      handleAPIError(error);
    } else {
      handleNetworkError(error);
    }
  }
}

function handleAPIError(error) {
  switch (error.code) {
    case 'UNAUTHORIZED':
    case 'TOKEN_EXPIRED':
      // Redirect to login or refresh token
      refreshToken().catch(() => redirectToLogin());
      break;
    
    case 'VALIDATION_ERROR':
      // Show form validation errors
      showValidationErrors(error.message);
      break;
    
    case 'NOT_FOUND':
      // Show 404 page or message
      showNotFoundMessage();
      break;
    
    case 'RATE_LIMIT_EXCEEDED':
      // Show rate limit message, implement backoff
      showRateLimitMessage();
      scheduleRetry();
      break;
    
    case 'DUPLICATE_EMAIL':
    case 'DUPLICATE_USERNAME':
      // Show specific field error
      highlightDuplicateField(error.code);
      break;
    
    default:
      // Show generic error
      showGenericError(error.message);
  }
}
```

### Python Error Handling

```python
class APIError(Exception):
    def __init__(self, message: str, code: str, status: int):
        self.message = message
        self.code = code
        self.status = status
        super().__init__(message)


def handle_api_error(error: APIError):
    """Handle API errors based on error code"""
    
    if error.code in ['UNAUTHORIZED', 'TOKEN_EXPIRED', 'INVALID_TOKEN']:
        # Re-authenticate
        try:
            refresh_token()
        except:
            redirect_to_login()
    
    elif error.code == 'RATE_LIMIT_EXCEEDED':
        # Implement exponential backoff
        time.sleep(calculate_backoff())
        
    elif error.code in ['NOT_FOUND', 'USER_NOT_FOUND', 'MODEL_NOT_FOUND']:
        # Handle missing resource
        log_warning(f"Resource not found: {error.message}")
        
    elif error.status == 400:
        # Validation error - log and notify
        log_error(f"Validation error: {error.message}")
        
    elif error.status >= 500:
        # Server error - retry with backoff
        schedule_retry()
    
    else:
        # Unknown error
        log_error(f"Unknown error: {error.code} - {error.message}")
```

### Retry Strategy with Exponential Backoff

```python
import time
import random

def make_request_with_retry(func, max_retries=3, base_delay=1):
    """
    Make API request with exponential backoff retry
    
    Args:
        func: Function to execute
        max_retries: Maximum retry attempts
        base_delay: Base delay in seconds
    """
    last_error = None
    
    for attempt in range(max_retries + 1):
        try:
            return func()
            
        except APIError as e:
            last_error = e
            
            # Don't retry client errors (4xx) except rate limits
            if 400 <= e.status < 500 and e.code != 'RATE_LIMIT_EXCEEDED':
                raise
            
            # Calculate delay with jitter
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            
            if attempt < max_retries:
                print(f"Retry {attempt + 1}/{max_retries} in {delay:.2f}s...")
                time.sleep(delay)
    
    raise last_error
```

## Validation Error Details

For validation errors, the API may return additional field-level details:

```json
{
  "success": false,
  "error": {
    "message": "Validation failed",
    "code": "VALIDATION_ERROR",
    "details": {
      "email": "Invalid email format",
      "password": "Password must be at least 8 characters",
      "username": "Username already taken"
    }
  }
}
```

## Rate Limit Headers

When rate limited, the API includes headers:

```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1734433660
Retry-After: 60
```

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Requests allowed per window |
| `X-RateLimit-Remaining` | Requests remaining |
| `X-RateLimit-Reset` | Unix timestamp when limit resets |
| `Retry-After` | Seconds until retry allowed |

## Error Logging

### What to Log

```python
# Good error logging
logger.error(
    "API Error",
    extra={
        "error_code": error.code,
        "status": error.status,
        "endpoint": request.path,
        "user_id": current_user_id,
        "request_id": request_id,
        "timestamp": datetime.utcnow().isoformat()
    }
)

# Log format
# 2024-12-17T10:30:00Z ERROR API Error 
#   error_code=NOT_FOUND status=404 endpoint=/api/v1/models/999 
#   user_id=1 request_id=abc123
```

### What NOT to Log

- Passwords or password hashes
- Full JWT tokens
- Credit card numbers
- Personal identifying information (PII)
- API keys or secrets

## Common Error Scenarios

### Scenario 1: Token Expiration

```
Request: GET /api/v1/collections
Response: 401 Unauthorized

{
  "success": false,
  "error": {
    "message": "Token has expired",
    "code": "TOKEN_EXPIRED"
  }
}

Recovery:
1. POST /api/v1/auth/refresh with refresh token
2. Retry original request with new access token
```

### Scenario 2: Duplicate Registration

```
Request: POST /api/v1/auth/register
Body: { "email": "existing@example.com", ... }
Response: 409 Conflict

{
  "success": false,
  "error": {
    "message": "Email already registered",
    "code": "DUPLICATE_EMAIL"
  }
}

Recovery:
1. Prompt user to use different email
2. Offer password reset if they forgot
```

### Scenario 3: Self-Purchase Prevention

```
Request: POST /api/v1/marketplace/transactions
Body: { "listing_id": 100 } // User's own listing
Response: 409 Conflict

{
  "success": false,
  "error": {
    "message": "Cannot purchase from yourself",
    "code": "SELF_TRANSACTION"
  }
}

Recovery:
1. Hide "Buy" button on own listings
2. Show error message to user
```

### Scenario 4: Resource Not Found

```
Request: GET /api/v1/catalog/models/999999
Response: 404 Not Found

{
  "success": false,
  "error": {
    "message": "Car model not found",
    "code": "MODEL_NOT_FOUND"
  }
}

Recovery:
1. Check if ID is valid
2. Redirect to search or listing page
3. Show "not found" message
```

### Scenario 5: Rate Limit Exceeded

```
Request: GET /api/v1/catalog/models (100+ requests/min)
Response: 429 Too Many Requests

{
  "success": false,
  "error": {
    "message": "Rate limit exceeded. Try again in 45 seconds.",
    "code": "RATE_LIMIT_EXCEEDED"
  }
}

Headers:
X-RateLimit-Remaining: 0
Retry-After: 45

Recovery:
1. Wait for Retry-After duration
2. Implement request throttling
3. Cache responses where possible
```

## Error Code Quick Reference

```
AUTHENTICATION
├── UNAUTHORIZED         - No auth token
├── INVALID_TOKEN        - Malformed token
├── TOKEN_EXPIRED        - Expired token
├── INVALID_CREDENTIALS  - Wrong login
├── ACCOUNT_DISABLED     - Deactivated account
├── FORBIDDEN            - No permission
├── DUPLICATE_EMAIL      - Email exists
└── DUPLICATE_USERNAME   - Username exists

RESOURCES
├── NOT_FOUND            - Generic not found
├── USER_NOT_FOUND       - No such user
├── MODEL_NOT_FOUND      - No such model
├── LISTING_NOT_FOUND    - No such listing
├── COLLECTION_NOT_FOUND - No such collection item
└── TRANSACTION_NOT_FOUND - No such transaction

VALIDATION
├── VALIDATION_ERROR     - General validation
├── INVALID_EMAIL        - Bad email format
├── INVALID_PASSWORD     - Password too weak
├── INVALID_YEAR         - Year < 1968
├── INVALID_PRICE        - Price <= 0
├── INVALID_RATING       - Rating not 1-5
├── INVALID_CONDITION    - Bad condition value
└── INVALID_RARITY       - Bad rarity value

BUSINESS LOGIC
├── SELF_TRANSACTION     - Can't buy own listing
├── LISTING_NOT_ACTIVE   - Listing unavailable
├── ALREADY_EXISTS       - Duplicate item
├── ALREADY_REVIEWED     - Review exists
└── INSUFFICIENT_QUANTITY - Not enough stock

SYSTEM
├── RATE_LIMIT_EXCEEDED  - Too many requests
├── INTERNAL_ERROR       - Server error
└── SERVICE_UNAVAILABLE  - System down
```

---

**Next:** [API Overview](api-overview.md) | [Best Practices](../advanced/best-practices.md)


# API Reference Overview

This document provides a comprehensive reference for all Hot Wheels Collector API endpoints.

## Base URL

```
Production:  https://api.hotwheels-collector.com/api/v1
Development: http://localhost:5000/api/v1
```

## API Conventions

### Request Format

- **Content-Type**: `application/json`
- **Character Encoding**: UTF-8
- **Date Format**: ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`)

### Response Format

All responses follow a consistent JSON structure:

**Success Response:**
```json
{
  "success": true,
  "data": {
    // Response data
  },
  "message": "Optional success message"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": {
    "message": "Error description",
    "code": "ERROR_CODE"
  }
}
```

### Pagination

Paginated endpoints return:

```json
{
  "success": true,
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 150,
      "total_pages": 8,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

**Pagination Parameters:**

| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `page` | integer | 1 | - | Page number |
| `per_page` | integer | 20 | 100 | Items per page |

## Authentication

Protected endpoints require a valid JWT token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

See [Authentication Guide](../guides/authentication.md) for details.

## Endpoint Summary

### Authentication (`/api/v1/auth`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/register` | No | Register new user |
| POST | `/login` | No | User login |
| POST | `/logout` | Yes | User logout |
| GET | `/me` | Yes | Get current user |
| PUT | `/me` | Yes | Update profile |
| POST | `/change-password` | Yes | Change password |
| POST | `/refresh` | Refresh | Refresh access token |

### Catalog (`/api/v1/catalog`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/models` | Optional | Search car models |
| GET | `/models/{id}` | Optional | Get model by ID |
| GET | `/models/rare` | Optional | Get rare models |
| GET | `/models/recent` | Optional | Get recent releases |
| GET | `/models/popular` | Optional | Get popular models |
| GET | `/castings` | Optional | Get all castings |
| GET | `/castings/search` | Optional | Search castings |
| GET | `/castings/{id}` | Optional | Get casting by ID |
| GET | `/castings/{id}/models` | Optional | Get casting models |
| GET | `/series` | Optional | Get all series |
| GET | `/series/{id}` | Optional | Get series by ID |
| GET | `/series/{id}/models` | Optional | Get series models |
| GET | `/manufacturers` | Optional | Get manufacturers |
| GET | `/stats` | Optional | Get catalog stats |

### Collections (`/api/v1/collections`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/` | Yes | Get user collection |
| POST | `/` | Yes | Add to collection |
| PUT | `/{id}` | Yes | Update collection item |
| DELETE | `/{id}` | Yes | Remove from collection |
| GET | `/stats` | Yes | Get collection stats |
| GET | `/wishlist` | Yes | Get wishlist |
| POST | `/wishlist` | Yes | Add to wishlist |
| DELETE | `/wishlist/{id}` | Yes | Remove from wishlist |

### Marketplace (`/api/v1/marketplace`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/listings` | Optional | Get active listings |
| POST | `/listings` | Yes | Create listing |
| GET | `/listings/{id}` | Optional | Get listing by ID |
| PUT | `/listings/{id}` | Yes | Update listing |
| POST | `/listings/{id}/cancel` | Yes | Cancel listing |
| POST | `/transactions` | Yes | Create transaction |
| GET | `/transactions/purchases` | Yes | Get user purchases |
| GET | `/transactions/sales` | Yes | Get user sales |
| POST | `/reviews` | Yes | Create review |

---

## Detailed Endpoint Documentation

### Authentication Endpoints

#### POST /auth/register

Register a new user account.

**Request Body:**

```json
{
  "username": "hotwheels_fan",
  "email": "collector@example.com",
  "password": "SecureP@ss123",
  "full_name": "John Smith",
  "country": "United States",
  "city": "Los Angeles",
  "bio": "Collecting Hot Wheels since 1985"
}
```

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `username` | string | Yes | 3-50 chars, alphanumeric |
| `email` | string | Yes | Valid email format |
| `password` | string | Yes | 8-128 chars |
| `full_name` | string | No | Max 150 chars |
| `country` | string | No | Max 50 chars |
| `city` | string | No | Max 100 chars |
| `bio` | string | No | Text |

**Success Response (201):**

```json
{
  "success": true,
  "data": {
    "user": {
      "user_id": 1,
      "username": "hotwheels_fan",
      "full_name": "John Smith",
      "country": "United States",
      "city": "Los Angeles",
      "bio": "Collecting Hot Wheels since 1985",
      "is_verified": false,
      "is_active": true,
      "role": "collector",
      "created_at": "2024-12-17T10:30:00Z"
    }
  },
  "message": "User registered successfully"
}
```

**Error Responses:**

| Status | Code | Description |
|--------|------|-------------|
| 400 | VALIDATION_ERROR | Missing/invalid fields |
| 409 | DUPLICATE_EMAIL | Email already exists |
| 409 | DUPLICATE_USERNAME | Username already taken |

---

#### POST /auth/login

Authenticate user and return JWT tokens.

**Request Body:**

```json
{
  "email": "collector@example.com",
  "password": "SecureP@ss123"
}
```

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 86400,
    "user": {
      "user_id": 1,
      "username": "hotwheels_fan",
      "role": "collector"
    }
  },
  "message": "Login successful"
}
```

**Error Responses:**

| Status | Code | Description |
|--------|------|-------------|
| 400 | VALIDATION_ERROR | Missing email/password |
| 401 | INVALID_CREDENTIALS | Wrong email or password |
| 401 | ACCOUNT_DISABLED | Account is deactivated |

---

### Catalog Endpoints

#### GET /catalog/models

Search and filter car models.

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | - | Search query (casting name) |
| `page` | integer | 1 | Page number |
| `per_page` | integer | 20 | Items per page (max 100) |
| `year_min` | integer | - | Minimum release year |
| `year_max` | integer | - | Maximum release year |
| `rarity` | string | - | Rarity level filter |
| `color` | string | - | Color filter |
| `series` | string | - | Series name filter |

**Example Request:**

```bash
GET /api/v1/catalog/models?q=Camaro&year_min=2020&rarity=Rare&per_page=10
```

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "models": [
      {
        "model_id": 1,
        "casting_id": 42,
        "series_id": 15,
        "release_year": 2024,
        "color": "Spectraflame Red",
        "tampo_design": "Racing stripes #7",
        "wheel_type": "5-Spoke",
        "rarity_level": "Rare",
        "msrp": 1.29,
        "casting_name": "'67 Camaro",
        "series_name": "Mainline 2024",
        "created_at": "2024-01-15T00:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 45,
      "total_pages": 5,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

---

#### GET /catalog/models/{model_id}

Get detailed information about a specific car model.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | integer | Car model ID |

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "model": {
      "model_id": 1,
      "casting_id": 42,
      "series_id": 15,
      "release_year": 2024,
      "color": "Spectraflame Red",
      "tampo_design": "Racing stripes #7",
      "wheel_type": "5-Spoke",
      "base_color": "Chrome",
      "window_color": "Tinted",
      "interior_color": "Black",
      "production_code": "L2593",
      "sku": "HCW35-N9B1",
      "rarity_level": "Rare",
      "estimated_production_quantity": 5000,
      "msrp": 1.29,
      "casting_name": "'67 Camaro",
      "series_name": "Mainline 2024",
      "created_at": "2024-01-15T00:00:00Z",
      "updated_at": "2024-01-15T00:00:00Z"
    }
  }
}
```

**Error Response (404):**

```json
{
  "success": false,
  "error": {
    "message": "Car model not found",
    "code": "NOT_FOUND"
  }
}
```

---

### Collection Endpoints

#### POST /collections

Add a car model to user's collection.

**Headers Required:** `Authorization: Bearer <token>`

**Request Body:**

```json
{
  "model_id": 1,
  "acquisition_date": "2024-06-15",
  "acquisition_price": 4.99,
  "condition": "Mint",
  "is_in_package": true,
  "package_condition": "Mint",
  "quantity": 1,
  "storage_location": "Display Case A",
  "notes": "Found at local Target",
  "is_for_trade": false,
  "is_for_sale": false
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `model_id` | integer | Yes | - | Car model ID |
| `acquisition_date` | date | No | Today | Date acquired |
| `acquisition_price` | float | No | null | Purchase price |
| `condition` | string | No | "Mint" | Item condition |
| `is_in_package` | boolean | No | true | In packaging |
| `package_condition` | string | No | null | Package condition |
| `quantity` | integer | No | 1 | Number of items |
| `storage_location` | string | No | null | Storage location |
| `notes` | string | No | null | Notes |
| `is_for_trade` | boolean | No | false | Available for trade |
| `is_for_sale` | boolean | No | false | For sale |

**Condition Values:**
- `Mint`
- `Near Mint`
- `Excellent`
- `Good`
- `Fair`
- `Poor`

**Success Response (201):**

```json
{
  "success": true,
  "data": {
    "collection_item": {
      "collection_id": 25,
      "user_id": 1,
      "model_id": 1,
      "acquisition_date": "2024-06-15",
      "acquisition_price": 4.99,
      "condition": "Mint",
      "is_in_package": true,
      "package_condition": "Mint",
      "quantity": 1,
      "storage_location": "Display Case A",
      "notes": "Found at local Target",
      "is_for_trade": false,
      "is_for_sale": false,
      "car_model": {
        "model_id": 1,
        "casting_name": "'67 Camaro",
        "color": "Spectraflame Red"
      },
      "created_at": "2024-12-17T10:30:00Z"
    }
  },
  "message": "Added to collection successfully"
}
```

---

### Marketplace Endpoints

#### POST /marketplace/listings

Create a new marketplace listing.

**Headers Required:** `Authorization: Bearer <token>`

**Request Body:**

```json
{
  "model_id": 1,
  "listing_type": "sale",
  "condition": "Mint",
  "price": 15.99,
  "description": "Pristine condition, never opened",
  "collection_item_id": 25,
  "expires_at": "2024-12-31T23:59:59Z"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model_id` | integer | Yes | Car model ID |
| `listing_type` | string | Yes | "sale", "trade", or "auction" |
| `condition` | string | Yes | Item condition |
| `price` | float | For sales | Sale price |
| `description` | string | No | Listing description |
| `collection_item_id` | integer | No | Link to collection |
| `expires_at` | datetime | No | Expiration date |

**Success Response (201):**

```json
{
  "success": true,
  "data": {
    "listing": {
      "listing_id": 100,
      "seller_id": 1,
      "model_id": 1,
      "listing_type": "sale",
      "price": 15.99,
      "condition": "Mint",
      "description": "Pristine condition, never opened",
      "status": "active",
      "views_count": 0,
      "seller": {
        "username": "hotwheels_fan",
        "is_verified": false
      },
      "car_model": {
        "model_id": 1,
        "casting_name": "'67 Camaro",
        "color": "Spectraflame Red"
      },
      "created_at": "2024-12-17T10:30:00Z"
    }
  },
  "message": "Listing created successfully"
}
```

---

#### POST /marketplace/transactions

Create a purchase transaction.

**Headers Required:** `Authorization: Bearer <token>`

**Request Body:**

```json
{
  "listing_id": 100,
  "payment_method": "PayPal"
}
```

**Success Response (201):**

```json
{
  "success": true,
  "data": {
    "transaction": {
      "transaction_id": 50,
      "listing_id": 100,
      "buyer_id": 2,
      "seller_id": 1,
      "transaction_type": "purchase",
      "amount": 15.99,
      "payment_method": "PayPal",
      "payment_status": "pending",
      "shipping_status": "not_shipped",
      "buyer_username": "buyer123",
      "seller_username": "hotwheels_fan",
      "created_at": "2024-12-17T10:35:00Z"
    }
  },
  "message": "Transaction completed successfully"
}
```

**Error Responses:**

| Status | Code | Description |
|--------|------|-------------|
| 404 | NOT_FOUND | Listing not found |
| 409 | SELF_TRANSACTION | Cannot buy from yourself |
| 409 | LISTING_NOT_ACTIVE | Listing not available |

---

## HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT |
| 201 | Created | Successful POST |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Duplicate/invalid state |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

---

**Next:** [Error Codes](error-codes.md) | [Data Models](data-models.md)


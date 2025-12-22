# Getting Started with the Hot Wheels Collector API

This guide will help you make your first API call in under 5 minutes.

## Prerequisites

- Basic knowledge of REST APIs
- A tool to make HTTP requests (cURL, Postman, or your favorite HTTP client)
- An internet connection

## Step 1: Check API Health

First, let's verify the API is running:

```bash
curl -X GET https://api.hotwheels-collector.com/health
```

**Expected Response:**

```json
{
  "status": "healthy",
  "service": "Hot Wheels API",
  "version": "1.0.0"
}
```

## Step 2: Register a New Account

Create your collector account:

```bash
curl -X POST https://api.hotwheels-collector.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "my_collector_name",
    "email": "collector@example.com",
    "password": "SecureP@ss123",
    "full_name": "John Collector"
  }'
```

**Expected Response (201 Created):**

```json
{
  "success": true,
  "data": {
    "user": {
      "user_id": 1,
      "username": "my_collector_name",
      "full_name": "John Collector",
      "role": "collector",
      "is_verified": false,
      "created_at": "2024-12-17T10:30:00Z"
    }
  },
  "message": "User registered successfully"
}
```

## Step 3: Login and Get Your Token

Authenticate to receive your access token:

```bash
curl -X POST https://api.hotwheels-collector.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "collector@example.com",
    "password": "SecureP@ss123"
  }'
```

**Expected Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 86400
  },
  "message": "Login successful"
}
```

> **Important:** Save your `access_token` - you'll need it for authenticated requests.

## Step 4: Browse the Catalog

Now let's explore the Hot Wheels catalog (no authentication required):

```bash
curl -X GET "https://api.hotwheels-collector.com/api/v1/catalog/models?q=Camaro&per_page=5"
```

**Expected Response:**

```json
{
  "success": true,
  "data": {
    "models": [
      {
        "model_id": 1,
        "casting_name": "'67 Camaro",
        "color": "Spectraflame Red",
        "release_year": 2024,
        "rarity_level": "Common",
        "msrp": 1.29
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 5,
      "total": 150,
      "total_pages": 30,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

## Step 5: Add to Your Collection

Add a model to your personal collection (authentication required):

```bash
curl -X POST https://api.hotwheels-collector.com/api/v1/collections \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "model_id": 1,
    "condition": "Mint",
    "is_in_package": true,
    "acquisition_price": 1.29,
    "notes": "Found at local Target"
  }'
```

**Expected Response (201 Created):**

```json
{
  "success": true,
  "data": {
    "collection_item": {
      "collection_id": 1,
      "model_id": 1,
      "condition": "Mint",
      "is_in_package": true,
      "acquisition_price": 1.29,
      "notes": "Found at local Target",
      "car_model": {
        "model_id": 1,
        "casting_name": "'67 Camaro",
        "color": "Spectraflame Red"
      }
    }
  },
  "message": "Added to collection successfully"
}
```

## Step 6: View Your Collection

See all items in your collection:

```bash
curl -X GET https://api.hotwheels-collector.com/api/v1/collections \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## What's Next?

Now that you've made your first API calls, explore these topics:

1. **[Authentication Deep-Dive](authentication.md)** - Learn about token refresh, logout, and security best practices

2. **[Integration Tutorial](integration-tutorial.md)** - Build a complete collector application

3. **[API Reference](../reference/api-overview.md)** - Explore all available endpoints

4. **[Marketplace Guide](../reference/endpoints.md#marketplace)** - Buy, sell, and trade with other collectors

## Quick Reference

### Base URL
```
https://api.hotwheels-collector.com/api/v1
```

### Authentication Header
```
Authorization: Bearer <your_access_token>
```

### Common Endpoints

| Action | Method | Endpoint |
|--------|--------|----------|
| Register | POST | `/auth/register` |
| Login | POST | `/auth/login` |
| Search Models | GET | `/catalog/models?q=search` |
| Get Collection | GET | `/collections` |
| Add to Collection | POST | `/collections` |
| Browse Listings | GET | `/marketplace/listings` |

### Response Format

All responses follow this structure:

```json
{
  "success": true|false,
  "data": { ... },
  "message": "Optional message"
}
```

### Error Response Format

```json
{
  "success": false,
  "error": {
    "message": "Description of what went wrong",
    "code": "ERROR_CODE"
  }
}
```

## Troubleshooting

### "Authentication required" Error

Make sure you're including the Authorization header:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### "Token expired" Error

Your access token has expired. Use the refresh token to get a new one:

```bash
curl -X POST https://api.hotwheels-collector.com/api/v1/auth/refresh \
  -H "Authorization: Bearer YOUR_REFRESH_TOKEN"
```

### "Resource not found" Error

Check that the resource ID exists. Use the catalog endpoints to find valid model IDs.

---

**Need help?** Contact support@hotwheels-collector.com


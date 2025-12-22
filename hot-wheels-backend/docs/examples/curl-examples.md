# cURL Examples

This document provides ready-to-use cURL commands for all API endpoints.

## Setup

Set your base URL and token:

```bash
# Development
export API_BASE="http://localhost:5000/api/v1"

# Production
export API_BASE="https://api.hotwheels-collector.com/api/v1"

# After login, set your token
export TOKEN="your_access_token_here"
```

---

## Authentication

### Register User

```bash
curl -X POST "$API_BASE/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "hotwheels_fan",
    "email": "collector@example.com",
    "password": "SecureP@ss123",
    "full_name": "John Collector",
    "country": "United States",
    "city": "Los Angeles"
  }'
```

### Login

```bash
curl -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "collector@example.com",
    "password": "SecureP@ss123"
  }'
```

**Save the token:**
```bash
export TOKEN=$(curl -s -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "collector@example.com", "password": "SecureP@ss123"}' \
  | jq -r '.data.access_token')
```

### Get Current User

```bash
curl -X GET "$API_BASE/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

### Update Profile

```bash
curl -X PUT "$API_BASE/auth/me" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "full_name": "John Smith Jr.",
    "bio": "Updated bio",
    "city": "San Francisco"
  }'
```

### Change Password

```bash
curl -X POST "$API_BASE/auth/change-password" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "old_password": "SecureP@ss123",
    "new_password": "NewSecureP@ss456"
  }'
```

### Logout

```bash
curl -X POST "$API_BASE/auth/logout" \
  -H "Authorization: Bearer $TOKEN"
```

### Refresh Token

```bash
curl -X POST "$API_BASE/auth/refresh" \
  -H "Authorization: Bearer $REFRESH_TOKEN"
```

---

## Catalog

### Search Models

```bash
# Basic search
curl -X GET "$API_BASE/catalog/models?q=Camaro"

# With filters
curl -X GET "$API_BASE/catalog/models?q=Mustang&year_min=2020&rarity=Rare&per_page=10"

# Pagination
curl -X GET "$API_BASE/catalog/models?page=2&per_page=50"
```

### Get Model by ID

```bash
curl -X GET "$API_BASE/catalog/models/1"
```

### Get Rare Models

```bash
curl -X GET "$API_BASE/catalog/models/rare?per_page=20"
```

### Get Recent Releases

```bash
curl -X GET "$API_BASE/catalog/models/recent?year=2024"
```

### Get Popular Models

```bash
curl -X GET "$API_BASE/catalog/models/popular?limit=10"
```

### Get All Castings

```bash
curl -X GET "$API_BASE/catalog/castings?page=1&per_page=50"
```

### Search Castings

```bash
curl -X GET "$API_BASE/catalog/castings/search?q=Mustang"
```

### Get Casting by ID

```bash
curl -X GET "$API_BASE/catalog/castings/1"
```

### Get Casting Models

```bash
curl -X GET "$API_BASE/catalog/castings/1/models?per_page=20"
```

### Get All Series

```bash
curl -X GET "$API_BASE/catalog/series?year=2024"
```

### Get Series by ID

```bash
curl -X GET "$API_BASE/catalog/series/1"
```

### Get Series Models

```bash
curl -X GET "$API_BASE/catalog/series/1/models"
```

### Get Manufacturers

```bash
curl -X GET "$API_BASE/catalog/manufacturers"
```

### Get Catalog Statistics

```bash
curl -X GET "$API_BASE/catalog/stats"
```

---

## Collections

### Get My Collection

```bash
# All items
curl -X GET "$API_BASE/collections" \
  -H "Authorization: Bearer $TOKEN"

# With filters
curl -X GET "$API_BASE/collections?for_sale=true&condition=Mint" \
  -H "Authorization: Bearer $TOKEN"

# Pagination
curl -X GET "$API_BASE/collections?page=1&per_page=50" \
  -H "Authorization: Bearer $TOKEN"
```

### Add to Collection

```bash
curl -X POST "$API_BASE/collections" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
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
  }'
```

### Update Collection Item

```bash
curl -X PUT "$API_BASE/collections/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "condition": "Near Mint",
    "is_for_trade": true,
    "notes": "Updated notes"
  }'
```

### Remove from Collection

```bash
curl -X DELETE "$API_BASE/collections/1" \
  -H "Authorization: Bearer $TOKEN"
```

### Get Collection Statistics

```bash
curl -X GET "$API_BASE/collections/stats" \
  -H "Authorization: Bearer $TOKEN"
```

### Get Wishlist

```bash
curl -X GET "$API_BASE/collections/wishlist" \
  -H "Authorization: Bearer $TOKEN"
```

### Add to Wishlist

```bash
curl -X POST "$API_BASE/collections/wishlist" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "model_id": 1,
    "priority": 3,
    "max_price_willing": 25.00,
    "notes": "Looking for loose or carded"
  }'
```

### Remove from Wishlist

```bash
curl -X DELETE "$API_BASE/collections/wishlist/1" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Marketplace

### Get Listings

```bash
# All active listings
curl -X GET "$API_BASE/marketplace/listings"

# With filters
curl -X GET "$API_BASE/marketplace/listings?listing_type=sale&price_min=5&price_max=50"

# By seller
curl -X GET "$API_BASE/marketplace/listings?seller_id=1"
```

### Create Listing (Sale)

```bash
curl -X POST "$API_BASE/marketplace/listings" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "model_id": 1,
    "listing_type": "sale",
    "condition": "Mint",
    "price": 15.99,
    "description": "Pristine condition, never opened",
    "collection_item_id": 25
  }'
```

### Create Listing (Trade)

```bash
curl -X POST "$API_BASE/marketplace/listings" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "model_id": 1,
    "listing_type": "trade",
    "condition": "Near Mint",
    "description": "Looking to trade for Chase variants"
  }'
```

### Get Listing by ID

```bash
curl -X GET "$API_BASE/marketplace/listings/1"
```

### Update Listing

```bash
curl -X PUT "$API_BASE/marketplace/listings/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "price": 12.99,
    "description": "Updated description - price reduced!"
  }'
```

### Cancel Listing

```bash
curl -X POST "$API_BASE/marketplace/listings/1/cancel" \
  -H "Authorization: Bearer $TOKEN"
```

### Create Transaction (Purchase)

```bash
curl -X POST "$API_BASE/marketplace/transactions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "listing_id": 1,
    "payment_method": "PayPal"
  }'
```

### Get My Purchases

```bash
curl -X GET "$API_BASE/marketplace/transactions/purchases" \
  -H "Authorization: Bearer $TOKEN"
```

### Get My Sales

```bash
curl -X GET "$API_BASE/marketplace/transactions/sales" \
  -H "Authorization: Bearer $TOKEN"
```

### Create Review

```bash
curl -X POST "$API_BASE/marketplace/reviews" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "transaction_id": 1,
    "reviewee_id": 2,
    "rating": 5,
    "comment": "Excellent seller! Fast shipping, item as described."
  }'
```

---

## Health Check

```bash
curl -X GET "http://localhost:5000/health"
```

---

## Utility Scripts

### Fetch All Pages

```bash
#!/bin/bash
# Fetch all pages of models matching a query

QUERY="Camaro"
PAGE=1
PER_PAGE=100
ALL_MODELS="[]"

while true; do
  RESPONSE=$(curl -s "$API_BASE/catalog/models?q=$QUERY&page=$PAGE&per_page=$PER_PAGE")
  
  MODELS=$(echo "$RESPONSE" | jq '.data.models')
  HAS_NEXT=$(echo "$RESPONSE" | jq '.data.pagination.has_next')
  
  ALL_MODELS=$(echo "$ALL_MODELS $MODELS" | jq -s 'add')
  
  echo "Fetched page $PAGE..."
  
  if [ "$HAS_NEXT" != "true" ]; then
    break
  fi
  
  PAGE=$((PAGE + 1))
done

echo "Total models: $(echo "$ALL_MODELS" | jq 'length')"
echo "$ALL_MODELS" > "all_${QUERY}_models.json"
```

### Test All Endpoints

```bash
#!/bin/bash
# Quick endpoint test script

echo "Testing API endpoints..."

# Health check
echo -n "Health: "
curl -s -o /dev/null -w "%{http_code}" "$API_BASE/../health"
echo ""

# Catalog (no auth)
echo -n "Catalog Models: "
curl -s -o /dev/null -w "%{http_code}" "$API_BASE/catalog/models"
echo ""

echo -n "Catalog Stats: "
curl -s -o /dev/null -w "%{http_code}" "$API_BASE/catalog/stats"
echo ""

# Auth required endpoints
if [ -n "$TOKEN" ]; then
  echo -n "Collections: "
  curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $TOKEN" "$API_BASE/collections"
  echo ""
  
  echo -n "Wishlist: "
  curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $TOKEN" "$API_BASE/collections/wishlist"
  echo ""
else
  echo "Set TOKEN to test authenticated endpoints"
fi
```

---

## Error Handling

### Example Error Responses

**Validation Error (400):**
```bash
curl -X POST "$API_BASE/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "invalid-email"}'
# Returns: {"success": false, "error": {"message": "Missing required fields: username, password"}}
```

**Unauthorized (401):**
```bash
curl -X GET "$API_BASE/collections"
# Returns: {"success": false, "error": {"message": "Authentication required"}}
```

**Not Found (404):**
```bash
curl -X GET "$API_BASE/catalog/models/999999"
# Returns: {"success": false, "error": {"message": "Car model not found"}}
```

---

*Replace `$API_BASE` and `$TOKEN` with actual values when testing.*


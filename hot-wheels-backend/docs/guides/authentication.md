# Authentication Guide

This guide provides a comprehensive overview of the Hot Wheels Collector API authentication system.

## Overview

The API uses **JWT (JSON Web Token)** based authentication. This provides a secure, stateless authentication mechanism suitable for modern web and mobile applications.

## Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AUTHENTICATION FLOW                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌─────────┐         ┌─────────────┐         ┌─────────────┐           │
│   │  User   │         │  API Server │         │  Database   │           │
│   └────┬────┘         └──────┬──────┘         └──────┬──────┘           │
│        │                     │                       │                   │
│        │ 1. POST /auth/login │                       │                   │
│        │ {email, password}   │                       │                   │
│        │────────────────────>│                       │                   │
│        │                     │                       │                   │
│        │                     │ 2. Validate           │                   │
│        │                     │    credentials        │                   │
│        │                     │──────────────────────>│                   │
│        │                     │                       │                   │
│        │                     │ 3. User data          │                   │
│        │                     │<──────────────────────│                   │
│        │                     │                       │                   │
│        │                     │ 4. Generate JWT       │                   │
│        │                     │    tokens             │                   │
│        │                     │                       │                   │
│        │ 5. Return tokens    │                       │                   │
│        │ {access_token,      │                       │                   │
│        │  refresh_token}     │                       │                   │
│        │<────────────────────│                       │                   │
│        │                     │                       │                   │
│        │ 6. GET /collections │                       │                   │
│        │ Authorization:      │                       │                   │
│        │ Bearer <token>      │                       │                   │
│        │────────────────────>│                       │                   │
│        │                     │                       │                   │
│        │                     │ 7. Validate JWT       │                   │
│        │                     │ 8. Extract user_id    │                   │
│        │                     │                       │                   │
│        │                     │ 9. Fetch data         │                   │
│        │                     │──────────────────────>│                   │
│        │                     │                       │                   │
│        │ 10. Response        │<──────────────────────│                   │
│        │<────────────────────│                       │                   │
│        │                     │                       │                   │
│   └────┴────┘         └──────┴──────┘         └──────┴──────┘           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Token Types

### Access Token

- **Purpose**: Authenticate API requests
- **Expiration**: 24 hours (86,400 seconds)
- **Usage**: Include in `Authorization` header

### Refresh Token

- **Purpose**: Obtain new access tokens
- **Expiration**: 30 days (2,592,000 seconds)
- **Usage**: POST to `/auth/refresh` endpoint

## Registration

### Endpoint

```
POST /api/v1/auth/register
```

### Request

```json
{
  "username": "hotwheels_fan",
  "email": "collector@example.com",
  "password": "SecureP@ss123",
  "full_name": "John Collector",
  "country": "United States",
  "city": "Los Angeles",
  "bio": "Collecting since 1985"
}
```

### Requirements

| Field | Requirements |
|-------|--------------|
| `username` | 3-50 characters, unique, alphanumeric with underscores |
| `email` | Valid email format, unique |
| `password` | 8-128 characters |
| `full_name` | Optional, max 150 characters |
| `country` | Optional, max 50 characters |
| `city` | Optional, max 100 characters |
| `bio` | Optional, text |

### Response

```json
{
  "success": true,
  "data": {
    "user": {
      "user_id": 1,
      "username": "hotwheels_fan",
      "full_name": "John Collector",
      "country": "United States",
      "city": "Los Angeles",
      "bio": "Collecting since 1985",
      "is_verified": false,
      "is_active": true,
      "role": "collector",
      "created_at": "2024-12-17T10:30:00Z"
    }
  },
  "message": "User registered successfully"
}
```

### Error Responses

| Status | Reason |
|--------|--------|
| 400 | Missing required fields |
| 400 | Invalid email format |
| 400 | Password too short |
| 409 | Email already registered |
| 409 | Username already taken |

## Login

### Endpoint

```
POST /api/v1/auth/login
```

### Request

```json
{
  "email": "collector@example.com",
  "password": "SecureP@ss123"
}
```

### Response

```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzM0NTIwMDAwfQ.signature",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzM3MTEyMDAwfQ.signature",
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

### Error Responses

| Status | Reason |
|--------|--------|
| 400 | Missing email or password |
| 401 | Invalid credentials |
| 401 | Account is deactivated |

## Using Access Tokens

Include the access token in the `Authorization` header for all authenticated requests:

```http
GET /api/v1/collections HTTP/1.1
Host: api.hotwheels-collector.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

### cURL Example

```bash
curl -X GET https://api.hotwheels-collector.com/api/v1/collections \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### JavaScript Example

```javascript
const response = await fetch('https://api.hotwheels-collector.com/api/v1/collections', {
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
});
```

### Python Example

```python
import requests

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

response = requests.get(
    'https://api.hotwheels-collector.com/api/v1/collections',
    headers=headers
)
```

## Token Refresh

When your access token expires, use the refresh token to obtain a new one:

### Endpoint

```
POST /api/v1/auth/refresh
```

### Request

Include the refresh token in the Authorization header:

```bash
curl -X POST https://api.hotwheels-collector.com/api/v1/auth/refresh \
  -H "Authorization: Bearer YOUR_REFRESH_TOKEN"
```

### Response

```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.NEW_TOKEN..."
  },
  "message": "Token refreshed successfully"
}
```

## Logout

Invalidate your session and tokens:

### Endpoint

```
POST /api/v1/auth/logout
```

### Request

```bash
curl -X POST https://api.hotwheels-collector.com/api/v1/auth/logout \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Response

```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

## Password Management

### Change Password

```
POST /api/v1/auth/change-password
```

```json
{
  "old_password": "CurrentP@ss123",
  "new_password": "NewSecureP@ss456"
}
```

After changing your password, you'll need to login again with the new credentials.

## User Roles and Permissions

### Roles

| Role | Description | Permissions |
|------|-------------|-------------|
| `collector` | Default role | Manage own collection, wishlist, create listings |
| `trader` | Verified trader | All collector permissions + enhanced marketplace features |
| `moderator` | Platform moderator | Moderate listings, manage reports |
| `admin` | Administrator | Full platform access |

### Permission Matrix

| Action | Collector | Trader | Moderator | Admin |
|--------|-----------|--------|-----------|-------|
| View catalog | ✓ | ✓ | ✓ | ✓ |
| Manage own collection | ✓ | ✓ | ✓ | ✓ |
| Create listings | ✓ | ✓ | ✓ | ✓ |
| View own transactions | ✓ | ✓ | ✓ | ✓ |
| Moderate content | ✗ | ✗ | ✓ | ✓ |
| Manage users | ✗ | ✗ | ✗ | ✓ |
| System settings | ✗ | ✗ | ✗ | ✓ |

## Security Best Practices

### Token Storage

**DO:**
- Store tokens securely (secure storage, encrypted)
- Use HTTPS for all API calls
- Implement token refresh logic
- Clear tokens on logout

**DON'T:**
- Store tokens in localStorage (XSS vulnerable)
- Include tokens in URLs
- Share tokens between applications
- Store tokens in plain text

### Recommended Implementation

```javascript
// Good: Secure token handling
class AuthService {
  private accessToken: string | null = null;
  
  setToken(token: string) {
    this.accessToken = token;
    // Store securely (e.g., secure HTTP-only cookie or encrypted storage)
  }
  
  getAuthHeader() {
    if (!this.accessToken) throw new Error('Not authenticated');
    return { Authorization: `Bearer ${this.accessToken}` };
  }
  
  async refreshToken() {
    const response = await fetch('/api/v1/auth/refresh', {
      method: 'POST',
      headers: this.getAuthHeader()
    });
    const data = await response.json();
    this.setToken(data.data.access_token);
  }
  
  logout() {
    this.accessToken = null;
    // Call logout endpoint
  }
}
```

### Automatic Token Refresh

Implement automatic token refresh before expiration:

```javascript
async function makeAuthenticatedRequest(url, options = {}) {
  // Check if token is about to expire (within 5 minutes)
  if (isTokenExpiringSoon(accessToken)) {
    await refreshAccessToken();
  }
  
  const response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${accessToken}`
    }
  });
  
  // Handle 401 - token might have expired
  if (response.status === 401) {
    await refreshAccessToken();
    return makeAuthenticatedRequest(url, options);
  }
  
  return response;
}
```

## JWT Token Structure

### Access Token Payload

```json
{
  "sub": "1",
  "iat": 1734433600,
  "exp": 1734520000,
  "fresh": true,
  "type": "access"
}
```

| Field | Description |
|-------|-------------|
| `sub` | User ID (subject) |
| `iat` | Issued at timestamp |
| `exp` | Expiration timestamp |
| `fresh` | Token freshness flag |
| `type` | Token type (access/refresh) |

### Decoding Tokens

You can decode the payload (not verify) client-side:

```javascript
function decodeToken(token) {
  const payload = token.split('.')[1];
  return JSON.parse(atob(payload));
}

const tokenData = decodeToken(accessToken);
console.log('Expires:', new Date(tokenData.exp * 1000));
```

## Error Handling

### Authentication Errors

| Status | Code | Description | Action |
|--------|------|-------------|--------|
| 401 | UNAUTHORIZED | No token provided | Redirect to login |
| 401 | TOKEN_EXPIRED | Token has expired | Refresh token |
| 401 | INVALID_TOKEN | Token is malformed | Re-login |
| 403 | FORBIDDEN | Insufficient permissions | Show error message |

### Error Response Example

```json
{
  "success": false,
  "error": {
    "message": "Authentication required",
    "code": "UNAUTHORIZED"
  }
}
```

## Rate Limiting

Authentication endpoints have specific rate limits:

| Endpoint | Rate Limit |
|----------|------------|
| `/auth/login` | 10 requests/minute |
| `/auth/register` | 5 requests/minute |
| `/auth/refresh` | 30 requests/minute |
| `/auth/change-password` | 5 requests/minute |

When rate limited, you'll receive:

```json
{
  "success": false,
  "error": {
    "message": "Rate limit exceeded. Try again in 60 seconds.",
    "code": "RATE_LIMIT_EXCEEDED"
  }
}
```

---

**Next:** [Integration Tutorial](integration-tutorial.md) | [API Reference](../reference/api-overview.md)


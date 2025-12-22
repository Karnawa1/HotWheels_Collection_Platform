# Changelog

All notable changes to the Hot Wheels Collector API will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-17

### Added

#### Authentication
- User registration with email verification
- JWT-based authentication (access + refresh tokens)
- User profile management
- Password change functionality
- Role-based access control (collector, trader, admin, moderator)

#### Catalog
- Car model search with full-text search
- Filtering by year, rarity, color, and series
- Casting management and browsing
- Series catalog with year filtering
- Manufacturer directory
- Popular models endpoint
- Rare models endpoint
- Recent releases endpoint
- Catalog statistics

#### Collections
- Personal collection management
- Item condition tracking
- Package condition tracking
- Storage location notes
- Trade/sale marking
- Collection statistics
- Wishlist management with priority levels

#### Marketplace
- Listing creation (sale, trade, auction)
- Listing search and filtering
- Transaction processing
- Purchase/sales history
- Review system (1-5 stars)

#### Infrastructure
- PostgreSQL database with migrations
- Redis caching for sessions
- MongoDB for image metadata
- Docker containerization
- Automatic database migrations
- Comprehensive logging

### Security
- Password hashing with bcrypt
- JWT token expiration (24h access, 30d refresh)
- Rate limiting (100 req/min anonymous, 500 req/min authenticated)
- CORS configuration
- Input validation and sanitization
- SQL injection prevention

### Documentation
- OpenAPI 3.1 specification
- Getting Started guide
- Authentication deep-dive
- Integration tutorial
- API reference documentation
- Error handling guide
- Architecture documentation
- Database schema documentation

---

## Versioning Strategy

### API Versioning

The API uses URL path versioning:
- Current: `/api/v1/`
- Future: `/api/v2/` (when breaking changes are introduced)

### Breaking Changes

Breaking changes will only be introduced in major versions:
- Endpoint removal or renaming
- Required parameter changes
- Response structure changes
- Authentication method changes

### Non-Breaking Changes

These changes may occur in minor versions:
- New endpoints
- New optional parameters
- New response fields
- Bug fixes
- Performance improvements

### Deprecation Policy

1. Deprecated features are marked in documentation
2. Deprecation warnings included in responses
3. Minimum 6 months notice before removal
4. Email notification to registered developers

---

## Upcoming Features

### Version 1.1.0 (Planned)

- [ ] Image upload for listings
- [ ] Advanced search with Elasticsearch
- [ ] Notification system
- [ ] Email verification
- [ ] Password reset via email
- [ ] OAuth2 social login

### Version 1.2.0 (Planned)

- [ ] Real-time notifications (WebSocket)
- [ ] Auction countdown timers
- [ ] Price history tracking
- [ ] Collection value estimates
- [ ] Export collection to CSV/PDF

### Version 2.0.0 (Future)

- [ ] GraphQL API
- [ ] Mobile SDK
- [ ] Webhook integrations
- [ ] API analytics dashboard

---

## Migration Guides

### Migrating from Beta to 1.0.0

No breaking changes from beta. Update your base URL:

```diff
- https://beta-api.hotwheels-collector.com/api/v1
+ https://api.hotwheels-collector.com/api/v1
```

---

## Support

For questions about API changes:
- Email: support@hotwheels-collector.com
- Documentation: https://docs.hotwheels-collector.com
- Status Page: https://status.hotwheels-collector.com


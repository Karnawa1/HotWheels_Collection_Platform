# Hot Wheels Collector API Documentation

Welcome to the official documentation for the **Hot Wheels Collector API** - a comprehensive platform for Hot Wheels collectors to manage their collections, trade with other collectors, and explore the complete Hot Wheels catalog.

## Documentation Structure

```
docs/
├── README.md                    # This file - documentation overview
├── openapi.yaml                 # OpenAPI 3.1 specification
├── guides/
│   ├── getting-started.md       # Quick start guide
│   ├── authentication.md        # Authentication deep-dive
│   └── integration-tutorial.md  # Step-by-step integration tutorial
├── reference/
│   ├── api-overview.md          # API reference overview
│   ├── endpoints.md             # Detailed endpoint documentation
│   ├── data-models.md           # Data model descriptions
│   └── error-codes.md           # Error handling documentation
├── architecture/
│   ├── system-overview.md       # High-level architecture
│   ├── request-flow.md          # Request/response flow
│   └── database-schema.md       # Database design
├── advanced/
│   ├── pagination.md            # Pagination strategies
│   ├── rate-limiting.md         # Rate limiting documentation
│   ├── best-practices.md        # API best practices
│   └── versioning.md            # API versioning strategy
├── examples/
│   ├── curl-examples.md         # cURL examples
│   ├── python-examples.md       # Python SDK examples
│   └── javascript-examples.md   # JavaScript examples
└── changelog.md                 # Version history and changes
```

## Quick Links

| Section | Description |
|---------|-------------|
| [Getting Started](guides/getting-started.md) | Quick setup and first API call |
| [Authentication Guide](guides/authentication.md) | JWT authentication deep-dive |
| [Integration Tutorial](guides/integration-tutorial.md) | Build a complete integration |
| [API Reference](reference/api-overview.md) | Complete endpoint documentation |
| [Error Handling](reference/error-codes.md) | Error codes and recovery |
| [Architecture Overview](architecture/system-overview.md) | System design and diagrams |

## API Version

- **Current Version:** 1.0.0
- **Base URL:** `https://api.hotwheels-collector.com/api/v1`
- **OpenAPI Spec:** [openapi.yaml](openapi.yaml)

## Features

### Core Functionality

- **Authentication**: Secure JWT-based authentication with access and refresh tokens
- **Catalog Management**: Browse 50+ years of Hot Wheels models, castings, and series
- **Collection Tracking**: Track personal collections with detailed condition and storage info
- **Wishlist**: Maintain a wishlist of desired models with priority levels
- **Marketplace**: Buy, sell, and trade with other collectors
- **Reviews**: Rate and review transactions for community trust

### Technical Features

- RESTful API design following industry best practices
- Comprehensive error handling with descriptive messages
- Pagination support for all list endpoints
- Search and filtering capabilities
- Rate limiting for fair usage
- CORS support for web applications

## Getting Help

- **API Support**: support@hotwheels-collector.com
- **Bug Reports**: Create an issue in the repository
- **Documentation Issues**: Submit a PR or create an issue

## Standards Compliance

This API documentation follows:

- **OpenAPI 3.1** specification
- **REST** architectural principles
- **JSON:API** response formatting conventions
- **OAuth 2.0 / JWT** authentication standards
- **Semantic Versioning** (SemVer) for API versions

## Documentation Validation

The OpenAPI specification has been validated using:

- Swagger Editor
- Spectral (API linting)
- Redocly CLI

## License

MIT License - See LICENSE file for details.

---

*Documentation Version: 1.0.0 | Last Updated: December 2024*


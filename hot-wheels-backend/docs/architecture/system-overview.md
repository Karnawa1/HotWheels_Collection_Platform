# System Architecture Overview

This document provides a high-level overview of the Hot Wheels Collector API architecture, including system components, data flow, and deployment topology.

## System Context Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SYSTEM CONTEXT                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   ┌───────────────┐                                      ┌───────────────┐      │
│   │               │                                      │               │      │
│   │  Web Client   │                                      │ Mobile App    │      │
│   │  (Browser)    │                                      │ (iOS/Android) │      │
│   │               │                                      │               │      │
│   └───────┬───────┘                                      └───────┬───────┘      │
│           │                                                      │              │
│           │              HTTPS / REST API                        │              │
│           │                                                      │              │
│           └──────────────────────┬───────────────────────────────┘              │
│                                  │                                               │
│                                  ▼                                               │
│   ┌──────────────────────────────────────────────────────────────────────────┐  │
│   │                                                                           │  │
│   │                    HOT WHEELS COLLECTOR API                               │  │
│   │                                                                           │  │
│   │   ┌─────────────────────────────────────────────────────────────────┐    │  │
│   │   │                       Flask Application                          │    │  │
│   │   │                                                                  │    │  │
│   │   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │    │  │
│   │   │  │   Auth   │  │ Catalog  │  │Collection│  │Marketplace│        │    │  │
│   │   │  │  Module  │  │  Module  │  │  Module  │  │  Module   │        │    │  │
│   │   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │    │  │
│   │   │                                                                  │    │  │
│   │   └─────────────────────────────────────────────────────────────────┘    │  │
│   │                                                                           │  │
│   └──────────────────────────────────────────────────────────────────────────┘  │
│                                  │                                               │
│           ┌──────────────────────┼──────────────────────┐                       │
│           │                      │                      │                       │
│           ▼                      ▼                      ▼                       │
│   ┌───────────────┐      ┌───────────────┐      ┌───────────────┐              │
│   │               │      │               │      │               │              │
│   │  PostgreSQL   │      │    Redis      │      │   MongoDB     │              │
│   │   Database    │      │    Cache      │      │   (Images)    │              │
│   │               │      │               │      │               │              │
│   └───────────────┘      └───────────────┘      └───────────────┘              │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           COMPONENT ARCHITECTURE                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                            API GATEWAY LAYER                                │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │ │
│  │  │    NGINX     │  │  Rate Limit  │  │     CORS     │  │   Logging    │   │ │
│  │  │   Reverse    │  │   Handler    │  │   Handler    │  │  Middleware  │   │ │
│  │  │    Proxy     │  │              │  │              │  │              │   │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                           │
│                                      ▼                                           │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                          APPLICATION LAYER                                  │ │
│  │                                                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────────────┐   │ │
│  │  │                         ROUTES (Blueprints)                          │   │ │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐  ┌──────────────┐    │   │ │
│  │  │  │  /auth   │  │ /catalog │  │ /collections │  │ /marketplace │    │   │ │
│  │  │  └────┬─────┘  └────┬─────┘  └──────┬───────┘  └──────┬───────┘    │   │ │
│  │  └───────┼─────────────┼───────────────┼─────────────────┼────────────┘   │ │
│  │          │             │               │                 │                 │ │
│  │          ▼             ▼               ▼                 ▼                 │ │
│  │  ┌─────────────────────────────────────────────────────────────────────┐   │ │
│  │  │                         SERVICES LAYER                               │   │ │
│  │  │  ┌────────────┐ ┌────────────┐ ┌────────────────┐ ┌──────────────┐  │   │ │
│  │  │  │   Auth     │ │  Catalog   │ │   Collection   │ │  Marketplace │  │   │ │
│  │  │  │  Service   │ │  Service   │ │    Service     │ │   Service    │  │   │ │
│  │  │  └────────────┘ └────────────┘ └────────────────┘ └──────────────┘  │   │ │
│  │  └─────────────────────────────────────────────────────────────────────┘   │ │
│  │                                      │                                      │ │
│  └──────────────────────────────────────┼──────────────────────────────────────┘ │
│                                         │                                        │
│                                         ▼                                        │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                           DATA ACCESS LAYER                                 │ │
│  │                                                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────────────┐   │ │
│  │  │                         MODELS (SQLAlchemy)                          │   │ │
│  │  │  ┌──────┐ ┌───────┐ ┌────────┐ ┌───────┐ ┌───────┐ ┌───────────┐   │   │ │
│  │  │  │ User │ │Casting│ │CarModel│ │Series │ │Listing│ │Transaction│   │   │ │
│  │  │  └──────┘ └───────┘ └────────┘ └───────┘ └───────┘ └───────────┘   │   │ │
│  │  │                                                                      │   │ │
│  │  │  ┌────────────────┐  ┌──────────┐  ┌────────┐  ┌────────────────┐   │   │ │
│  │  │  │ UserCollection │  │ Wishlist │  │ Review │  │  Manufacturer  │   │   │ │
│  │  │  └────────────────┘  └──────────┘  └────────┘  └────────────────┘   │   │ │
│  │  └─────────────────────────────────────────────────────────────────────┘   │ │
│  │                                                                             │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Module Descriptions

### Authentication Module (`/api/v1/auth`)

| Component | Description |
|-----------|-------------|
| **Routes** | `auth.py` - Registration, login, logout, profile management |
| **Service** | `auth_service.py` - User authentication, JWT token management |
| **Middleware** | `auth_middleware.py` - JWT validation decorators |
| **Model** | `user.py` - User entity with password hashing |

**Key Responsibilities:**
- User registration and validation
- Password hashing with bcrypt
- JWT token generation and validation
- Session management
- Role-based access control

### Catalog Module (`/api/v1/catalog`)

| Component | Description |
|-----------|-------------|
| **Routes** | `catalog.py` - Model search, casting/series browsing |
| **Service** | `catalog_service.py` - Search, filtering, statistics |
| **Models** | `car_model.py`, `casting.py`, `series.py`, `manufacturer.py` |

**Key Responsibilities:**
- Car model search and filtering
- Casting management
- Series organization
- Manufacturer data
- Catalog statistics

### Collections Module (`/api/v1/collections`)

| Component | Description |
|-----------|-------------|
| **Routes** | `collections.py` - Collection and wishlist management |
| **Service** | `collection_service.py` - CRUD operations, statistics |
| **Models** | `user.py` (UserCollection, Wishlist entities) |

**Key Responsibilities:**
- Personal collection management
- Wishlist tracking
- Collection statistics
- Trade/sale marking

### Marketplace Module (`/api/v1/marketplace`)

| Component | Description |
|-----------|-------------|
| **Routes** | `marketplace.py` - Listings, transactions, reviews |
| **Service** | `marketplace_service.py` - Marketplace operations |
| **Models** | `listing.py`, `transaction.py` (Transaction, Review) |

**Key Responsibilities:**
- Listing creation and management
- Transaction processing
- Review system
- View tracking

## Data Flow Diagrams

### Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AUTHENTICATION DATA FLOW                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Client                    API                      Database                │
│     │                        │                          │                    │
│     │  POST /auth/login      │                          │                    │
│     │  {email, password}     │                          │                    │
│     │───────────────────────>│                          │                    │
│     │                        │                          │                    │
│     │                        │  SELECT user WHERE email │                    │
│     │                        │─────────────────────────>│                    │
│     │                        │                          │                    │
│     │                        │  User record             │                    │
│     │                        │<─────────────────────────│                    │
│     │                        │                          │                    │
│     │                        │  Verify password hash    │                    │
│     │                        │  Generate JWT tokens     │                    │
│     │                        │                          │                    │
│     │                        │  Store session (Redis)   │                    │
│     │                        │  ────────────────────>   │                    │
│     │                        │                          │                    │
│     │  {access_token,        │                          │                    │
│     │   refresh_token}       │                          │                    │
│     │<───────────────────────│                          │                    │
│     │                        │                          │                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Collection Add Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ADD TO COLLECTION DATA FLOW                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Client                    API                      Database                │
│     │                        │                          │                    │
│     │  POST /collections     │                          │                    │
│     │  Authorization: Bearer │                          │                    │
│     │  {model_id, ...}       │                          │                    │
│     │───────────────────────>│                          │                    │
│     │                        │                          │                    │
│     │                        │  1. Validate JWT token   │                    │
│     │                        │  2. Extract user_id      │                    │
│     │                        │                          │                    │
│     │                        │  SELECT model WHERE id   │                    │
│     │                        │─────────────────────────>│                    │
│     │                        │                          │                    │
│     │                        │  Model exists?           │                    │
│     │                        │<─────────────────────────│                    │
│     │                        │                          │                    │
│     │                        │  INSERT usercollection   │                    │
│     │                        │─────────────────────────>│                    │
│     │                        │                          │                    │
│     │                        │  Collection item         │                    │
│     │                        │<─────────────────────────│                    │
│     │                        │                          │                    │
│     │  {collection_item}     │                          │                    │
│     │<───────────────────────│                          │                    │
│     │                        │                          │                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Transaction Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TRANSACTION DATA FLOW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Buyer                     API                    Seller    Database        │
│     │                        │                       │          │            │
│     │  POST /transactions    │                       │          │            │
│     │  {listing_id}          │                       │          │            │
│     │───────────────────────>│                       │          │            │
│     │                        │                       │          │            │
│     │                        │  1. Validate listing active      │            │
│     │                        │  2. Verify buyer ≠ seller        │            │
│     │                        │─────────────────────────────────>│            │
│     │                        │                                  │            │
│     │                        │  BEGIN TRANSACTION               │            │
│     │                        │                                  │            │
│     │                        │  3. Create transaction record    │            │
│     │                        │─────────────────────────────────>│            │
│     │                        │                                  │            │
│     │                        │  4. Update listing status='sold' │            │
│     │                        │─────────────────────────────────>│            │
│     │                        │                                  │            │
│     │                        │  COMMIT                          │            │
│     │                        │                                  │            │
│     │                        │                       │          │            │
│     │  {transaction}         │  (Notification)       │          │            │
│     │<───────────────────────│──────────────────────>│          │            │
│     │                        │                       │          │            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Web Framework** | Flask 2.3+ | REST API development |
| **ORM** | SQLAlchemy | Database abstraction |
| **Authentication** | Flask-JWT-Extended | JWT token management |
| **Database** | PostgreSQL 15 | Primary data store |
| **Caching** | Redis 7 | Session storage, caching |
| **Document Store** | MongoDB 6 | Image metadata storage |
| **Containerization** | Docker | Application packaging |
| **Orchestration** | Docker Compose | Multi-container deployment |

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DEPLOYMENT ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                           Docker Network                                │ │
│  │                                                                         │ │
│  │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐               │ │
│  │   │             │    │             │    │             │               │ │
│  │   │   NGINX     │    │   Flask     │    │   Flask     │               │ │
│  │   │  (Reverse   │───>│   App       │    │   App       │               │ │
│  │   │   Proxy)    │    │ (Instance 1)│    │ (Instance 2)│               │ │
│  │   │   :80/443   │    │   :5000     │    │   :5001     │               │ │
│  │   │             │    │             │    │             │               │ │
│  │   └─────────────┘    └──────┬──────┘    └──────┬──────┘               │ │
│  │          │                  │                  │                       │ │
│  │          │                  └────────┬─────────┘                       │ │
│  │          │                           │                                 │ │
│  │          │                           ▼                                 │ │
│  │          │            ┌──────────────────────────┐                    │ │
│  │          │            │                          │                    │ │
│  │          │            │       PostgreSQL         │                    │ │
│  │          │            │        :5432             │                    │ │
│  │          │            │                          │                    │ │
│  │          │            └──────────────────────────┘                    │ │
│  │          │                           │                                 │ │
│  │          ▼                           │                                 │ │
│  │   ┌─────────────┐    ┌─────────────┐│    ┌─────────────┐             │ │
│  │   │             │    │             ││    │             │             │ │
│  │   │   Redis     │    │   MongoDB   │▼    │   Volumes   │             │ │
│  │   │   :6379     │    │   :27017    │     │  (Persist)  │             │ │
│  │   │             │    │             │     │             │             │ │
│  │   └─────────────┘    └─────────────┘     └─────────────┘             │ │
│  │                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SECURITY LAYERS                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  Layer 1: NETWORK SECURITY                                              │ │
│  │  • TLS/HTTPS encryption (443)                                           │ │
│  │  • Docker network isolation                                             │ │
│  │  • Firewall rules                                                       │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                       │
│                                      ▼                                       │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  Layer 2: API GATEWAY                                                   │ │
│  │  • Rate limiting (100 req/min anonymous, 500 req/min authenticated)     │ │
│  │  • CORS policy enforcement                                              │ │
│  │  • Request validation                                                   │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                       │
│                                      ▼                                       │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  Layer 3: AUTHENTICATION                                                │ │
│  │  • JWT token validation                                                 │ │
│  │  • Token expiration (24h access, 30d refresh)                          │ │
│  │  • Session management (Redis)                                           │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                       │
│                                      ▼                                       │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  Layer 4: AUTHORIZATION                                                 │ │
│  │  • Role-based access control (RBAC)                                     │ │
│  │  • Resource ownership validation                                        │ │
│  │  • Action permissions                                                   │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                       │
│                                      ▼                                       │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  Layer 5: DATA SECURITY                                                 │ │
│  │  • Password hashing (bcrypt/PBKDF2)                                    │ │
│  │  • SQL injection prevention (parameterized queries)                     │ │
│  │  • Input sanitization                                                   │ │
│  │  • Database encryption at rest                                          │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Performance Considerations

### Caching Strategy

| Cache Level | Technology | TTL | Use Case |
|-------------|------------|-----|----------|
| Session | Redis | 24h | User sessions, JWT blacklist |
| Query | Redis | 5-30min | Catalog queries, stats |
| Static | CDN | 1d | Images, static assets |

### Database Optimization

- **Indexes**: Created on frequently queried columns
- **Connection Pooling**: Pool size 10, max overflow 20
- **Query Optimization**: Eager loading for related entities
- **Pagination**: Default 20 items, max 100

## Scalability

### Horizontal Scaling

```
                    ┌─────────────┐
                    │   Load      │
                    │  Balancer   │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
   ┌───────────┐    ┌───────────┐    ┌───────────┐
   │  Flask    │    │  Flask    │    │  Flask    │
   │  App 1    │    │  App 2    │    │  App N    │
   └───────────┘    └───────────┘    └───────────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
                    ┌──────┴──────┐
                    │             │
               ┌────▼────┐  ┌─────▼────┐
               │PostgreSQL│  │  Redis   │
               │ Primary  │  │ Cluster  │
               └────┬─────┘  └──────────┘
                    │
               ┌────▼────┐
               │PostgreSQL│
               │ Replica  │
               └──────────┘
```

---

**Next:** [Request Flow](request-flow.md) | [Database Schema](database-schema.md)


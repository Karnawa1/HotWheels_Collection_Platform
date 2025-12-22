# Architecture Documentation

## Overview

The Hot Wheels Collector Platform is built using Next.js 16 with the App Router, following Feature-Sliced Design (FSD) principles for maintainability and scalability.

## Core Principles

### 1. Feature-Sliced Design (FSD)

The application is organized into layers:

- **app/**: Next.js pages and routes
- **shared/**: Framework-agnostic utilities, UI components, API layer
- **entities/**: Business entities (User, Auth state)
- **features/**: User-facing features (forms, filters)
- **widgets/**: Composite UI components (header, cards)

### 2. State Management

**Redux Toolkit + RTK Query**
- Global state managed by Redux
- API caching and invalidation via RTK Query
- Automatic loading states and error handling
- Optimistic updates for better UX

### 3. Data Flow

```
User Action → Component → Redux Action → RTK Query → API
                ↓                                      ↓
            UI Update ← Redux Store ← Cache Update ← Response
```

### 4. Authentication Flow

1. User submits credentials
2. API returns access + refresh tokens
3. Access token stored in memory
4. Refresh token used to get new access token on 401
5. Auto-redirect to login on refresh failure

### 5. API Layer

All API calls go through RTK Query:
- Automatic request deduplication
- Cache management with tags
- Optimistic updates
- Error normalization

### 6. Form Handling

React Hook Form + Zod:
- Type-safe validation
- Minimal re-renders
- Great DX with TypeScript

### 7. Error Handling

- Error Boundary catches React errors
- API errors mapped to user-friendly messages
- Toast notifications for feedback
- Proper HTTP status code handling

## File Structure

```
├── app/                      # Next.js App Router
│   ├── (auth)/              # Auth pages
│   ├── catalog/             # Catalog pages
│   ├── marketplace/         # Marketplace pages
│   ├── collection/          # Collection page
│   ├── wishlist/            # Wishlist page
│   ├── transactions/        # Transactions page
│   ├── profile/             # Profile page
│   ├── analytics/           # Analytics page
│   ├── ai-identify/         # AI identify page
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Landing page
│
├── shared/                   # Shared layer
│   ├── api/                 # RTK Query APIs
│   ├── components/          # Reusable components
│   ├── lib/                 # Utilities
│   ├── providers/           # Context providers
│   ├── store/               # Redux store
│   ├── types/               # TypeScript types
│   └── ui/                  # UI components
│
├── entities/                 # Business entities
│   └── auth/                # Auth entity
│
├── features/                 # Features
│   ├── auth/                # Auth forms
│   └── catalog/             # Catalog filters
│
├── widgets/                  # Widgets
│   ├── header.tsx           # App header
│   ├── model-card.tsx       # Model card
│   └── listing-card.tsx     # Listing card
│
├── __tests__/               # Tests
│   ├── components/          # Component tests
│   ├── lib/                 # Utility tests
│   └── store/               # Store tests
│
└── e2e/                     # E2E tests
    ├── auth.spec.ts         # Auth flow tests
    └── collection.spec.ts   # Collection tests
```

## Best Practices

1. **Always read before write**: Use RTK Query hooks to fetch data
2. **Colocate related code**: Keep features self-contained
3. **Type everything**: Use TypeScript strictly
4. **Test coverage**: Aim for >80% coverage
5. **Error handling**: Always handle errors gracefully
6. **Loading states**: Show skeletons for async operations
7. **Accessibility**: Use semantic HTML and ARIA labels
8. **Performance**: Use React.memo and useMemo when appropriate

## Scaling Considerations

- **Code splitting**: Automatic with Next.js App Router
- **API pagination**: Implemented for lists
- **Image optimization**: Use Next.js Image component
- **Lazy loading**: For heavy components
- **Caching strategy**: RTK Query handles cache invalidation
- **Error boundaries**: Prevent full app crashes

## Security

- JWT tokens with refresh mechanism
- HTTPS only in production
- Input validation on client and server
- SQL injection prevention (backend)
- XSS prevention via React
- CSRF protection via SameSite cookies

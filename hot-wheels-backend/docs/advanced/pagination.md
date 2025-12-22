# Pagination Guide

This guide covers pagination strategies and best practices for the Hot Wheels Collector API.

## Overview

All list endpoints in the API use **offset-based pagination** with consistent parameters and response format.

## Pagination Parameters

| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `page` | integer | 1 | - | Page number (1-indexed) |
| `per_page` | integer | 20 | 100 | Items per page |

## Response Format

All paginated endpoints return:

```json
{
  "success": true,
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 1500,
      "total_pages": 75,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

### Pagination Object

| Field | Type | Description |
|-------|------|-------------|
| `page` | integer | Current page number |
| `per_page` | integer | Items per page |
| `total` | integer | Total number of items |
| `total_pages` | integer | Total number of pages |
| `has_next` | boolean | Whether next page exists |
| `has_prev` | boolean | Whether previous page exists |

## Basic Usage

### Request First Page

```bash
GET /api/v1/catalog/models?page=1&per_page=20
```

### Request Specific Page

```bash
GET /api/v1/catalog/models?page=5&per_page=50
```

### Maximum Page Size

```bash
GET /api/v1/catalog/models?page=1&per_page=100  # Max allowed
```

## Paginated Endpoints

| Endpoint | Default per_page | Max per_page |
|----------|------------------|--------------|
| `/catalog/models` | 20 | 100 |
| `/catalog/models/rare` | 20 | 100 |
| `/catalog/models/recent` | 20 | 100 |
| `/catalog/castings` | 50 | 100 |
| `/catalog/series` | 50 | 100 |
| `/collections` | 20 | 100 |
| `/collections/wishlist` | 20 | 100 |
| `/marketplace/listings` | 20 | 100 |
| `/marketplace/transactions/purchases` | 20 | 100 |
| `/marketplace/transactions/sales` | 20 | 100 |

## Implementation Examples

### Python: Fetch Single Page

```python
def fetch_page(page: int = 1, per_page: int = 20):
    """Fetch a single page of models"""
    response = client.search_models(page=page, per_page=per_page)
    
    return {
        'items': response['models'],
        'pagination': response['pagination']
    }

# Usage
result = fetch_page(page=1, per_page=50)
print(f"Showing {len(result['items'])} of {result['pagination']['total']} models")
```

### Python: Fetch All Pages

```python
def fetch_all_models(query: str = None, per_page: int = 100):
    """Fetch all models across all pages"""
    all_models = []
    page = 1
    
    while True:
        response = client.search_models(
            query=query,
            page=page,
            per_page=per_page
        )
        
        models = response['models']
        all_models.extend(models)
        
        pagination = response['pagination']
        print(f"Fetched page {page}/{pagination['total_pages']}")
        
        if not pagination['has_next']:
            break
        
        page += 1
    
    return all_models

# Usage
all_camaros = fetch_all_models(query="Camaro")
print(f"Total Camaro models: {len(all_camaros)}")
```

### Python: Generator Pattern

```python
def paginate_models(query: str = None, per_page: int = 50):
    """Generator that yields models page by page"""
    page = 1
    
    while True:
        response = client.search_models(
            query=query,
            page=page,
            per_page=per_page
        )
        
        for model in response['models']:
            yield model
        
        if not response['pagination']['has_next']:
            break
        
        page += 1

# Usage - memory efficient
for model in paginate_models(query="Mustang"):
    process_model(model)
```

### JavaScript: Async Iterator

```javascript
async function* paginateModels(query = '', perPage = 50) {
  let page = 1;
  
  while (true) {
    const response = await fetch(
      `${API_BASE}/catalog/models?q=${query}&page=${page}&per_page=${perPage}`,
      { headers: { 'Content-Type': 'application/json' } }
    );
    
    const data = await response.json();
    
    for (const model of data.data.models) {
      yield model;
    }
    
    if (!data.data.pagination.has_next) {
      break;
    }
    
    page++;
  }
}

// Usage
for await (const model of paginateModels('Camaro')) {
  console.log(model.casting_name);
}
```

### JavaScript: Fetch All with Progress

```javascript
async function fetchAllModels(query = '', onProgress = null) {
  const allModels = [];
  let page = 1;
  let totalPages = 1;
  
  while (page <= totalPages) {
    const response = await fetch(
      `${API_BASE}/catalog/models?q=${query}&page=${page}&per_page=100`
    );
    const data = await response.json();
    
    allModels.push(...data.data.models);
    totalPages = data.data.pagination.total_pages;
    
    if (onProgress) {
      onProgress({
        current: page,
        total: totalPages,
        itemsFetched: allModels.length,
        totalItems: data.data.pagination.total
      });
    }
    
    page++;
  }
  
  return allModels;
}

// Usage with progress
const models = await fetchAllModels('', (progress) => {
  console.log(`Progress: ${progress.current}/${progress.total} pages`);
  console.log(`Items: ${progress.itemsFetched}/${progress.totalItems}`);
});
```

## Pagination Strategies

### Strategy 1: Page-Based Navigation

Best for: User interfaces with page numbers

```python
class PaginatedView:
    """UI pagination helper"""
    
    def __init__(self, client, endpoint: str, per_page: int = 20):
        self.client = client
        self.endpoint = endpoint
        self.per_page = per_page
        self.current_page = 1
        self.pagination = None
    
    def go_to_page(self, page: int):
        """Navigate to specific page"""
        response = self.client.get(
            self.endpoint,
            params={'page': page, 'per_page': self.per_page}
        )
        self.current_page = page
        self.pagination = response['pagination']
        return response['items']
    
    def next_page(self):
        """Navigate to next page"""
        if self.pagination and self.pagination['has_next']:
            return self.go_to_page(self.current_page + 1)
        return None
    
    def prev_page(self):
        """Navigate to previous page"""
        if self.pagination and self.pagination['has_prev']:
            return self.go_to_page(self.current_page - 1)
        return None
    
    def get_page_range(self, window: int = 5):
        """Get page numbers for pagination UI"""
        if not self.pagination:
            return [1]
        
        total = self.pagination['total_pages']
        current = self.current_page
        
        start = max(1, current - window // 2)
        end = min(total, start + window - 1)
        start = max(1, end - window + 1)
        
        return list(range(start, end + 1))
```

### Strategy 2: Infinite Scroll

Best for: Mobile apps, continuous loading

```javascript
class InfiniteScrollLoader {
  constructor(fetchFn, perPage = 20) {
    this.fetchFn = fetchFn;
    this.perPage = perPage;
    this.items = [];
    this.currentPage = 0;
    this.totalPages = 1;
    this.loading = false;
  }
  
  async loadMore() {
    if (this.loading || this.currentPage >= this.totalPages) {
      return false;
    }
    
    this.loading = true;
    
    try {
      const response = await this.fetchFn(
        this.currentPage + 1,
        this.perPage
      );
      
      this.items.push(...response.items);
      this.currentPage = response.pagination.page;
      this.totalPages = response.pagination.total_pages;
      
      return response.pagination.has_next;
    } finally {
      this.loading = false;
    }
  }
  
  hasMore() {
    return this.currentPage < this.totalPages;
  }
  
  reset() {
    this.items = [];
    this.currentPage = 0;
    this.totalPages = 1;
  }
}

// Usage
const loader = new InfiniteScrollLoader(
  (page, perPage) => client.searchModels({ page, per_page: perPage })
);

// Initial load
await loader.loadMore();

// On scroll to bottom
window.addEventListener('scroll', async () => {
  if (nearBottom() && loader.hasMore()) {
    await loader.loadMore();
    renderItems(loader.items);
  }
});
```

### Strategy 3: Cursor-Based (Simulated)

For consistent results across pages:

```python
class StablePaginator:
    """Stable pagination using IDs"""
    
    def __init__(self, client, per_page: int = 50):
        self.client = client
        self.per_page = per_page
        self.last_id = None
    
    def fetch_next(self, filters: dict = None):
        """Fetch next batch after last_id"""
        all_filters = filters or {}
        
        # Get items
        response = self.client.search_models(
            per_page=self.per_page,
            **all_filters
        )
        
        items = response['models']
        
        # Filter out items we've seen
        if self.last_id:
            items = [i for i in items if i['model_id'] > self.last_id]
        
        # Update cursor
        if items:
            self.last_id = max(i['model_id'] for i in items)
        
        return items
    
    def reset(self):
        """Reset pagination"""
        self.last_id = None
```

## Performance Optimization

### Parallel Page Fetching

```python
import asyncio
import aiohttp

async def fetch_page_async(session, page, per_page):
    """Fetch single page asynchronously"""
    async with session.get(
        f"{API_BASE}/catalog/models",
        params={'page': page, 'per_page': per_page}
    ) as response:
        return await response.json()

async def fetch_pages_parallel(start_page: int, end_page: int, per_page: int = 100):
    """Fetch multiple pages in parallel"""
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_page_async(session, page, per_page)
            for page in range(start_page, end_page + 1)
        ]
        results = await asyncio.gather(*tasks)
    
    # Combine results in order
    all_items = []
    for result in results:
        all_items.extend(result['data']['models'])
    
    return all_items

# Usage - fetch pages 1-10 in parallel
models = asyncio.run(fetch_pages_parallel(1, 10, per_page=100))
```

### Caching Paginated Results

```python
class CachedPaginator:
    """Paginator with page caching"""
    
    def __init__(self, client, cache_ttl: int = 300):
        self.client = client
        self.cache_ttl = cache_ttl
        self._cache = {}
        self._cache_time = {}
    
    def get_page(self, endpoint: str, page: int, per_page: int, **filters):
        """Get page with caching"""
        cache_key = self._make_key(endpoint, page, per_page, filters)
        
        # Check cache
        if cache_key in self._cache:
            if time.time() < self._cache_time[cache_key]:
                return self._cache[cache_key]
        
        # Fetch fresh
        response = self.client.get(
            endpoint,
            params={'page': page, 'per_page': per_page, **filters}
        )
        
        # Cache it
        self._cache[cache_key] = response
        self._cache_time[cache_key] = time.time() + self.cache_ttl
        
        return response
    
    def _make_key(self, endpoint, page, per_page, filters):
        """Generate cache key"""
        filter_str = '&'.join(f"{k}={v}" for k, v in sorted(filters.items()))
        return f"{endpoint}?page={page}&per_page={per_page}&{filter_str}"
    
    def invalidate(self, endpoint: str = None):
        """Invalidate cache"""
        if endpoint:
            keys_to_delete = [k for k in self._cache if k.startswith(endpoint)]
            for key in keys_to_delete:
                del self._cache[key]
                del self._cache_time[key]
        else:
            self._cache.clear()
            self._cache_time.clear()
```

## Best Practices

### Do's

- ✅ Use reasonable page sizes (20-50 for UI, 100 for bulk operations)
- ✅ Check `has_next` before requesting next page
- ✅ Handle empty results gracefully
- ✅ Cache paginated results when appropriate
- ✅ Show loading states during page transitions

### Don'ts

- ❌ Request more than `per_page=100` (will be capped)
- ❌ Fetch all pages when only first page is needed
- ❌ Ignore pagination metadata
- ❌ Make rapid sequential page requests (use throttling)

---

**Next:** [Rate Limiting](rate-limiting.md) | [Best Practices](best-practices.md)


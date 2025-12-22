# Documentation Setup Instructions

This guide explains how to set up, validate, and serve the API documentation.

## Quick Start

### 1. View Documentation Locally

The simplest way to view the documentation is to open the Markdown files directly in a Markdown viewer or IDE like VS Code.

### 2. Use Swagger UI Online

1. Go to [Swagger Editor](https://editor.swagger.io/)
2. Copy contents of `docs/openapi.yaml`
3. Paste into the editor
4. View interactive documentation on the right panel

### 3. Use Redoc Online

1. Go to [Redocly Demo](https://redocly.github.io/redoc/)
2. Enter URL to raw `openapi.yaml` file (if hosted)
3. Or use the local method below

---

## Local Documentation Server

### Option A: Python HTTP Server

```bash
cd docs
python -m http.server 8080
```

Then open: http://localhost:8080

### Option B: Swagger UI with Docker

```bash
# Run Swagger UI container
docker run -p 8080:8080 \
  -e SWAGGER_JSON=/docs/openapi.yaml \
  -v $(pwd)/docs:/docs \
  swaggerapi/swagger-ui

# Open http://localhost:8080
```

### Option C: Redoc with Docker

```bash
# Run Redoc container
docker run -p 8080:80 \
  -v $(pwd)/docs/openapi.yaml:/usr/share/nginx/html/openapi.yaml \
  -e SPEC_URL=openapi.yaml \
  redocly/redoc

# Open http://localhost:8080
```

### Option D: Generate Static HTML

```bash
# Install Redocly CLI
npm install -g @redocly/cli

# Generate HTML
redocly build-docs docs/openapi.yaml --output docs/generated/index.html

# Open docs/generated/index.html in browser
```

---

## Validate OpenAPI Specification

### Option 1: Swagger Editor (Online)

1. Go to https://editor.swagger.io/
2. Paste `openapi.yaml` contents
3. Check for errors in the editor

### Option 2: Spectral CLI

```bash
# Install Spectral
npm install -g @stoplight/spectral-cli

# Validate
spectral lint docs/openapi.yaml
```

### Option 3: Redocly CLI

```bash
# Install Redocly
npm install -g @redocly/cli

# Validate
redocly lint docs/openapi.yaml
```

### Option 4: OpenAPI Generator

```bash
# Install (using npm)
npm install -g @openapitools/openapi-generator-cli

# Validate
openapi-generator-cli validate -i docs/openapi.yaml
```

### Option 5: Python Validator

```bash
# Install
pip install openapi-spec-validator

# Validate
openapi-spec-validator docs/openapi.yaml
```

---

## Generate SDK/Client Code

### Python Client

```bash
openapi-generator-cli generate \
  -i docs/openapi.yaml \
  -g python \
  -o generated/python-client
```

### JavaScript/TypeScript Client

```bash
openapi-generator-cli generate \
  -i docs/openapi.yaml \
  -g typescript-fetch \
  -o generated/typescript-client
```

### Postman Collection

```bash
openapi-generator-cli generate \
  -i docs/openapi.yaml \
  -g postman-collection \
  -o generated/postman
```

---

## Recommended Tools Installation

### Node.js Tools

```bash
# Install all recommended tools
npm install -g @stoplight/spectral-cli @redocly/cli @openapitools/openapi-generator-cli
```

### Python Tools

```bash
# Install Python validation tools
pip install openapi-spec-validator pyyaml
```

---

## Directory Structure After Setup

```
docs/
├── README.md                    # Documentation index
├── openapi.yaml                 # OpenAPI specification
├── DOCUMENTATION_STRATEGY.md    # Documentation strategy report
├── SETUP_INSTRUCTIONS.md        # This file
├── changelog.md                 # Version history
│
├── guides/
│   ├── getting-started.md
│   ├── authentication.md
│   └── integration-tutorial.md
│
├── reference/
│   ├── api-overview.md
│   └── error-codes.md
│
├── architecture/
│   ├── system-overview.md
│   └── database-schema.md
│
├── advanced/
│   ├── pagination.md
│   └── best-practices.md
│
├── examples/
│   └── curl-examples.md
│
├── scripts/
│   ├── validate-openapi.sh
│   └── generate-docs.sh
│
└── generated/                   # Generated files (gitignored)
    ├── index.html               # Redoc HTML
    └── openapi.json             # JSON version
```

---

## Continuous Integration

### GitHub Actions Example

```yaml
# .github/workflows/docs.yml
name: Validate API Documentation

on:
  push:
    paths:
      - 'docs/**'
  pull_request:
    paths:
      - 'docs/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Spectral
        run: npm install -g @stoplight/spectral-cli
      
      - name: Validate OpenAPI
        run: spectral lint docs/openapi.yaml
      
      - name: Install Redocly
        run: npm install -g @redocly/cli
        
      - name: Build Documentation
        run: redocly build-docs docs/openapi.yaml --output docs/generated/index.html
      
      - name: Upload Documentation
        uses: actions/upload-artifact@v3
        with:
          name: api-docs
          path: docs/generated/
```

---

## Troubleshooting

### "YAML syntax error"

```bash
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('docs/openapi.yaml'))"
```

### "Schema validation failed"

- Ensure all `$ref` references are valid
- Check that required fields are present
- Verify enum values match schema

### "Swagger UI not loading"

- Check CORS settings if loading from different origin
- Ensure YAML is valid JSON when converted
- Try clearing browser cache

---

## Support

For documentation issues:
- Create an issue in the repository
- Contact: support@hotwheels-collector.com

---

*Last Updated: December 2024*


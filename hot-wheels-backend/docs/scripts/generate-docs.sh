#!/bin/bash
# Documentation Generation Script
# Generates documentation site from OpenAPI specification

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$(dirname "$SCRIPT_DIR")"
OPENAPI_FILE="$DOCS_DIR/openapi.yaml"
OUTPUT_DIR="$DOCS_DIR/generated"

echo "======================================"
echo "  API Documentation Generator"
echo "======================================"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Generate Redoc HTML (standalone documentation)
echo "📄 Generating Redoc HTML..."
if command -v redocly &> /dev/null; then
    redocly build-docs "$OPENAPI_FILE" --output "$OUTPUT_DIR/index.html"
    echo "   ✅ Redoc HTML generated: $OUTPUT_DIR/index.html"
else
    echo "   ⚠️  Redocly not installed. Trying npx..."
    npx @redocly/cli build-docs "$OPENAPI_FILE" --output "$OUTPUT_DIR/index.html" 2>/dev/null || \
        echo "   ❌ Could not generate Redoc HTML"
fi
echo ""

# Generate OpenAPI JSON (for tools that prefer JSON)
echo "📄 Converting to JSON..."
if command -v yq &> /dev/null; then
    yq -o=json "$OPENAPI_FILE" > "$OUTPUT_DIR/openapi.json"
    echo "   ✅ JSON version generated: $OUTPUT_DIR/openapi.json"
else
    echo "   ℹ️  yq not installed. Using Python..."
    python3 -c "
import yaml
import json
with open('$OPENAPI_FILE', 'r') as f:
    spec = yaml.safe_load(f)
with open('$OUTPUT_DIR/openapi.json', 'w') as f:
    json.dump(spec, f, indent=2)
print('   ✅ JSON version generated: $OUTPUT_DIR/openapi.json')
" 2>/dev/null || echo "   ⚠️  Could not convert to JSON"
fi
echo ""

# Generate Postman Collection
echo "📄 Generating Postman Collection..."
if command -v openapi-generator-cli &> /dev/null; then
    openapi-generator-cli generate \
        -i "$OPENAPI_FILE" \
        -g postman-collection \
        -o "$OUTPUT_DIR/postman" 2>/dev/null && \
        echo "   ✅ Postman collection generated: $OUTPUT_DIR/postman/"
else
    echo "   ℹ️  OpenAPI Generator not installed. Skipping Postman generation."
fi
echo ""

echo "======================================"
echo "  Generation Complete"
echo "======================================"
echo ""
echo "Generated files:"
ls -la "$OUTPUT_DIR/" 2>/dev/null || echo "No files generated"
echo ""
echo "To view documentation:"
echo "  1. Open $OUTPUT_DIR/index.html in a browser"
echo "  2. Or start a local server: python3 -m http.server -d $OUTPUT_DIR 8080"
echo ""


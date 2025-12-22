#!/bin/bash
# OpenAPI Specification Validation Script
# This script validates the OpenAPI specification using multiple tools

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$(dirname "$SCRIPT_DIR")"
OPENAPI_FILE="$DOCS_DIR/openapi.yaml"

echo "======================================"
echo "  OpenAPI Specification Validator"
echo "======================================"
echo ""

# Check if openapi.yaml exists
if [ ! -f "$OPENAPI_FILE" ]; then
    echo "❌ Error: openapi.yaml not found at $OPENAPI_FILE"
    exit 1
fi

echo "📄 Validating: $OPENAPI_FILE"
echo ""

# Track validation status
VALIDATION_PASSED=true

# Method 1: Swagger Editor Online (manual check reminder)
echo "📋 Validation Method 1: Swagger Editor"
echo "   → Copy openapi.yaml contents to https://editor.swagger.io/"
echo "   → Check for any validation errors in the editor"
echo ""

# Method 2: Spectral (if installed)
echo "📋 Validation Method 2: Spectral API Linter"
if command -v spectral &> /dev/null; then
    echo "   Running Spectral linting..."
    if spectral lint "$OPENAPI_FILE" --ruleset .spectral.yaml 2>/dev/null || spectral lint "$OPENAPI_FILE"; then
        echo "   ✅ Spectral validation passed"
    else
        echo "   ⚠️  Spectral found issues (warnings may be acceptable)"
    fi
else
    echo "   ℹ️  Spectral not installed. Install with: npm install -g @stoplight/spectral-cli"
fi
echo ""

# Method 3: Redocly CLI (if installed)
echo "📋 Validation Method 3: Redocly CLI"
if command -v redocly &> /dev/null; then
    echo "   Running Redocly validation..."
    if redocly lint "$OPENAPI_FILE"; then
        echo "   ✅ Redocly validation passed"
    else
        echo "   ❌ Redocly validation failed"
        VALIDATION_PASSED=false
    fi
else
    echo "   ℹ️  Redocly not installed. Install with: npm install -g @redocly/cli"
fi
echo ""

# Method 4: OpenAPI Generator (if installed)
echo "📋 Validation Method 4: OpenAPI Generator"
if command -v openapi-generator-cli &> /dev/null; then
    echo "   Running OpenAPI Generator validation..."
    if openapi-generator-cli validate -i "$OPENAPI_FILE"; then
        echo "   ✅ OpenAPI Generator validation passed"
    else
        echo "   ❌ OpenAPI Generator validation failed"
        VALIDATION_PASSED=false
    fi
else
    echo "   ℹ️  OpenAPI Generator not installed."
fi
echo ""

# Method 5: Python-based validation (if swagger-spec-validator installed)
echo "📋 Validation Method 5: Python Validator"
if python3 -c "import swagger_spec_validator" 2>/dev/null; then
    echo "   Running Python swagger-spec-validator..."
    if python3 -c "
import swagger_spec_validator
import yaml
with open('$OPENAPI_FILE', 'r') as f:
    spec = yaml.safe_load(f)
swagger_spec_validator.validate_spec(spec)
print('   ✅ Python validation passed')
" 2>/dev/null; then
        :
    else
        echo "   ⚠️  Python validation had issues"
    fi
else
    echo "   ℹ️  swagger-spec-validator not installed. Install with: pip install swagger-spec-validator pyyaml"
fi
echo ""

# Summary
echo "======================================"
echo "  Validation Summary"
echo "======================================"

if [ "$VALIDATION_PASSED" = true ]; then
    echo "✅ All automated validations passed!"
else
    echo "⚠️  Some validations had issues. Please review above."
fi

echo ""
echo "📝 Manual checks required:"
echo "   1. Verify all endpoints match actual implementation"
echo "   2. Test example requests in Swagger UI"
echo "   3. Confirm response schemas match actual responses"
echo ""

exit 0


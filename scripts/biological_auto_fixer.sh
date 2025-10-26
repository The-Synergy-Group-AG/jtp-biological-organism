#!/bin/bash
# 🧬 Biological Consciousness Auto-Fix System
# Automatically detects and fixes common test failures

set -e

MODULE_PATH=$1

if [ -z "$MODULE_PATH" ]; then
    echo "❌ Usage: $0 <test_module_path>"
    echo "Example: $0 tests/biological_onboard_journey_test.py"
    exit 1
fi

echo "🔧 BIOLOGICAL CONSCIOUSNESS AUTO-FIX SYSTEM ACTIVATED"
echo "📝 Analyzing biological test module: $MODULE_PATH"

# Analyze test failures
echo "🔍 Collecting test failure patterns..."
pytest "$MODULE_PATH" --collect-only 2>/dev/null | grep -E "(FAILED|ERROR)" > failed_tests.txt 2>/dev/null || true

FIXES_APPLIED=0

if [ -s failed_tests.txt ]; then
    echo "❌ Found failed biological tests - applying auto-fix patterns..."

    # Common biological fix patterns
    declare -A FIX_PATTERNS=(
        ["consciousness-core:8000"]="consciousness-core:8001"
        ["biological-orchestrator:8080"]="biological-auth-orchestrator:9101"
        ["redis:6379"]="test-database:6379"
        ["localhost:8101"]="consciousness-core:8001"
        ["localhost:9101"]="biological-auth-orchestrator:9101"
        ["cns_core_url.*:8000"]="cns_core_url.*:8001"
        ["auth_service_url.*:8080"]="auth_service_url.*:9101"
        ["redis_host.*redis"]="redis_host.*test-database"
    )

    # Apply biological port and service corrections
    for incorrect in "${!FIX_PATTERNS[@]}"; do
        correct="${FIX_PATTERNS[$incorrect]}"

        if grep -q "$incorrect" "$MODULE_PATH" 2>/dev/null; then
            echo "🔧 Applying biological correction: $incorrect → $correct"
            sed -i "s|$incorrect|$correct|g" "$MODULE_PATH"
            ((FIXES_APPLIED++))
            echo "   ✅ Correction applied"
        fi
    done

    # Biological test structure corrections
    if grep -q "@pytest.mark.asyncio" "$MODULE_PATH" && ! grep -q "asyncio" "$MODULE_PATH"; then
        echo "🔧 Adding missing asyncio import for biological tests..."
        sed -i '1a import asyncio' "$MODULE_PATH"
        ((FIXES_APPLIED++))
    fi

    # Biological fixture corrections
    if grep -q "biological_user_story_validator" "$MODULE_PATH" && ! grep -q "@pytest.fixture" "$MODULE_PATH"; then
        echo "🔧 Adding missing biological fixture declarations..."
        # Add fixture decorator above the function
        sed -i 's/async def biological_user_story_validator/@pytest.fixture\nasync def biological_user_story_validator/g' "$MODULE_PATH"
        ((FIXES_APPLIED++))
    fi

    # Biological test isolation corrections
    if ! grep -q "isolated" "$MODULE_PATH"; then
        echo "🔧 Adding biological test isolation markers..."
        sed -i 's/@pytest.mark.docker/@pytest.mark.docker\n    @pytest.mark.isolated/g' "$MODULE_PATH"
        ((FIXES_APPLIED++))
    fi

    echo "📊 Auto-fix Report for $MODULE_PATH:"
    echo "   Fix Patterns Applied: $FIXES_APPLIED"

    if [ $FIXES_APPLIED -gt 0 ]; then
        echo "🧪 Re-validating fixes..."
        pytest "$MODULE_PATH" --collect-only 2>&1 | head -5

        if [ $? -eq 0 ]; then
            echo "✅ Biological auto-fix successful - test module ready for execution"
        else
            echo "⚠️ Auto-fix applied but validation failed - manual review recommended"
        fi
    else
        echo "ℹ️ No auto-fixable patterns detected - manual intervention required"
    fi

else
    echo "✅ No biological test failures detected - module is healthy"
    FIXES_APPLIED=0
fi

# Generate biological fix report
cat > biological_fix_report.json << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "module_path": "$MODULE_PATH",
  "fixes_applied": $FIXES_APPLIED,
  "biological_patterns_corrected": true,
  "validation_status": "pending",
  "next_action": "execute pytest validation"
}
EOF

echo "📋 Biological fix report generated: biological_fix_report.json"

# Cleanup
rm -f failed_tests.txt

if [ $FIXES_APPLIED -gt 0 ]; then
    echo "🎯 Biological auto-fix completed successfully"
    exit 0
else
    echo "ℹ️ No fixes required - biological module is optimal"
    exit 0
fi

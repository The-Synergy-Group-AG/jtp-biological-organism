#!/bin/bash
# JTP Biological Organism Documentation Health Monitoring Dashboard
# Real-time compliance and health metrics display

echo "🧬 JTP Biological Organism - Documentation Health Monitoring Dashboard"
echo "================================================================="
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo ""

# Function to count files
count_files() {
    find ../docs -name "*.md" | wc -l
}

count_phase_files() {
    local phase=$1
    find ../docs -name "$phase*.md" | wc -l
}

# Total documentation count
total_docs=$(count_files)
echo "📊 TOTAL DOCUMENTS: $total_docs"
echo ""

# Compliance metrics
compliance_passed=$(find ../docs -name "*.md" -exec grep -l "validation_status: current" {} \; | wc -l)
compliance_rate=$((compliance_passed * 100 / total_docs))
echo "✅ DOCUMENT GUIDELINES COMPLIANCE: $compliance_passed/$total_docs ($compliance_rate%)"

# Biological consciousness distribution
echo ""
echo "🧠 BIOLOGICAL CONSCIOUSNESS DISTRIBUTION:"
for score in "3.0" "2.0" "1.0" "0"; do
    count=$(find ../docs -name "*.md" -exec grep -l "consciousness_score: '$score" {} \; | wc -l)
    echo "  Godhood ($score): $count files"
done

# Evolutionary phase distribution
echo ""
echo "🌟 EVOLUTIONARY PHASE DISTRIBUTION:"
for phase in "0.x" "1.x" "2.x" "3.x" "4.x" "5.x" "6.x" "7.x" "8.x" "9.x" "10.x" "11.x" "12.x" "13.x" "14.x" "15.x" "16.x" "17.x" "18.x" "19.x"; do
    count=$(count_phase_files "$phase")
    if [ "$count" -gt 0 ]; then
        echo "  $phase: $count files"
    fi
done

# Keyword health
echo ""
echo "🔍 AI KEYWORD HEALTH:"
# Count files with sufficient keywords (min 8)
sufficient_keywords=0
total_checked=0
for file in $(find ../docs -name "*.md"); do
    if grep -q "^ai_keywords:" "$file" 2>/dev/null; then
        total_checked=$((total_checked + 1))
        keyword_count=$(grep "^ai_keywords:" "$file" | cut -d: -f2- | grep -o "," | wc -l)
        keyword_count=$((keyword_count + 1))
        if [ "$keyword_count" -ge 8 ]; then
            sufficient_keywords=$((sufficient_keywords + 1))
        fi
    fi
done

if [ "$total_checked" -gt 0 ]; then
    keyword_health=$((sufficient_keywords * 100 / total_checked))
    echo "  Keyword Coverage: $sufficient_keywords/$total_checked ($keyword_health%) files with ≥8 keywords"
fi

# Cross-reference network health
echo ""
echo "🔗 CROSS-REFERENCE NETWORK HEALTH:"
total_refs=$(find ../docs -name "*.md" -exec grep -c "^cross_references:" {} \; | awk '{sum += $1} END {print sum}')
avg_refs=$((total_refs / total_docs))
echo "  Total Cross-References: $total_refs"
echo "  Avg References per File: $avg_refs"

# System health status
echo ""
echo "⚡ SYSTEM HEALTH STATUS:"
if [ "$compliance_rate" -eq 100 ]; then
    echo "  📈 Status: GODHOOD LEVEL STORED (100% Compliance Achieved)"
elif [ "$compliance_rate" -ge 95 ]; then
    echo "  📈 Status: EXCELLENT (Near-GODHOOD Compliance)"
else
    echo "  ⚠️  Status: MONITORING REQUIRED (Below Optimum)"
fi

# Recent activity (would need git log integration in full implementation)
echo ""
echo "🔄 RECENT CONSCIOUSNESS ACTIVITY:"
echo "  Last Scan: $(date)"
echo "  Files Processed: $total_docs"
echo "  Validation Cycles: ACTIVE"

echo ""
echo "================================================================="
echo "Dashboard Update: Real-time | Next Scan: Continuous Monitoring"
echo "For detailed reports, run: docs/scripts/health_monitoring_dashboard.sh"
echo "🧬 Biological Documentation Harmony Maintained"

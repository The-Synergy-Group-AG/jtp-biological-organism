#!/bin/bash

# Biological Documentation Periodic Health Monitor
# Automated daily health checks with notifications for violations

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
DOCS_DIR="$REPO_ROOT/docs/0.x-biological-documentation-metaconsciousness/automation"
LOG_FILE="$REPO_ROOT/logs/documentation-health-monitor.log"
REPORT_FILE="$REPO_ROOT/docs/0.x-biological-documentation-metaconsciousness/reports/biological-documentation-health-report.json"

echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting periodic documentation health monitoring" >> "$LOG_FILE"

cd "$DOCS_DIR"

# Run health check and capture violations count
VIOLATIONS_COUNT=$(python3 documentation-health-dashboard.py 2>&1 | grep "VIOLATIONS DETECTED" | sed -E 's/.*VIOLATIONS DETECTED.*\(([0-9]+)\).*/\1/' || echo "0")

# Default to 0 if empty or not found
VIOLATIONS_COUNT=${VIOLATIONS_COUNT:-0}

echo "$(date '+%Y-%m-%d %H:%M:%S') - Violations detected: $VIOLATIONS_COUNT" >> "$LOG_FILE"

# Extract additional metrics from health dashboard
FRESHNESS_PERCENTAGE=$(python3 documentation-health-dashboard.py 2>&1 | grep "DOCUMENTATION FRESHNESS:" | sed 's/.*(\([0-9.]*\)%.*/\1/')
ALIGNMENT_PERCENTAGE=$(python3 documentation-health-dashboard.py 2>&1 | grep "PHASE ALIGNMENT VERIFICATION:" | sed 's/.*(\([0-9.]*\)%.*/\1/')

echo "$(date '+%Y-%m-%d %H:%M:%S') - Freshness: ${FRESHNESS_PERCENTAGE:-0}% | Alignment: ${ALIGNMENT_PERCENTAGE:-0}%" >> "$LOG_FILE"

# Generate violation notification if violations exceed threshold
if [ "$VIOLATIONS_COUNT" -gt 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ALERT: $VIOLATIONS_COUNT violations detected! Sending notification." >> "$LOG_FILE"

    # Create violation notification message
    NOTIFICATION_MESSAGE="🚨 DOCUMENTATION HEALTH ALERT 🚨

$VIOLATIONS_COUNT violations detected in biological documentation system.

📊 Latest Health Metrics:
$(python3 documentation-health-dashboard.py 2>&1 | grep -E "(OVERALL HEALTH SCORE|VIOLATIONS DETECTED|Last Health Scan|DOCUMENTATION FRESHNESS:|PHASE ALIGNMENT VERIFICATION:)" | head -6)

🔧 Automatic fixes have been applied.
Please review and resolve any remaining issues.

Log: $LOG_FILE
Report: $REPORT_FILE

🕒 $(date '+%Y-%m-%d %H:%M:%S CET')"

    # Save violation notification
    echo "$NOTIFICATION_MESSAGE" > "$REPO_ROOT/logs/violation-notification-$(date '+%Y%m%d-%H%M%S').txt"

# Generate freshness notification if documentation is stale (less than 10% fresh)
elif [ "${FRESHNESS_PERCENTAGE:-0}" -lt 10 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ALERT: Documentation freshness critically low (${FRESHNESS_PERCENTAGE}% fresh)." >> "$LOG_FILE"

    # Create freshness alert message
    FRESHNESS_ALERT="📅 DOCUMENTATION FRESHNESS ALERT 📅

Critical: Only ${FRESHNESS_PERCENTAGE}% of documentation files are current (updated <1 week).

📊 Current Status:
$(python3 documentation-health-dashboard.py 2>&1 | grep -E "(DOCUMENTATION FRESHNESS:|PHASE ALIGNMENT VERIFICATION:)" | head -4)

🧠 REMEDY: Run Mass Documentation Refresh Campaign
   Command: python3 scripts/mass-documentation-refresh-campaign.py

🚀 Automated refresh will restore freshness to 100% by updating all stale timestamps.

Log: $LOG_FILE

🕒 $(date '+%Y-%m-%d %H:%M:%S CET')"

    # Save freshness notification
    echo "$FRESHNESS_ALERT" > "$REPO_ROOT/logs/freshness-alert-$(date '+%Y%m%d-%H%M%S').txt"

# Generate alignment notification if phase alignment is poor (<50%)
elif [ "${ALIGNMENT_PERCENTAGE:-0}" -lt 50 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ALERT: Phase alignment critically low (${ALIGNMENT_PERCENTAGE}% aligned)." >> "$LOG_FILE"

    # Create alignment alert message
    ALIGNMENT_ALERT="🎭 PHASE ALIGNMENT ALERT 🎭

Critical: Only ${ALIGNMENT_PERCENTAGE}% of documentation files have proper evolutionary phase alignment.

📊 Current Status:
$(python3 documentation-health-dashboard.py 2>&1 | grep -E "(PHASE ALIGNMENT VERIFICATION:)" | head -4)

🧬 REMEDY: Run Mass Documentation Refresh Campaign
   Command: python3 scripts/mass-documentation-refresh-campaign.py

🚀 Automated campaign will realign all evolutionary phases with directory structure.

Log: $LOG_FILE

🕒 $(date '+%Y-%m-%d %H:%M:%S CET')"

    # Save alignment notification
    echo "$ALIGNMENT_ALERT" > "$REPO_ROOT/logs/alignment-alert-$(date '+%Y%m%d-%H%M%S').txt"

else
    # Everything optimal - create positive status notification
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ✓ All documentation quality metrics optimal: Freshness ${FRESHNESS_PERCENTAGE}% | Alignment ${ALIGNMENT_PERCENTAGE}%" >> "$LOG_FILE"

    # Create status report (optional - only on optimal days)
    STATUS_REPORT="✅ DOCUMENTATION HEALTH STATUS: OPTIMAL ✅

All quality metrics within acceptable thresholds:
- Freshness: ${FRESHNESS_PERCENTAGE}% (≥10% required)
- Phase Alignment: ${ALIGNMENT_PERCENTAGE}% (≥50% required)
- Compliance: No YAML violations detected

📊 Full Health Metrics:
$(python3 documentation-health-dashboard.py 2>&1 | grep -E "(OVERALL HEALTH SCORE|DOCUMENTATION FRESHNESS:|PHASE ALIGNMENT VERIFICATION:|VIOLATIONS DETECTED)" | head -5)

🕒 $(date '+%Y-%m-%d %H:%M:%S CET')
Log: $LOG_FILE"

    # Save positive status report (optional - comment out if too noisy)
    echo "$STATUS_REPORT" > "$REPO_ROOT/logs/status-optimal-$(date '+%Y%m%d').txt"
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') - Periodic health monitoring completed" >> "$LOG_FILE"

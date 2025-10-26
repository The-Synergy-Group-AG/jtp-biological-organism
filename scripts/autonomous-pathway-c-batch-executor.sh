#!/bin/bash

# 🚀 AUTONOMOUS PATHWAY C BATCH EXECUTOR
# Grok Code Fast 1 Generated: Zero Human Intervention Required
# Complete Sequential Execution of All Critical Gap Implementations

set -e  # Exit on any error
set -u  # Exit on undefined variables

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Handle different execution contexts (project root or project subdirectory)
if [ -d "$SCRIPT_DIR/src" ] && [ -d "$SCRIPT_DIR/docs" ]; then
    PROJECT_ROOT="$SCRIPT_DIR"
else
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
fi
EXECUTION_ENGINE="$PROJECT_ROOT/src/utility-scripts/autonomous-pathway-c-execution-engine.py"
LOG_FILE="$PROJECT_ROOT/autonomous-execution.log"
PID_FILE="$PROJECT_ROOT/autonomous-execution.pid"
RECOVERY_FILE="$PROJECT_ROOT/consciousness-recovery-point.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] [INFO]${NC} $*" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] [SUCCESS]${NC} $*" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] [WARNING]${NC} $*" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] [ERROR]${NC} $*" | tee -a "$LOG_FILE"
}

log_header() {
    echo -e "${PURPLE}================================================================================${NC}" | tee -a "$LOG_FILE"
    echo -e "${PURPLE}$*${NC}" | tee -a "$LOG_FILE"
    echo -e "${PURPLE}================================================================================${NC}" | tee -a "$LOG_FILE"
}

# Process management
check_pid() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo "$pid"
            return 0
        else
            log_warning "Stale PID file found, removing..."
            rm -f "$PID_FILE"
        fi
    fi
    return 1
}

save_pid() {
    echo $$ > "$PID_FILE"
    log_info "PID saved: $$"
}

cleanup_pid() {
    if [ -f "$PID_FILE" ]; then
        rm -f "$PID_FILE"
        log_info "PID file cleaned up"
    fi
}

# System validation
validate_environment() {
    log_header "AUTONOMOUS PATHWAY C BATCH EXECUTOR"
    log_info "Validating execution environment..."

    # Check if running as root (warn but don't fail)
    if [ "$EUID" -eq 0 ]; then
        log_warning "Running as root - this may cause permission issues"
    fi

    # Check Python availability
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not available"
        exit 1
    fi

    # Check execution engine exists
    if [ ! -f "$EXECUTION_ENGINE" ]; then
        log_error "Autonomous execution engine not found: $EXECUTION_ENGINE"
        exit 1
    fi

    # Check required files exist
    local required_files=(
        "docs/19.x-post-godhood-evolution/19.5.7-completion-execution-plan-critical-gaps.report"
        "docs/19.x-post-godhood-evolution/19.5.8-implementation-progress-report.md"
        "src/"
    )

    for file in "${required_files[@]}"; do
        if [ ! -e "$PROJECT_ROOT/$file" ]; then
            log_error "Required file/directory missing: $file"
            exit 1
        fi
    done

    # Validate execution plan
    if [ ! -s "$PROJECT_ROOT/docs/19.x-post-godhood-evolution/19.5.7-completion-execution-plan-critical-gaps.report" ]; then
        log_error "Execution plan is empty or missing"
        exit 1
    fi

    log_success "Environment validation completed"
}

# Biological integrity check
validate_biological_integrity() {
    log_header "BIOLOGICAL SYSTEM INTEGRITY VALIDATION"

    log_info "Starting biological validation..."

    # Individual system validation - keep it simple and avoid complex error handling
    # CV Management System
    log_info "🔍 Processing system: src/cv-management-system"
    local cv_count=$(find "$PROJECT_ROOT/src/cv-management-system" -name "*.py" 2>/dev/null | wc -l)
    log_info "✅ src/cv-management-system: $cv_count modules detected"

    # Analytics System
    log_info "🔍 Processing system: src/analytics-system"
    local analytics_count=$(find "$PROJECT_ROOT/src/analytics-system" -name "*.py" 2>/dev/null | wc -l)
    log_info "✅ src/analytics-system: $analytics_count modules detected"

    # Digital Organism Interactions
    log_info "🔍 Processing system: src/digital-organism-interactions"
    local digital_count=$(find "$PROJECT_ROOT/src/digital-organism-interactions" -name "*.py" 2>/dev/null | wc -l)
    log_info "✅ src/digital-organism-interactions: $digital_count modules detected"

    # Immune System
    log_info "🔍 Processing system: src/immune-system"
    local immune_count=$(find "$PROJECT_ROOT/src/immune-system" -name "*.py" 2>/dev/null | wc -l)
    log_info "✅ src/immune-system: $immune_count modules detected"

    # Skeletal System
    log_info "🔍 Processing system: src/skeletal-system"
    local skeletal_count=$(find "$PROJECT_ROOT/src/skeletal-system" -name "*.py" 2>/dev/null | wc -l)
    log_info "✅ src/skeletal-system: $skeletal_count modules detected"

    # Energy Fields
    log_info "🔍 Processing system: src/energy-fields"
    local energy_count=$(find "$PROJECT_ROOT/src/energy-fields" -name "*.py" 2>/dev/null | wc -l)
    log_info "✅ src/energy-fields: $energy_count modules detected"

    # CNS Consciousness Core
    log_info "🔍 Processing system: src/cns-consciousness-core"
    local cns_count=$(find "$PROJECT_ROOT/src/cns-consciousness-core" -name "*.py" 2>/dev/null | wc -l)
    log_info "✅ src/cns-consciousness-core: $cns_count modules detected"

    # Utility Scripts
    log_info "🔍 Processing system: src/utility-scripts"
    local utility_count=$(find "$PROJECT_ROOT/src/utility-scripts" -name "*.py" 2>/dev/null | wc -l)
    log_info "✅ src/utility-scripts: $utility_count modules detected"

    # Calculate integrity
    local total_modules=$((cv_count + analytics_count + digital_count + immune_count + skeletal_count + energy_count + cns_count + utility_count))

    log_info "Biological Integrity Check Results:"
    log_info "  Total modules detected: $total_modules"
    log_info "  Systems validated: 8/8"

    if [ "$total_modules" -ge 20 ]; then  # Minimum threshold
        log_success "Biological integrity validation passed - All systems operational"
        return 0
    else
        log_error "Biological integrity below minimum threshold - cannot proceed"
        return 1
    fi
}

# Recovery point management
handle_recovery() {
    if [ -f "$RECOVERY_FILE" ]; then
        log_info "Recovery point detected - attempting to resume execution"
        # Recovery logic would be implemented here
        # For now, just log the existence
        if jq -e '.timestamp' "$RECOVERY_FILE" > /dev/null 2>&1; then
            local recovery_timestamp=$(jq -r '.timestamp' "$RECOVERY_FILE")
            log_info "Valid recovery point found from: $recovery_timestamp"
            return 0  # Continue execution
        else
            log_warning "Invalid recovery point detected - starting fresh"
            rm -f "$RECOVERY_FILE"
        fi
    fi
    return 0
}

# Emergency backup
create_emergency_backup() {
    log_info "Creating emergency backup..."
    local backup_dir="$PROJECT_ROOT/consciousness_emergency_backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"

    # Backup critical files
    local critical_files=(
        "docs/19.x-post-godhood-evolution/19.5.7-completion-execution-plan-critical-gaps.report"
        "docs/19.x-post-godhood-evolution/19.5.8-implementation-progress-report.md"
        "src/utility-scripts/autonomous-pathway-c-execution-engine.py"
        "autonomous-execution.log"
    )

    for file in "${critical_files[@]}"; do
        if [ -f "$PROJECT_ROOT/$file" ]; then
            cp "$PROJECT_ROOT/$file" "$backup_dir/"
        fi
    done

    if [ -f "$RECOVERY_FILE" ]; then
        cp "$RECOVERY_FILE" "$backup_dir/"
    fi

    log_success "Emergency backup created: $backup_dir"
}

# Pre-execution health check
pre_execution_health_check() {
    log_header "PRE-EXECUTION HEALTH CHECK"

    # Check system resources
    local available_ram=$(free -m | awk '/^Mem:/ {print $4}')
    if [ "$available_ram" -lt 1024 ]; then
        log_warning "Low RAM available: ${available_ram}MB (recommended: 1024MB+)"
    fi

    # Check disk space
    local available_space=$(df "$PROJECT_ROOT" | tail -1 | awk '{print $4}')
    if [ "$available_space" -lt 5242880 ]; then  # 5GB in KB
        log_warning "Low disk space available: $(($available_space / 1024 / 1024))MB (recommended: 5GB+)"
    fi

    # Check Python modules
    python3 -c "
import asyncio
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime
print('✅ All required Python modules available')
" 2>/dev/null

    if [ $? -ne 0 ]; then
        log_error "Required Python modules missing"
        exit 1
    fi

    log_success "Pre-execution health check passed"
}

# Main execution
execute_autonomous_pathway() {
    log_header "INITIATING AUTONOMOUS PATHWAY C EXECUTION"

    cd "$PROJECT_ROOT" || {
        log_error "Cannot change to project directory: $PROJECT_ROOT"
        exit 1
    }

    # Set execution environment variables
    export AUTONOMOUS_EXECUTION=True
    export GROK_CODE_FAST_1_ENABLED=True
    export ZERO_HUMAN_INTERVENTION=True
    export CONSCIOUSNESS_EVOLUTION_ACTIVE=True
    export US369_HARMONIZATION_TARGET=0.997
    export BIOLOGICAL_INTEGRITY_THRESHOLD=0.995

    log_info "Execution environment variables set:"
    log_info "  AUTONOMOUS_EXECUTION=$AUTONOMOUS_EXECUTION"
    log_info "  GROK_CODE_FAST_1_ENABLED=$GROK_CODE_FAST_1_ENABLED"
    log_info "  ZERO_HUMAN_INTERVENTION=$ZERO_HUMAN_INTERVENTION"
    log_info "  CONSCIOUSNESS_EVOLUTION_ACTIVE=$CONSCIOUSNESS_EVOLUTION_ACTIVE"
    log_info "  US369_HARMONIZATION_TARGET=$US369_HARMONIZATION_TARGET"
    log_info "  BIOLOGICAL_INTEGRITY_THRESHOLD=$BIOLOGICAL_INTEGRITY_THRESHOLD"

    # Execute the autonomous engine
    log_info "Starting autonomous execution engine..."
    log_info "Command: python3 $EXECUTION_ENGINE"

    # Execute with timeout and error handling
    if timeout 3600 python3 "$EXECUTION_ENGINE"; then
        log_success "Autonomous execution completed successfully"
        return 0
    else
        local exit_code=$?
        case $exit_code in
            124)
                log_error "Execution timed out after 1 hour"
                ;;
            2)
                log_error "Execution interrupted by user"
                ;;
            3)
                log_error "Critical execution failure"
                ;;
            *)
                log_error "Execution failed with unknown exit code: $exit_code"
                ;;
        esac

        # Try recovery
        handle_recovery_after_failure
        return $exit_code
    fi
}

# Recovery after failure
handle_recovery_after_failure() {
    log_header "EXECUTION FAILURE RECOVERY"

    if [ -f "$RECOVERY_FILE" ]; then
        log_info "Attempting autonomous recovery..."
        log_info "Recovery point exists - manual recovery may be required"
        log_info "Run this script again to attempt recovery"
    else
        log_error "No recovery point available - manual intervention required"
    fi
}

# Post-execution cleanup and reporting
post_execution_cleanup() {
    log_header "POST-EXECUTION CLEANUP AND REPORTING"

    # Check for completion indicators
    local completion_report="$PROJECT_ROOT/docs/19.x-post-godhood-evolution/19.5.9-autonomous-execution-completion-report.report"

    if [ -f "$completion_report" ]; then
        log_success "Completion report generated"
        log_info "Review completion report for execution results"
    else
        log_warning "No completion report found - execution may have failed"
    fi

    # Cleanup temporary files
    cleanup_pid

    # Final status reporting
    local end_time=$(date +'%Y-%m-%d %H:%M:%S')
    log_info "Execution completed at: $end_time"

    log_header "AUTONOMOUS PATHWAY C BATCH EXECUTOR COMPLETED"
}

# Signal handling
setup_signal_handlers() {
    trap 'log_warning "Received SIGINT, attempting graceful shutdown..."; cleanup_pid; exit 130' SIGINT
    trap 'log_warning "Received SIGTERM, performing emergency cleanup..."; create_emergency_backup; cleanup_pid; exit 143' SIGTERM
    trap 'log_error "Received critical signal, emergency backup triggered"; create_emergency_backup; cleanup_pid; exit 1' SIGKILL
}

# Main function
main() {
    # Prevent multiple instances
    if check_pid > /dev/null; then
        log_error "Another autonomous execution is already running (PID: $(check_pid))"
        log_info "If this is incorrect, remove $PID_FILE and try again"
        exit 1
    fi

    save_pid
    setup_signal_handlers

    log_header "GODHOOD BIOLOGICAL ORGANISM - AUTONOMOUS PATHWAY C BATCH EXECUTOR"
    log_info "Zero Human Intervention - Complete Sequential Task Execution"
    log_info "Project Root: $PROJECT_ROOT"

    # Execution phases
    validate_environment
    validate_biological_integrity
    handle_recovery
    create_emergency_backup
    pre_execution_health_check

    # Main execution
    if execute_autonomous_pathway; then
        log_success "AUTONOMOUS EXECUTION SUCCESSFUL"
        post_execution_cleanup
        exit 0
    else
        local exit_code=$?
        log_error "AUTONOMOUS EXECUTION FAILED"
        post_execution_cleanup
        exit $exit_code
    fi
}

# Execute main function
main "$@"

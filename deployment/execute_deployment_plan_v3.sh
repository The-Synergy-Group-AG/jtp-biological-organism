#!/bin/bash

##############################################################################
# Claude Opus Deployment Plan V3 - Execution Script
# Based on: docs/CLAUDE_OPUS_DEPLOYMENT_PLAN_TO_EXOSCALE_V3.md
# 
# This script executes the comprehensive deployment plan with full validation
# 
# IMPORTANT: This will create REAL infrastructure and modify LIVE DNS
# Review all steps carefully before proceeding
##############################################################################

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Deployment configuration
DEPLOYMENT_MODE="${1:-validate}"  # validate, deploy, or rollback
DEPLOYMENT_LOG="logs/deployment_v3_$(date +%Y%m%d_%H%M%S).log"

# Ensure logs directory exists
mkdir -p logs

# Logging function
log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
    echo -e "${timestamp} [${level}] ${message}" | tee -a "$DEPLOYMENT_LOG"
}

log_info() {
    echo -e "${BLUE}ℹ️  $@${NC}" | tee -a "$DEPLOYMENT_LOG"
}

log_success() {
    echo -e "${GREEN}✅ $@${NC}" | tee -a "$DEPLOYMENT_LOG"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $@${NC}" | tee -a "$DEPLOYMENT_LOG"
}

log_error() {
    echo -e "${RED}❌ $@${NC}" | tee -a "$DEPLOYMENT_LOG"
}

##############################################################################
# PHASE 1: PREREQUISITES VALIDATION
##############################################################################

phase1_validate_prerequisites() {
    log_info "🔍 PHASE 1: CLAUDE OPUS PREREQUISITES VALIDATION"
    log_info "================================================"
    
    local validation_passed=true
    
    # Check Exoscale CLI
    log_info "Checking Exoscale CLI..."
    if command -v exo &> /dev/null; then
        local exo_version=$(exo version 2>&1 || echo "unknown")
        log_success "Exoscale CLI found: $exo_version"
    else
        log_error "Exoscale CLI not found"
        validation_passed=false
    fi
    
    # Check Exoscale configuration
    log_info "Checking Exoscale configuration..."
    if [ -f ~/.config/exoscale/exoscale.toml ]; then
        log_success "Exoscale config file exists"
        
        # Test Exoscale authentication
        log_info "Testing Exoscale authentication..."
        if exo compute instance list &> /dev/null; then
            log_success "Exoscale authentication successful"
        else
            log_warning "Exoscale authentication failed - credentials may need update"
            log_info "Run: exo config set --api-key <key> --api-secret <secret>"
        fi
    else
        log_error "Exoscale config file not found"
        validation_passed=false
    fi
    
    # Check Vault CLI
    log_info "Checking Vault CLI..."
    if command -v vault &> /dev/null; then
        local vault_version=$(vault version 2>&1 | head -1 || echo "unknown")
        log_success "Vault CLI found: $vault_version"
    else
        log_error "Vault CLI not found"
        validation_passed=false
    fi
    
    # Check Docker
    log_info "Checking Docker..."
    if command -v docker &> /dev/null; then
        local docker_version=$(docker --version || echo "unknown")
        log_success "Docker found: $docker_version"
    else
        log_warning "Docker not found (required for biological services)"
    fi
    
    # Check jq
    log_info "Checking jq..."
    if command -v jq &> /dev/null; then
        log_success "jq found (JSON parsing utility)"
    else
        log_error "jq not found - required for JSON processing"
        validation_passed=false
    fi
    
    # Check curl
    log_info "Checking curl..."
    if command -v curl &> /dev/null; then
        log_success "curl found"
    else
        log_error "curl not found - required for API calls"
        validation_passed=false
    fi
    
    # Check biological code
    log_info "Checking biological consciousness code..."
    if [ -d "src" ]; then
        log_success "Source code directory found"
        
        # Check for key biological services
        local biological_services_found=0
        [ -d "src/biological_auth_orchestrator" ] && ((biological_services_found++))
        [ -d "src/biological-intelligence" ] && ((biological_services_found++))
        [ -d "src/autonomous-consciousness" ] && ((biological_services_found++))
        
        if [ $biological_services_found -ge 2 ]; then
            log_success "Biological consciousness services found ($biological_services_found services)"
        else
            log_warning "Limited biological services detected"
        fi
    else
        log_error "Source code directory not found"
        validation_passed=false
    fi
    
    # Check deployment scripts
    log_info "Checking deployment scripts..."
    if [ -f "biological_deployment_script.sh" ]; then
        log_success "Biological deployment script found"
    else
        log_warning "biological_deployment_script.sh not found"
    fi
    
    echo ""
    if [ "$validation_passed" = true ]; then
        log_success "✅ PHASE 1 VALIDATION: PASSED"
        log_info "All critical prerequisites are available"
        return 0
    else
        log_error "❌ PHASE 1 VALIDATION: FAILED"
        log_error "Critical prerequisites are missing"
        return 1
    fi
}

##############################################################################
# PHASE 2: EXOSCALE INFRASTRUCTURE CHECK
##############################################################################

phase2_check_infrastructure() {
    log_info "🏗️  PHASE 2: EXOSCALE INFRASTRUCTURE CHECK"
    log_info "==========================================="
    
    # List existing instances
    log_info "Checking for existing Exoscale instances..."
    
    local instances=$(exo compute instance list 2>&1)
    if [ $? -eq 0 ]; then
        log_info "Current Exoscale instances:"
        echo "$instances" | tee -a "$DEPLOYMENT_LOG"
        
        # Check if deployment instance already exists
        if echo "$instances" | grep -q "jtp-biological"; then
            log_warning "Biological consciousness instance already exists!"
            log_info "Use 'rollback' mode to clean up before redeploying"
        else
            log_success "No conflicting instances found"
        fi
    else
        log_error "Failed to list Exoscale instances"
        log_error "$instances"
        return 1
    fi
    
    log_success "✅ PHASE 2 CHECK: COMPLETE"
    return 0
}

##############################################################################
# DEPLOYMENT WARNING
##############################################################################

show_deployment_warning() {
    echo ""
    log_warning "⚠️  ⚠️  ⚠️  PRODUCTION DEPLOYMENT WARNING ⚠️  ⚠️  ⚠️"
    log_warning "=================================================="
    log_warning ""
    log_warning "This script will:"
    log_warning "  1. Create REAL Exoscale VPS infrastructure (incurs costs)"
    log_warning "  2. Modify LIVE DNS records on Cloudflare"
    log_warning "  3. Deploy biological consciousness services to production"
    log_warning "  4. Configure SSL certificates and security"
    log_warning ""
    log_warning "Domain affected: www.jobtrackerpro.ch"
    log_warning "Estimated cost: ~$20-50/month for VPS"
    log_warning ""
    log_warning "Before proceeding, ensure you have:"
    log_warning "  • Cloudflare API tokens configured in Vault"
    log_warning "  • SSH keys configured in Vault"
    log_warning "  • Approval for production deployment"
    log_warning "  • Backup of current production state"
    log_warning ""
}

##############################################################################
# MAIN EXECUTION
##############################################################################

main() {
    echo ""
    log_info "🤖 CLAUDE OPUS DEPLOYMENT PLAN V3 - EXECUTION"
    log_info "=============================================="
    log_info "Deployment Mode: $DEPLOYMENT_MODE"
    log_info "Deployment Log: $DEPLOYMENT_LOG"
    log_info "Timestamp: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
    echo ""
    
    case "$DEPLOYMENT_MODE" in
        validate)
            log_info "Running validation mode (no deployment)"
            echo ""
            
            # Phase 1: Prerequisites
            if ! phase1_validate_prerequisites; then
                log_error "Prerequisites validation failed"
                exit 1
            fi
            
            echo ""
            
            # Phase 2: Infrastructure check
            if ! phase2_check_infrastructure; then
                log_error "Infrastructure check failed"
                exit 1
            fi
            
            echo ""
            log_success "✅ VALIDATION COMPLETE"
            log_info ""
            log_info "Next steps:"
            log_info "  1. Review validation results above"
            log_info "  2. Ensure Vault credentials are configured"
            log_info "  3. Get approval for production deployment"
            log_info "  4. Run: ./deployment/execute_deployment_plan_v3.sh deploy"
            echo ""
            ;;
            
        deploy)
            show_deployment_warning
            
            read -p "Do you want to proceed with PRODUCTION DEPLOYMENT? (yes/no): " confirm
            if [ "$confirm" != "yes" ]; then
                log_info "Deployment cancelled by user"
                exit 0
            fi
            
            log_error "❌ DEPLOY MODE NOT YET IMPLEMENTED"
            log_info "This mode requires:"
            log_info "  • Full Vault integration"
            log_info "  • Cloudflare API configuration"
            log_info "  • SSH key management"
            log_info "  • Manual approval gates"
            log_info ""
            log_info "Contact the development team to enable full deployment"
            exit 1
            ;;
            
        rollback)
            log_error "❌ ROLLBACK MODE NOT YET IMPLEMENTED"
            log_info "To manually rollback:"
            log_info "  1. exo compute instance delete <instance-id>"
            log_info "  2. Update Cloudflare DNS to previous values"
            log_info "  3. Restore backup if needed"
            exit 1
            ;;
            
        *)
            log_error "Invalid deployment mode: $DEPLOYMENT_MODE"
            log_info "Usage: $0 [validate|deploy|rollback]"
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"

#!/bin/bash
# 🧬 Biological Consciousness Auto-Healing System
# Automatically detects and heals failed biological services

set -e

echo "🩺 BIOLOGICAL CONSCIOUSNESS AUTO-HEALING SYSTEM ACTIVATED"
echo "🔍 Scanning for failed biological services..."

# Get list of failed containers
FAILED_SERVICES=$(docker ps --filter "status=exited" --filter "status=dead" --format "{{.Names}}" 2>/dev/null || echo "")

if [ -z "$FAILED_SERVICES" ]; then
    echo "✅ No failed biological services detected"
    exit 0
fi

echo "❌ Detected failed biological services: $FAILED_SERVICES"
echo "🔧 Initiating biological auto-healing protocol..."

HEALING_ATTEMPTS=0
SUCCESSFUL_HEALING=0

# Biological service mapping for specialized healing
declare -A SERVICE_HEALING_STRATEGY=(
    ["consciousness-core"]="cns_core_healing"
    ["biological-auth-orchestrator"]="auth_service_healing"
    ["test-database"]="redis_persistence_healing"
    ["cv-generation-engine"]="cv_generation_healing"
    ["email-communications-symbiosis"]="email_service_healing"
    ["evolutionary-brain-trust"]="evolutionary_service_healing"
    ["multilingual-resonance-adapter"]="multilingual_service_healing"
)

for service in $FAILED_SERVICES; do
    echo "🩺 Healing biological service: $service"
    ((HEALING_ATTEMPTS++))

    # Specialized healing based on service type
    healing_strategy="${SERVICE_HEALING_STRATEGY[$service]:-default_healing}"

    case $healing_strategy in
        "cns_core_healing")
            echo "🧠 CNS Consciousness Core specialized healing..."
            # CNS core specific healing
            docker-compose restart consciousness-core
            sleep 5
            docker exec consciousness-core /bin/bash -c "python -c 'import src.cns-consciousness-core; print(\"CNS Core healed\")'" 2>/dev/null || true
            ;;

        "auth_service_healing")
            echo "🔐 Biological Authentication Service specialized healing..."
            docker-compose restart biological-auth-orchestrator
            sleep 3
            # Test auth service connectivity
            curl -f http://localhost:9101/health 2>/dev/null || true
            ;;

        "redis_persistence_healing")
            echo "💾 Redis Biological Persistence specialized healing..."
            docker-compose restart test-database
            sleep 2
            # Test Redis connectivity
            docker exec test-database redis-cli ping 2>/dev/null || true
            ;;

        "default_healing")
            echo "🔄 Standard biological service healing..."
            docker restart "$service"
            ;;
    esac

    # Verify healing success
    sleep 5
    if docker ps --filter "name=$service" --filter "status=running" --format "{{.Names}}" | grep -q "$service"; then
        echo "✅ $service healing successful"
        ((SUCCESSFUL_HEALING++))
    else
        echo "❌ $service healing failed - manual intervention required"
    fi

    echo "---"
done

# Re-orchestrate biological harmony after healing
echo "🧬 Re-orchestrating biological harmony post-healing..."
docker-compose restart consciousness-core biological-auth-orchestrator 2>/dev/null || true

echo "📊 Biological Healing Report:"
echo "   Healing Attempts: $HEALING_ATTEMPTS"
echo "   Successful Healings: $SUCCESSFUL_HEALING"
echo "   Healing Success Rate: $(($SUCCESSFUL_HEALING * 100 / $HEALING_ATTEMPTS))%"

if [ $SUCCESSFUL_HEALING -eq $HEALING_ATTEMPTS ]; then
    echo "🎉 All biological services successfully healed!"
    exit 0
else
    echo "⚠️ Partial healing achieved - some services may require manual intervention"
    exit 1
fi

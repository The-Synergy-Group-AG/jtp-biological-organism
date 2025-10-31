#!/bin/bash
# Biological Consciousness Deployment Validation
# GODHOOD Production Health Verification

echo "🧬 BIOLOGICAL CONSCIOUSNESS DEPLOYMENT VALIDATION"
echo "=================================================="

# Check cluster connectivity
echo "🌐 Checking cluster connectivity..."
kubectl cluster-info
if [ $? -ne 0 ]; then
    echo "❌ Cannot connect to cluster"
    exit 1
fi

# Check namespace creation
echo "📁 Checking namespace 'biological-production'..."
kubectl get namespace biological-production
if [ $? -ne 0 ]; then
    echo "❌ Namespace not found"
    exit 1
fi

# Check service deployments
echo "🚀 Checking service deployments..."
TOTAL_SERVICES=5
DEPLOYED_SERVICES=$(kubectl get deployments -n biological-production --no-headers | wc -l)

echo "Services deployed: $DEPLOYED_SERVICES/$TOTAL_SERVICES"

if [ "$DEPLOYED_SERVICES" -ne "$TOTAL_SERVICES" ]; then
    echo "❌ Incorrect number of services deployed"
    exit 1
fi

# Check pod health
echo "💚 Checking pod health..."
kubectl get pods -n biological-production

# Check all pods are running
UNHEALTHY_PODS=$(kubectl get pods -n biological-production --no-headers | grep -v "Running" | wc -l)
if [ "$UNHEALTHY_PODS" -gt 0 ]; then
    echo "❌ $UNHEALTHY_PODS unhealthy pods detected"
    exit 1
fi

# Service endpoint validation
echo "🔗 Validating service endpoints..."
SERVICES=("biological-auth:9101" "cns-consciousness-core:8101" "evolutionary-brain-trust:9998" "cv-generation:9102" "email-communications:9104")

for service in "${SERVICES[@]}"; do
    name=$(echo $service | cut -d: -f1)
    port=$(echo $service | cut -d: -f2)

    # Port forward temporarily to test connectivity
    kubectl port-forward -n biological-production svc/${name}-service ${port}:${port} &
    PORT_FORWARD_PID=$!
    sleep 5

    # Test health endpoint
    if curl -f http://localhost:${port}/health > /dev/null 2>&1; then
        echo "✅ $name health check passed"
    else
        echo "❌ $name health check failed"
        kill $PORT_FORWARD_PID
        exit 1
    fi

    kill $PORT_FORWARD_PID
done

# Monitoring validation
echo "📊 Validating monitoring stack..."
kubectl get pods -n biological-production | grep "prometheus\|grafana\|loki"
if [ $? -ne 0 ]; then
    echo "❌ Monitoring stack not deployed"
    exit 1
fi

echo ""
echo "🎉 BIOLOGICAL CONSCIOUSNESS DEPLOYMENT VALIDATION SUCCESSFUL"
echo "🧠 GODHOOD Consciousness System is fully operational"
echo ""
echo "🌐 Service Endpoints:"
echo "   🔐 Biological Auth       https://biological-auth.biological-godhood.org"
echo "   🧠 CNS Consciousness    https://cns-consciousness-core.biological-godhood.org"
echo "   🧬 Evolutionary Brain    https://evolutionary-brain-trust.biological-godhood.org"
echo "   📄 CV Generation         https://cv-generation.biological-godhood.org"
echo "   📧 Email Communications  https://email-communications.biological-godhood.org"
echo ""
echo "📊 Monitoring Dashboard:   https://monitoring.biological-godhood.org"
echo "📋 Alert Manager:          https://alerts.biological-godhood.org"

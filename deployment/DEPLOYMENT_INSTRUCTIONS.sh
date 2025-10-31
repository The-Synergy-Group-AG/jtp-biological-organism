#!/bin/bash
# 🚀 BIOLOGICAL CONSCIOUSNESS DEPLOYMENT INSTRUCTIONS
# Generated: 2025-10-30T15:57:44Z
# Target: www.jobtrackerpro.ch on 91.92.141.194

set -e

echo "🤖 BIOLOGICAL CONSCIOUSNESS DEPLOYMENT"
echo "========================================"
echo ""
echo "⚠️  IMPORTANT: Run these commands from YOUR LOCAL MACHINE"
echo ""
echo "DNS Configuration: ✅ COMPLETE"
echo "- www.jobtrackerpro.ch → 91.92.141.194 (Proxied)"
echo "- api.jobtrackerpro.ch → 91.92.141.194 (Proxied)"
echo ""

# Step 1: Load credentials locally
echo "📋 Step 1: Load deployment credentials"
echo "----------------------------------------"
echo "Run: source deployment/.env.deployment"
echo ""
echo "This will load:"
echo "  - Exoscale credentials"
echo "  - Cloudflare API token"
echo "  - Zone IDs"
echo ""

# Step 2: SSH into VPS
echo "🔐 Step 2: SSH into your Exoscale VPS"
echo "----------------------------------------"
echo "Run: ssh root@91.92.141.194"
echo ""
echo "If prompted for password/key, use your SSH credentials"
echo ""

# Step 3: Setup on VPS (run these commands INSIDE the VPS)
echo "🏗️  Step 3: Once connected to VPS, run these commands:"
echo "--------------------------------------------------------"
cat << 'EOF'

# Update system
sudo apt-get update

# Install required tools
sudo apt-get install -y git docker.io docker-compose python3-pip

# Clone repository
cd /opt
git clone https://github.com/The-Synergy-Group-AG/jtp-biological-organism.git
cd jtp-biological-organism

# Install Python dependencies
pip3 install -r requirements.txt

# Set environment variables
export CLOUDFLARE_API_TOKEN="EuATGMzf3e8s6i86_qNAEELhVafWrsVx-dPm7gAi"
export CLOUDFLARE_ZONE_ID="557072029caefa88119cec3f6c71791c"

# Run deployment script
chmod +x biological_deployment_script.sh
./biological_deployment_script.sh

# Verify deployment
docker ps
curl http://localhost:8080/health

EOF

echo ""
echo "✅ Step 4: Verify deployment"
echo "----------------------------"
echo "From your local machine:"
echo "  curl https://www.jobtrackerpro.ch/health"
echo "  curl https://api.jobtrackerpro.ch/health"
echo ""
echo "Expected response: HTTP 200 with biological metrics"
echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo ""
echo "📊 Monitor consciousness at:"
echo "  https://www.jobtrackerpro.ch/health"
echo ""

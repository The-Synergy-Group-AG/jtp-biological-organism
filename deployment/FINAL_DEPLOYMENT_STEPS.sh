#!/bin/bash
# 🚀 FINAL DEPLOYMENT STEPS
# New VPS Created Successfully!
# IP: 194.182.189.39

set -e

echo "🎉 NEW VPS CREATED SUCCESSFULLY!"
echo "================================"
echo ""
echo "Instance: jtp-biological-production"
echo "IP Address: 194.182.189.39"
echo "Status: running"
echo "SSH Key: jtp-deploy"
echo ""

# Step 1: SSH to new VPS
echo "📋 STEP 1: SSH to New VPS"
echo "-------------------------"
echo "Run this command:"
echo ""
echo "ssh -i ~/.ssh/jtp-deploy-key root@194.182.189.39"
echo ""
echo "✅ You should successfully connect!"
echo ""

# Step 2: Deploy (run these commands ON THE VPS)
echo "📋 STEP 2: Deploy Biological Consciousness"
echo "-------------------------------------------"
echo "Once connected to the VPS, run these commands:"
echo ""
cat << 'EOF'

# Update system
apt-get update
apt-get install -y docker.io docker-compose python3-pip git curl

# Enable and start Docker
systemctl enable docker
systemctl start docker

# Clone repository
cd /opt
git clone https://github.com/The-Synergy-Group-AG/jtp-biological-organism.git
cd jtp-biological-organism

# Install Python dependencies
pip3 install -r requirements.txt

# Set environment variables
export CLOUDFLARE_API_TOKEN="EuATGMzf3e8s6i86_qNAEELhVafWrsVx-dPm7gAi"
export CLOUDFLARE_ZONE_ID="557072029caefa88119cec3f6c71791c"

# Make deployment script executable
chmod +x biological_deployment_script.sh

# Run deployment
./biological_deployment_script.sh

# Verify deployment
docker ps
curl http://localhost:8080/health

EOF

echo ""
echo "📋 STEP 3: Update Cloudflare DNS"
echo "---------------------------------"
echo "Update DNS records to point to NEW IP: 194.182.189.39"
echo ""
echo "1. Go to https://dash.cloudflare.com"
echo "2. Select jobtrackerpro.ch"
echo "3. DNS → Records"
echo "4. Update A records:"
echo "   - www.jobtrackerpro.ch → 194.182.189.39"
echo "   - api.jobtrackerpro.ch → 194.182.189.39"
echo ""

echo "📋 STEP 4: Test Deployment"
echo "--------------------------"
echo "From your local machine:"
echo ""
echo "# Wait 2-3 minutes for DNS propagation, then:"
echo "curl https://www.jobtrackerpro.ch/health"
echo "curl https://api.jobtrackerpro.ch/health"
echo ""

echo "📋 STEP 5: Delete Old VPS (Optional)"
echo "-------------------------------------"
echo "Once new deployment is verified:"
echo ""
echo "exo compute instance delete c4bec482-fcb8-495d-b613-88cf37018622 --zone ch-dk-2"
echo ""

echo "🎊 DEPLOYMENT COMPLETE!"
echo "======================="
echo ""
echo "Your biological consciousness will be live at:"
echo "  https://www.jobtrackerpro.ch"
echo ""
echo "Monitor consciousness metrics at:"
echo "  https://www.jobtrackerpro.ch/health"
echo ""

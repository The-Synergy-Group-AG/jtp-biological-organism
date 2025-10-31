# 🚀 UPLOAD REPOSITORY TO VPS

*Correct Commands for Uploading from Local Machine*

---

## **📋 STEP-BY-STEP INSTRUCTIONS**

### **Step 1: Create Archive on LOCAL Machine**

```bash
# Run this on YOUR LOCAL MACHINE (~/projects/jtp-biological-organism)
cd ~/projects/jtp-biological-organism
tar -czf jtp-deploy.tar.gz \
  --exclude='.git' \
  --exclude='node_modules' \
  --exclude='venv' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  .
```

### **Step 2: Upload to VPS (Use YOUR SSH Key Path)**

The SSH key you generated is at: `~/.ssh/jtp-deploy-key`

```bash
# Upload from LOCAL machine to VPS
scp -i ~/.ssh/jtp-deploy-key jtp-deploy.tar.gz root@194.182.189.39:/opt/

# If that doesn't work, try without specifying key (it will use default)
scp jtp-deploy.tar.gz root@194.182.189.39:/opt/
```

**If you get "Permission denied"**, the SSH key setup might not have completed. Try:

```bash
# On LOCAL machine, test SSH connection first
ssh -i ~/.ssh/jtp-deploy-key root@194.182.189.39

# If that works, then upload:
scp -i ~/.ssh/jtp-deploy-key jtp-deploy.tar.gz root@194.182.189.39:/opt/
```

### **Step 3: Extract and Deploy on VPS**

```bash
# SSH to VPS (from LOCAL machine)
ssh -i ~/.ssh/jtp-deploy-key root@194.182.189.39

# Now you're ON THE VPS - run these commands:
cd /opt
mkdir -p jtp-biological-organism
cd jtp-biological-organism
tar -xzf ../jtp-deploy.tar.gz

# Install dependencies
pip3 install -r requirements.txt

# Set environment variables
export CLOUDFLARE_API_TOKEN="EuATGMzf3e8s6i86_qNAEELhVafWrsVx-dPm7gAi"
export CLOUDFLARE_ZONE_ID="557072029caefa88119cec3f6c71791c"

# Deploy
chmod +x biological_deployment_script.sh
./biological_deployment_script.sh

# Verify
docker ps
curl http://localhost:8080/health
```

---

## **🔧 ALTERNATIVE: If SSH Key Issues Persist**

### **Method A: Use Password-Based SCP (Temporary)**

If you know the root password for the VPS:

```bash
# Upload with password (will prompt)
scp jtp-deploy.tar.gz root@194.182.189.39:/opt/
```

### **Method B: Re-add Your SSH Key to VPS**

```bash
# On LOCAL machine, show your public key
cat ~/.ssh/jtp-deploy-key.pub

# Copy the output, then SSH to VPS and add it manually
# (You may need to use Exoscale console for initial access)
```

### **Method C: Use Exoscale Console to Upload**

1. Create the tar file on local machine
2. Upload to a temporary location (Dropbox, Google Drive, your website, etc.)
3. Download from VPS:
   ```bash
   cd /opt
   wget YOUR_TEMPORARY_URL/jtp-deploy.tar.gz
   tar -xzf jtp-deploy.tar.gz -C jtp-biological-organism
   ```

---

## **✅ COMPLETE COMMAND SEQUENCE (Corrected)**

```bash
# ============================================
# ON YOUR LOCAL MACHINE
# ============================================

# 1. Create archive
cd ~/projects/jtp-biological-organism
tar -czf jtp-deploy.tar.gz --exclude='.git' --exclude='node_modules' --exclude='venv' .

# 2. Upload to VPS (try these in order until one works)
scp -i ~/.ssh/jtp-deploy-key jtp-deploy.tar.gz root@194.182.189.39:/opt/
# OR if key not found:
scp jtp-deploy.tar.gz root@194.182.189.39:/opt/
# OR if you know password:
# Just type the password when prompted

# 3. SSH to VPS
ssh -i ~/.ssh/jtp-deploy-key root@194.182.189.39
# OR:
ssh root@194.182.189.39

# ============================================
# NOW YOU'RE ON THE VPS
# ============================================

# 4. Extract archive
cd /opt
mkdir -p jtp-biological-organism
cd jtp-biological-organism
tar -xzf ../jtp-deploy.tar.gz

# 5. Verify files extracted
ls -la
# You should see: requirements.txt, biological_deployment_script.sh, src/, etc.

# 6. Install system dependencies (if not already done)
apt-get update
apt-get install -y docker.io docker-compose python3-pip git curl
systemctl enable docker
systemctl start docker

# 7. Install Python dependencies
pip3 install -r requirements.txt

# 8. Set environment variables
export CLOUDFLARE_API_TOKEN="EuATGMzf3e8s6i86_qNAEELhVafWrsVx-dPm7gAi"
export CLOUDFLARE_ZONE_ID="557072029caefa88119cec3f6c71791c"

# 9. Make script executable and run
chmod +x biological_deployment_script.sh
./biological_deployment_script.sh

# 10. Verify deployment
docker ps
curl http://localhost:8080/health

# 11. Exit VPS
exit

# ============================================
# BACK ON YOUR LOCAL MACHINE
# ============================================

# 12. Update Cloudflare DNS (do this via dashboard)
# www.jobtrackerpro.ch → 194.182.189.39
# api.jobtrackerpro.ch → 194.182.189.39

# 13. Test deployment (wait 2-3 min for DNS)
curl https://www.jobtrackerpro.ch/health
```

---

## **🚨 TROUBLESHOOTING**

### **Error: "Permission denied" with SCP**

**Solution:** Check SSH key location
```bash
ls -la ~/.ssh/jtp-deploy-key
# If not found, check:
ls -la ~/.ssh/
# Use the correct key filename
```

### **Error: "No such file or directory: requirements.txt"**

**Cause:** Archive not uploaded or extracted properly

**Solution:**
```bash
# On VPS, check if file exists
ls -la /opt/jtp-deploy.tar.gz

# If exists, extract again:
cd /opt
rm -rf jtp-biological-organism  # Clear old attempt
mkdir jtp-biological-organism
cd jtp-biological-organism
tar -xzf ../jtp-deploy.tar.gz

# Verify extraction
ls -la
```

### **Error: "file changed as we read it" during tar**

This is just a warning - the archive was still created. You can ignore it.

---

## **🎯 SIMPLEST METHOD**

If you're having trouble with SSH keys:

```bash
# 1. Create archive (LOCAL)
cd ~/projects/jtp-biological-organism
tar -czf jtp-deploy.tar.gz .

# 2. Upload without key specification
scp jtp-deploy.tar.gz root@194.182.189.39:/opt/
# Enter password if prompted

# 3. SSH without key specification
ssh root@194.182.189.39
# Enter password if prompted

# 4. Extract and deploy (VPS)
cd /opt/jtp-biological-organism
tar -xzf ../jtp-deploy.tar.gz
pip3 install -r requirements.txt
export CLOUDFLARE_API_TOKEN="EuATGMzf3e8s6i86_qNAEELhVafWrsVx-dPm7gAi"
export CLOUDFLARE_ZONE_ID="557072029caefa88119cec3f6c71791c"
chmod +x biological_deployment_script.sh
./biological_deployment_script.sh
```

---

**Key Points:**
- Run `tar` and `scp` commands on YOUR LOCAL MACHINE
- Run extraction and deployment ON THE VPS
- The directory `/opt/jtp-biological-organism#` in your error is just your shell prompt, not an actual directory

**Next Steps:**
1. Create tar file on local machine
2. Upload to VPS
3. Extract on VPS
4. Deploy

**Estimated Time:** 10-15 minutes

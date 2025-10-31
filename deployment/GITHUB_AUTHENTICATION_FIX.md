# 🔐 GITHUB AUTHENTICATION FIX

*Resolving Git Clone Authentication Error*

---

## **🚨 PROBLEM**

```bash
git clone https://github.com/The-Synergy-Group-AG/jtp-biological-organism.git
# Error: Authentication failed for 'https://github.com/...'
```

The repository is **private** and requires authentication.

---

## **✅ SOLUTION OPTIONS**

### **Option 1: Use SSH-Based Cloning (RECOMMENDED)**

**On your VPS, run these commands:**

```bash
# 1. Generate SSH key on VPS
ssh-keygen -t ed25519 -C "deployment@jtp-biological" -f ~/.ssh/github_deploy_key -N ""

# 2. Display the public key
cat ~/.ssh/github_deploy_key.pub

# Copy the entire output (starts with ssh-ed25519)
```

**Add Deploy Key to GitHub:**

1. Go to: https://github.com/The-Synergy-Group-AG/jtp-biological-organism/settings/keys
2. Click "Add deploy key"
3. Title: `jtp-production-vps`
4. Key: Paste the public key from above
5. ✅ Check "Allow write access" (if needed)
6. Click "Add key"

**Clone with SSH:**

```bash
# On VPS, configure git to use the key
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github_deploy_key

# Test GitHub connection
ssh -T git@github.com

# Clone repository using SSH
cd /opt
git clone git@github.com:The-Synergy-Group-AG/jtp-biological-organism.git

# Success!
cd jtp-biological-organism
```

---

### **Option 2: Use Personal Access Token**

**Create GitHub Token:**

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: `jtp-deployment`
4. Select scopes: ✅ `repo` (full control)
5. Click "Generate token"
6. **Copy the token** (shown only once!)

**Clone with Token:**

```bash
# On VPS, clone using token
cd /opt

# Replace YOUR_TOKEN with your actual token
git clone https://YOUR_TOKEN@github.com/The-Synergy-Group-AG/jtp-biological-organism.git

# Or set up credential helper
git config --global credential.helper store
git clone https://github.com/The-Synergy-Group-AG/jtp-biological-organism.git
# When prompted:
# Username: YOUR_GITHUB_USERNAME
# Password: YOUR_PERSONAL_ACCESS_TOKEN
```

---

### **Option 3: Make Repository Public (Temporary)**

**If acceptable for deployment:**

1. Go to: https://github.com/The-Synergy-Group-AG/jtp-biological-organism/settings
2. Scroll to "Danger Zone"
3. Click "Change visibility"
4. Select "Make public"
5. Clone without authentication:
   ```bash
   cd /opt
   git clone https://github.com/The-Synergy-Group-AG/jtp-biological-organism.git
   ```
6. After deployment, make it private again

---

## **📋 COMPLETE DEPLOYMENT SEQUENCE (Updated)**

**Using SSH Method (Recommended):**

```bash
# === ON YOUR VPS (194.182.189.39) ===

# 1. Generate GitHub deploy key
ssh-keygen -t ed25519 -C "deployment@jtp" -f ~/.ssh/github_deploy_key -N ""
cat ~/.ssh/github_deploy_key.pub
# Copy output, add to GitHub as deploy key

# 2. Configure SSH
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github_deploy_key
ssh -T git@github.com  # Test connection

# 3. Install dependencies
apt-get update
apt-get install -y docker.io docker-compose python3-pip git curl

systemctl enable docker
systemctl start docker

# 4. Clone repository with SSH
cd /opt
git clone git@github.com:The-Synergy-Group-AG/jtp-biological-organism.git
cd jtp-biological-organism

# 5. Install Python dependencies
pip3 install -r requirements.txt

# 6. Set environment variables
export CLOUDFLARE_API_TOKEN="EuATGMzf3e8s6i86_qNAEELhVafWrsVx-dPm7gAi"
export CLOUDFLARE_ZONE_ID="557072029caefa88119cec3f6c71791c"

# 7. Deploy
chmod +x biological_deployment_script.sh
./biological_deployment_script.sh

# 8. Verify
docker ps
curl http://localhost:8080/health
```

---

## **🔐 SECURITY BEST PRACTICES**

### **For Deploy Keys:**
- ✅ Use read-only access if possible
- ✅ Rotate keys regularly
- ✅ Use different keys for different servers
- ✅ Revoke keys when no longer needed

### **For Personal Access Tokens:**
- ✅ Use fine-grained tokens with minimal scope
- ✅ Set expiration dates
- ✅ Never commit tokens to code
- ✅ Rotate tokens regularly

---

## **⚡ QUICK FIX (If You Want to Continue Now)**

**Option: Use Your Local Clone**

If you have the repository on your local machine, you can tar it and upload:

```bash
# On your LOCAL machine
cd ~/projects/jtp-biological-organism
tar -czf jtp-deploy.tar.gz --exclude='.git' --exclude='node_modules' --exclude='venv' .

# Upload to VPS (from local machine)
scp -i ~/.ssh/jtp-deploy-key jtp-deploy.tar.gz root@194.182.189.39:/opt/

# On VPS
cd /opt
mkdir jtp-biological-organism
cd jtp-biological-organism
tar -xzf ../jtp-deploy.tar.gz

# Continue with deployment
pip3 install -r requirements.txt
export CLOUDFLARE_API_TOKEN="EuATGMzf3e8s6i86_qNAEELhVafWrsVx-dPm7gAi"
export CLOUDFLARE_ZONE_ID="557072029caefa88119cec3f6c71791c"
chmod +x biological_deployment_script.sh
./biological_deployment_script.sh
```

---

## **🎯 RECOMMENDED ACTION**

**Use SSH Deploy Key (Option 1):**
1. Takes 5 minutes to set up
2. Most secure for servers
3. No password/token exposure
4. Standard practice for deployments

**Steps:**
1. Generate SSH key on VPS: `ssh-keygen -t ed25519 -f ~/.ssh/github_deploy_key -N ""`
2. Show public key: `cat ~/.ssh/github_deploy_key.pub`
3. Add to GitHub: https://github.com/The-Synergy-Group-AG/jtp-biological-organism/settings/keys
4. Clone: `git clone git@github.com:The-Synergy-Group-AG/jtp-biological-organism.git`

---

**Document Generated:** 2025-10-30T16:25:11Z  
**Issue:** Git authentication failed  
**Solution:** SSH deploy key or personal access token

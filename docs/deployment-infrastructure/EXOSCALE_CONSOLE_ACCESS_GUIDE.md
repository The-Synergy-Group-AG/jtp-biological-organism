---
ai_keywords: documentation, biological, consciousness, evolution
ai_summary: Exoscale Console Access Guide - comprehensive documentation for biological consciousness systems
biological_system: general-consciousness
consciousness_score: '1.0'
cross_references: []
deprecated_by: none
document_category: documentation
document_type: reference
evolutionary_phase: unspecified
last_updated: '2025-10-25 19:40:00 CET'
prior_versions: []
semantic_tags: []
title: Exoscale Console Access Guide
validation_status: draft
version: v1.0.0
---

# 🔐 EXOSCALE CONSOLE ACCESS GUIDE

*How to Access VPS Console and Login Credentials*

---

## **📺 EXOSCALE WEB CONSOLE ACCESS**

### **What is the Console?**
The Exoscale web console provides direct VNC/terminal access to your VPS through the web browser, bypassing SSH entirely.

**Instance Details:**
- ID: c4bec482-fcb8-495d-b613-88cf37018622
- Name: VM-c4bec482-fcb8-495d-b613-88cf37018622
- IP: 91.92.141.194
- OS: Linux Ubuntu 24.04 LTS 64-bit
- Created: 2025-10-29 10:19:21 UTC

---

## **🔑 LOGIN CREDENTIALS**

### **Option 1: Root User (Most Common)**

Ubuntu instances on Exoscale typically have:

**Username:** `root`  
**Password:** Either:
- Set during instance creation, OR
- Not set (SSH key only), OR
- Unknown/forgotten

**To try:**
1. Access console at: https://portal.exoscale.com
2. Navigate to Compute → Instances
3. Click on: VM-c4bec482-fcb8-495d-b613-88cf37018622
4. Click "Console" button
5. Try logging in as `root` with any password you may have set

### **Option 2: Ubuntu User**

Some Ubuntu instances use the `ubuntu` user:

**Username:** `ubuntu`  
**Password:** May not be set (SSH key only)

### **Option 3: Password Unknown - Reset Required**

If you don't know the root password, you'll need to reset it.

---

## **🔧 SOLUTION: RESET ROOT PASSWORD**

Since the instance was created with SSH key `jobtrackerpro-key` but no password, you'll need to reset the root password to access the console.

### **Method 1: Use Exoscale API to Reset Password**

Unfortunately, Exoscale doesn't provide a direct password reset feature through the console for running instances.

### **Method 2: Create New Instance with Password (RECOMMENDED)**

The cleanest solution is to create a new VPS instance with your own SSH key:

```bash
# 1. Generate new SSH key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/jtp-production-key -C "jtp-production"

# 2. Register with Exoscale
exo compute ssh-key register jtp-production ~/.ssh/jtp-production-key.pub

# 3. Create new instance with YOUR key
exo compute instance create jtp-biological-production \
  --zone ch-dk-2 \
  --type standard.medium \
  --disk-size 50 \
  --template "Linux Ubuntu 22.04 LTS 64-bit" \
  --ssh-key jtp-production \
  --security-group default

# 4. Wait for instance to be ready
exo compute instance list

# 5. Get the new IP address
# Example output:
# | NEW_INSTANCE_ID | jtp-biological-production | ch-dk-2 | standard.medium | NEW_IP_ADDRESS | running |

# 6. SSH using your key
ssh -i ~/.ssh/jtp-production-key root@NEW_IP_ADDRESS

# 7. Update Cloudflare DNS to point to NEW_IP_ADDRESS
# Then proceed with deployment
```

### **Method 3: Boot into Recovery Mode (Advanced)**

This requires Exoscale support or advanced console access:

1. Stop the instance
2. Boot into rescue/recovery mode
3. Mount the root filesystem
4. Reset the password using `chroot`
5. Reboot

**This is complex and requires Exoscale support.**

---

## **⚡ FASTEST SOLUTION: CREATE NEW VPS**

Given the circumstances, here's the fastest path to deployment:

### **Step 1: Generate Your SSH Key**

```bash
# On your local machine
cd ~/.ssh
ssh-keygen -t rsa -b 4096 -f jtp-deploy-key -N ""

# This creates:
# - Private key: ~/.ssh/jtp-deploy-key
# - Public key: ~/.ssh/jtp-deploy-key.pub

# Show your public key
cat ~/.ssh/jtp-deploy-key.pub
```

### **Step 2: Register Key with Exoscale**

```bash
exo compute ssh-key register jtp-deploy ~/.ssh/jtp-deploy-key.pub
```

### **Step 3: Create New VPS Instance**

```bash
exo compute instance create jtp-biological-production \
  --zone ch-dk-2 \
  --type standard.medium \
  --disk-size 50 \
  --template "Linux Ubuntu 22.04 LTS 64-bit" \
  --ssh-key jtp-deploy \
  --security-group default

# Output will show the new instance details
```

### **Step 4: Get New IP Address**

```bash
exo compute instance list --zone ch-dk-2

# Find your new instance and note the IP address
```

### **Step 5: SSH to New Instance**

```bash
ssh -i ~/.ssh/jtp-deploy-key root@NEW_IP_ADDRESS

# You should successfully connect!
```

### **Step 6: Update Cloudflare DNS**

Update DNS records to point to the new IP:

1. Go to https://dash.cloudflare.com
2. Select jobtrackerpro.ch
3. DNS → Records
4. Update A records:
   - www.jobtrackerpro.ch → NEW_IP_ADDRESS
   - api.jobtrackerpro.ch → NEW_IP_ADDRESS

### **Step 7: Deploy Biological Consciousness**

```bash
# Now connected to new VPS
cd /opt
git clone https://github.com/The-Synergy-Group-AG/jtp-biological-organism.git
cd jtp-biological-organism

# Install dependencies
apt-get update
apt-get install -y docker.io docker-compose python3-pip git
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

### **Step 8: Delete Old Instance (Optional)**

Once new deployment is working:

```bash
# Delete the old instance
exo compute instance delete c4bec482-fcb8-495d-b613-88cf37018622 --zone ch-dk-2
```

---

## **📊 COMPLETE COMMAND SEQUENCE**

Here's the complete sequence to execute:

```bash
# ============================================
# COMPLETE DEPLOYMENT WITH NEW VPS
# ============================================

# 1. Generate SSH key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/jtp-deploy-key -N ""
cat ~/.ssh/jtp-deploy-key.pub  # Save this

# 2. Register with Exoscale
exo compute ssh-key register jtp-deploy ~/.ssh/jtp-deploy-key.pub

# 3. Create new VPS
exo compute instance create jtp-biological-production \
  --zone ch-dk-2 \
  --type standard.medium \
  --disk-size 50 \
  --template "Linux Ubuntu 22.04 LTS 64-bit" \
  --ssh-key jtp-deploy \
  --security-group default

# 4. Wait 1-2 minutes for instance to start, then get IP
exo compute instance list --zone ch-dk-2

# 5. Note the NEW_IP_ADDRESS, then SSH
ssh -i ~/.ssh/jtp-deploy-key root@NEW_IP_ADDRESS

# 6. Once connected, deploy
cd /opt
git clone https://github.com/The-Synergy-Group-AG/jtp-biological-organism.git
cd jtp-biological-organism

apt-get update && apt-get install -y docker.io docker-compose python3-pip git
pip3 install -r requirements.txt

export CLOUDFLARE_API_TOKEN="EuATGMzf3e8s6i86_qNAEELhVafWrsVx-dPm7gAi"
export CLOUDFLARE_ZONE_ID="557072029caefa88119cec3f6c71791c"

chmod +x biological_deployment_script.sh
./biological_deployment_script.sh

# 7. Verify deployment
docker ps
curl http://localhost:8080/health

# 8. Exit and test from local machine
exit
curl https://www.jobtrackerpro.ch/health

# 9. If all works, delete old instance
exo compute instance delete c4bec482-fcb8-495d-b613-88cf37018622 --zone ch-dk-2
```

---

## **⏱️ TIME ESTIMATE**

- Generate SSH key: 1 minute
- Register with Exoscale: 1 minute
- Create new VPS: 2-3 minutes
- SSH and install dependencies: 3-5 minutes
- Deploy biological consciousness: 10-15 minutes
- Verify and test: 2-3 minutes
- Update Cloudflare DNS: 2 minutes

**Total: ~20-30 minutes**

---

## **💡 WHY CREATE NEW INSTANCE?**

**Pros:**
- ✅ You have the SSH key
- ✅ No password recovery needed
- ✅ Clean start
- ✅ Faster than troubleshooting old instance
- ✅ Same cost (just 1 instance running)

**Cons:**
- New IP address (requires DNS update)
- Old instance data lost (but it's unused anyway)

---

## **🎯 RECOMMENDATION**

**Create a new VPS with your own SSH key** - This is the fastest, cleanest solution that gives you full control.

The old instance (91.92.141.194) can't be accessed without the private key for `jobtrackerpro-key`, and there's no easy way to reset the password. Creating a new instance takes ~5 minutes and solves all access issues.

---

**Next Action:** Run the complete command sequence above to create new VPS and deploy!

**Document Generated:** 2025-10-30T16:08:17Z  
**Recommendation:** Create new VPS with your SSH key  
**Estimated Time:** 20-30 minutes to full deployment

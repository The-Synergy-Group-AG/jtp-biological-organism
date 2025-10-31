---
ai_keywords: documentation, biological, consciousness, evolution
ai_summary: Cloudflare Api Token Configuration - comprehensive documentation for biological consciousness systems
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
title: Cloudflare Api Token Configuration
validation_status: draft
version: v1.0.0
---

# 🔐 **CLOUDFLARE API TOKEN CONFIGURATION**

*Required Permissions for Claude Opus Deployment Plan V3*

---

## **📄 DOCUMENT METADATA**

| **Field** | **Value** |
|-----------|-----------|
| **Document Title** | Cloudflare API Token Configuration Guide |
| **Document ID** | CF-API-TOKEN-CONFIG-2025-001 |
| **Version** | 1.0.0 |
| **Date Created** | 2025-10-30 |
| **Purpose** | Configure Cloudflare API token for Exoscale deployment |
| **Domain** | www.jobtrackerpro.ch |

---

## **🎯 RECOMMENDED CLOUDFLARE API TOKEN**

### **Option 1: Custom Token (RECOMMENDED)**

For the Claude Opus Deployment Plan V3, you need a **Custom API Token** with the following permissions:

#### **Required Permissions:**

1. **Zone - DNS - Edit**
   - Allows creating/updating A records for:
     - www.jobtrackerpro.ch
     - api.jobtrackerpro.ch
     - consciousness.jobtrackerpro.ch

2. **Zone - SSL and Certificates - Edit**
   - Allows configuring:
     - SSL/TLS settings
     - Certificate authority selection
     - TLS version requirements
     - Cipher suites

3. **Zone - Firewall Services - Edit**
   - Allows configuring:
     - WAF (Web Application Firewall) rules
     - Custom firewall rules
     - Security policies

4. **Zone - Rate Limiting - Edit**
   - Allows configuring:
     - API rate limiting rules
     - Request throttling
     - Protection for biological endpoints

5. **Zone - Zone Settings - Read**
   - Required for:
     - Verifying zone configuration
     - Reading current settings

---

## **🔧 STEP-BY-STEP TOKEN CREATION**

### **Step 1: Access Cloudflare Dashboard**
1. Login to: https://dash.cloudflare.com
2. Go to **My Profile** (top right)
3. Select **API Tokens** from left menu
4. Click **Create Token**

### **Step 2: Choose Token Type**
- Select: **Create Custom Token**
- Token Name: `jtp-biological-deployment-v3`

### **Step 3: Configure Permissions**

Click **+ Add more** to add each permission:

```
Permission Group: Zone
Permission: DNS
Access Level: Edit

Permission Group: Zone
Permission: SSL and Certificates
Access Level: Edit

Permission Group: Zone
Permission: Firewall Services
Access Level: Edit

Permission Group: Zone
Permission: Rate Limiting
Access Level: Edit

Permission Group: Zone
Permission: Zone Settings
Access Level: Read
```

### **Step 4: Configure Zone Resources**

**Specify the zone:**
- Zone Resources: **Specific zone**
- Select zone: `jobtrackerpro.ch`

This ensures the token only works for your specific domain.

### **Step 5: Optional Settings**

**Client IP Address Filtering** (Optional but recommended):
- Add your deployment server's IP address
- Example: `91.92.141.194` (your existing Exoscale VPS)
- This restricts token usage to specific IPs

**TTL (Time to Live)** (Optional):
- Start Date: Now
- End Date: Set expiration (e.g., 1 year)
- Or leave blank for no expiration

### **Step 6: Create and Save Token**

1. Click **Continue to summary**
2. Review permissions
3. Click **Create Token**
4. **IMPORTANT**: Copy the token immediately (shown only once!)
5. Store securely in Vault:
   ```bash
   vault kv put secret/cloudflare/global_api_key value=<your-token-here>
   ```

---

## **✅ ALTERNATIVE: USE EXISTING TEMPLATE**

### **Option 2: Edit Zone DNS Template (Limited)**

If you only need basic DNS management:

1. Select template: **Edit zone DNS**
2. Configure:
   - Zone Resources: Specific zone → `jobtrackerpro.ch`
   - Client IP filtering: Optional
3. Create token

**⚠️ Limitations:**
- Only DNS editing capability
- Cannot configure SSL/TLS
- Cannot configure WAF/firewall
- Cannot configure rate limiting

**Use case:** Manual SSL/WAF configuration via dashboard

---

## **📋 TOKEN VERIFICATION**

### **Test Your Token**

Once created, verify the token works:

```bash
# Test token validity
curl -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json"

# Expected response:
{
  "success": true,
  "result": {
    "id": "...",
    "status": "active"
  }
}
```

### **Test DNS Access**

```bash
# Get zone ID
curl -X GET "https://api.cloudflare.com/client/v4/zones?name=jobtrackerpro.ch" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json"

# Save the zone ID from response
```

---

## **🔐 SECURITY BEST PRACTICES**

### **Token Storage**

**DO:**
- ✅ Store in HashiCorp Vault
- ✅ Use environment variables
- ✅ Restrict access with IAM
- ✅ Set expiration dates
- ✅ Enable IP filtering

**DON'T:**
- ❌ Commit to Git
- ❌ Share in plain text
- ❌ Use in public repositories
- ❌ Store in application code
- ❌ Use without expiration

### **Token Rotation**

**Best Practice Schedule:**
- Production tokens: Rotate every 90 days
- Development tokens: Rotate every 30 days
- Compromised tokens: Revoke immediately

**Rotation Process:**
1. Create new token with same permissions
2. Update Vault with new token
3. Test new token functionality
4. Revoke old token
5. Monitor for any issues

---

## **📊 REQUIRED CLOUDFLARE INFORMATION**

### **For Vault Configuration:**

After creating the token, you need to store these values in Vault:

```bash
# 1. API Token
vault kv put secret/cloudflare/global_api_key value=<your-api-token>

# 2. Zone ID (get from dashboard or API)
vault kv put secret/cloudflare/zone_id value=<your-zone-id>

# 3. Account ID (optional, for organization tracking)
vault kv put secret/cloudflare/account_id value=36de3cd7-89ef-4901-822d-416a7d1b6d8d
```

### **How to Get Zone ID:**

**Method 1: From Cloudflare Dashboard**
1. Login to https://dash.cloudflare.com
2. Select your domain: `jobtrackerpro.ch`
3. Scroll down on Overview page
4. Find **Zone ID** in the right sidebar
5. Copy the ID

**Method 2: Using API**
```bash
curl -X GET "https://api.cloudflare.com/client/v4/zones?name=jobtrackerpro.ch" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" | jq -r '.result[0].id'
```

---

## **📝 COMPLETE CONFIGURATION CHECKLIST**

### **Cloudflare Token Setup:**
- [ ] Login to Cloudflare dashboard
- [ ] Create Custom API Token
- [ ] Add DNS Edit permission
- [ ] Add SSL and Certificates Edit permission
- [ ] Add Firewall Services Edit permission
- [ ] Add Rate Limiting Edit permission
- [ ] Add Zone Settings Read permission
- [ ] Set Zone Resources to `jobtrackerpro.ch`
- [ ] (Optional) Add IP filtering for 91.92.141.194
- [ ] Copy token immediately after creation
- [ ] Test token with verify endpoint
- [ ] Get Zone ID for jobtrackerpro.ch

### **Vault Configuration:**
- [ ] Store Cloudflare API token in Vault
- [ ] Store Zone ID in Vault
- [ ] Store Account ID in Vault (optional)
- [ ] Verify Vault credentials accessible
- [ ] Test deployment script with credentials

---

## **🚀 DEPLOYMENT-READY CONFIGURATION**

Once you have the token, your complete Vault configuration should be:

```bash
# Cloudflare credentials
vault kv put secret/cloudflare/global_api_key value=<your-cloudflare-token>
vault kv put secret/cloudflare/zone_id value=<your-zone-id>

# Exoscale credentials (already configured)
# vault kv put secret/exoscale/api_key value=<key>
# vault kv put secret/exoscale/api_secret value=<secret>

# SSH deployment key
vault kv put secret/ssh/biological_deploy_key value=@~/.ssh/id_rsa

# Verify all credentials
vault kv get secret/cloudflare/global_api_key
vault kv get secret/cloudflare/zone_id
```

---

## **⚡ QUICK SUMMARY**

**RECOMMENDED APPROACH:**

1. **Create Custom Token** (not pre-built template)
2. **Add 5 Permissions:**
   - Zone → DNS → Edit
   - Zone → SSL and Certificates → Edit
   - Zone → Firewall Services → Edit
   - Zone → Rate Limiting → Edit
   - Zone → Zone Settings → Read
3. **Restrict to Zone:** `jobtrackerpro.ch`
4. **Optional:** IP filter to `91.92.141.194`
5. **Store in Vault:** Use commands above
6. **Test:** Verify token works
7. **Deploy:** Run `./deployment/execute_deployment_plan_v3.sh deploy`

---

**Token Name:** `jtp-biological-deployment-v3`  
**Zone:** `jobtrackerpro.ch`  
**Permissions:** DNS, SSL, Firewall, Rate Limiting, Zone Settings  
**Security:** IP-filtered, expiration set, Vault-stored  
**Status:** Ready for production deployment

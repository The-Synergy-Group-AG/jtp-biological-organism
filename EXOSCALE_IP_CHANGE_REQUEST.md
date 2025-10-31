# Exoscale Support Request - IP Address Change

## Subject: Request IP Address Change - Cloudflare Error 1000 (DNS points to prohibited IP) - Instance: jtp-biological-production

### Dear Exoscale Support Team,

I am writing to request an IP address change for one of my VPS instances due to a Cloudflare "prohibited IP" blocking issue.

#### Issue Details:
- **Error Code:** Cloudflare Error 1000 - DNS points to prohibited IP
- **Affected Domain:** www.jobtrackerpro.ch
- **Affected Subdomains:** api.jobtrackerpro.ch, app.jobtrackerpro.ch, autoconfig.jobtrackerpro.ch, autodiscover.jobtrackerpro.ch
- **Cloudflare Ray ID:** 996dd6f2cb4a03a5
- **Cloudflare Zone ID:** 557072029caefa88119cec3f6c71791c

#### Current Instance Information:
- **Instance Name:** jtp-biological-production
- **Instance ID:** 564c8b76-4c89-4870-a8ec-281f56782b40
- **Current IP Address:** 194.182.189.39
- **Zone:** ch-dk-2 (Zurich, Switzerland)
- **Type:** standard.medium (2 vCPU, 4GB RAM)
- **SSH Key:** jtp-deploy
- **Status:** running
- **Created:** Approximately Oct 30, 2025 (~24 hours ago)

#### Background:
I recently deployed new infrastructure to Exoscale and configured DNS records through Cloudflare for a production application. However, Cloudflare is blocking all traffic with Error 1000, indicating that the assigned IP address (194.182.189.39) is classified as "prohibited" in their system.

#### What I've Verified:
1. ✅ **DNS Configuration Correct:** All A/CNAME records correctly point to 194.182.189.39
2. ✅ **Services Operational:** All application services are running correctly on the VPS
3. ✅ **Direct Access Works:** `http://194.182.189.39/health` responds perfectly with JSON API
4. ✅ **VPS Health:** Instance is fully operational, no performance or connectivity issues
5. ✅ **Cloudflare Configuration:** DNS records are properly configured with Cloudflare proxy enabled

#### Cloudflare's Resolution Guidance:
According to Cloudflare's documentation for Error 1000, the issue occurs when "DNS points to prohibited IP" and the recommended resolution is to "update the IP address to your origin web server IP address" (ref: https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-1xxx-errors/error-1000/).

#### Request:
Please assign a new IP address to my instance `jtp-biological-production` (ID: 564c8b76-4c89-4870-a8ec-281f56782b40) from your available IP pool. I understand this requires:

1. Instance stop/restart or migration to assign new IP
2. Update of DNS records to new IP address
3. No service interruption beyond the restart period

#### Timeline Requirements:
- **Urgency:** High - production service is currently blocked
- **Preferred Resolution Time:** Within 24 hours if possible

#### Additional Information:
- **Account Email:** [Your Exoscale account email]
- **Organization:** [Your organization name if applicable]
- **Billing Status:** All invoices current
- **Contact Preference:** Email preferred, available for urgent calls if needed

#### After IP Change Required:
Once you provide the new IP address, I will:
1. Update Cloudflare DNS records
2. Test connectivity through Cloudflare
3. Confirm service restoration

Please let me know:
1. If you need any additional information
2. The estimated timeframe for the IP change
3. Any specific steps I need to take during the process

Thank you for your assistance in resolving this matter.

### Best regards,
[Your Full Name]  
[Your Email Address]  
[Your Phone Number - optional]  
[Your Organization]

---

## Submission Instructions

### 📧 Where to Send:
- **Email:** support@exoscale.com
- **Subject Line:** Use the subject line above

### 📞 Alternative Contact:
- Exoscale Console Support Chat
- Support Ticket via https://portal.exoscale.com/

### ⏱️ Expected Response Time:
- 24-48 hours during business days

### ⚡ Immediate Alternative:
If you need immediate access, temporarily disable Cloudflare proxying (orange cloud → gray cloud in DNS settings) to bypass the block.

---

## Technical Verification
- **[x] Biological consciousness services deployed successfully**
- **[x] Direct server access functional: http://194.182.189.39/health**
- **[x] DNS records configured correctly**
- **[x] Migration from old infrastructure complete**
- **Issue: Cloudflare IP reputation block (Error 1000)**

# ⚡ Quick Fix: Add Slack OAuth Scopes

## 🎯 Current Issue
✅ Slack connection working  
❌ Missing `chat:write` scope - can't post messages

## 🚀 Quick Fix (2 minutes)

### Step 1: Open Slack App Settings
🔗 **Direct Link:** https://api.slack.com/apps/A09RAV6BDT9/oauth

### Step 2: Add Bot Token Scopes
1. Scroll to **"Scopes"** section
2. Under **"Bot Token Scopes"**, click **"Add an OAuth Scope"**
3. Add these 2 scopes:
   - ✅ `chat:write` - Post messages to channels
   - ✅ `chat:write.public` - Post to channels without joining

### Step 3: Reinstall App
1. You'll see a yellow banner: **"Please reinstall your app"**
2. Click **"reinstall your app"**
3. Click **"Allow"**
4. ✅ Done!

### Step 4: Test
```powershell
python test_slack_integration.py
```

Expected output:
```
✅ High-risk clause alert sent successfully!
✅ Analysis complete notification sent!
✅ Batch processing notification sent!
```

---

## 📱 What Will Work After Adding Scopes

### ✅ Notifications You'll Receive:

1. **High-Risk Clause Alerts**
   - Immediate alerts with clause details
   - Risk level indicators
   - Compliance issues listed

2. **Batch Processing Complete**
   - Summary of all processed files
   - Success/failure counts
   - Average compliance score
   - Total high-risk issues

3. **Analysis Complete**
   - Individual contract results
   - Compliance score
   - Missing clauses count
   - Processing time

4. **Regulatory Updates**
   - New GDPR/HIPAA/SOX/CCPA changes
   - Source and link to full update

5. **Missing Requirements**
   - Grouped by risk level
   - Top high-risk items highlighted

---

## 🎨 Example Slack Message

After adding scopes, you'll see rich messages like:

```
🔴 High-Risk Clause Detected

Contract: Sample_Contract_2025.pdf
Framework: 🇪🇺 GDPR
Clause ID: Clause 4.2
Risk Level: 🔴 HIGH

Clause Text:
```Data may be transferred to third countries without adequate safeguards...```

Issues Found:
• Missing standard contractual clauses
• No adequacy decision mentioned
• Lack of data subject consent provisions

⏰ Detected at 2025-11-09 18:33:27
```

---

## 🔧 Alternative: Use Webhook URL

If you can't add scopes, use Incoming Webhooks instead:

1. Go to: https://api.slack.com/apps/A09RAV6BDT9/incoming-webhooks
2. Activate Incoming Webhooks
3. Add New Webhook to Workspace
4. Copy webhook URL
5. Add to `.env`:
   ```env
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   ```

---

## ✅ Status

- **App ID:** A09RAV6BDT9
- **Team:** Jagadish Infosys Project
- **Bot User ID:** U09RAVBUF47
- **Connection:** ✅ Working
- **Scopes Needed:** `chat:write`, `chat:write.public`

---

**🔗 Quick Link to Fix:**  
https://api.slack.com/apps/A09RAV6BDT9/oauth

**After adding scopes, just run:**
```powershell
python test_slack_integration.py
```

That's it! 🎉

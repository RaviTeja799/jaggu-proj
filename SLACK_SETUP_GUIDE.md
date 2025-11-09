# 🔔 Slack Integration Setup Guide

## ✅ Current Status

- **Connection:** ✅ Working
- **Team:** Jagadish Infosys Project
- **Bot User ID:** U09SLLFJR7A
- **Issue:** Missing OAuth scopes for posting messages

---

## 🔧 Required OAuth Scopes

Your Slack app needs the following **Bot Token Scopes**:

### Required for Notifications:
- ✅ `chat:write` - Post messages to channels
- ✅ `chat:write.public` - Post to public channels without joining
- ⚠️ `channels:read` - View channels (optional)
- ⚠️ `groups:read` - View private channels (optional)

---

## 📝 How to Add Scopes

### Step 1: Go to Slack App Settings
1. Open: https://api.slack.com/apps
2. Select your app: **Jagadish Infosys Project**

### Step 2: Add Bot Token Scopes
1. Click **OAuth & Permissions** (left sidebar)
2. Scroll to **Scopes** section
3. Under **Bot Token Scopes**, click **Add an OAuth Scope**
4. Add these scopes:
   - `chat:write`
   - `chat:write.public`
   - `channels:read` (optional)

### Step 3: Reinstall App
1. After adding scopes, you'll see a banner: **"Reinstall your app"**
2. Click **reinstall your app**
3. Review permissions
4. Click **Allow**

### Step 4: Update Token (if needed)
1. After reinstalling, Slack will show your new **Bot User OAuth Token**
2. Copy the token (starts with `xoxb-`)
3. Update `.env`:
   ```env
   SLACK_ACCESS_TOKEN=xoxb-your-new-token-here
   ```

---

## 🚀 Quick Test

After adding scopes and reinstalling, run:

```powershell
python test_slack_integration.py
```

You should see:
```
✅ High-risk clause alert sent successfully!
✅ Analysis complete notification sent!
✅ Batch processing notification sent!
```

---

## 📊 What You Can Do With Slack Integration

### 1. **High-Risk Clause Alerts**
Get immediate notifications when high-risk clauses are detected:
- 🔴 Missing data transfer safeguards
- 🔴 Inadequate breach notification procedures
- 🔴 Insufficient data subject rights

### 2. **Batch Processing Notifications**
Receive summaries when processing multiple contracts:
- Total files processed
- Success/failure count
- Average compliance score
- High-risk issue count

### 3. **Analysis Complete Notifications**
Get notified when single contract analysis finishes:
- Compliance score
- Missing clauses
- Processing time
- Risk breakdown

### 4. **Regulatory Updates**
Stay informed about new regulations:
- GDPR updates
- HIPAA changes
- SOX amendments
- CCPA modifications

### 5. **Missing Requirements Alerts**
Track compliance gaps:
- High-risk missing clauses
- Medium-risk issues
- Low-risk improvements

---

## 🎯 Using Slack in Your Workflow

### Option 1: Auto-Notify on Analysis
```python
from services.slack_notifier import SlackNotifier

slack = SlackNotifier()

# After analyzing a contract
slack.notify_analysis_complete(
    contract_name="MyContract.pdf",
    compliance_score=85.0,
    framework="GDPR",
    missing_clauses_count=3,
    high_risk_issues=1,
    processing_time=5.2
)
```

### Option 2: Batch Processing Notifications
```python
from services.batch_processor import BatchProcessor

# Enable Slack in batch processor
processor = BatchProcessor(
    max_workers=4,
    enable_slack=True,
    slack_channel="#compliance-alerts"
)

# Process files - auto-sends Slack notification when done
summary = processor.process_batch(file_paths, framework="GDPR")
```

### Option 3: Custom Alerts
```python
slack = SlackNotifier()

# Alert on high-risk clause
slack.notify_high_risk_clause(
    contract_name="Contract.pdf",
    clause_id="Section 4.2",
    clause_text="Your problematic clause...",
    risk_level="high",
    framework="GDPR",
    issues=["Missing safeguards", "No consent"]
)
```

---

## 📱 Channel Configuration

### Default Channel
By default, notifications go to `#general`. Change it:

```python
# In app initialization
slack = SlackNotifier(default_channel="#compliance-alerts")
```

### Channel per Notification Type
```python
# High-risk alerts to urgent channel
slack.notify_high_risk_clause(
    ...,
    channel="#urgent-compliance"
)

# Regular updates to general channel
slack.notify_analysis_complete(
    ...,
    channel="#compliance-reports"
)
```

### Recommended Channels
- `#compliance-alerts` - High-priority issues
- `#compliance-reports` - Daily summaries
- `#regulatory-updates` - Legal changes
- `#batch-results` - Bulk processing results

---

## 🔒 Security Note

**Never commit your Slack tokens to GitHub!**

✅ **Tokens are in `.env`** (ignored by git)  
✅ **Template in `.env.example`** (safe to commit)  
❌ **Never put tokens in code**

---

## 🆘 Troubleshooting

### Error: `missing_scope`
**Solution:** Add required scopes (see Step 2 above) and reinstall app

### Error: `channel_not_found`
**Solution:** 
- Use channel ID instead of name: `C12345ABC`
- Or invite bot to channel: `/invite @YourBotName`

### Error: `not_authed` or `invalid_auth`
**Solution:** 
- Token expired - regenerate in Slack app settings
- Wrong token format - should start with `xoxb-` or `xoxe.xoxp-`

### Messages not appearing
**Solution:**
- Check channel permissions
- Bot must be member of private channels
- Public channels work with `chat:write.public` scope

---

## 📞 Need Help?

1. **Slack API Docs:** https://api.slack.com/docs
2. **OAuth Scopes:** https://api.slack.com/scopes
3. **Your App Settings:** https://api.slack.com/apps

---

## ✅ Checklist

- [ ] Add `chat:write` scope
- [ ] Add `chat:write.public` scope
- [ ] Reinstall Slack app
- [ ] Update token in `.env` (if changed)
- [ ] Run `python test_slack_integration.py`
- [ ] Create `#compliance-alerts` channel (optional)
- [ ] Invite bot to channels (if private)
- [ ] Test notification in Streamlit app

---

**Once scopes are added, your Slack integration will be fully operational!** 🎉

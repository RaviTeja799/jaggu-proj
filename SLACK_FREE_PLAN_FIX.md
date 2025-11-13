# 🔓 Slack Setup for Free/Standard Plans

## ❌ The Problem
Your workspace is on **Free/Standard plan** (not Enterprise Grid).
The scope `chat:write.public` requires Enterprise, causing the installation to fail.

## ✅ Solution: Use Basic Scopes Only

### Step 1: Remove Enterprise-Only Scopes

🔗 **Go to:** https://api.slack.com/apps/A09RAV6BDT9/oauth

1. Under **"Bot Token Scopes"**, you should see:
   - ❌ `chat:write.public` ← **REMOVE THIS** (Enterprise only)
   
2. Keep/Add only these scopes:
   - ✅ `chat:write` - Post messages to channels the bot is invited to
   - ✅ `channels:read` - View basic channel information
   - ✅ `channels:join` - Join public channels

### Step 2: Reinstall App
1. Click **"reinstall your app"** (yellow banner)
2. Click **"Allow"**
3. ✅ Should install successfully now!

### Step 3: Invite Bot to Your Channel
Since we removed `chat:write.public`, the bot needs to be **invited** to channels:

1. Go to your Slack channel (e.g., `#compliance-alerts`)
2. Type: `/invite @Infosys-Project`
3. Bot will join the channel
4. ✅ Now it can post messages!

### Step 4: Test
```powershell
python test_slack_integration.py
```

---

## 📱 Alternative: Use Incoming Webhooks (Easiest!)

If you still have issues, **webhooks are simpler** and work on all plans:

### Option A: Incoming Webhooks (Recommended)

1. **Go to:** https://api.slack.com/apps/A09RAV6BDT9/incoming-webhooks
2. **Toggle:** "Activate Incoming Webhooks" to **ON**
3. **Click:** "Add New Webhook to Workspace"
4. **Select** your channel (e.g., `#compliance-alerts`)
5. **Click:** "Allow"
6. **Copy** the webhook URL (looks like: `https://hooks.slack.com/services/T.../B.../abc...`)

7. **Update .env:**
   ```env
   # Comment out or keep bot token
   # SLACK_BOT_TOKEN=xoxb-YOUR-BOT-TOKEN-HERE
   
   # Add webhook URL
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   ```

8. **I'll update the code** to support webhooks automatically!

---

## 🎯 Which Option Should You Choose?

### Option 1: Bot Token (chat:write only)
**Pros:**
- More flexible (can post to multiple channels)
- Can interact with users
- Professional bot presence

**Cons:**
- Need to invite bot to each channel
- Slightly more setup

**Best for:** Multiple channels, interactive features

### Option 2: Incoming Webhooks
**Pros:**
- ✅ Easiest setup (3 minutes)
- ✅ Works on ALL Slack plans
- ✅ No scope issues
- ✅ No bot invitation needed

**Cons:**
- One webhook per channel
- Can't reply to users

**Best for:** Simple notifications to one channel

---

## 🚀 Quick Setup (Choose One)

### A. Bot Token Method (Recommended if you want multi-channel)

1. **Remove `chat:write.public` scope**
2. **Keep only:** `chat:write`, `channels:read`, `channels:join`
3. **Reinstall app**
4. **Invite bot to channel:** `/invite @Infosys-Project`
5. **Test:** `python test_slack_integration.py`

### B. Webhook Method (Easiest - 3 minutes)

1. **Activate Incoming Webhooks:** https://api.slack.com/apps/A09RAV6BDT9/incoming-webhooks
3. **Create webhook** for your channel
4. **Copy webhook URL**
5. **Add to .env:**
   ```env
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR_WORKSPACE/YOUR_CHANNEL/YOUR_TOKEN
   ```
6. **Tell me**, and I'll update `slack_notifier.py` to use webhooks!

---

## 📋 Current Status

- **App ID:** A09RAV6BDT9
- **Team:** Jagadish Infosys Project
- **Bot User ID:** U09RAVBUF47
- **Issue:** Enterprise-only scope blocking installation
- **Solution:** Use `chat:write` only OR webhooks

---

**Which option do you prefer?**
- Type **"bot"** for Option A (bot token with manual invite)
- Type **"webhook"** for Option B (incoming webhook - easiest!)

I'll help you set it up! 🎉

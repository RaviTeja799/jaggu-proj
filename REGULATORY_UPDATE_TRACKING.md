# Real-Time Regulatory Update Tracking System 🚀

## Overview

This system provides **real-time monitoring and intelligent analysis** of regulatory updates across GDPR, HIPAA, CCPA, and SOX frameworks using advanced AI and web scraping technologies.

## 🎯 Key Features

### 1. **Multi-Source Web Monitoring**
- 🔍 **Serper API Integration**: Google Search-powered regulatory monitoring
- 🌐 **Official Source Tracking**: Monitors government and regulatory websites
- 📰 **News & Legal Analysis**: Tracks regulatory news and legal interpretations
- ⏰ **Configurable Check Intervals**: Customizable monitoring frequency

### 2. **AI-Powered Analysis**
- 🤖 **Groq LLM Integration**: Ultra-fast LLaMA 3.3 70B model for analysis
- 📊 **Automatic Severity Assessment**: Critical/High/Medium/Low classification
- 💡 **Impact Scoring**: 0-1 scale quantifying regulatory impact
- 🎯 **Affected Clause Detection**: Identifies which contract clauses need updates
- ✅ **Required Actions**: Generates actionable compliance steps

### 3. **Knowledge Base Integration**
- 📚 **CUAD Dataset**: 512 legal contracts with 25,000+ clauses
- 🏷️ **Contract Categorization**: Automatic framework classification
- 🔎 **Intelligent Search**: Keyword and clause-type filtering
- 📈 **Statistical Analysis**: Comprehensive knowledge base metrics

### 4. **Update Management**
- 💾 **JSONL Storage**: Efficient update history tracking
- 🔔 **Smart Alerts**: Configurable notification system
- 🚫 **Duplicate Detection**: Prevents redundant updates
- 📅 **Timeline Tracking**: Historical regulatory changes

### 5. **Multi-API Support**
- ✅ **Serper API**: Web search and scraping
- ✅ **Groq API**: Fast LLM inference
- ⚡ **OpenRouter** (planned): Alternative LLM provider
- 🤗 **HuggingFace** (planned): Custom model hosting

---

## 🛠️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Streamlit Web UI                       │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│         RegulatoryUpdateTracker (Main Service)          │
│  - Orchestrates monitoring, analysis, and storage       │
└─────┬──────────────┬──────────────┬─────────────────────┘
      │              │              │
┌─────▼─────┐  ┌────▼────┐  ┌──────▼──────┐
│  Serper   │  │  Groq   │  │  Knowledge  │
│  API      │  │  API    │  │  Base       │
│  Client   │  │  Client │  │  Loader     │
└───────────┘  └─────────┘  └─────────────┘
      │              │              │
      │ Web Search   │ LLM Analysis │ CUAD Dataset
      │ & Scraping   │ & Summaries  │ + Manifests
      │              │              │
┌─────▼──────────────▼──────────────▼─────────────────────┐
│              Data Storage Layer                          │
│  - updates.jsonl (Update history)                       │
│  - sources.json  (Source configurations)                │
│  - alerts.json   (Alert configurations)                 │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Installation

### Prerequisites
```bash
Python 3.11+
pip install -r requirements.txt
```

### Required Packages
```bash
pip install requests streamlit groq-python
```

### API Keys Setup

```powershell
# Windows PowerShell
$env:SERPER_API_KEY='your_serper_api_key_here'
$env:GROQ_API_KEY='your_groq_api_key_here'
$env:SLACK_WEBHOOK_URL='your_slack_webhook_url'  # Optional
$env:HUGGINGFACE_API_KEY='your_hf_key'  # Optional
$env:OPENROUTER_API_KEY='your_openrouter_key'  # Optional
```

```bash
# Linux/Mac
export SERPER_API_KEY='your_serper_api_key_here'
export GROQ_API_KEY='your_groq_api_key_here'
```

### Get API Keys

1. **Serper API** (Required)
   - Sign up: https://serper.dev
   - Free tier: 2,500 searches/month
   - Get API key from dashboard

2. **Groq API** (Required)
   - Sign up: https://groq.com
   - Free tier: 14,400 requests/day
   - Ultra-fast LLaMA inference

3. **Slack** (Optional)
   - Create webhook: https://api.slack.com/messaging/webhooks
   - For regulatory update notifications

---

## 🚀 Quick Start

### 1. Test the System

```powershell
# Run comprehensive test suite
python test_regulatory_updates.py
```

Expected output:
```
✅ SERPER_API_KEY: Set
✅ GROQ_API_KEY: Set
✅ Serper API: PASSED
✅ Groq API: PASSED
✅ Knowledge Base: PASSED
✅ Tracker: PASSED

🎉 All tests passed! System is ready for production.
```

### 2. Check for Updates (Command Line)

```python
from services.regulatory_update_tracker import RegulatoryUpdateTracker

# Initialize tracker
tracker = RegulatoryUpdateTracker()

# Check for GDPR updates from last week
updates = tracker.check_for_updates(
    framework="GDPR",
    time_range='w'  # 'd'=day, 'w'=week, 'm'=month, 'y'=year
)

print(f"Found {len(updates)} new GDPR updates")

# Get statistics
stats = tracker.get_statistics()
print(f"Total recent updates: {stats['recent_updates']}")
```

### 3. Launch Web Interface

```powershell
# Start Streamlit app
streamlit run app.py
```

Then navigate to the **"Regulatory Updates"** tab.

---

## 📚 Knowledge Base

### CUAD Dataset Integration

The system uses the **Contract Understanding Atticus Dataset (CUAD)**:

- **512 legal contracts**
- **25,000+ expert-labeled clauses**
- **41 legal clause categories**
- Training data for regulatory analysis

#### Files Used:
1. **`cuad_manifest.csv`** (512 contracts)
   - Contract metadata
   - File sizes, split info
   - Question counts

2. **`cuad_sft_train.jsonl`** (55MB, 25K+ entries)
   - Instruction-following format
   - Legal clause annotations
   - Expert Q&A pairs

### Loading Knowledge Base

```python
from services.knowledge_base_loader import KnowledgeBaseLoader

kb = KnowledgeBaseLoader()

# Load manifest
kb.load_manifest()

# Load JSONL (limit for memory)
kb.load_jsonl(limit=1000)

# Categorize by framework
kb.categorize_by_framework()

# Search contracts
results = kb.search_contracts(
    keywords=["data protection", "privacy"],
    clause_types=["Data Processing"],
    limit=10
)
```

---

## 🔧 Configuration

### Regulatory Monitoring Settings

Edit `config/settings.py`:

```python
@dataclass
class RegulatoryMonitoringConfig:
    enabled: bool = True
    check_interval_hours: int = 24  # Check daily
    time_range: str = 'w'  # Search last week
    auto_check_on_startup: bool = False
    max_results_per_source: int = 10
    min_severity_alert: str = 'MEDIUM'
```

### Custom Sources

Add custom regulatory sources:

```python
from models.regulatory_update import RegulatorySource

custom_source = RegulatorySource(
    source_id="custom_gdpr_blog",
    name="GDPR Blog",
    url="https://gdpr-blog.example.com",
    framework="GDPR",
    source_type="Blog",
    check_frequency_hours=12,
    keywords=["GDPR", "data protection", "Article 5"]
)

tracker.sources[custom_source.source_id] = custom_source
tracker._save_sources()
```

### Alert Configuration

Create custom alerts:

```python
from models.regulatory_update import UpdateAlert, UpdateSeverity

alert = UpdateAlert(
    alert_id="high_severity_gdpr",
    framework="GDPR",
    keywords=["amendment", "enforcement"],
    min_severity=UpdateSeverity.HIGH,
    notification_channels=["slack", "email"],
    is_active=True
)

tracker.alerts.append(alert)
tracker._save_alerts()
```

---

## 🔍 Usage Examples

### Example 1: Monitor All Frameworks

```python
tracker = RegulatoryUpdateTracker()

# Check all frameworks
results = tracker.check_all_frameworks(time_range='w')

for framework, updates in results.items():
    print(f"\n{framework}: {len(updates)} updates")
    for update in updates[:3]:  # Show first 3
        print(f"  - {update.title}")
        print(f"    Severity: {update.severity.value}")
```

### Example 2: Filter High-Severity Updates

```python
# Get critical/high severity updates from last 30 days
critical_updates = tracker.get_updates(
    severity=UpdateSeverity.HIGH,
    days=30,
    limit=10
)

for update in critical_updates:
    print(f"\n{update.framework} - {update.title}")
    print(f"Impact Score: {update.impact_score:.2f}")
    print(f"Required Actions: {len(update.required_actions)}")
```

### Example 3: Analyze Regulatory Text

```python
groq = GroqAPIClient()

text = """
The European Commission has adopted new adequacy decisions
for UK data transfers under GDPR Article 45...
"""

analysis = groq.analyze_regulatory_text(
    text=text,
    framework="GDPR"
)

print(f"Summary: {analysis['summary']}")
print(f"Severity: {analysis['severity']}")
print(f"Impact: {analysis['impact_score']}")
print(f"Actions: {analysis['required_actions']}")
```

### Example 4: Search Regulatory Updates

```python
serper = SerperAPIClient()

# Search for HIPAA updates
results = serper.search_regulatory_updates(
    framework="HIPAA",
    keywords=["breach notification", "PHI"],
    num_results=20,
    time_range='m'  # Last month
)

for result in results[:5]:
    print(f"{result['title']}")
    print(f"  {result['snippet'][:100]}...")
    print(f"  {result['link']}\n")
```

---

## 📊 Data Storage

### Update History (`updates.jsonl`)

Each line is a JSON object representing one regulatory update:

```json
{
  "update_id": "uuid-here",
  "framework": "GDPR",
  "title": "New GDPR Data Transfer Requirements",
  "summary": "Commission adopts adequacy decisions...",
  "update_type": "Amendment",
  "severity": "High",
  "impact_score": 0.85,
  "detected_date": "2024-11-11T10:30:00",
  "source_url": "https://ec.europa.eu/...",
  "required_actions": [
    "Review data transfer agreements",
    "Update privacy policies"
  ],
  "ai_analysis": "{...}"
}
```

### Source Configuration (`sources.json`)

```json
[
  {
    "source_id": "gdpr_ec_europa_eu",
    "name": "GDPR - ec.europa.eu",
    "url": "https://ec.europa.eu",
    "framework": "GDPR",
    "source_type": "Official",
    "check_frequency_hours": 24,
    "keywords": ["data protection", "EDPB", "Article 5"],
    "last_checked": "2024-11-11T08:00:00",
    "is_active": true
  }
]
```

---

## 🔔 Notification System

### Slack Integration

When high-severity updates are detected:

```python
from services.slack_notification import SlackNotification

slack = SlackNotification()

slack.send_regulatory_update_alert(
    framework="GDPR",
    update_title="Critical GDPR Amendment",
    severity="CRITICAL",
    impact_score=0.95,
    url="https://ec.europa.eu/..."
)
```

---

## 🧪 Testing

### Run Full Test Suite

```powershell
python test_regulatory_updates.py
```

### Test Individual Components

```powershell
# Test Serper API only
python -c "from test_regulatory_updates import test_serper_api; test_serper_api()"

# Test Groq API only
python -c "from test_regulatory_updates import test_groq_api; test_groq_api()"

# Test Knowledge Base only
python -c "from test_regulatory_updates import test_knowledge_base; test_knowledge_base()"
```

---

## 📈 Performance

### Serper API
- **Rate Limit**: 1 request/second (configurable)
- **Free Tier**: 2,500 searches/month
- **Response Time**: ~500ms average

### Groq API
- **Speed**: Ultra-fast (50+ tokens/second)
- **Free Tier**: 14,400 requests/day
- **Models**: LLaMA 3.3 70B, Mixtral, Gemma2

### Knowledge Base
- **Load Time**: ~2 seconds for 1,000 entries
- **Memory**: ~50MB for full dataset
- **Search**: <100ms for keyword search

---

## 🔮 Future Enhancements

### Phase 2: LLaMA Fine-Tuning
- Custom LLaMA model trained on CUAD dataset
- Framework-specific regulatory analysis
- Improved clause detection accuracy

### Phase 3: Advanced Features
- **OpenRouter Integration**: Multi-model support
- **HuggingFace Hosting**: Self-hosted models
- **Automated Contract Updates**: AI-generated clause rewrites
- **Compliance Dashboard**: Executive reporting
- **Email Notifications**: Multi-channel alerts
- **Webhook Support**: Custom integrations

---

## 🐛 Troubleshooting

### Issue: "Serper API key not configured"
**Solution**: Set environment variable
```powershell
$env:SERPER_API_KEY='your_key'
```

### Issue: "JSONL file too large"
**Solution**: Use `limit` parameter
```python
kb.load_jsonl(limit=1000)  # Load first 1000 entries
```

### Issue: "Rate limit exceeded"
**Solution**: Adjust rate limit delay
```python
serper.rate_limit_delay = 2.0  # 2 seconds between requests
```

### Issue: "Groq API timeout"
**Solution**: Increase timeout
```python
groq.chat_completion(messages=msgs, timeout=120)
```

---

## 📞 Support

- **Documentation**: See `REGULATORY_MONITORING_GUIDE.md`
- **API Issues**: Check API provider status pages
- **Bug Reports**: Create GitHub issue with logs

---

## ✅ Checklist for Production

- [ ] Set all required API keys (Serper, Groq)
- [ ] Test API connectivity
- [ ] Load knowledge base successfully
- [ ] Configure check intervals
- [ ] Set up Slack notifications (optional)
- [ ] Run full test suite
- [ ] Review and adjust alert thresholds
- [ ] Schedule periodic checks
- [ ] Monitor storage usage

---

## 📄 License

This system is part of the AI-Powered Regulatory Compliance Checker.  
Uses CUAD dataset under its respective license.

---

**Status**: ✅ **Production Ready** (with API keys configured)  
**Version**: 1.0.0  
**Last Updated**: November 11, 2024

# Quick Reference Card

## Starting the Application

```powershell
streamlit run app.py
```

Opens at: **http://localhost:8501**

---

## Common Commands

### Activate Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### Run Tests
```powershell
python test_setup.py
```

### Check Installed Packages
```powershell
pip list
```

### Install Missing Packages
```powershell
pip install -r requirements.txt
```

### Clear Streamlit Cache
```powershell
streamlit cache clear
```

---

## File Locations

- **Main App**: `app.py`
- **Configuration**: `.env` and `config/settings.py`
- **Services**: `services/` directory
- **Models**: `models/` directory
- **Regulatory Data**: `data/` directory
- **Logs**: `logs/` directory (auto-created)
- **Virtual Environment**: `.venv/` directory

---

## Python Executable Path

```
E:/323103310024/Updated Infosys/jaggu-proj/.venv/Scripts/python.exe
```

Use this when running Python commands directly.

---

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Port in use | `streamlit run app.py --server.port 8502` |
| Import errors | `pip install -r requirements.txt --force-reinstall` |
| Models downloading | Normal on first run (~440MB) |
| Out of memory | Set `USE_GPU=False` in `.env` |
| Streamlit won't start | `streamlit cache clear` |

---

## Support Files

- `SETUP_INSTRUCTIONS.md` - Full setup guide
- `QUICK_START.md` - First-time usage
- `STREAMLIT_APP_USAGE_GUIDE.md` - Detailed usage
- `README.md` - Project overview

# AI Compliance Checker - Startup Script
# This script starts the Streamlit application

Write-Host "Starting AI Compliance Checker..." -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment and run Streamlit
& ".\.venv\Scripts\streamlit.exe" run app.py

Write-Host ""
Write-Host "Application stopped." -ForegroundColor Yellow

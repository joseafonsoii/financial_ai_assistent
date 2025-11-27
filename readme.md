# 🧠 Financial AI Assistant

#  Author

A sophisticated AI-powered financial assistant with real-time stock analysis, portfolio management, and financial calculations.

## 🚀 Features

- **Stock Analysis**: Real-time stock prices and historical data
- **Portfolio Management**: Investment performance tracking  
- **Financial Calculations**: Compound interest, loan payments, ROI
- **Market News**: Latest financial news updates
- **AI-Powered**: Google Gemini integration for intelligent responses

## 🏗️ Tech Stack

- **Backend**: Flask + LangGraph + Google Gemini
- **Frontend**: React + Vite + Lucide Icons
- **AI Model**: Gemini 2.0 Flash
- **Data Sources**: Alpha Vantage, Yahoo Finance, Google News RSS

## 📦 Installation

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python app.py
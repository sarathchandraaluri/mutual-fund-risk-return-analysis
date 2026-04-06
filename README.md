# 📊 Mutual Fund Analytics & Portfolio Optimization Tool

## 📌 Project Overview

This project is a **data-driven mutual fund analysis tool** that allows users to:

- Select mutual funds dynamically (no manual codes)
- Analyze performance based on different timeframes
- Compare multiple funds
- Evaluate risk-adjusted returns using Sharpe Ratio
- Get portfolio allocation suggestions

The tool uses **real-time NAV data** from external APIs and provides actionable insights for investment decisions.

---

## 🚀 Features

### 🔹 Fund Selection
- Choose from a live list of mutual funds
- No need to input scheme codes manually

### 🔹 Timeframe Analysis
- 3 Months  
- 1 Year  
- 2 Years  
- 3 Years  
- 5 Years  

### 🔹 Performance Metrics
- 📈 Annualized Return  
- 📉 Risk (Volatility)  
- ⚖️ Sharpe Ratio  

### 🔹 Multi-Fund Comparison
- Compare multiple funds simultaneously
- View results in a structured table

### 🔹 Best Fund Recommendation
- Automatically selects the best fund
- Based on highest Sharpe Ratio

### 🔹 Portfolio Allocation
- Suggests weights for selected funds
- Based on risk-adjusted performance

---

## 🧠 Methodology

The tool performs the following operations:

1. Fetches real-time NAV data using API  
2. Cleans and processes data  
3. Calculates daily returns  
4. Computes:
   - Annualized Return
   - Standard Deviation (Risk)
   - Sharpe Ratio  
5. Ranks funds based on performance  
6. Allocates portfolio weights proportionally  

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** (UI & deployment)
- **Pandas** (data processing)
- **NumPy** (calculations)
- **Requests** (API integration)

---

## 🌐 Live Data Source

- Mutual Fund API: https://api.mfapi.in/

---

## ▶️ How to Run Locally

1. Clone the repository:
```bash
git clone https://github.com/your-username/mutual-fund-tool.git
cd mutual-fund-tool

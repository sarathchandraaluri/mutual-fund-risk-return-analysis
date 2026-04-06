import streamlit as st
import pandas as pd
import requests
import numpy as np
from datetime import timedelta

st.set_page_config(page_title="Mutual Fund Tool", layout="wide")

st.title("📊 Mutual Fund Analytics & Portfolio Tool")

# -----------------------------
# FETCH FUND LIST
# -----------------------------
@st.cache_data
def get_fund_list():
    url = "https://api.mfapi.in/mf"
    data = requests.get(url).json()
    return pd.DataFrame(data)

fund_df = get_fund_list()

# -----------------------------
# MULTI SELECT FUNDS
# -----------------------------
selected_funds = st.multiselect(
    "Select Mutual Funds",
    fund_df['schemeName']
)

# -----------------------------
# TIMEFRAME
# -----------------------------
timeframe = st.selectbox(
    "Select Timeframe",
    ["3 Months", "1 Year", "2 Years", "3 Years", "5 Years"]
)

results = []

# -----------------------------
# PROCESS EACH FUND
# -----------------------------
for fund in selected_funds:

    scheme_code = fund_df[fund_df['schemeName'] == fund]['schemeCode'].values[0]

    url = f"https://api.mfapi.in/mf/{scheme_code}"
    data = requests.get(url).json()

    df = pd.DataFrame(data['data'])

    df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')

    df = df.dropna().sort_values("date")

    # -----------------------------
    # TIME FILTER
    # -----------------------------
    today = df['date'].max()

    if timeframe == "3 Months":
        cutoff = today - timedelta(days=90)
    elif timeframe == "1 Year":
        cutoff = today - timedelta(days=365)
    elif timeframe == "2 Years":
        cutoff = today - timedelta(days=730)
    elif timeframe == "3 Years":
        cutoff = today - timedelta(days=1095)
    elif timeframe == "5 Years":
        cutoff = today - timedelta(days=1825)

    df = df[df['date'] >= cutoff]

    # -----------------------------
    # CALCULATIONS
    # -----------------------------
    df['returns'] = df['nav'].pct_change()

    avg_return = df['returns'].mean() * 252
    risk = df['returns'].std() * np.sqrt(252)
    rf = 0.06

    sharpe = (avg_return - rf) / risk

    results.append({
        "Fund": fund,
        "Return": avg_return,
        "Risk": risk,
        "Sharpe": sharpe
    })

# -----------------------------
# DISPLAY RESULTS
# -----------------------------
if results:

    result_df = pd.DataFrame(results)

    st.subheader("📊 Comparison Table")
    st.dataframe(result_df.style.format({
        "Return": "{:.2%}",
        "Risk": "{:.2%}",
        "Sharpe": "{:.2f}"
    }))

    # -----------------------------
    # BEST FUND
    # -----------------------------
    best = result_df.loc[result_df['Sharpe'].idxmax()]

    st.subheader("🏆 Best Fund Recommendation")
    st.success(f"""
    Best Fund: {best['Fund']}

    ✔ Sharpe Ratio: {best['Sharpe']:.2f}  
    ✔ Better risk-adjusted return
    """)

    # -----------------------------
    # PORTFOLIO ALLOCATION
    # -----------------------------
    st.subheader("📊 Portfolio Allocation")

    sharpe_values = result_df['Sharpe'].clip(lower=0)

    if sharpe_values.sum() == 0:
        weights = [1/len(sharpe_values)] * len(sharpe_values)
    else:
        weights = sharpe_values / sharpe_values.sum()

    result_df['Weight'] = weights

    st.dataframe(result_df.style.format({
        "Return": "{:.2%}",
        "Risk": "{:.2%}",
        "Sharpe": "{:.2f}",
        "Weight": "{:.2%}"
    }))

    st.success("Portfolio weights based on Sharpe Ratio")

    # -----------------------------
    # VISUALIZATION
    # -----------------------------
    st.subheader("📈 Risk vs Return Chart")
    chart_df = result_df.set_index("Fund")[["Return", "Risk"]]
    st.bar_chart(chart_df)

else:
    st.warning("Please select at least one fund")
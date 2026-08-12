import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Earnings Language Analyzer", layout="wide")

st.title("📊 Earnings Call Language Analyzer")

st.markdown("""
This dashboard analyzes whether management language in earnings calls predicts 
future stock returns. It compares **prepared remarks** (scripted, sanitized) 
with **Q&A sessions** (unscripted, revealing).
""")

# Try to load the dataset
try:
    df = pd.read_csv("./output/dataset.csv")
except FileNotFoundError:
    st.error("❌ Dataset not found. Run `python3 build_dataset.py` first.")
    st.stop()

# Summary metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Calls Analyzed", len(df))

with col2:
    st.metric("Companies", df["ticker"].nunique())

with col3:
    avg_return = df["return_60d"].mean()
    st.metric("Avg 60-day Return", f"{avg_return:.2f}%")

st.divider()

# Section 1: Sentiment Comparison
st.subheader("1️⃣ Sentiment: Prepared Remarks vs Q&A")

st.caption("""
Prepared remarks are written by IR and legal teams — uniformly positive. 
Q&A is live and unscripted. The gap between them reveals true confidence.
""")

sentiment_data = df.set_index("ticker")[["sentiment_prepared", "sentiment_qa"]].round(2)
st.bar_chart(sentiment_data)

st.write("""
**What you're seeing:**
- Higher scores = more positive language
- Notice which companies sound better off-script vs on-script
- Large gaps suggest confidence differences
""")

st.divider()

# Section 2: Does sentiment predict returns?
st.subheader("2️⃣ Does Language Predict Returns?")

col1, col2 = st.columns(2)

with col1:
    st.write("**Sentiment Gap vs 60-day Return**")
    st.scatter_chart(df, x="sentiment_gap", y="return_60d", color="ticker", height=400)

with col2:
    st.write("**Hedging in Q&A vs 60-day Return**")
    st.scatter_chart(df, x="hedging_qa", y="return_60d", color="ticker", height=400)

st.info("""
**Key insight:** 
With n=12 data points, these correlations are too small to prove anything.
See the README for why this is expected and what real evidence would require.
""")

st.divider()

# Section 3: Raw Data
st.subheader("3️⃣ Full Dataset")

# Format for display
display_df = df[[
    "ticker", "quarter", "call_date",
    "sentiment_prepared", "sentiment_qa", "sentiment_gap",
    "confidence_qa", "hedging_qa", "return_60d"
]].round(3)

st.dataframe(display_df, use_container_width=True)

st.divider()

# Section 4: Key Findings
st.subheader("📌 Key Findings")

st.warning("""
**n = 12 calls.** This sample is too small to establish real relationships. 
All correlations tested were near zero (p > 0.76). This is a null result, 
and null results are real results.

**What this means:**
- The pipeline works end-to-end ✓
- The hypothesis (language predicts returns) is not supported in this data
- A real test would need 200+ calls across multiple years and sectors
- This is an honest, reproducible finding
""")

st.info("""
**For a college application, the story is:**

"I built a full NLP pipeline that analyzes earnings call language using Claude API.
I tested whether management tone predicts stock returns on 12 semiconductor calls.
The result was null (no correlation), which taught me more about statistics than 
a positive result would have. I understand what real evidence requires, and my 
code is modular enough to scale when more data is available."
""")

st.divider()

# Section 5: Technical Details
with st.expander("🔧 Technical Details"):
    st.write("""
    **Architecture:**
    - Transcripts → Claude sentiment analysis → SQLite database
    - Stock returns from yfinance (60 trading days forward)
    - Pearson correlation + p-value testing
    
    **Companies:** AMD, NVDA, QCOM, TXN (semiconductors)
    
    **Quarters:** 2025 Q3 – 2026 Q2
    
    **Limitations:**
    - Single sector (semiconductors)
    - Single market regime (AI boom)
    - Limited forward return data (recent calls)
    - Subjective Claude scoring (not validated)
    """)

st.divider()

st.caption("Built with Claude API, yfinance, Streamlit | See GitHub for full code")

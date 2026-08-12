import streamlit as st
import pandas as pd

st.set_page_config(page_title="Earnings Language Analyzer", layout="wide")
st.title("Earnings Call Language vs. Forward Returns")

df = pd.read_csv("output/dataset.csv")

st.metric("Calls analyzed", len(df))

st.subheader("Sentiment: prepared remarks vs. Q&A")
st.caption(
    "Prepared remarks are scripted and reviewed by IR and legal. "
    "Q&A is unscripted. The gap between them is the signal of interest."
)

chart_data = df.set_index("ticker")[["sentiment_prepared", "sentiment_qa"]]
st.bar_chart(chart_data)

st.subheader("Sentiment gap vs. 60-day return")
st.scatter_chart(df, x="sentiment_gap", y="return_60d", color="ticker")

st.subheader("Full data")
st.dataframe(df)

st.warning(
    f"n = {len(df)}. This sample is far too small to establish a real "
    "relationship. Results shown are exploratory only."
)
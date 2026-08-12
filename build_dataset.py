import sqlite3
import pandas as pd
from returns import forward_return

conn = sqlite3.connect("earnings.db")

# Load scores, one row per ticker+quarter with prepared and qa side by side
df = pd.read_sql("SELECT * FROM analyses", conn)

wide = df.pivot_table(
    index=["ticker", "quarter"],
    columns="section",
    values=["sentiment", "confidence", "hedging"],
)
wide.columns = [f"{metric}_{section}" for metric, section in wide.columns]
wide = wide.reset_index()

# Attach call dates
calls = pd.read_csv("calls.csv")
merged = wide.merge(calls, on=["ticker", "quarter"], how="inner")

print(f"{len(merged)} calls matched to dates.")

# The headline feature: how much does tone drop when the script ends?
merged["sentiment_gap"] = merged["sentiment_qa"] - merged["sentiment_prepared"]
merged["hedging_gap"] = merged["hedging_qa"] - merged["hedging_prepared"]

# Fetch returns
print("Downloading prices...")
returns = []
for _, row in merged.iterrows():
    r = forward_return(row["ticker"], row["call_date"], trading_days=60)
    print(f"  {row['ticker']} {row['quarter']}: {r}")
    returns.append(r)

merged["return_60d"] = returns

merged = merged.dropna(subset=["return_60d"])
merged.to_csv("output/dataset.csv", index=False)

print(f"\nSaved {len(merged)} complete rows to output/dataset.csv")
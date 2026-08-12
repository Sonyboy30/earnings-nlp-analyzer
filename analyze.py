import pandas as pd
from scipy import stats

df = pd.read_csv("output/dataset.csv")

print(f"Sample size: n = {len(df)}\n")

features = [
    "sentiment_prepared",
    "sentiment_qa",
    "sentiment_gap",
    "confidence_qa",
    "hedging_qa",
    "hedging_gap",
]

print(f"{'feature':22} {'corr':>7} {'p-value':>9}  {'reading'}")
print("-" * 60)

for feature in features:
    sub = df[[feature, "return_60d"]].dropna()
    if len(sub) < 5:
        continue

    r, p = stats.pearsonr(sub[feature], sub["return_60d"])

    if p < 0.05:
        reading = "significant (but check n!)"
    elif p < 0.20:
        reading = "suggestive"
    else:
        reading = "noise"

    print(f"{feature:22} {r:>7.3f} {p:>9.3f}  {reading}")

print("\n--- Averages by tone of Q&A ---")
if "tone_qa" in df.columns:
    print(df.groupby("tone_qa")["return_60d"].agg(["mean", "count"]))
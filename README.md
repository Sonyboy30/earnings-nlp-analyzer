# Earnings Call NLP Analyzer

A pipeline that analyzes the language of earnings call transcripts to test whether management tone predicts stock returns.

## The Insight

Most "earnings sentiment" projects analyze the entire transcript as one blob. **This one splits prepared remarks from Q&A.**

Prepared remarks are written by lawyers and IR teams — they're sanitized and uniformly positive. The Q&A is unscripted, and that's where hedging, deflection, and evasion show up.

By comparing the two sections, you can measure **how much more confident (or evasive) management gets when questioned.**

## How It Works

```
Transcripts (PDF/text)
       ↓
[PDF extraction if needed]
       ↓
Split into prepared remarks + Q&A
       ↓
Send each section to Claude
       ↓
Claude scores:
  - sentiment (-1.0 to 1.0)
  - confidence (0.0 to 1.0)
  - hedging count (integer)
  - forward-looking tone
       ↓
Join with stock returns (60 days forward)
       ↓
Test correlation
```

## The Results

**Sample size: n = 12 calls** (16 files, 4 without enough forward price history)

| Feature | Correlation | P-value | Interpretation |
|---|---|---|---|
| sentiment_prepared | -0.087 | 0.788 | noise |
| sentiment_qa | -0.096 | 0.766 | noise |
| sentiment_gap | -0.047 | 0.885 | noise |
| confidence_qa | -0.049 | 0.880 | noise |
| hedging_qa | -0.097 | 0.764 | noise |
| hedging_gap | -0.065 | 0.841 | noise |

**Translation:** No relationship between any measure of language and subsequent 60-day returns.

## Why You Shouldn't Believe This

1. **n = 12 is too small.** With 12 data points, you can find spurious correlations in random noise. A real test requires 200+ calls across multiple years and sectors.

2. **Multiple comparisons problem.** I tested 6 features. With pure random data, you'd expect roughly one to show p < 0.20 by chance alone. Every result here is above 0.76.

3. **Single sector, single time period.** All calls are from semiconductors in 2025-2026, during a specific market regime (AI boom). Results won't generalize.

4. **60-day window is arbitrary.** Maybe the signal appears at 20 days or 120 days. Haven't tested.

5. **Claude's scoring might be noisy.** The model is consistent, but it's still making subjective judgments about "confidence" and "hedging." Ground truth would require human annotation and inter-rater reliability testing.

## What Would Actually Prove This

To turn this into real evidence:

- **Scale to 500+ calls** across 5+ years and multiple sectors
- **Holdout test:** Train on 2020-2023 data, test untouched on 2024-2025
- **Control for market regime:** Compare semiconductor call language to semiconductor sector returns, not absolute returns
- **Validate Claude's scoring:** Have humans label 50 random snippets as "hedged" or "direct," measure agreement
- **Multiple time horizons:** Test 20, 60, 120 day returns
- **Adjust for multiple comparisons:** Use Bonferroni correction or pre-register hypotheses

## What This Project Actually Shows

This is a **working pipeline for analyzing earnings language at scale.** The fact that it found no signal is valuable — it's a null result, and null results are real results.

The code is modular and reusable. Scaling it to 500 calls would be straightforward (add the Financial Modeling Prep API for transcript collection). The hard part — actually building and validating an analysis system — is done.

## Files

- `split.py` — Separates prepared remarks from Q&A using regex patterns
- `analyzer.py` — Wraps Claude API, sends text, gets structured JSON back
- `database.py` — Caches results in SQLite so re-runs are cheap
- `main.py` — Orchestrates the pipeline
- `pdf_extract.py` — Converts PDF transcripts to plain text
- `returns.py` — Downloads 60-day forward returns via yfinance
- `build_dataset.py` — Joins language scores with returns
- `analyze.py` — Computes correlations and p-values
- `calls.csv` — Metadata (ticker, quarter, call date)

## Running It

```bash
# One-time setup
pip install anthropic yfinance pandas python-dotenv pypdf scipy

# Extract text from any PDFs
python3 pdf_extract.py

# Analyze all transcripts
python3 main.py

# Build dataset and test
python3 build_dataset.py
python3 analyze.py
```

## What's Next

If this were real research:

1. **Automate collection** via Financial Modeling Prep API (gets you to 500+ calls)
2. **Sector-relative returns** instead of absolute returns
3. **Per-question analysis** instead of treating Q&A as one blob
4. **Trend analysis** — does hedging increase across quarters before a bad year?
5. **Holdout validation** to avoid overfitting

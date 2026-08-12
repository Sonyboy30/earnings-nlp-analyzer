import yfinance as yf
from datetime import datetime, timedelta


def forward_return(ticker, call_date, trading_days=60):
    """Percent return over N trading days, starting the day AFTER the call.

    Returns None if there isn't enough price history.
    """
    start = datetime.strptime(call_date, "%Y-%m-%d")
    end = start + timedelta(days=trading_days * 2 + 40)

    try:
        df = yf.Ticker(ticker).history(
            start=start.strftime("%Y-%m-%d"),
            end=end.strftime("%Y-%m-%d"),
            auto_adjust=True,
        )
    except Exception as e:
        print(f"    price download failed for {ticker}: {e}")
        return None

    if df.empty:
        return None

    # Keep only days strictly after the call date
    df = df[df.index.date > start.date()]

    if len(df) < trading_days:
        return None

    entry = float(df["Close"].iloc[0])
    exit_price = float(df["Close"].iloc[trading_days - 1])

    return (exit_price - entry) / entry * 100
import yfinance as yf
import pandas as pd
from get_tickers import get_tickers

def calculate_macd(df):
    # Calculate MACD and Signal line
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def check_bearish_macd_cross():
    tickers = get_tickers()
    bearish_crosses = []

    for ticker in tickers[:100]:  # limit for testing; remove slice for all
        try:
            data = yf.download(ticker, period="2mo", interval="1d", progress=False)
            if data.empty:
                continue

            macd, signal = calculate_macd(data)
            # Check if MACD crossed below Signal on the last day
            if macd.iloc[-2] > signal.iloc[-2] and macd.iloc[-1] < signal.iloc[-1]:
                bearish_crosses.append(ticker)
        except Exception as e:
            print(f"Error processing {ticker}: {e}")

    print(f"Bearish MACD crossovers found: {bearish_crosses}")
    return bearish_crosses

if __name__ == "__main__":
    check_bearish_macd_cross()

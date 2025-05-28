import sys
import os
import yfinance as yf

# Add parent directory to path so get_tickers and telegram_config can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from get_tickers import get_tickers
from telegram_config import send_telegram_message


def calculate_macd(df):
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal


def check_bearish_macd_cross():
    tickers = get_tickers()
    bearish_crosses = []

    for ticker in tickers[:100]:  # Limit for testing; adjust as needed
        try:
            data = yf.download(ticker, period="2mo", interval="1d", progress=False, auto_adjust=True)
            if data.empty or len(data) < 30:
                continue

            macd, signal = calculate_macd(data)

            if macd.iloc[-2] > signal.iloc[-2] and macd.iloc[-1] < signal.iloc[-1]:
                bearish_crosses.append(ticker)
        except Exception as e:
            print(f"Error processing {ticker}: {e}")

    if bearish_crosses:
        message = "📉 Bearish MACD Crossovers Detected:\n\n" + "\n".join(bearish_crosses)
        send_telegram_message(message)
    else:
        print("No bearish crossovers detected.")

    return bearish_crosses


if __name__ == "__main__":
    check_bearish_macd_cross()

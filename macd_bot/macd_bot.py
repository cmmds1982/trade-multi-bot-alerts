import os
import requests
import yfinance as yf
import pandas as pd
from datetime import datetime

def calculate_macd(df):
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    df['MACD'] = macd
    df['Signal'] = signal
    return df

def check_bearish_crossover(df):
    if len(df) < 2:
        return False
    return df['MACD'].iloc[-2] > df['Signal'].iloc[-2] and df['MACD'].iloc[-1] < df['Signal'].iloc[-1]

def send_telegram(message, chat_id=None):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not chat_id:
        chat_id = os.getenv("TELEGRAM_CHAT_ID_MACD")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=payload)
    print(f"Telegram response: {response.text}")

def main():
    # Example ticker list — replace with your dynamic list if you want
    tickers = ["AAPL", "TSLA", "MSFT", "GOOG"]

    for ticker in tickers:
        print(f"Checking {ticker}...")
        df = yf.download(ticker, period="2mo", interval="1d")
        df = calculate_macd(df)

        if check_bearish_crossover(df):
            message = f"📉 Bearish MACD crossover detected for {ticker} on {datetime.now().strftime('%Y-%m-%d')}"
            send_telegram(message)
        else:
            print(f"No bearish crossover for {ticker}")

if __name__ == "__main__":
    main()

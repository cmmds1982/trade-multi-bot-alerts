import yfinance as yf
from datetime import datetime
from telegram_config import send_telegram

def calculate_macd(data):
    short_ema = data['Close'].ewm(span=12, adjust=False).mean()
    long_ema = data['Close'].ewm(span=26, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def get_macd_crossovers(tickers):
    for ticker in tickers:
        try:
            df = yf.download(ticker, period="6mo", interval="1d")
            macd, signal = calculate_macd(df)
            df['MACD'], df['Signal'] = macd, signal
            bull = (df['MACD'].iloc[-1] > df['Signal'].iloc[-1]) and (df['MACD'].iloc[-2] <= df['Signal'].iloc[-2])
            bear = (df['MACD'].iloc[-1] < df['Signal'].iloc[-1]) and (df['MACD'].iloc[-2] >= df['Signal'].iloc[-2])
            if bull or bear:
                direction = "📈 Bullish" if bull else "📉 Bearish"
                send_telegram(f"{ticker} - {direction} MACD crossover on {datetime.now().strftime('%Y-%m-%d')}")
        except Exception as e:
            print(f"Error with {ticker}: {e}")

if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "TSLA"]
    get_macd_crossovers(tickers)


import requests
import pandas as pd
from io import StringIO
import os

def get_tickers_from_private_repo():
    token = os.getenv("G_PAT")  # The name of your secret/env variable
    if not token:
        print("❌ G_PAT environment variable not found.")
        return []

    url = "https://api.github.com/repos/cmmds1982/nasdaq-tickers-fetcher/contents/nasdaq_tickers.csv"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3.raw"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        tickers = df['Ticker'].dropna().tolist()
        print(f"✅ Loaded {len(tickers)} tickers from private GitHub repo.")
        return tickers
    else:
        print(f"❌ Failed to fetch tickers: HTTP {response.status_code}")
        return []

if __name__ == "__main__":
    tickers = get_tickers_from_private_repo()
    # Optional: print first 10 tickers for sanity check
    print("Sample tickers:", tickers[:10])

import os
import requests

def get_tickers():
    token = os.getenv("G_PAT")
    if not token:
        print("❌ G_PAT environment variable not found.")
        return []

    url = "https://api.github.com/repos/cmmds1982/nasdaq-tickers-fetcher/contents/nasdaq_tickers.csv?ref=main"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3.raw"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("✅ Successfully fetched tickers.")
        content = response.text
        # Each line is a ticker symbol (strip empty lines)
        tickers = [line.strip() for line in content.splitlines() if line.strip()]
        print(f"Sample tickers: {tickers[:10]}")
        return tickers
    else:
        print(f"❌ Failed to fetch tickers: HTTP {response.status_code}")
        print("Response:", response.text)
        return []

if __name__ == "__main__":
    get_tickers()

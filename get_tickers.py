import requests

def get_tickers():
    # Public raw URL for your CSV file in main branch
    url = "https://raw.githubusercontent.com/cmmds1982/nasdaq-tickers-fetcher/main/nasdaq_tickers.csv"
    
    response = requests.get(url)
    if response.status_code == 200:
        print("✅ Successfully fetched tickers.")
        content = response.text
        tickers = [line.strip() for line in content.splitlines() if line.strip()]
        print(f"Sample tickers: {tickers[:10]}")
        return tickers
    else:
        print(f"❌ Failed to fetch tickers: HTTP {response.status_code}")
        print("Response:", response.text)
        return []

if __name__ == "__main__":
    get_tickers()

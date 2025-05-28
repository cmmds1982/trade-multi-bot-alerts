import os
import requests

def send_telegram_message(message):
    bot_token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    if not bot_token or not chat_id:
        print("Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID")
        return
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Failed to send message: {response.status_code} - {response.text}")
    else:
        print("Message sent!")

if __name__ == "__main__":
    send_telegram_message("Hello from GitHub Actions test!")

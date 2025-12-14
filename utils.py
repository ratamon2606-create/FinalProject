import requests
import time
import threading

BASE_URL = "https://api.binance.com/api/v3"

def safe_api_call(endpoint, params=None, retries=3):
    """
    ฟังก์ชันสำหรับเรียก API แบบปลอดภัย มีการลองใหม่ (Retry) ถ้าล้มเหลว
    """
    url = f"{BASE_URL}{endpoint}"
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Error ({endpoint}): {e} - Attempt {attempt+1}/{retries}")
            time.sleep(1)
    return None

def fetch_ticker_24hr():
    return safe_api_call("/ticker/24hr")

def fetch_klines(symbol, interval, limit=60):
    params = {"symbol": f"{symbol}USDT", "interval": interval, "limit": limit}
    return safe_api_call("/klines", params)

def fetch_depth(symbol, limit=10):
    params = {"symbol": f"{symbol}USDT", "limit": limit}
    return safe_api_call("/depth", params)

def fetch_recent_trades(symbol, limit=20):
    params = {"symbol": f"{symbol}USDT", "limit": limit}
    return safe_api_call("/trades", params)
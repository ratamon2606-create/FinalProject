import requests
import time
from PIL import Image # ต้อง import Image มาใช้สร้างภาพ

BASE_URL = "https://api.binance.com/api/v3"

# --- [NEW] ส่วนจัดการ Gradient Background ---
def hex_to_rgb(hex_color):
    """แปลงรหัสสี Hex เป็น Tuple RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_gradient_image(width, height, color1_hex, color2_hex):
    """สร้างรูปภาพ Gradient แนวตั้ง"""
    base = Image.new('RGB', (width, height), color1_hex)
    top = Image.new('RGB', (width, height), color2_hex)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base
# ------------------------------------------

def safe_api_call(endpoint, params=None, retries=3):
# ... (โค้ด API เดิมด้านล่างเหมือนเดิม ไม่ต้องแก้) ...
    url = f"{BASE_URL}{endpoint}"
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            time.sleep(1) 
    return None

def fetch_ticker_24hr(): return safe_api_call("/ticker/24hr")
def fetch_klines(symbol, interval, limit=60):
    params = {"symbol": f"{symbol}USDT", "interval": interval, "limit": limit}
    return safe_api_call("/klines", params)
def fetch_depth(symbol, limit=10):
    params = {"symbol": f"{symbol}USDT", "limit": limit}
    return safe_api_call("/depth", params)
def fetch_recent_trades(symbol, limit=20):
    params = {"symbol": f"{symbol}USDT", "limit": limit}
    return safe_api_call("/trades", params)
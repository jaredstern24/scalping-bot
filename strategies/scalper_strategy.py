import requests

def fetch_klines(pair, interval='1min', limit=15):
    url = f"https://api.kucoin.com/api/v1/market/candles?type={interval}&symbol={pair}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        candles = response.json()['data']
        closes = [float(candle[2]) for candle in candles[:limit]]
        closes.reverse()
        return closes
    except Exception as e:
        print(f"Error fetching candles for {pair}: {e}")
        return []

def calculate_rsi(closes, period=14):
    if len(closes) < period:
        return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        delta = closes[i] - closes[i - 1]
        if delta > 0: gains.append(delta)
        else: losses.append(abs(delta))
    if not gains: return 0
    if not losses: return 100
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    return 100 - (100 / (1 + rs))

def check_signal(pair):
    closes = fetch_klines(pair, limit=15)
    if not closes or len(closes) < 14:
        print(f"Not enough data for {pair}")
        return "hold"
    rsi = calculate_rsi(closes)
    print(f"{pair} RSI: {rsi:.2f}")
    if rsi < 30: return "buy"
    elif rsi > 70: return "sell"
    else: return "hold"
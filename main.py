import os
print("✅ main.py loaded")
print("KUCOIN_API_KEY:", os.getenv("KUCOIN_API_KEY"))
print("FORCE_TRADE_MODE:", os.getenv("FORCE_TRADE_MODE"))

import os
import threading
import time
from dotenv import load_dotenv
from strategies.scalper_strategy import check_signal
from utils.kucoin_api import place_order
from utils.logger import log_signal

load_dotenv()

LIVE_MODE = os.getenv("LIVE_MODE", "False") == "True"
FORCE_TRADE_MODE = os.getenv("FORCE_TRADE_MODE", "False") == "True"
TRADING_PAIRS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "XRP-USDT", "DOGE-USDT"]

def trade_worker(pair):
    signal = check_signal(pair)
    log_signal(pair, signal)
    print(f"{pair} signal: {signal.upper()}")
    if LIVE_MODE and (signal in ["buy", "sell"] or FORCE_TRADE_MODE):
        place_order(pair, signal)
        time.sleep(3)

def run_bot():
    while True:
        threads = []
        for pair in TRADING_PAIRS:
            thread = threading.Thread(target=trade_worker, args=(pair,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        time.sleep(10)

if __name__ == "__main__":
    run_bot()

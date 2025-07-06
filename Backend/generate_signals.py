import requests
import datetime

API_KEY = "a24ff933811047d994b9e76f1e9d7280"
BASE_URL = "https://api.twelvedata.com"
PAIRS = [
    "EUR/USD", "USD/JPY", "GBP/USD", "USD/CHF", "USD/CAD",
    "AUD/USD", "NZD/USD", "BTC/USD", "ETH/USD", "XAU/USD"
]

def fetch_macd_ema(symbol):
    params = {
        "symbol": symbol,
        "interval": "1min",
        "apikey": API_KEY,
        "outputsize": 2,
    }

    macd_url = f"{BASE_URL}/macd"
    ema_url = f"{BASE_URL}/ema"

    macd_params = params.copy()
    macd_params.update({"series_type": "close", "fast_period": 12, "slow_period": 26, "signal_period": 9})

    ema_params = params.copy()
    ema_params.update({"series_type": "close", "time_period": 21})

    macd_data = requests.get(macd_url, params=macd_params).json()
    ema_data = requests.get(ema_url, params=ema_params).json()

    return macd_data, ema_data

def generate_latest_signals():
    signals = []
    for pair in PAIRS:
        macd_data, ema_data = fetch_macd_ema(pair)

        try:
            macd = float(macd_data["values"][0]["macd"])
            signal_line = float(macd_data["values"][0]["signal"])
            ema = float(ema_data["values"][0]["ema"])
            close_price = float(macd_data["values"][0]["close"])

            if macd > signal_line and close_price > ema:
                action = "Buy"
            elif macd < signal_line and close_price < ema:
                action = "Sell"
            else:
                continue

            strength = min(100, abs(macd - signal_line) * 100)
            signals.append({
                "pair": pair,
                "action": action,
                "strength": round(strength),
                "price": close_price,
                "time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            })
        except Exception as e:
            print(f"⚠️ Failed to process {pair}: {e}")
            continue

    return signals

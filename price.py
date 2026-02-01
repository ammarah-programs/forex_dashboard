import requests
import os
import time
import streamlit as st

TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")
BASE_URL = "https://api.twelvedata.com"

# --------------------------------------------------
# INTERNAL HELPER (cached)
# --------------------------------------------------
@st.cache_data(ttl=60)
def _get_pair_percent(symbol: str):
    """Fetch percent_change for a single FX pair"""

    if not symbol or not isinstance(symbol, str):
        return None

    clean_symbol = symbol.strip()


    try:
        r = requests.get(
            f"{BASE_URL}/quote",
            params={
                "symbol": clean_symbol,
                "apikey": TWELVE_DATA_API_KEY
            },
            timeout=10
        )

        data = r.json()
        
        pct = data.get("percent_change")
        return float(pct) if pct is not None else None

    except Exception:
        return None


# --------------------------------------------------
# PUBLIC FUNCTION
# --------------------------------------------------
def get_price_movement(symbol: str):
    """
    Returns percentage movement for:
    - FX pairs
    - DXY (proxy using weighted FX basket)
    """

    if not symbol or not isinstance(symbol, str):
        return None

    symbol = symbol.upper().strip()
    # 🔒 Ensure valid Twelve Data FX symbol
    if "/" not in symbol and len(symbol) == 6:
        symbol = f"{symbol[:3]}/{symbol[3:]}"
    print("FINAL SYMBOL SENT TO TWELVE:", symbol)


    # --------------------------------------------------
    # ✅ DXY PROXY (CACHED)
    # --------------------------------------------------
    if symbol == "DXY":
        eurusd = _get_pair_percent("EUR/USD")
        gbpusd = _get_pair_percent("GBP/USD")
        usdjpy = _get_pair_percent("USD/JPY")

        if None in (eurusd, gbpusd, usdjpy):
            return None

        proxy_change = (
            (-eurusd * 0.576) +
            (-gbpusd * 0.119) +
            (usdjpy * 0.136)
        )

        proxy_change = round(proxy_change, 2)

        return {
            "percent": abs(proxy_change),
            "direction": "up" if proxy_change > 0 else "down" if proxy_change < 0 else "flat"
        }

    # --------------------------------------------------
    # ✅ NORMAL FX PAIRS
    # --------------------------------------------------
    pct = _get_pair_percent(symbol)

    if pct is None:
        return None

    pct = round(pct, 2)

    return {
        "percent": abs(pct),
        "direction": "up" if pct > 0 else "down" if pct < 0 else "flat"
    }

"""
The Saac Terminal - Yahoo Finance Market Data Provider
Fetches live and historical price quotes for any ticker symbol with fallback datasets.
"""

import urllib.request
import json
from typing import Dict, Any, Optional

def fetch_live_quote(symbol: str) -> Optional[Dict[str, Any]]:
    """
    Fetches real-time market quote from Yahoo Finance API v8.
    """
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?interval=1m&range=1d"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            result = data.get("chart", {}).get("result", [])
            if not result:
                return None
            meta = result[0].get("meta", {})
            return {
                "symbol": meta.get("symbol", symbol),
                "regularMarketPrice": meta.get("regularMarketPrice", 0.0),
                "previousClose": meta.get("previousClose", 0.0),
                "currency": meta.get("currency", "USD"),
                "exchangeName": meta.get("exchangeName", "")
            }
    except Exception:
        return None

def fetch_multi_quotes(symbols: list) -> Dict[str, Dict[str, Any]]:
    """
    Fetches quotes for a list of ticker symbols.
    """
    results = {}
    for s in symbols:
        q = fetch_live_quote(s)
        if q:
            results[s] = q
    return results

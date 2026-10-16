"""
The Saac Terminal - Universal Financial Analytics
Mathematical calculations for price changes, returns, drawdowns, and formatting.
"""

from typing import List, Dict, Any, Tuple

def calculate_return(start_val: float, end_val: float) -> Tuple[float, float]:
    """
    Returns (percentage_return, absolute_delta).
    """
    if not start_val or start_val == 0:
        return 0.0, 0.0
    abs_delta = end_val - start_val
    pct_return = (abs_delta / start_val) * 100.0
    return pct_return, abs_delta

def calculate_high_low(series: List[Dict[str, Any]], key: str = "close") -> Tuple[float, float, float]:
    """
    Returns (min_val, max_val, spread).
    """
    if not series:
        return 0.0, 0.0, 0.0
    vals = [float(item.get(key, item.get("close", 0))) for item in series if item.get(key) is not None or item.get("close") is not None]
    if not vals:
        return 0.0, 0.0, 0.0
    min_v = min(vals)
    max_v = max(vals)
    return min_v, max_v, max_v - min_v

def calculate_max_drawdown(series: List[Dict[str, Any]], key: str = "close") -> float:
    """
    Computes maximum peak-to-trough drop percentage across the series.
    """
    if not series:
        return 0.0
    peak = -float("inf")
    max_dd = 0.0
    for item in series:
        val = float(item.get(key, item.get("close", 0)))
        if val > peak:
            peak = val
        if peak > 0:
            dd = ((val - peak) / peak) * 100.0
            if dd < max_dd:
                max_dd = dd
    return max_dd

def format_currency(val: float, symbol: str = "$", decimals: int = 2) -> str:
    if val is None:
        return f"{symbol}0.00"
    return f"{symbol}{val:,.{decimals}f}"

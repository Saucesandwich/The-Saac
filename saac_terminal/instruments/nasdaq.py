"""
The Saac Terminal - Nasdaq Composite & Tech Equity Instrument
Implements the universal Instrument schema for tech indices (^IXIC, QQQ).
"""

from typing import Dict, Any
from ..core.instrument import InstrumentConfig, SecondarySeriesConfig

NASDAQ_HISTORICAL_RECORDS = [
    {"date": "1990-01", "close": 420.0, "qqq": 10.2, "us10y": 8.43, "event": "Early 90s Tech Baseline"},
    {"date": "1995-01", "close": 750.0, "qqq": 18.3, "us10y": 7.59, "event": "Netscape & Commercial Web Genesis"},
    {"date": "1998-10", "close": 1770.0, "qqq": 43.1, "us10y": 4.41, "event": "Dot-Com Parabolic Acceleration"},
    {"date": "2000-03", "close": 5048.6, "qqq": 120.5, "us10y": 6.03, "event": "Dot-Com Mania Peak ($5,048.62 ATH)"},
    {"date": "2002-10", "close": 1114.1, "qqq": 20.1, "us10y": 3.82, "event": "Dot-Com Bust Trough (-78% Decline)"},
    {"date": "2007-10", "close": 2859.1, "qqq": 54.2, "us10y": 4.77, "event": "Pre-GFC Multi-Year Expansion High"},
    {"date": "2009-03", "close": 1268.6, "qqq": 25.5, "us10y": 2.84, "event": "Great Financial Crisis Generational Low"},
    {"date": "2015-06", "close": 5106.6, "qqq": 111.0, "us10y": 2.37, "event": "Breakout Past Year 2000 Peak After 15 Years"},
    {"date": "2020-03", "close": 6860.6, "qqq": 170.2, "us10y": 0.69, "event": "COVID Lockdown Flash Liquidity Dip"},
    {"date": "2021-11", "close": 16057.4, "qqq": 403.9, "us10y": 1.51, "event": "Pandemic Stimulus High ($16,057)"},
    {"date": "2022-10", "close": 10088.8, "qqq": 254.2, "us10y": 4.08, "event": "Fed Rate Hike Compression Cycle Low"},
    {"date": "2024-03", "close": 16379.4, "qqq": 444.0, "us10y": 4.21, "event": "AI Infrastructure Breakout"},
    {"date": "2024-10", "close": 18518.6, "qqq": 490.2, "us10y": 4.28, "event": "Tech Mega-Cap Momentum Run"},
    {"date": "2026-10", "close": 20340.5, "qqq": 495.2, "us10y": 5.217, "event": "Current Verified Market Benchmark"}
]

def calculate_nasdaq_derivatives(pts: float) -> Dict[str, float]:
    """
    Computes derivative metrics for Nasdaq futures and ETF proxies.
    """
    return {
        "micro_futures_notional": pts * 2.0,   # CME MNQ ($2 per index point)
        "emini_futures_notional": pts * 20.0,  # CME NQ ($20 per index point)
        "qqq_proxy": pts / 41.0,
        "est_pe_multiple": pts / 680.0
    }

NASDAQ_INSTRUMENT = InstrumentConfig(
    id="nasdaq",
    symbol="IXIC",
    name="Nasdaq Composite Tech Equity Terminal",
    ticker="^IXIC",
    unit="pts",
    currency="USD",
    theme_color="#00c853",
    default_price=20340.50,
    exchange="NASDAQ Global Select",
    secondary_series=[
        SecondarySeriesConfig(id="qqq", name="Invesco QQQ", ticker="QQQ", unit="$", decimals=2, default_val=495.20),
        SecondarySeriesConfig(id="us10y", name="US 10Y Yield", ticker="^TNX", unit="%", decimals=3, default_val=5.217)
    ],
    historical_records=NASDAQ_HISTORICAL_RECORDS
)

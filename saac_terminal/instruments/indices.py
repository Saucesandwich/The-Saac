"""
The Saac Terminal - Broad Market Benchmark Indices
S&P 500 (^GSPC, SPY, VIX) and macro assets.
"""

from typing import Dict, Any
from ..core.instrument import InstrumentConfig, SecondarySeriesConfig

SP500_HISTORICAL_RECORDS = [
    {"date": "1990-01", "close": 340.0, "spy": 34.0, "us10y": 8.43, "event": "Pre-Gulf War"},
    {"date": "2000-03", "close": 1527.5, "spy": 152.7, "us10y": 6.03, "event": "Dot-Com Peak"},
    {"date": "2002-10", "close": 776.8, "spy": 77.7, "us10y": 3.82, "event": "Tech Bear Market Bottom"},
    {"date": "2007-10", "close": 1565.1, "spy": 156.5, "us10y": 4.77, "event": "Pre-GFC All-Time High"},
    {"date": "2009-03", "close": 676.5, "spy": 67.6, "us10y": 2.84, "event": "Devil's Bottom (666 Intraday Low)"},
    {"date": "2020-03", "close": 2237.4, "spy": 223.7, "us10y": 0.69, "event": "COVID Liquidity Shock Low"},
    {"date": "2022-10", "close": 3577.0, "spy": 357.7, "us10y": 4.08, "event": "2022 Rate Shock Bear Low"},
    {"date": "2024-10", "close": 5850.2, "spy": 585.0, "us10y": 4.28, "event": "All-Time High Expansion"},
    {"date": "2026-10", "close": 5850.2, "spy": 585.0, "us10y": 5.217, "event": "Current Market Benchmark"}
]

SP500_INSTRUMENT = InstrumentConfig(
    id="sp500",
    symbol="SPX",
    name="S&P 500 Large-Cap Macro Terminal",
    ticker="^GSPC",
    unit="pts",
    currency="USD",
    theme_color="#38bdf8",
    default_price=5850.20,
    exchange="S&P Dow Jones Indices",
    secondary_series=[
        SecondarySeriesConfig(id="spy", name="SPDR S&P 500", ticker="SPY", unit="$", decimals=2, default_val=585.0),
        SecondarySeriesConfig(id="vix", name="CBOE Volatility", ticker="^VIX", unit="pts", decimals=2, default_val=15.42)
    ],
    historical_records=SP500_HISTORICAL_RECORDS
)

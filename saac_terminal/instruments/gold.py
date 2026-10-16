"""
The Saac Terminal - Gold & Thai Precious Metals Instrument
Verified CME COMEX GC=F, Bank of Thailand THB=X, CBOE ^TNX, and Thai Gold Traders standards.
"""

from typing import Dict, Any
from ..core.instrument import InstrumentConfig, SecondarySeriesConfig

TROY_OZ_TO_GRAMS = 31.1034768
THAI_BAHT_BAR_GRAMS = 15.244
THAI_BAHT_ORNAMENT_GRAMS = 15.16
THAI_GOLD_PURITY_965 = 0.965

HISTORICAL_RECORDS = [
    {"date": "1990-01", "gold": 410.0, "thb": 25.60, "us10y": 8.43, "event": "Pre-Gulf War"},
    {"date": "1990-08", "gold": 385.0, "thb": 25.45, "us10y": 8.86, "event": "Gulf War Oil Shock"},
    {"date": "1991-01", "gold": 385.0, "thb": 25.50, "us10y": 8.03, "event": "Operation Desert Storm"},
    {"date": "1992-01", "gold": 354.0, "thb": 25.45, "us10y": 7.31, "event": "Post-Cold War Easing"},
    {"date": "1993-01", "gold": 329.0, "thb": 25.40, "us10y": 6.39, "event": "Disinflationary Environment"},
    {"date": "1994-07", "gold": 385.0, "thb": 25.05, "us10y": 7.095, "event": "1994 Great Bond Massacre"},
    {"date": "1995-01", "gold": 379.0, "thb": 25.05, "us10y": 7.593, "event": "Mexican Peso Tequila Crisis"},
    {"date": "1996-01", "gold": 399.0, "thb": 25.20, "us10y": 5.581, "event": "US Tech Boom Expansion"},
    {"date": "1997-01", "gold": 355.0, "thb": 25.60, "us10y": 6.503, "event": "Speculative Pressure on Baht"},
    {"date": "1997-06", "gold": 340.0, "thb": 25.80, "us10y": 6.502, "event": "Eve of Baht Unpegging"},
    {"date": "1997-07", "gold": 325.0, "thb": 30.50, "us10y": 6.004, "event": "Tom Yum Kung: July 2 Peg Abandoned"},
    {"date": "1997-10", "gold": 313.0, "thb": 37.80, "us10y": 5.819, "event": "Asian Financial Contagion Spreads"},
    {"date": "1998-01", "gold": 289.0, "thb": 53.80, "us10y": 5.512, "event": "Baht All-Time Low (Intraday 56.10)"},
    {"date": "1998-09", "gold": 288.0, "thb": 40.20, "us10y": 4.410, "event": "Russian Debt Default & LTCM Bailout"},
    {"date": "1999-08", "gold": 256.0, "thb": 38.20, "us10y": 5.979, "event": "Brown Bottom: UK Gold Auction Low ($252)"},
    {"date": "2000-08", "gold": 278.3, "thb": 40.80, "us10y": 5.729, "event": "Dot-Com Peak Bubble Era"},
    {"date": "2001-09", "gold": 292.4, "thb": 44.50, "us10y": 4.575, "event": "September 11 Terror Attacks"},
    {"date": "2002-06", "gold": 313.5, "thb": 42.10, "us10y": 4.824, "event": "Multi-Year Gold Secular Bull Run Inception"},
    {"date": "2003-03", "gold": 335.9, "thb": 42.80, "us10y": 3.823, "event": "US Invasion of Iraq"},
    {"date": "2003-12", "gold": 415.7, "thb": 39.55, "us10y": 4.257, "event": "Gold Breaches $400 / oz Barrier"},
    {"date": "2004-12", "gold": 437.5, "thb": 38.71, "us10y": 4.216, "event": "Commodities Supercycle Expansion"},
    {"date": "2005-12", "gold": 517.1, "thb": 40.93, "us10y": 4.395, "event": "Gold Breaches $500 / oz Milestone"},
    {"date": "2006-05", "gold": 642.5, "thb": 38.08, "us10y": 5.113, "event": "Global Commodities Runup (High $725)"},
    {"date": "2007-07", "gold": 669.4, "thb": 32.52, "us10y": 4.771, "event": "Subprime Mortgage Liquidity Tremors"},
    {"date": "2008-03", "gold": 916.2, "thb": 31.50, "us10y": 3.432, "event": "Bear Stearns Collapse (Intraday $1,014)"},
    {"date": "2008-10", "gold": 716.8, "thb": 34.60, "us10y": 3.970, "event": "Lehman Brothers Bankruptcy GFC Panic"},
    {"date": "2009-01", "gold": 927.3, "thb": 35.46, "us10y": 2.844, "event": "Fed Launches Quantitative Easing (QE1)"},
    {"date": "2009-12", "gold": 1095.2, "thb": 32.93, "us10y": 3.843, "event": "Gold Crosses $1,000 / oz Benchmark"},
    {"date": "2010-06", "gold": 1245.5, "thb": 32.12, "us10y": 2.951, "event": "European Sovereign Debt Crisis Erupts"},
    {"date": "2010-11", "gold": 1385.0, "thb": 29.99, "us10y": 2.797, "event": "Federal Reserve Announces QE2"},
    {"date": "2011-08", "gold": 1828.5, "thb": 31.26, "us10y": 2.218, "event": "S&P Downgrades US Sovereign Rating (AAA->AA+)"},
    {"date": "2011-09", "gold": 1620.4, "thb": 30.51, "us10y": 1.924, "event": "2011 All-Time High Spike ($1,920.70)"},
    {"date": "2012-09", "gold": 1771.1, "thb": 30.70, "us10y": 1.637, "event": "Fed Launches Open-Ended QE3"},
    {"date": "2013-04", "gold": 1472.2, "thb": 30.10, "us10y": 1.675, "event": "Historic Two-Day Gold Flash Crash (-$200)"},
    {"date": "2013-12", "gold": 1202.3, "thb": 32.81, "us10y": 3.026, "event": "Ben Bernanke Announces Fed Taper"},
    {"date": "2015-12", "gold": 1060.3, "thb": 36.00, "us10y": 2.269, "event": "Cyclical Bear Low; Fed First Rate Hike"},
    {"date": "2016-07", "gold": 1349.0, "thb": 34.59, "us10y": 1.458, "event": "UK Brexit Referendum Flight to Safety"},
    {"date": "2018-08", "gold": 1200.3, "thb": 32.26, "us10y": 2.853, "event": "US-China Trade War Escalation"},
    {"date": "2019-06", "gold": 1409.7, "thb": 30.77, "us10y": 2.000, "event": "Gold Breaks 6-Year Ceiling Above $1,400"},
    {"date": "2019-12", "gold": 1519.0, "thb": 29.97, "us10y": 1.919, "event": "Pre-COVID Baseline"},
    {"date": "2020-03", "gold": 1573.0, "thb": 32.40, "us10y": 0.698, "event": "COVID Lockdown Shock (10Y Yield Low: 0.54%)"},
    {"date": "2020-08", "gold": 1978.6, "thb": 31.56, "us10y": 0.693, "event": "Historic ATH $2,075 / oz amid Unlimited QE"},
    {"date": "2021-03", "gold": 1713.8, "thb": 31.17, "us10y": 1.746, "event": "Post-Vaccine Economic Reopening Rotation"},
    {"date": "2021-12", "gold": 1828.6, "thb": 33.33, "us10y": 1.512, "event": "Global Inflation Wave Begins Accelerating"},
    {"date": "2022-03", "gold": 1949.2, "thb": 34.43, "us10y": 2.327, "event": "Russia Invades Ukraine; Gold Spikes to $2,070"},
    {"date": "2022-09", "gold": 1672.0, "thb": 37.87, "us10y": 3.804, "event": "Aggressive Fed 75 bps Rate Hikes"},
    {"date": "2022-10", "gold": 1640.7, "thb": 38.45, "us10y": 4.077, "event": "Baht Touches 16-Year Low at 38.45"},
    {"date": "2023-03", "gold": 1969.0, "thb": 33.96, "us10y": 3.494, "event": "Silicon Valley Bank Collapse Sparks Gold Flight"},
    {"date": "2023-10", "gold": 1983.0, "thb": 36.20, "us10y": 4.875, "event": "US 10-Year Yield Peaks at 5.02% (16-Year High)"},
    {"date": "2024-03", "gold": 2217.4, "thb": 37.00, "us10y": 4.206, "event": "Historic Breakout: Gold Crosses $2,200"},
    {"date": "2024-05", "gold": 2322.9, "thb": 36.73, "us10y": 4.514, "event": "Gold Crosses $2,300 Milestone"},
    {"date": "2024-08", "gold": 2527.6, "thb": 32.35, "us10y": 3.911, "event": "Gold Crosses $2,500; Fed Pivot Anticipation"},
    {"date": "2024-10", "gold": 2749.3, "thb": 33.70, "us10y": 4.284, "event": "All-Time High Run ($2,790 High)"},
    {"date": "2025-02", "gold": 2848.5, "thb": 34.05, "us10y": 4.231, "event": "Central Bank Diversification Buying Wave"},
    {"date": "2025-06", "gold": 3293.2, "thb": 32.71, "us10y": 4.230, "event": "Gold Crosses $3,000 Milestone"},
    {"date": "2025-10", "gold": 3996.5, "thb": 32.30, "us10y": 4.101, "event": "Global Monetary Realignment Rally"},
    {"date": "2026-01", "gold": 4745.1, "thb": 31.23, "us10y": 4.241, "event": "Historic ATH Spike ($5,586 Intraday)"},
    {"date": "2026-06", "gold": 4038.5, "thb": 33.37, "us10y": 4.418, "event": "Post-Spike Market Consolidation"},
    {"date": "2026-08", "gold": 4481.5, "thb": 33.56, "us10y": 4.758, "event": "Summer Safe-Haven Rebound"},
    {"date": "2026-09", "gold": 4186.7, "thb": 33.61, "us10y": 5.293, "event": "High-Level Range Consolidation ($4,186)"},
    {"date": "2026-10", "gold": 4180.6, "thb": 33.52, "us10y": 5.217, "event": "Current Verified Market Benchmark"}
]

def calculate_thai_gold(gold_usd: float, usd_thb: float) -> Dict[str, float]:
    """
    Computes authentic Thai gold metrics using Thai Gold Traders Association standard formulas.
    """
    gold_thb_oz = gold_usd * usd_thb
    pure_gram_thb = gold_thb_oz / TROY_OZ_TO_GRAMS
    pure_gram_usd = gold_usd / TROY_OZ_TO_GRAMS
    thai_bar_thb = pure_gram_thb * THAI_BAHT_BAR_GRAMS * THAI_GOLD_PURITY_965
    thai_ornament_thb = pure_gram_thb * THAI_BAHT_ORNAMENT_GRAMS * THAI_GOLD_PURITY_965

    return {
        "gold_thb_oz": gold_thb_oz,
        "pure_gram_thb": pure_gram_thb,
        "pure_gram_usd": pure_gram_usd,
        "thai_gold_bar": thai_bar_thb,
        "thai_gold_ornament": thai_ornament_thb,
        "kg_bar_usd": pure_gram_usd * 1000.0,
        "kg_bar_thb": pure_gram_thb * 1000.0
    }

GOLD_INSTRUMENT = InstrumentConfig(
    id="gold",
    symbol="XAU",
    name="Gold Futures & Thai Precious Metals Terminal",
    ticker="GC=F",
    unit="oz",
    currency="USD",
    theme_color="#ff9800",
    default_price=4169.30,
    exchange="CME COMEX",
    secondary_series=[
        SecondarySeriesConfig(id="thb", name="USD/THB", ticker="THB=X", unit="฿", decimals=4, default_val=33.56),
        SecondarySeriesConfig(id="us10y", name="US 10Y Yield", ticker="^TNX", unit="%", decimals=3, default_val=5.217)
    ],
    historical_records=HISTORICAL_RECORDS
)

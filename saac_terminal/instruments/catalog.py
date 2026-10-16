"""
The Saac Financial Terminal - Python Multi-Asset Macro Catalog
Registers comprehensive institutional coverage across Commodities, Indices, ETFs, Bonds, and Forex.
Excludes single stocks strictly.
"""

from ..core.instrument import InstrumentConfig, registry
from .gold import GOLD_INSTRUMENT
from .nasdaq import NASDAQ_INSTRUMENT
from .indices import SP500_INSTRUMENT

# Explicit categories
GOLD_INSTRUMENT.category = "commodities"
NASDAQ_INSTRUMENT.category = "indices"
SP500_INSTRUMENT.category = "indices"

# 1. Commodities
SILVER_INSTRUMENT = InstrumentConfig(
    id="silver",
    symbol="XAG",
    name="Silver Spot & Futures Benchmark",
    ticker="SI=F",
    category="commodities",
    unit="oz",
    currency="USD",
    theme_color="#cbd5e1",
    default_price=32.40,
    exchange="CME COMEX Silver Futures (SI=F)"
)

CRUDE_OIL_INSTRUMENT = InstrumentConfig(
    id="crude_oil",
    symbol="CL",
    name="WTI Crude Oil Energy Benchmark",
    ticker="CL=F",
    category="commodities",
    unit="bbl",
    currency="USD",
    theme_color="#ef4444",
    default_price=78.40,
    exchange="NYMEX Light Sweet Crude (CL=F)"
)

NATURAL_GAS_INSTRUMENT = InstrumentConfig(
    id="natural_gas",
    symbol="NG",
    name="Natural Gas Henry Hub Spot",
    ticker="NG=F",
    category="commodities",
    unit="MMBtu",
    currency="USD",
    theme_color="#06b6d4",
    default_price=2.85,
    exchange="NYMEX Henry Hub Natural Gas (NG=F)"
)

COPPER_INSTRUMENT = InstrumentConfig(
    id="copper",
    symbol="HG",
    name="High Grade Copper Futures",
    ticker="HG=F",
    category="commodities",
    unit="lb",
    currency="USD",
    theme_color="#f97316",
    default_price=4.45,
    exchange="CME COMEX High Grade Copper (HG=F)"
)

# 2. Major Indices
DOW_INSTRUMENT = InstrumentConfig(
    id="dowjones",
    symbol="DJI",
    name="Dow Jones Industrial Average",
    ticker="^DJI",
    category="indices",
    unit="pts",
    currency="USD",
    theme_color="#3b82f6",
    default_price=42950.0,
    exchange="S&P Dow Jones Indices (^DJI)"
)

RUSSELL_INSTRUMENT = InstrumentConfig(
    id="russell2000",
    symbol="RUT",
    name="Russell 2000 US Small-Cap Index",
    ticker="^RUT",
    category="indices",
    unit="pts",
    currency="USD",
    theme_color="#8b5cf6",
    default_price=2240.8,
    exchange="FTSE Russell Indices (^RUT)"
)

NIKKEI_INSTRUMENT = InstrumentConfig(
    id="nikkei225",
    symbol="N225",
    name="Nikkei 225 Japan Benchmark",
    ticker="^N225",
    category="indices",
    unit="pts",
    currency="JPY",
    theme_color="#ec4899",
    default_price=38950.0,
    exchange="Tokyo Stock Exchange (^N225)"
)

DAX_INSTRUMENT = InstrumentConfig(
    id="dax40",
    symbol="DAX",
    name="DAX 40 Germany Blue-Chip Index",
    ticker="^GDAXI",
    category="indices",
    unit="pts",
    currency="EUR",
    theme_color="#f59e0b",
    default_price=19480.0,
    exchange="Deutsche Boerse (^GDAXI)"
)

FTSE_INSTRUMENT = InstrumentConfig(
    id="ftse100",
    symbol="FTSE",
    name="FTSE 100 London UK Benchmark",
    ticker="^FTSE",
    category="indices",
    unit="pts",
    currency="GBP",
    theme_color="#0ea5e9",
    default_price=8250.0,
    exchange="London Stock Exchange (^FTSE)"
)

HANGSENG_INSTRUMENT = InstrumentConfig(
    id="hangseng",
    symbol="HSI",
    name="Hang Seng Index (Hong Kong)",
    ticker="^HSI",
    category="indices",
    unit="pts",
    currency="HKD",
    theme_color="#e11d48",
    default_price=20600.0,
    exchange="Hong Kong Exchanges (^HSI)"
)

# 3. ETFs
SPY_INSTRUMENT = InstrumentConfig(
    id="spy",
    symbol="SPY",
    name="SPDR S&P 500 ETF Trust",
    ticker="SPY",
    category="etfs",
    unit="shares",
    currency="USD",
    theme_color="#38bdf8",
    default_price=584.50,
    exchange="NYSE Arca: SPY"
)

QQQ_INSTRUMENT = InstrumentConfig(
    id="qqq",
    symbol="QQQ",
    name="Invesco QQQ Trust (Nasdaq 100)",
    ticker="QQQ",
    category="etfs",
    unit="shares",
    currency="USD",
    theme_color="#00c853",
    default_price=495.20,
    exchange="NASDAQ: QQQ"
)

GLD_INSTRUMENT = InstrumentConfig(
    id="gld",
    symbol="GLD",
    name="SPDR Gold Shares Physical Bullion ETF",
    ticker="GLD",
    category="etfs",
    unit="shares",
    currency="USD",
    theme_color="#ff9800",
    default_price=252.60,
    exchange="NYSE Arca: GLD"
)

AGG_INSTRUMENT = InstrumentConfig(
    id="agg",
    symbol="AGG",
    name="iShares Core US Aggregate Bond ETF",
    ticker="AGG",
    category="etfs",
    unit="shares",
    currency="USD",
    theme_color="#8b5cf6",
    default_price=97.80,
    exchange="NYSE Arca: AGG"
)

USO_INSTRUMENT = InstrumentConfig(
    id="uso",
    symbol="USO",
    name="United States Oil Fund LP",
    ticker="USO",
    category="etfs",
    unit="shares",
    currency="USD",
    theme_color="#ef4444",
    default_price=74.20,
    exchange="NYSE Arca: USO"
)

# 4. Sovereign Country Bonds
US10Y_INSTRUMENT = InstrumentConfig(
    id="us10y",
    symbol="US10Y",
    name="United States 10-Year Treasury Yield",
    ticker="^TNX",
    category="bonds",
    unit="%",
    currency="USD",
    theme_color="#a855f7",
    default_price=5.217,
    exchange="CBOE ^TNX / Federal Reserve Board"
)

US02Y_INSTRUMENT = InstrumentConfig(
    id="us02y",
    symbol="US02Y",
    name="United States 2-Year Treasury Yield",
    ticker="^IRX",
    category="bonds",
    unit="%",
    currency="USD",
    theme_color="#c084fc",
    default_price=4.885,
    exchange="CBOE ^IRX / St. Louis FRED"
)

BUND10Y_INSTRUMENT = InstrumentConfig(
    id="bund10y",
    symbol="BUND10Y",
    name="German 10-Year Government Bund Yield",
    ticker="DE10Y.F",
    category="bonds",
    unit="%",
    currency="EUR",
    theme_color="#eab308",
    default_price=2.215,
    exchange="Deutsche Bundesbank / Eurex"
)

GILT10Y_INSTRUMENT = InstrumentConfig(
    id="gilt10y",
    symbol="GILT10Y",
    name="United Kingdom 10-Year Gilt Yield",
    ticker="GB10Y.L",
    category="bonds",
    unit="%",
    currency="GBP",
    theme_color="#06b6d4",
    default_price=4.185,
    exchange="UK Debt Management Office (DMO)"
)

JGB10Y_INSTRUMENT = InstrumentConfig(
    id="jgb10y",
    symbol="JGB10Y",
    name="Japan 10-Year Government Bond Yield",
    ticker="JP10Y.T",
    category="bonds",
    unit="%",
    currency="JPY",
    theme_color="#f43f5e",
    default_price=0.965,
    exchange="Bank of Japan / Tokyo SE"
)

# 5. Forex & Macro
DXY_INSTRUMENT = InstrumentConfig(
    id="dxy",
    symbol="DXY",
    name="US Dollar Index (Trade-Weighted DXY)",
    ticker="DX-Y.NYB",
    category="forex",
    unit="pts",
    currency="USD",
    theme_color="#10b981",
    default_price=103.45,
    exchange="ICE Futures US: DX"
)

EURUSD_INSTRUMENT = InstrumentConfig(
    id="eurusd",
    symbol="EURUSD",
    name="Euro / US Dollar Currency Pair",
    ticker="EURUSD=X",
    category="forex",
    unit="EUR/USD",
    currency="USD",
    theme_color="#38bdf8",
    default_price=1.0850,
    exchange="Interbank Forex / ECB Reference"
)

USDJPY_INSTRUMENT = InstrumentConfig(
    id="usdjpy",
    symbol="USDJPY",
    name="US Dollar / Japanese Yen Currency Pair",
    ticker="USDJPY=X",
    category="forex",
    unit="JPY",
    currency="JPY",
    theme_color="#ec4899",
    default_price=149.50,
    exchange="Interbank Forex / Bank of Japan"
)

USDTHB_INSTRUMENT = InstrumentConfig(
    id="usdthb",
    symbol="USDTHB",
    name="US Dollar / Thai Baht Forex Exchange",
    ticker="THB=X",
    category="forex",
    unit="THB",
    currency="THB",
    theme_color="#06b6d4",
    default_price=33.560,
    exchange="Bank of Thailand Reference Rate"
)

ALL_CATALOG_INSTRUMENTS = [
    GOLD_INSTRUMENT, SILVER_INSTRUMENT, CRUDE_OIL_INSTRUMENT, NATURAL_GAS_INSTRUMENT, COPPER_INSTRUMENT,
    SP500_INSTRUMENT, NASDAQ_INSTRUMENT, DOW_INSTRUMENT, RUSSELL_INSTRUMENT, NIKKEI_INSTRUMENT, DAX_INSTRUMENT, FTSE_INSTRUMENT, HANGSENG_INSTRUMENT,
    SPY_INSTRUMENT, QQQ_INSTRUMENT, GLD_INSTRUMENT, AGG_INSTRUMENT, USO_INSTRUMENT,
    US10Y_INSTRUMENT, US02Y_INSTRUMENT, BUND10Y_INSTRUMENT, GILT10Y_INSTRUMENT, JGB10Y_INSTRUMENT,
    DXY_INSTRUMENT, EURUSD_INSTRUMENT, USDJPY_INSTRUMENT, USDTHB_INSTRUMENT
]

def register_all():
    for inst in ALL_CATALOG_INSTRUMENTS:
        registry.register(inst)

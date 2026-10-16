# MASTER IMPLEMENTATION PLAN: MULTI-ASSET FINANCIAL TERMINAL

## Goal Overview
Transform the terminal from a gold-centric interface into a comprehensive, multi-asset institutional terminal. Gold will become one tracker among a full suite of macro asset classes. No individual stocks—only major index funds, ETFs, commodities, sovereign country bond yields, and forex/macro pairs. Below every tracker, an automated news and major market catalyst feed will update dynamically whenever the terminal is opened.

---

## 1. Tracker Categorization & Universe

### A. Major Index Funds & Benchmarks
- **S&P 500 Index** (`^GSPC` / SPX)
- **Nasdaq 100 / Composite** (`^IXIC` / `^NDX` / NDX)
- **Dow Jones Industrial Average** (`^DJI` / DJI)
- **Russell 2000 US Small-Caps** (`^RUT` / RUT)
- **Nikkei 225 (Japan)** (`^N225` / N225)
- **FTSE 100 (UK)** (`^FTSE` / FTSE)
- **DAX 40 (Germany)** (`^GDAXI` / DAX)
- **Hang Seng Index (Hong Kong/China)** (`^HSI` / HSI)

### B. Benchmark ETFs
- **SPY**: SPDR S&P 500 ETF Trust
- **QQQ**: Invesco Nasdaq 100 ETF
- **IWM**: iShares Russell 2000 ETF
- **VTI**: Vanguard Total Stock Market ETF
- **AGG**: iShares Core U.S. Aggregate Bond ETF
- **GLD**: SPDR Gold Shares ETF
- **USO**: United States Oil Fund
- **EEM**: iShares MSCI Emerging Markets ETF

### C. Core Commodities
- **Gold** (`GC=F` / XAU) - preserved with full CME COMEX and Thai Gold conversions
- **Silver** (`SI=F` / XAG) - COMEX Silver & Gold/Silver Ratio
- **WTI Crude Oil** (`CL=F`) - NYMEX Light Sweet Crude
- **Brent Crude Oil** (`BZ=F`) - ICE Global Benchmark
- **Natural Gas** (`NG=F`) - Henry Hub Pipeline Spot
- **Copper** (`HG=F`) - "Doctor Copper" Economic Activity Bellwether

### D. Sovereign Country Bonds & Yields
- **US 10-Year Treasury Yield** (`^TNX` / US10Y)
- **US 2-Year Treasury Yield** (`^IRX` / US02Y) & 2Y/10Y Yield Curve Spread
- **German 10-Year Bund Yield** (Eurozone Risk-Free Benchmark)
- **UK 10-Year Gilt Yield** (Bank of England Benchmark)
- **Japan 10-Year JGB Yield** (Bank of Japan YCC Benchmark)

### E. Currencies & Macro
- **US Dollar Index** (`DX-Y.NYB` / DXY)
- **EUR/USD** (Euro / US Dollar)
- **USD/JPY** (US Dollar / Japanese Yen)
- **USD/THB** (US Dollar / Thai Baht)

---

## 2. Automated Live News & Macro Catalyst Feed (Bottom Section)

### Core Requirement
When navigating into any specific tracker, directly below the chart, comparison banner, and metric tables, there must be an automatically updating news and market events component. It must update automatically every time the program is opened without manual entry.

### Technical Implementation
1. **Automated Live Feed Engine (`src/js/services/news_service.js`)**:
   - Queries real-time financial RSS/APIs for the active symbol:
     - Primary: Yahoo Finance RSS headline feed (`https://feeds.finance.yahoo.com/rss/2.0/headline?s={TICKER}`)
     - Secondary: Google News RSS financial search (`https://news.google.com/rss/search?q={ASSET}+market+when:30d`)
   - Uses zero-auth CORS proxies (`corsproxy.io`, `api.allorigins.win`) with automatic failover.
   - Parses XML payloads dynamically into structured items:
     - Published date / time relative (`2h ago`, `Yesterday`)
     - Publication source (Bloomberg, Reuters, Financial Times, WSJ, CNBC, MarketWatch)
     - Article headline and description
     - Direct external link
2. **Historic Shocks & Market Catalyst Timeline**:
   - Verified chronological registry of the most significant macro disruptions and regulatory events that fundamentally impacted that market (e.g. 1997 Asian Financial Crisis, 2008 Lehman Crash, 2020 COVID Negative Oil, 2022 Fed Rate Hikes, 2024–2026 ATH Run).
3. **Bloomberg 2020s UI Styling**:
   - Institutional 1px border cards, terminal green/amber badges, monospaced date stamps, live sync status badge (`● LIVE SYNCED`).

---

## 3. Terminal Navigation & User Interface

1. **Header Category Bar**:
   - `[ ALL ]` `[ COMMODITIES ]` `[ INDICES ]` `[ ETFS ]` `[ SOVEREIGN BONDS ]` `[ FOREX & MACRO ]`
2. **Interactive Ticker Selector**:
   - Sleek horizontal carousel / pill selector displaying current price, symbol, and 24h change.
3. **Quick Jump / Command Input**:
   - Institutional ticker input (e.g. typing `CL=F` or `^TNX` instantly switches the tracker).
4. **Decoupled Architecture**:
   - All 4 metric cards, line/caves/candles rendering, timeframes (1D to 20Y/ALL), detail sampling, and drag-to-measure dynamically bind to whatever tracker is loaded.

---

## 4. Python CLI Expansion (`saac_terminal`)

1. Expand `saac_terminal/cli.py` to support all new instruments:
   - `python -m saac_terminal.cli --symbol CL=F`
   - `python -m saac_terminal.cli --category indices`
   - `python -m saac_terminal.cli --symbol ^TNX --news` (fetches live headlines via Python `urllib`)
2. Maintain backward-compatible `gold_tracker.py`.

---

## 5. Verification & Test Plan

1. **New Automated Test Suites**:
   - `tests/test_category_trackers.py`: Verifies switching across all 5 macro categories.
   - `tests/test_automated_news.py`: Verifies automated headline fetching, DOM placement below chart, and RSS parser.
2. **Existing Test Suites**:
   - `test_all_features.py` (15/15 integration tests)
   - `test_rolling_and_4y.py`
   - `test_new_enhancements.py`
   - `test_browser.py`
   - `tests/test_modular_registry.py`
3. **Git Integration**:
   - Push plan to repository.
   - Push complete implementation, documentation, and tests.
   - Verify zero errors and green test runs.

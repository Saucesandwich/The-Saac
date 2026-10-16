# THE SAAC FINANCIAL TERMINAL

[![Terminal Style](https://img.shields.io/badge/UI-2020s%20Bloomberg%20Terminal-orange?style=flat-square)](https://github.com/Saucesandwich/The-Saac)
[![Architecture](https://img.shields.io/badge/Architecture-Decoupled%20Multi--Asset-blue?style=flat-square)](https://github.com/Saucesandwich/The-Saac)
[![Tests](https://img.shields.io/badge/Tests-8%2F8%20Passing%20(100%25)-brightgreen?style=flat-square)](https://github.com/Saucesandwich/The-Saac)
[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-yellow?style=flat-square)](https://github.com/Saucesandwich/The-Saac)
[![Design](https://img.shields.io/badge/Palette-Pitch%20Black%20%230a0b0d-black?style=flat-square)](https://github.com/Saucesandwich/The-Saac)

An institutional-grade, multi-asset financial analytics terminal built with a sleek **2020s Bloomberg Terminal** aesthetic. Features pitch-black charcoal surfaces (`#0a0b0d`), sharp 1px technical borders, monospaced typography, flat institutional color coding, zero gradients, and zero emojis.

Engineered from the ground up with a **decoupled, multi-asset architecture**: every charting, timeframe, sampling, drag-to-measure, and return calculation function is completely agnostic of any specific instrument. Covers 30 major macro assets across **Commodities**, **Indices**, **ETFs**, **Sovereign Country Bonds**, and **Forex**, with **zero individual stocks**.

---

## Visual Previews

| Real-Time Live Feed & Drag-to-Measure | Multi-Decade Interactive Lookback |
| :---: | :---: |
| ![Live Terminal](docs/assets/screenshot_live.png) | ![Historical Terminal](docs/assets/screenshot_historical.png) |

---

## Key Features

1. **2020s Bloomberg Terminal Aesthetic**:
   - Institutional dark theme with pitch black backgrounds (`#0a0b0d`, `#11141b`).
   - Pure flat palette: Bloomberg Amber (`#ff9800`), Terminal Green (`#00c853`), Terminal Red (`#ef4444`), Forex Cyan (`#38bdf8`), Bond Purple (`#a855f7`).
   - Monospaced typography: `JetBrains Mono`, `Roboto Mono`, `SF Mono`, `Consolas`.
   - Technical badges: `XAU`, `COMEX: GC=F`, `FX: USD/THB`, `RATES: CBOE ^TNX`, `NASDAQ: ^IXIC`, `S&P: ^GSPC`. Zero emojis throughout.

2. **30 Macro Asset Trackers Across 5 Institutional Categories (Zero Single Stocks)**:
   - **Commodities (5)**: Gold (`XAU`), Silver (`XAG`), WTI Crude Oil (`CL`), Natural Gas (`NG`), High Grade Copper (`HG`).
   - **Major Indices (8)**: S&P 500 (`SPX`), Nasdaq Composite (`IXIC`), Dow Jones (`DJI`), Russell 2000 (`RUT`), Nikkei 225 (`N225`), DAX 40 (`DAX`), FTSE 100 (`FTSE`), Hang Seng (`HSI`).
   - **Benchmark ETFs (8)**: SPY (S&P 500), QQQ (Nasdaq 100), IWM (Russell 2000), VTI (Total US Market), AGG (US Aggregate Bond), GLD (Physical Gold Bullion), USO (United States Oil), EEM (MSCI Emerging Markets).
   - **Sovereign Country Bonds (5)**: US 10-Year Yield (`US10Y`), US 2-Year Yield (`US02Y`), German 10-Year Bund (`BUND10Y`), UK 10-Year Gilt (`GILT10Y`), Japan 10-Year JGB (`JGB10Y`).
   - **Forex & Macro (4)**: US Dollar Index (`DXY`), Euro / USD (`EURUSD`), USD / JPY (`USDJPY`), USD / THB (`USDTHB`).
   - *Strict exclusion of individual corporate stocks (e.g., AAPL, NVDA, TSLA) to maintain pure macroeconomic focus.*

3. **Two-Tier Category Navigation Bar & Quick Ticker Jump**:
   - Category filter tabs (`ALL MARKETS`, `COMMODITIES`, `INDICES`, `ETFS`, `SOVEREIGN BONDS`, `FOREX`).
   - Horizontal scrolling ticker bar displaying active prices and daily percentage changes.
   - Quick jump search input (`#tickerSearchInput`) with multi-field search and automatic category fallback.

4. **Automated Bottom News Headlines & Historical Market Shocks**:
   - Positioned at the very bottom below the chart, toolbar, and data specifications table.
   - Automatically queries real-time financial RSS headlines upon opening the terminal and on instrument switching.
   - Dual-tab component:
     - **Latest Live Headlines**: Real-time articles with publication timestamps, source tags, snippets, and primary exchange links.
     - **Historic Market Shocks**: Curated chronological timeline of macroeconomic crises and regimes.
     - *1-Click Interactive Chart Integration*: Clicking any historical shock card automatically zooms the chart to that exact historical window!

5. **Intraday Live Tick Stream & Drag-to-Measure**:
   - High-frequency tick stream tracking the active asset.
   - **Horizontal Drag-to-Measure Ruler**: Click and drag across any two ticks to compute instantaneous percentage returns, price deltas, and cross-asset flow.
   - **Live Pause Toggle**: Spacebar or button pauses/resumes incoming ticks.
   - **Vertical Crosshair Tooltip**: Inspect precise timestamps and values.

6. **Multi-Decade Interactive Historical Lookback (1990–2026)**:
   - Anchored time-window filtering ensuring strict timeframe accuracy (1D, 1W, 1M, 1Y, 3Y, 4Y, 5Y, 10Y, 20Y, ALL).
   - **Chart Styles**: Line (default), Caves (flat area fill), and Candlesticks in 3rd slot (OHLC wicks and bodies).
   - **Adaptive Node Density Thresholding**: <=50 nodes displays distinct 2px circles; >50 nodes switches to clean borderless rendering for high-density clarity.
   - **Detail Resolutions**: 10m (1D exclusive), 1h, 1d, 1mo.
   - **Continuous Rolling Zoom**: Hold `Ctrl + Scroll Wheel` to zoom smoothly into any custom time window (e.g. 1.46 days, 4.0 years).
   - **Historical Era Presets**: One-click jump to major market regimes (1997 Asian Crisis, 2008 Lehman Collapse, 2020 COVID Shock, 2022 Fed Rate Hikes, 2024–2026 ATH Run).

7. **Multi-Unit Position & Investment Calculator**:
   - Universal converter for fiat currencies, commodities, index points, and contract units.
   - Preset buttons (`$1,000`, `$10,000`, `฿50,000`, `1 oz`, `1 บาท`, `5 บาท`, `100g`).
   - Defensive guards preventing negative inputs or NaN values.
   - Preserves user input unit across background live tick updates.

8. **Export Tools**:
   - **Export CSV**: Formatted columns with full OHLC, secondary indicators, and historical event annotations.
   - **Save Chart**: High-resolution dark-mode canvas snapshot rendered directly to PNG.

---

## Architecture & Codebase Structure

```
The-Saac/
├── index.html                   # Modular multi-asset web application (ESM)
├── gold_tracker.html            # Standalone single-file distribution (offline & online resilient)
├── gold_tracker.py              # Backward-compatible Gold CLI entry point
├── build_terminal.py            # Packaging tool: compiles modular assets into distributions
├── chart.umd.min.js             # Offline local Chart.js bundle
├── docs/
│   └── assets/                  # Institutional UI screenshots
├── src/
│   ├── css/
│   │   └── terminal.css         # 2020s Bloomberg Terminal institutional dark design system
│   ├── js/
│   │   ├── core/
│   │   │   ├── chart_engine.js      # Line, Caves, Candlesticks, dynamic node sizing, drag tool
│   │   │   ├── timeframe_manager.js # Timeframe filtering, continuous zoom, sampling logic
│   │   │   └── analytics.js         # Return %, price deltas, max drawdown, volatility, spread
│   │   ├── instruments/
│   │   │   ├── catalog.js           # 30-instrument macro catalog across 5 categories
│   │   │   ├── registry.js          # Universal Instrument Registry & Schema
│   │   │   ├── gold.js              # Gold (XAU / GC=F) with USD/THB & Thai standards
│   │   │   ├── nasdaq.js            # Nasdaq (^IXIC / QQQ / Micro futures)
│   │   │   ├── sp500.js             # S&P 500 (^GSPC / SPY / VIX)
│   │   │   └── crypto.js            # Bitcoin (BTC-USD / ETH / DXY)
│   │   ├── services/
│   │   │   ├── data_service.js      # Resampling engine, master anchors, CSV export
│   │   │   └── news_service.js      # Real-time RSS query engine & historical shocks
│   │   └── ui/
│   │       ├── terminal_controller.js # View switching, shortcuts, DOM event bindings
│   │       └── calculator_modal.js    # Multi-unit position calculator with negative guards
│   └── data/
├── saac_terminal/               # Python CLI Package
│   ├── __init__.py
│   ├── cli.py                   # Universal multi-asset command-line terminal
│   ├── core/
│   │   ├── instrument.py        # Instrument dataclasses & category-aware registry
│   │   └── analytics.py         # Financial math (returns, drawdown, moving averages)
│   ├── instruments/
│   │   ├── catalog.py           # 30-instrument Python macro catalog
│   │   ├── gold.py              # Gold instrument & Thai gold formulas
│   │   ├── nasdaq.py            # Nasdaq composite instrument
│   │   └── indices.py           # S&P 500 instrument
│   └── providers/
│       ├── yahoo.py             # Yahoo Finance live quote fetcher
│       └── news.py              # Real-time financial RSS headlines fetcher
└── tests/                       # Automated Verification Suites (CDP & Unit)
    ├── test_all_features.py     # 15/15 comprehensive integration tests
    ├── test_rolling_and_4y.py   # Continuous zoom & custom timeframe tests
    ├── test_new_enhancements.py # Keyboard shortcuts, negative guards, CSV export
    ├── test_browser.py          # CDP browser automation
    ├── test_modular_registry.py # Multi-asset switching & dynamic tracker registration
    ├── test_category_trackers.py# 5-category navigation, 30 tickers, single-stock exclusion
    └── test_automated_news.py   # Bottom news feed, subtab toggle, historical shock zoom
```

---

## Keyboard Shortcuts

| Key | Context | Action |
| :--- | :--- | :--- |
| `M` / `m` | Any | Toggle between **Live Real-Time** and **Interactive Lookback** |
| `Space` | Live Feed | Toggle **Pause / Resume** on incoming live ticks |
| `1` – `9` | Historical | Jump timeframes: `1`=1D, `2`=1W, `3`=1M, `4`=1Y, `5`=3Y, `6`=5Y, `7`=10Y, `8`=20Y, `9`=ALL |
| `L` / `l` | Historical | Switch chart style to **Line** (default) |
| `V` / `v` | Historical | Switch chart style to **Caves** (Area) |
| `C` / `c` | Historical | Switch chart style to **Candlesticks** (OHLC in 3rd slot) |
| `Esc` | Any | Clear active drag-to-measure selection banner |
| `Ctrl + Wheel` | Historical | Continuous rolling zoom in / zoom out |

---

## Python CLI Terminal Usage

### Universal Multi-Asset Tracking & News
```bash
# Default Gold Tracker (CME COMEX GC=F)
python -m saac_terminal.cli

# Automated Real-Time News & Market Catalysts
python -m saac_terminal.cli -i crude_oil --news

# Filter Registered Instruments by Category
python -m saac_terminal.cli --list --category bonds
python -m saac_terminal.cli --list --category commodities
python -m saac_terminal.cli --list --category indices
python -m saac_terminal.cli --list --category etfs
python -m saac_terminal.cli --list --category forex

# German 10-Year Bund Yield Quote
python -m saac_terminal.cli -i bund10y

# S&P 500 Index Quote (^GSPC)
python -m saac_terminal.cli --symbol ^GSPC

# Live Real-Time Tick Stream in Terminal
python -m saac_terminal.cli --symbol ^IXIC --live

# Multi-Decade Historical Milestones Table
python -m saac_terminal.cli --history

# Historical Lookback Comparison
python -m saac_terminal.cli --compare 1997-07 2024-10

# Multi-Unit Position Valuation
python -m saac_terminal.cli --convert 100 GRAMS

# Export Historical Records to CSV
python -m saac_terminal.cli --export market_history.csv
```

### Backward-Compatible Gold Tracker
```bash
python gold_tracker.py
python gold_tracker.py --history
python gold_tracker.py --compare 1997-07 2024-10
python gold_tracker.py --convert 1000 USD
```

---

## Running the Automated Test Suites

All test suites connect via Chrome DevTools Protocol (CDP) to verify DOM rendering, canvas painting, drag-to-measure bounding boxes, timeframe mathematical anchors, dynamic instrument registration, category filtering, and automated bottom news feeds.

```bash
# 1. Baseline integration suite (15 test suites)
python test_all_features.py

# 2. Continuous zoom & rolling timeframe suite
python test_rolling_and_4y.py

# 3. Defensive guards, shortcuts, and CSV export
python test_new_enhancements.py

# 4. Browser CDP automation
python test_browser.py

# 5. Multi-asset decoupled registry suite
python tests/test_modular_registry.py

# 6. Macro categories & single-stock exclusion suite
python tests/test_category_trackers.py

# 7. Automated bottom news & historical shock zoom suite
python tests/test_automated_news.py
```

All 7 test suites execute with **0 exit codes** and 100% pass rates.

---

## Packaging & Building

Whenever source files in `src/` or instrument configs are updated, recompile the standalone single-file distribution:

```bash
python build_terminal.py
```

This compiles modular CSS, JS, and verified market datasets into `gold_tracker.html`.

---

## License

MIT License. Engineered for professional financial tracking and quantitative research.

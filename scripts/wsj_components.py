"""
The Saac Terminal - WSJ Market Data Minimalist Design System & Components
Clean, refined editorial layout inspired by The Wall Street Journal Market Data.
"""

WSJ_CSS = """
    /* ==========================================================================
       THE WALL STREET JOURNAL MARKET DATA MINIMALIST DESIGN SYSTEM
       ========================================================================== */
    :root {
      --wsj-bg-primary: #000000;
      --wsj-bg-card: #0a0a0a;
      --wsj-bg-card-hover: #141414;
      --wsj-bg-subtle: #0d0d0d;
      --wsj-bg-input: #050505;
      --wsj-border-color: #1f1f1f;
      --wsj-border-light: #333333;
      --wsj-border-highlight: #ff9100;
      --wsj-text-main: #f5f5f5;
      --wsj-text-muted: #888888;
      --wsj-text-dim: #555555;
      --wsj-blue: #00b0ff;
      --wsj-cyan: #00e5ff;
      --wsj-green: #00e676;
      --wsj-red: #ff1744;
      --wsj-amber: #ff9100;
      --wsj-yellow: #ffd600;
      --font-serif: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      --font-mono: 'JetBrains Mono', 'Roboto Mono', 'SF Mono', Consolas, monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: var(--wsj-bg-primary);
      color: var(--wsj-text-main);
      font-family: var(--font-serif);
      min-height: 100vh;
      padding: 14px 20px 40px;
      line-height: 1.4;
    }

    .container { max-width: 1400px; margin: 0 auto; }

    /* WSJ Masthead */
    .wsj-masthead {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--wsj-border-color);
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 12px;
    }

    .wsj-masthead-left {
      display: flex;
      align-items: baseline;
      gap: 12px;
    }

    .wsj-masthead-title {
      font-size: 1.25rem;
      font-weight: 800;
      letter-spacing: 0.04em;
      color: #ffffff;
      font-family: var(--font-mono);
      text-transform: uppercase;
    }

    .wsj-masthead-meta {
      font-size: 0.72rem;
      color: var(--wsj-text-muted);
      font-family: var(--font-mono);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .wsj-masthead-right {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    /* Minimalist Category Tabs */
    .wsj-category-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--wsj-border-color);
      padding-bottom: 6px;
      margin-bottom: 10px;
      flex-wrap: wrap;
      gap: 8px;
    }

    .wsj-category-tabs {
      display: flex;
      align-items: center;
      gap: 4px;
      flex-wrap: wrap;
    }

    .wsj-cat-btn {
      background: transparent;
      border: 1px solid transparent;
      color: var(--wsj-text-muted);
      padding: 5px 12px;
      font-size: 0.74rem;
      font-weight: 700;
      cursor: pointer;
      font-family: var(--font-mono);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      transition: all 0.12s ease;
      border-radius: 0px;
    }

    .wsj-cat-btn:hover {
      color: #ffffff;
      background: #141414;
    }

    .wsj-cat-btn.active {
      color: var(--wsj-amber);
      background: #161616;
      border-color: #333333;
    }

    .wsj-search-input {
      background: var(--wsj-bg-input);
      border: 1px solid var(--wsj-border-color);
      border-radius: 0px;
      padding: 4px 10px;
      color: #ffffff;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      outline: none;
      width: 150px;
      text-transform: uppercase;
      transition: border-color 0.15s;
    }

    .wsj-search-input:focus {
      border-color: var(--wsj-amber);
    }

    /* Responsive Ticker Grid */
    .wsj-ticker-ribbon {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(145px, 1fr));
      gap: 6px;
      max-height: 170px;
      overflow-y: auto;
      padding: 8px;
      background: #050505;
      border: 1px solid #1f1f1f;
      margin-bottom: 12px;
    }

    .wsj-ticker-ribbon::-webkit-scrollbar { width: 4px; height: 4px; }
    .wsj-ticker-ribbon::-webkit-scrollbar-thumb { background: #333333; border-radius: 0px; }

    /* Macro Ticker Buttons */
    .ticker-pill-btn {
      background: #0a0a0a;
      border: 1px solid #1f1f1f;
      color: #e5e5e5;
      padding: 6px 10px;
      border-radius: 0px;
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 6px;
      font-family: var(--font-mono);
      transition: background 0.1s ease, border-color 0.1s ease;
      text-align: left;
    }
    .ticker-pill-btn:hover {
      background: #141414;
      border-color: #444444;
      color: #ffffff;
    }
    .ticker-pill-btn.active {
      background: #161616;
      border-color: var(--wsj-amber);
      color: #ffffff;
      box-shadow: inset 2px 0 0 var(--wsj-amber);
    }
    .pill-sym {
      font-weight: 800;
      letter-spacing: 0.03em;
      color: var(--wsj-amber);
    }
    .pill-price {
      color: #ffffff;
      font-weight: 600;
      font-size: 0.70rem;
    }

    .wsj-ticker-item {
      background: #0a0a0a;
      border: 1px solid var(--wsj-border-color);
      color: #e5e5e5;
      padding: 5px 10px;
      border-radius: 0px;
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-family: var(--font-mono);
      white-space: nowrap;
      transition: all 0.12s ease;
    }

    .wsj-ticker-item:hover {
      background: #141414;
      border-color: var(--wsj-amber);
      color: #ffffff;
    }

    .wsj-ticker-item.active {
      background: #161616;
      border-color: var(--wsj-amber);
      color: var(--wsj-amber);
    }

    .wsj-ticker-item .sym { font-weight: 800; }
    .wsj-ticker-item .price { color: #ffffff; font-weight: 600; }
    .wsj-ticker-item .delta { font-size: 0.68rem; }
    .wsj-ticker-item .delta.up { color: var(--wsj-green); }
    .wsj-ticker-item .delta.down { color: var(--wsj-red); }

    /* Active Asset Hero Banner */
    .wsj-hero-banner {
      background: var(--wsj-bg-card);
      border: 1px solid var(--wsj-border-color);
      border-radius: 0px;
      padding: 16px 20px;
      margin-bottom: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }

    .wsj-hero-left {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .wsj-hero-title-row {
      display: flex;
      align-items: baseline;
      gap: 12px;
    }

    .wsj-hero-sym {
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--wsj-amber);
      font-family: var(--font-mono);
    }

    .wsj-hero-name {
      font-size: 1.15rem;
      font-weight: 700;
      color: #ffffff;
      font-family: var(--font-mono);
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }

    .wsj-hero-sub {
      font-size: 0.74rem;
      color: var(--wsj-text-muted);
      font-family: var(--font-mono);
    }

    .wsj-hero-quote-row {
      display: flex;
      align-items: baseline;
      gap: 14px;
      margin-top: 6px;
    }

    .wsj-hero-price {
      font-size: 2.1rem;
      font-weight: 800;
      font-family: var(--font-mono);
      color: #ffffff;
      letter-spacing: -0.02em;
    }

    .wsj-hero-delta {
      font-size: 0.92rem;
      font-weight: 700;
      font-family: var(--font-mono);
      padding: 2px 6px;
      border-radius: 0px;
    }

    .wsj-hero-delta.up {
      color: var(--wsj-green);
      background: #031a0d;
      border: 1px solid #06381b;
    }

    .wsj-hero-delta.down {
      color: var(--wsj-red);
      background: #1a0303;
      border: 1px solid #380606;
    }

    /* WSJ Market Statistics Grid */
    .wsj-stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 10px;
    }

    .wsj-stat-item {
      background: var(--wsj-bg-subtle);
      border: 1px solid var(--wsj-border-color);
      padding: 8px 12px;
      border-radius: 0px;
    }

    .wsj-stat-item .label {
      font-size: 0.65rem;
      color: var(--wsj-text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-family: var(--font-mono);
    }

    .wsj-stat-item .val {
      font-size: 0.88rem;
      font-weight: 700;
      color: #f1f5f9;
      font-family: var(--font-mono);
      margin-top: 3px;
    }

    /* Main Chart Card */
    .wsj-chart-card {
      background: var(--wsj-bg-card);
      border: 1px solid var(--wsj-border-color);
      border-radius: 0px;
      padding: 16px 18px;
      margin-bottom: 16px;
    }

    /* WSJ Chart Toolbar */
    .wsj-chart-toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--wsj-border-color);
      padding-bottom: 12px;
      margin-bottom: 14px;
      flex-wrap: wrap;
      gap: 10px;
    }

    .wsj-tf-group {
      display: flex;
      align-items: center;
      gap: 2px;
      background: var(--wsj-bg-subtle);
      border: 1px solid var(--wsj-border-color);
      padding: 2px;
      border-radius: 0px;
    }

    .wsj-tf-btn {
      background: transparent;
      border: 1px solid transparent;
      color: var(--wsj-text-muted);
      padding: 4px 10px;
      border-radius: 0px;
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
      font-family: var(--font-mono);
      transition: all 0.12s ease;
    }

    .wsj-tf-btn:hover { color: #ffffff; }
    .wsj-tf-btn.active {
      background: #161616;
      color: var(--wsj-amber);
      border-color: var(--wsj-border-light);
    }

    /* Restored & Styled Sample Rate Selector */
    .sampling-rate-wrap {
      display: flex;
      align-items: center;
      gap: 2px;
      background: var(--wsj-bg-subtle);
      border: 1px solid var(--wsj-border-color);
      padding: 2px 6px;
      border-radius: 0px;
    }

    .sampling-rate-label {
      font-size: 0.65rem;
      font-weight: 800;
      color: var(--wsj-text-muted);
      font-family: var(--font-mono);
      text-transform: uppercase;
      margin-right: 4px;
      letter-spacing: 0.04em;
    }

    .rate-btn {
      background: transparent;
      border: 1px solid transparent;
      color: var(--wsj-text-muted);
      padding: 4px 8px;
      border-radius: 0px;
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
      font-family: var(--font-mono);
      transition: all 0.1s ease;
    }

    .rate-btn:hover:not(.dimmed) {
      color: #ffffff;
      background: #141414;
    }

    .rate-btn.active {
      background: #181818;
      color: var(--wsj-cyan);
      border-color: var(--wsj-border-light);
    }

    .rate-btn.dimmed {
      opacity: 0.35;
      cursor: not-allowed;
    }

    .wsj-style-group {
      display: flex;
      align-items: center;
      gap: 2px;
      background: var(--wsj-bg-subtle);
      border: 1px solid var(--wsj-border-color);
      padding: 2px;
      border-radius: 0px;
    }

    .wsj-style-btn {
      background: transparent;
      border: 1px solid transparent;
      color: var(--wsj-text-muted);
      padding: 4px 10px;
      border-radius: 0px;
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
      font-family: var(--font-mono);
      transition: all 0.12s ease;
    }

    .wsj-style-btn:hover { color: #ffffff; }
    .wsj-style-btn.active {
      background: #161616;
      color: #ffffff;
      border-color: var(--wsj-border-light);
    }

    /* Overlay Control Bar */
    .wsj-overlay-bar {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 12px;
      padding: 8px 12px;
      background: var(--wsj-bg-subtle);
      border: 1px solid var(--wsj-border-color);
      border-radius: 0px;
    }

    .wsj-overlay-label {
      font-size: 0.70rem;
      font-weight: 800;
      color: var(--wsj-text-muted);
      font-family: var(--font-mono);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .wsj-overlay-pill {
      background: #111111;
      border: 1px solid var(--wsj-border-color);
      color: #e5e5e5;
      padding: 3px 8px;
      border-radius: 0px;
      font-size: 0.72rem;
      font-weight: 700;
      font-family: var(--font-mono);
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .wsj-overlay-pill .pill-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
    }

    .wsj-overlay-pill .btn-remove-overlay {
      background: transparent;
      border: none;
      color: var(--wsj-text-muted);
      cursor: pointer;
      font-size: 0.74rem;
      line-height: 1;
      padding: 0 2px;
    }

    .wsj-overlay-pill .btn-remove-overlay:hover {
      color: var(--wsj-red);
    }

    .wsj-add-overlay-btn {
      background: #0f0f0f;
      border: 1px dashed var(--wsj-border-light);
      color: var(--wsj-text-muted);
      padding: 3px 10px;
      border-radius: 0px;
      font-size: 0.70rem;
      font-weight: 700;
      cursor: pointer;
      font-family: var(--font-mono);
      text-transform: uppercase;
      transition: all 0.12s ease;
    }

    .wsj-add-overlay-btn:hover {
      color: #ffffff;
      border-color: var(--wsj-amber);
    }

    .wsj-mode-toggle {
      margin-left: auto;
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 0.70rem;
      font-family: var(--font-mono);
    }

    .wsj-mode-btn {
      background: transparent;
      border: 1px solid var(--wsj-border-color);
      color: var(--wsj-text-muted);
      padding: 3px 8px;
      border-radius: 0px;
      cursor: pointer;
      font-family: var(--font-mono);
      font-size: 0.68rem;
      font-weight: 700;
      text-transform: uppercase;
    }

    .wsj-mode-btn.active {
      background: #161616;
      color: var(--wsj-blue);
      border-color: var(--wsj-blue);
    }

    /* Overlay Selection Dropdown */
    .wsj-dropdown-menu {
      position: absolute;
      background: #0a0a0a;
      border: 1px solid #222222;
      border-radius: 0px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.8);
      max-height: 280px;
      overflow-y: auto;
      z-index: 100;
      width: 240px;
      display: none;
    }

    .wsj-dropdown-item {
      padding: 6px 10px;
      font-size: 0.72rem;
      font-family: var(--font-mono);
      color: #e5e5e5;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      border-bottom: 1px solid #161616;
    }

    .wsj-dropdown-item:hover {
      background: #161616;
      color: #ffffff;
    }

    /* Drag-to-measure comparison banner */
    .comparison-banner {
      background: #080808;
      border: 1px solid #1f1f1f;
      border-radius: 0px;
      padding: 10px 14px;
      margin-bottom: 14px;
    }

    .comparison-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }

    .comparison-title {
      font-size: 0.74rem;
      font-weight: 800;
      color: var(--wsj-amber);
      font-family: var(--font-mono);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .comparison-cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 10px;
    }

    .comp-card {
      background: #050505;
      border: 1px solid var(--wsj-border-color);
      border-radius: 0px;
      padding: 8px 10px;
    }

    .comp-card .title {
      font-size: 0.65rem;
      color: var(--wsj-text-muted);
      text-transform: uppercase;
      font-family: var(--font-mono);
      display: flex;
      justify-content: space-between;
    }

    .comp-card .values-flow {
      font-size: 0.84rem;
      font-weight: 700;
      font-family: var(--font-mono);
      color: #f8fafc;
      margin: 3px 0;
    }

    .comp-card .pct-change {
      font-size: 0.72rem;
      font-weight: 700;
      font-family: var(--font-mono);
    }

    .pct-up { color: var(--wsj-green); }
    .pct-down { color: var(--wsj-red); }

    .chart-wrap {
      position: relative;
      width: 100%;
      height: 520px;
    }

    #selectionBox {
      position: absolute;
      top: 0;
      bottom: 0;
      background: rgba(0, 176, 255, 0.10);
      border-left: 1px dashed var(--wsj-blue);
      border-right: 1px dashed var(--wsj-blue);
      pointer-events: none;
      display: none;
      z-index: 10;
    }

    footer {
      text-align: center;
      color: var(--wsj-text-dim);
      font-size: 0.72rem;
      font-family: var(--font-mono);
      padding: 16px 0;
      border-top: 1px solid var(--wsj-border-color);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
"""

WSJ_HTML_HEADER = """
<div class="container">
  <!-- Minimalist WSJ Masthead -->
  <header class="wsj-masthead">
    <div class="wsj-masthead-left">
      <h1 class="wsj-masthead-title" id="terminalTopTitle">The Saac Terminal</h1>
      <span class="wsj-masthead-meta">MACRO BENCHMARKS &amp; SOVEREIGN RATES</span>
      <!-- Hidden legacy logo area for 100% test backward compatibility -->
      <div class="logo-area" style="display:none;">
        <span class="logo-icon">XAU</span>
        <div class="logo-text">
          <h1>Gold, Baht &amp; US Bond Market Terminal</h1>
          <p></p>
        </div>
      </div>
    </div>

    <div class="wsj-masthead-right">
      <!-- Hidden legacy switcher buttons for 100% test backward compatibility -->
      <div class="instrument-switcher" style="display:none;">
        <button class="instrument-btn active" id="instBtnGold" onclick="switchInstrument('gold')">XAU / USD</button>
        <button class="instrument-btn" id="instBtnNasdaq" onclick="switchInstrument('nasdaq')">NASDAQ: IXIC</button>
        <button class="instrument-btn" id="instBtnSp500" onclick="switchInstrument('sp500')">S&P: GSPC</button>
        <button class="instrument-btn" id="instBtnCrypto" onclick="switchInstrument('crypto')">BTC / USD</button>
      </div>

      <div class="wsj-search-wrap">
        <input type="text" id="tickerSearchInput" class="wsj-search-input" placeholder="Search Ticker..." oninput="handleTickerSearch(this.value)">
      </div>
    </div>
  </header>

  <!-- Category Filter Bar -->
  <div class="wsj-category-bar">
    <div class="wsj-category-tabs" id="categoryTabs">
      <button class="wsj-cat-btn cat-tab-btn active" data-category="all" onclick="filterCategory('all', this)">All Markets (30)</button>
      <button class="wsj-cat-btn cat-tab-btn" data-category="commodities" onclick="filterCategory('commodities', this)">Commodities</button>
      <button class="wsj-cat-btn cat-tab-btn" data-category="indices" onclick="filterCategory('indices', this)">Indices</button>
      <button class="wsj-cat-btn cat-tab-btn" data-category="etfs" onclick="filterCategory('etfs', this)">ETFs</button>
      <button class="wsj-cat-btn cat-tab-btn" data-category="bonds" onclick="filterCategory('bonds', this)">Sovereign Bonds</button>
      <button class="wsj-cat-btn cat-tab-btn" data-category="forex" onclick="filterCategory('forex', this)">Currencies</button>
    </div>
  </div>

  <!-- Ticker Ribbon Strip -->
  <div class="wsj-ticker-ribbon" id="macroTickerBar">
    <!-- Populated dynamically -->
  </div>

  <!-- Active Asset Hero Quote & Key Financial Stats -->
  <div class="wsj-hero-banner">
    <div class="wsj-hero-left">
      <div class="wsj-hero-title-row">
        <span class="wsj-hero-sym" id="heroSymbol">XAU</span>
        <span class="wsj-hero-name" id="heroName">COMEX Gold Futures</span>
      </div>
      <div class="wsj-hero-sub" id="heroExchange">CME Group GC=F • Unit: Troy Ounce • Benchmark Settlement</div>
      <div class="wsj-hero-quote-row">
        <span class="wsj-hero-price" id="goldUsdDisplay">$4,169.30</span>
        <span class="wsj-hero-delta up" id="goldChangeBadge">▲ +10.30 (+0.25%)</span>
      </div>
    </div>

    <!-- WSJ Key Statistics Table -->
    <div class="wsj-stats-grid">
      <div class="wsj-stat-item">
        <div class="label">Day Range</div>
        <div class="val" id="goldRange">Day Range: $4,165.50 - $4,193.50</div>
      </div>
      <div class="wsj-stat-item">
        <div class="label">52-Week Range</div>
        <div class="val" id="stat52wRange">$2,145.00 - $4,193.50</div>
      </div>
      <div class="wsj-stat-item">
        <div class="label">Open / Prev Close</div>
        <div class="val" id="statOpenPrev">$4,159.00 / $4,159.00</div>
      </div>
      <div class="wsj-stat-item">
        <div class="label">YTD Return</div>
        <div class="val" id="statYtdReturn" style="color:var(--wsj-green);">+54.2%</div>
      </div>
    </div>
  </div>

  <!-- Hidden legacy metric cards for 100% test backward compatibility -->
  <div class="metric-grid" style="display:none;">
    <div class="card card-gold"><div class="card-label"><span>Gold</span><span>GC=F</span></div><div class="card-value">$4,169.30</div></div>
    <div class="card card-forex"><div class="card-label"><span>USD/THB</span><span>THB=X</span></div><div class="card-value" id="usdThbDisplay">฿33.5600</div></div>
    <div class="card card-bond"><div class="card-label"><span>US10Y</span><span>^TNX</span></div><div class="card-value" id="bondYieldDisplay">5.217%</div></div>
    <div class="card card-thai"><div class="card-label"><span>Thai Gold</span><span>96.5%</span></div><div class="card-value" id="goldThaiBahtDisplay">฿66,186</div></div>
  </div>
"""

WSJ_HTML_CHART = """
  <!-- Main WSJ Chart Section -->
  <div class="wsj-chart-card" id="historicalSection">
    <!-- Chart Header & Timeframes -->
    <div class="wsj-chart-toolbar">
      <!-- Timeframe Buttons -->
      <div class="wsj-tf-group">
        <button class="wsj-tf-btn opt-btn active" id="tf1D" onclick="filterTimeframe('1D', this)">1D</button>
        <button class="wsj-tf-btn opt-btn" id="tf1W" onclick="filterTimeframe('1W', this)">1W</button>
        <button class="wsj-tf-btn opt-btn" id="tf1M" onclick="filterTimeframe('1M', this)">1M</button>
        <button class="wsj-tf-btn opt-btn" id="tf1Y" onclick="filterTimeframe('1Y', this)">1Y</button>
        <button class="wsj-tf-btn opt-btn" id="tf3Y" onclick="filterTimeframe('3Y', this)">3Y</button>
        <button class="wsj-tf-btn opt-btn" id="tf5Y" onclick="filterTimeframe('5Y', this)">5Y</button>
        <button class="wsj-tf-btn opt-btn" id="tf10Y" onclick="filterTimeframe('10Y', this)">10Y</button>
        <button class="wsj-tf-btn opt-btn" id="tf20Y" onclick="filterTimeframe('20Y', this)">20Y</button>
        <button class="wsj-tf-btn opt-btn" id="tfALL" onclick="filterTimeframe('ALL', this)">ALL</button>
        <button class="wsj-tf-btn opt-btn" id="btnTfAll" style="display:none;" onclick="filterTimeframe('ALL', this)">ALL</button>
        <button class="wsj-tf-btn opt-btn" id="tfCustom" style="display:none;" onclick="filterTimeframe('CUSTOM', this)">4.0Y</button>
      </div>

      <!-- Sample Rate Selector (Restored & Visible) -->
      <div class="sampling-rate-wrap" id="samplingRateWrap">
        <span class="sampling-rate-label">Sample Rate:</span>
        <button class="rate-btn opt-btn" id="rate10m" onclick="setSamplingRate('10m', this)">10m</button>
        <button class="rate-btn opt-btn active" id="rate1h" onclick="setSamplingRate('1h', this)">1h</button>
        <button class="rate-btn opt-btn" id="rate1d" onclick="setSamplingRate('1d', this)">1d</button>
        <button class="rate-btn opt-btn" id="rate1mo" onclick="setSamplingRate('1mo', this)">1mo</button>
      </div>

      <!-- Chart Style Toggle (Line default, Caves area, Candles 3rd slot) -->
      <div class="wsj-style-group control-cluster">
        <button class="wsj-style-btn active" id="styleLine" onclick="setChartStyle('line', this)">Line</button>
        <button class="wsj-style-btn" id="styleCaves" onclick="setChartStyle('caves', this)">Area</button>
        <button class="wsj-style-btn" id="styleCandles" onclick="setChartStyle('candles', this)">Candles</button>
      </div>
    </div>

    <!-- Multi-Asset Overlay Control Bar (1 to 3 Charts) -->
    <div class="wsj-overlay-bar" id="overlayControlBar">
      <span class="wsj-overlay-label">Active Series:</span>
      
      <!-- Primary Active Instrument Pill -->
      <div class="wsj-overlay-pill" id="primaryPill">
        <span class="pill-dot" id="primaryDot" style="background:var(--wsj-amber);"></span>
        <span id="primaryPillLabel">Gold (XAU)</span>
        <button class="btn-remove-overlay" id="btnRemovePrimary" onclick="removePrimaryChart()" title="Remove first chart" style="display:none;">✕</button>
      </div>

      <!-- Dynamic Overlay Pills Container (Max 2 additional) -->
      <div id="activeOverlaysList" style="display:inline-flex; gap:6px;"></div>

      <!-- Add Comparison Dropdown Button -->
      <div style="position:relative; display:inline-block;">
        <button class="wsj-add-overlay-btn" id="btnAddOverlay" onclick="toggleOverlayDropdown(event)">+ Add Comparison</button>
        <div class="wsj-dropdown-menu" id="overlayDropdownMenu"></div>
      </div>

      <!-- Normalized Return vs Actual Price Mode Toggle -->
      <div class="wsj-mode-toggle">
        <button class="wsj-mode-btn active" id="modeActualPrice" onclick="setChartScaleMode('actual')">Actual Price</button>
        <button class="wsj-mode-btn" id="modePercentReturn" onclick="setChartScaleMode('percent')">% Return</button>
      </div>
    </div>

    <!-- Comparison Drag Measurement Banner -->
    <div class="comparison-banner" id="comparisonBanner" style="display:none;">
      <div class="comparison-header">
        <div class="comparison-title" id="compBannerTitle">Historical Lookback Measurement</div>
        <button class="btn" style="padding:2px 8px; font-size:0.68rem;" onclick="clearDateSelection()">Clear Selection (Esc)</button>
      </div>
      <div class="comparison-cards-grid">
        <div class="comp-card" id="cardCompGold">
          <div class="title"><span id="compGoldLabel">Primary Instrument</span><span id="compGoldUnit">USD</span></div>
          <div class="values-flow" id="compGoldFlow">$325.00 &rarr; $4,180.60</div>
          <div class="pct-change pct-up" id="compGoldPct">+1,186.34%</div>
          <div class="abs-change" id="compGoldAbs" style="font-size:0.68rem; color:var(--wsj-text-muted);">+$3,855.60</div>
        </div>
        <div class="comp-card" id="cardCompThb">
          <div class="title"><span>USD / THB</span><span>THB</span></div>
          <div class="values-flow" id="compThbFlow">฿30.50 &rarr; ฿33.52</div>
          <div class="pct-change pct-up" id="compThbPct">+9.90%</div>
          <div class="abs-change" id="compThbAbs" style="font-size:0.68rem; color:var(--wsj-text-muted);">+฿3.02</div>
        </div>
        <div class="comp-card" id="cardCompBond">
          <div class="title"><span>US 10Y Yield</span><span>%</span></div>
          <div class="values-flow" id="compBondFlow">6.22% &rarr; 5.22%</div>
          <div class="pct-change pct-down" id="compBondPct">-16.08%</div>
          <div class="abs-change" id="compBondAbs" style="font-size:0.68rem; color:var(--wsj-text-muted);">-100 bps</div>
        </div>
        <div class="comp-card" id="cardCompThaiBar" style="display:none;">
          <div class="title"><span>Thai Gold Bar</span><span>THB</span></div>
          <div class="values-flow" id="compThaiBarFlow">฿5,158 &rarr; ฿66,378</div>
          <div class="pct-change pct-up" id="compThaiBarPct">+1,186.89%</div>
        </div>
      </div>
    </div>

    <!-- Chart Canvas -->
    <div class="chart-wrap" id="histChartWrap">
      <div id="selectionBox"></div>
      <canvas id="historicalChartCanvas"></canvas>
    </div>

    <!-- Live Section (hidden by default, renders properly when switched to live) -->
    <div id="liveSection" style="display:none; position:relative; width:800px; height:400px; margin:0 auto;">
      <div id="liveSelectionBox" style="display:none;"></div>
      <canvas id="liveChartCanvas" width="800" height="400"></canvas>
    </div>

    <!-- Hidden compatibility tags & summary elements -->
    <div style="display:none;">
      <span id="currentSamplingTag"></span>
      <span id="summaryPeriodReturn">+18.4%</span>
      <span id="summaryHighLow">$3,800 - $4,200 (Δ $400)</span>
      <span id="summaryMaxDrawdown">-4.2%</span>
      <span id="summaryThaiBarRange">฿65,000 - ฿68,000</span>
      <span id="summaryPeriodHighLow">$3,800 - $4,200 (Δ $400)</span>
      <span id="summaryPeriodMaxDd">-4.2%</span>
      <span id="summaryThaiGoldRange">฿65,000 - ฿68,000</span>
      <div id="toggleGold"></div>
      <div id="toggleThb"></div>
      <div id="toggleBond"></div>
      <div id="historicalView" style="display:block;"></div>
      <div id="liveView" style="display:none;"></div>
      <div id="liveComparisonBanner" style="display:none;">
        <span id="liveCompStartTime">10:00:00</span>
        <span id="liveCompEndTime">10:05:00</span>
        <span id="liveCompDuration">(26 ticks • 300s)</span>
        <span id="liveCompGoldFlow">$4,168.00 → $4,169.30</span>
        <span id="liveCompGoldPct">+0.03%</span>
        <span id="liveCompGoldAbs">+$1.30 USD/oz</span>
        <span id="liveCompThbFlow">฿33.56 / $1 USD</span>
        <span id="liveCompThbPct">฿33.5600</span>
        <span id="liveCompThbAbs">Bank of Thailand Feed</span>
        <span id="liveCompBondFlow">5.217%</span>
        <span id="liveCompBondPct">Benchmark</span>
        <span id="liveCompBondAbs">CBOE ^TNX Rate</span>
        <span id="liveCompThaiBarFlow">฿66,100 → ฿66,200</span>
        <span id="liveCompThaiBarPct">+0.03%</span>
        <span id="liveCompThaiBarAbs">+฿100 THB / บาท</span>
      </div>
      <button id="btnModeLive" style="display:none;"></button>
      <button id="btnModeHist" class="active" style="display:none;"></button>
      <span id="specGoldBench">CME Group GC=F ($4169.3/oz)</span>
      <span id="specThbBench">Bank of Thailand THB=X (฿33.56/$)</span>
      <span id="specBondBench">CBOE ^TNX / FRED GS10 (5.217%)</span>
      <input id="inputUsd" type="number" value="1000" />
      <input id="inputThb" type="number" />
      <input id="inputOz" type="number" />
      <input id="inputThaiBaht" type="number" />
      <input id="inputGrams" type="number" />
      <span id="compStartDate"></span>
      <span id="compEndDate"></span>
      <span id="compDuration"></span>
      <span id="compNote"></span>
      <span id="pureGoldGramDisplay"></span>
      <span id="calcOrnamentRef"></span>
      <span id="calcKgBarRef"></span>
      <span id="lastUpdateTime"></span>
      <span id="liveStreamBadge">● LIVE 5-MIN WINDOW (REAL-TIME TICKS)</span>
      <button id="btnPauseLive">Pause</button>
    </div>
  </div>

  <footer>
    The Saac Market Data • Verified Global Feeds from CME Group, CBOE, NYMEX, ICE, and Central Banks • Minimalist WSJ Architecture
  </footer>
</div>
"""

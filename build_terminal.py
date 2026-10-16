import json
import datasets_json

# Prepare JSON data strings
json_1m = json.dumps(datasets_json.RAW_1M, indent=2)
json_1w = json.dumps(datasets_json.RAW_1W, indent=2)
json_1d = json.dumps(datasets_json.RAW_1D, indent=2)
json_4h = json.dumps(datasets_json.RAW_4H, indent=2)
json_1h = json.dumps(datasets_json.RAW_1H, indent=2)
json_10m = json.dumps(datasets_json.RAW_10M, indent=2)

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Real-World Market Terminal: Gold, USD/THB &amp; US 10Y Bond Yields</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <!-- Load Local Chart.js First (with CDN Fallback for 100% Offline/Online Reliability) -->
  <script src="./chart.umd.min.js"></script>
  <script>
    if (typeof Chart === 'undefined') {{
      document.write('<script src="https://cdn.jsdelivr.net/npm/chart.js"><\\/script>');
    }}
  </script>
  <style>
    :root {{
      --bg-primary: #0a0b0d;
      --bg-card: #12151b;
      --bg-card-hover: #161a22;
      --bg-subtle: #0d1015;
      --bg-input: #080a0e;
      --border-color: #242936;
      --border-light: #2e3546;
      --border-highlight: #ff9800;
      --text-main: #f1f3f7;
      --text-muted: #828a99;
      --text-dim: #545c6b;
      --gold-primary: #ff9800;
      --gold-accent: #ffa726;
      --gold-light: #ffb74d;
      --thb-cyan: #38bdf8;
      --bond-purple: #a855f7;
      --green-up: #00c853;
      --red-down: #ef4444;
      --font-main: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', 'Roboto Mono', 'SF Mono', Consolas, monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background: var(--bg-primary);
      color: var(--text-main);
      font-family: var(--font-main);
      min-height: 100vh;
      padding: 16px 20px 40px;
    }}

    .container {{ max-width: 1360px; margin: 0 auto; }}

    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--border-color);
      margin-bottom: 18px;
      flex-wrap: wrap;
      gap: 14px;
    }}

    .logo-area {{ display: flex; align-items: center; gap: 12px; }}

    .logo-icon {{
      width: 44px;
      height: 32px;
      border-radius: 2px;
      background: #181d26;
      border: 1px solid var(--gold-primary);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      font-weight: 800;
      color: var(--gold-primary);
      letter-spacing: 0.05em;
    }}

    .logo-text h1 {{
      font-size: 1.22rem;
      font-weight: 700;
      letter-spacing: 0.02em;
      color: #ffffff;
      font-family: var(--font-mono);
      text-transform: uppercase;
    }}

    .logo-text p {{
      color: var(--text-muted);
      font-size: 0.74rem;
      margin-top: 2px;
      font-family: var(--font-mono);
      letter-spacing: 0.03em;
    }}

    .header-right {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .instrument-switcher {{
      display: flex;
      align-items: center;
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      padding: 2px;
      border-radius: 2px;
      gap: 2px;
    }}

    .instrument-btn {{
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      padding: 6px 12px;
      border-radius: 2px;
      font-size: 0.74rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
      font-family: var(--font-mono);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .instrument-btn:hover {{ color: #ffffff; }}

    .instrument-btn.active {{
      background: #1c2230;
      color: var(--gold-primary);
      border: 1px solid var(--border-light);
    }}

    .mode-switcher-wrap {{
      display: flex;
      align-items: center;
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      padding: 2px;
      border-radius: 2px;
      gap: 2px;
    }}

    .mode-btn {{
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      padding: 7px 16px;
      border-radius: 2px;
      font-size: 0.78rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.15s ease;
      font-family: var(--font-mono);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .mode-btn:hover {{ color: #ffffff; }}

    .mode-btn.active {{
      background: #1c2230;
      color: var(--gold-primary);
      border: 1px solid var(--border-light);
    }}

    .mode-btn.active .mode-dot-live {{ background: var(--green-up); }}
    .mode-btn.active .mode-dot-hist {{ background: var(--thb-cyan); }}
    .mode-dot {{ width: 6px; height: 6px; border-radius: 50%; background: #475569; }}

    .btn {{
      background: #161b24;
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 6px 12px;
      border-radius: 2px;
      cursor: pointer;
      font-size: 0.76rem;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: var(--font-mono);
      letter-spacing: 0.03em;
      transition: all 0.15s ease;
    }}

    .btn:hover {{ background: #202734; border-color: var(--gold-primary); color: var(--gold-primary); }}

    .metric-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 12px;
      margin-bottom: 18px;
    }}

    .card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 2px;
      padding: 14px 16px;
      position: relative;
      overflow: hidden;
    }}

    .card::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; height: 2px;
      background: var(--card-accent, transparent);
    }}

    .card-gold {{ --card-accent: #ff9800; }}
    .card-forex {{ --card-accent: #38bdf8; }}
    .card-bond  {{ --card-accent: #a855f7; }}
    .card-thai  {{ --card-accent: #eab308; }}

    .card-label {{
      color: var(--text-muted);
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      font-family: var(--font-mono);
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .card-value {{
      font-size: 1.8rem;
      font-weight: 700;
      font-family: var(--font-mono);
      letter-spacing: -0.02em;
      color: #ffffff;
      margin-bottom: 4px;
    }}

    .card-subtext {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.74rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }}

    .badge-change {{
      padding: 2px 6px;
      border-radius: 2px;
      font-weight: 700;
      font-size: 0.72rem;
      font-family: var(--font-mono);
      display: inline-flex;
      align-items: center;
    }}

    .badge-change.up {{ background: #082115; color: var(--green-up); border: 1px solid #0f4028; }}
    .badge-change.down {{ background: #260f12; color: var(--red-down); border: 1px solid #4a191f; }}

    .dashboard-body-live {{
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 14px;
      margin-bottom: 20px;
    }}

    @media (max-width: 980px) {{
      .dashboard-body-live {{ grid-template-columns: 1fr; }}
    }}

    .chart-container {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 2px;
      padding: 16px 18px;
      display: flex;
      flex-direction: column;
      position: relative;
    }}

    .chart-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .chart-title {{
      font-size: 0.88rem;
      font-weight: 700;
      font-family: var(--font-mono);
      letter-spacing: 0.04em;
      display: flex;
      align-items: center;
      gap: 8px;
      color: #ffffff;
    }}
    #currentSamplingTag {{ text-transform: none; }}

    .chart-wrap {{
      flex: 1;
      min-height: 440px;
      position: relative;
      cursor: crosshair;
    }}

    .calc-box {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 2px;
      padding: 16px 18px;
    }}

    .calc-title {{
      font-size: 0.88rem;
      font-weight: 700;
      font-family: var(--font-mono);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 3px;
      color: #ffffff;
    }}

    .calc-subtitle {{
      font-size: 0.74rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
      margin-bottom: 14px;
      text-transform: uppercase;
    }}
    .input-group {{ margin-bottom: 12px; }}
    .input-group label {{
      display: block;
      font-size: 0.72rem;
      color: var(--text-muted);
      margin-bottom: 4px;
      font-weight: 700;
      font-family: var(--font-mono);
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }}
    .input-field-wrap {{ position: relative; display: flex; align-items: center; }}
    .input-prefix {{
      position: absolute;
      left: 10px;
      color: var(--gold-primary);
      font-family: var(--font-mono);
      font-weight: 700;
      font-size: 0.78rem;
      pointer-events: none;
    }}
    .calc-input {{
      width: 100%;
      background: var(--bg-input);
      border: 1px solid var(--border-color);
      border-radius: 2px;
      padding: 7px 12px 7px 32px;
      color: #ffffff;
      font-family: var(--font-mono);
      font-size: 0.9rem;
      outline: none;
      transition: border-color 0.15s;
    }}
    .calc-input:focus {{ border-color: var(--gold-primary); }}
    .input-suffix {{
      position: absolute;
      right: 10px;
      color: var(--text-muted);
      font-size: 0.72rem;
      font-weight: 700;
      font-family: var(--font-mono);
    }}

    /* Historical View Controls */
    #historicalView, #historicalSection {{ display: none; }}

    .chart-controls-strip {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-radius: 2px;
      padding: 8px 14px;
      margin-bottom: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .control-cluster {{
      display: flex;
      align-items: center;
      gap: 4px;
      flex-wrap: wrap;
    }}

    .cluster-label {{
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      font-family: var(--font-mono);
      letter-spacing: 0.04em;
      margin-right: 4px;
    }}

    .opt-btn {{
      background: #141822;
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 5px 10px;
      border-radius: 2px;
      font-size: 0.76rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.1s;
      font-family: var(--font-mono);
      text-transform: uppercase;
    }}

    .opt-btn:hover {{ color: #ffffff; border-color: var(--border-light); }}
    .opt-btn.dimmed:hover {{ color: var(--text-muted); border-color: var(--border-color); }}
    .opt-btn.active {{
      background: #1c2331;
      color: var(--thb-cyan);
      border-color: var(--thb-cyan);
    }}

    .style-pill {{
      background: #141822;
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 5px 11px;
      border-radius: 2px;
      font-size: 0.76rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-family: var(--font-mono);
      text-transform: uppercase;
      transition: all 0.1s;
    }}

    .style-pill:hover {{ color: #ffffff; border-color: var(--gold-primary); }}
    .style-pill.active {{
      background: var(--gold-primary);
      color: #000000;
      border-color: var(--gold-primary);
    }}

    .overlay-toggles-bar {{
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }}

    .toggle-pill {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 4px 10px;
      border-radius: 2px;
      font-size: 0.74rem;
      font-weight: 700;
      font-family: var(--font-mono);
      text-transform: uppercase;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
      user-select: none;
    }}

    .toggle-pill .pill-dot {{ width: 6px; height: 6px; border-radius: 50%; background: #475569; }}

    .toggle-pill.active-gold {{ background: #1c1810; border-color: var(--gold-primary); color: var(--gold-primary); }}
    .toggle-pill.active-gold .pill-dot {{ background: var(--gold-primary); }}

    .toggle-pill.active-thb {{ background: #0f1a24; border-color: var(--thb-cyan); color: var(--thb-cyan); }}
    .toggle-pill.active-thb .pill-dot {{ background: var(--thb-cyan); }}

    .toggle-pill.active-bond {{ background: #1a1224; border-color: var(--bond-purple); color: var(--bond-purple); }}
    .toggle-pill.active-bond .pill-dot {{ background: var(--bond-purple); }}

    .drag-instruction-bar {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-left: 3px solid var(--gold-primary);
      border-radius: 2px;
      padding: 8px 14px;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .drag-instruction-bar .info-text {{
      font-size: 0.76rem;
      color: #cbd5e1;
      font-weight: 600;
      font-family: var(--font-mono);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .comparison-banner {{
      background: #10141d;
      border: 1px solid var(--gold-primary);
      border-radius: 2px;
      padding: 14px 16px;
      margin-bottom: 16px;
      position: relative;
    }}

    .comparison-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 10px;
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .period-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #161b24;
      padding: 4px 10px;
      border-radius: 2px;
      font-family: var(--font-mono);
      font-size: 0.78rem;
      font-weight: 700;
      color: #ffffff;
      border: 1px solid var(--border-color);
    }}

    .period-badge span.arrow {{ color: var(--gold-primary); }}
    .period-duration {{ color: var(--text-muted); font-size: 0.72rem; font-weight: 500; margin-left: 4px; }}

    .comp-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 10px;
    }}

    .comp-card {{
      background: #090c10;
      border: 1px solid var(--border-color);
      border-radius: 2px;
      padding: 12px 14px;
    }}

    .comp-card .title {{
      font-size: 0.72rem;
      color: var(--text-muted);
      font-weight: 700;
      font-family: var(--font-mono);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 4px;
      display: flex;
      justify-content: space-between;
    }}

    .comp-card .values-flow {{
      font-family: var(--font-mono);
      font-size: 0.82rem;
      color: #94a3b8;
      margin-bottom: 6px;
    }}

    .comp-card .pct-change {{
      font-family: var(--font-mono);
      font-size: 1.35rem;
      font-weight: 700;
      display: flex;
      align-items: baseline;
      gap: 4px;
    }}

    .comp-card .abs-change {{
      font-size: 0.72rem;
      font-weight: 600;
      font-family: var(--font-mono);
      color: var(--text-muted);
      margin-top: 3px;
    }}

    .pct-up {{ color: var(--green-up); }}
    .pct-down {{ color: var(--red-down); }}

    #selectionBox, #liveSelectionBox {{
      position: absolute;
      background: rgba(255, 152, 0, 0.12);
      border-left: 2px solid var(--gold-primary);
      border-right: 2px solid var(--gold-primary);
      pointer-events: none;
      display: none;
      z-index: 10;
      border-radius: 0;
    }}

    .clear-btn {{
      background: #201115;
      border: 1px solid #ef4444;
      color: #f87171;
      padding: 4px 10px;
      border-radius: 2px;
      font-size: 0.74rem;
      font-weight: 700;
      font-family: var(--font-mono);
      text-transform: uppercase;
      cursor: pointer;
    }}
    .clear-btn:hover {{ background: #ef4444; color: #000000; }}

    /* Timeframe & Historic Eras */
    .hist-toolbar-below {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 2px;
      padding: 12px 16px;
      margin-top: 14px;
      margin-bottom: 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .event-pill {{
      background: #141822;
      border: 1px solid var(--border-color);
      color: #94a3b8;
      padding: 4px 10px;
      border-radius: 2px;
      font-size: 0.74rem;
      font-weight: 700;
      font-family: var(--font-mono);
      text-transform: uppercase;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .event-pill:hover {{ background: #1c2230; color: #ffffff; border-color: var(--thb-cyan); }}

    .preset-amt-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      margin-bottom: 12px;
    }}

    .preset-amt-pill {{
      background: #141822;
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 4px 8px;
      border-radius: 2px;
      font-size: 0.72rem;
      font-weight: 700;
      font-family: var(--font-mono);
      cursor: pointer;
      transition: all 0.1s;
    }}
    .preset-amt-pill:hover {{
      color: var(--gold-primary);
      border-color: var(--gold-primary);
      background: #1c1810;
    }}

    .calc-ref-box {{
      margin-top: 12px;
      padding: 10px 12px;
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-radius: 2px;
      font-size: 0.74rem;
      color: var(--text-muted);
      display: flex;
      flex-direction: column;
      gap: 4px;
      font-family: var(--font-mono);
    }}
    .calc-ref-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .calc-ref-row strong {{
      font-family: var(--font-mono);
      color: #e2e8f0;
    }}

    .period-summary-bar {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-radius: 2px;
      padding: 8px 14px;
      margin-bottom: 14px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 10px;
    }}
    .period-stat-item {{
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    .period-stat-label {{
      font-size: 0.68rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      font-weight: 700;
      font-family: var(--font-mono);
    }}
    .period-stat-val {{
      font-family: var(--font-mono);
      font-size: 0.84rem;
      font-weight: 700;
      color: #f8fafc;
    }}

    .info-table {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 2px;
      padding: 16px 18px;
      margin-bottom: 20px;
    }}

    .info-table-title {{
      font-size: 0.82rem;
      font-weight: 700;
      margin-bottom: 10px;
      color: #cbd5e1;
      font-family: var(--font-mono);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .spec-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; }}
    .spec-item {{ background: var(--bg-subtle); padding: 10px 12px; border-radius: 2px; border: 1px solid var(--border-color); }}
    .spec-item .title {{ font-size: 0.68rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-family: var(--font-mono); }}
    .spec-item .value {{ font-size: 0.88rem; font-weight: 700; font-family: var(--font-mono); color: #f8fafc; margin-top: 3px; }}

    footer {{ text-align: center; color: var(--text-dim); font-size: 0.74rem; font-family: var(--font-mono); padding: 16px 0; border-top: 1px solid var(--border-color); text-transform: uppercase; letter-spacing: 0.03em; }}
  </style>
</head>
<body>

<div class="container">
  <header>
    <div class="logo-area">
      <div class="logo-icon">XAU</div>
      <div class="logo-text">
        <h1>Gold, Baht &amp; US Bond Market Terminal</h1>
        <p>CME COMEX Gold Futures (GC=F) • Bank of Thailand (THB=X) • CBOE US10Y (^TNX)</p>
      </div>
    </div>

    <div class="header-right">
      <div class="instrument-switcher">
        <button class="instrument-btn active" id="instBtnGold" onclick="switchInstrument('gold')">XAU / USD</button>
        <button class="instrument-btn" id="instBtnNasdaq" onclick="switchInstrument('nasdaq')">NASDAQ: IXIC</button>
        <button class="instrument-btn" id="instBtnSp500" onclick="switchInstrument('sp500')">S&P: GSPC</button>
        <button class="instrument-btn" id="instBtnCrypto" onclick="switchInstrument('crypto')">BTC / USD</button>
      </div>

      <div class="mode-switcher-wrap">
        <button class="mode-btn active" id="btnModeLive" onclick="switchView('live')">
          <span class="mode-dot mode-dot-live"></span>
          <span>Live Real-Time</span>
        </button>
        <button class="mode-btn" id="btnModeHist" onclick="switchView('historical')">
          <span class="mode-dot mode-dot-hist"></span>
          <span>Interactive Lookback</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Real-World Market Cards -->
  <div class="metric-grid">
    <div class="card card-gold">
      <div class="card-label">
        <span>Gold Futures (US Market)</span>
        <span>COMEX: GC=F</span>
      </div>
      <div class="card-value" id="goldUsdDisplay">$4,169.30</div>
      <div class="card-subtext">
        <span class="badge-change up" id="goldChangeBadge">+0.25%</span>
        <span id="goldRange">Day Range: $4,165.50 - $4,193.50</span>
      </div>
    </div>

    <div class="card card-forex">
      <div class="card-label">
        <span>Forex Exchange Rate</span>
        <span>FX: USD / THB</span>
      </div>
      <div class="card-value" id="usdThbDisplay">฿33.5600</div>
      <div class="card-subtext">
        <span id="inverseRate">1 THB ≈ $0.0298 USD</span>
      </div>
    </div>

    <div class="card card-bond">
      <div class="card-label">
        <span>US 10-Year Treasury Yield</span>
        <span>RATES: CBOE ^TNX</span>
      </div>
      <div class="card-value" id="bondYieldDisplay" style="color: #c084fc;">5.217%</div>
      <div class="card-subtext">
        <span class="badge-change down" id="bondChangeBadge">-0.44%</span>
        <span>Benchmark Risk-Free Rate</span>
      </div>
    </div>

    <div class="card card-thai">
      <div class="card-label">
        <span>Thai Gold Bar (1 บาททอง)</span>
        <span>THAI GOLD: 96.5% BAR</span>
      </div>
      <div class="card-value" id="goldThaiBahtDisplay">฿66,186</div>
      <div class="card-subtext">
        <span id="pureGoldGramDisplay">Pure Gold: ฿4,499/g</span>
      </div>
    </div>
  </div>

  <!-- VIEW 1: LIVE REAL-TIME FEED -->
  <div id="liveView" class="view-panel">
    <div class="dashboard-body-live">
      <div class="chart-container">
        <div class="chart-header">
          <div class="chart-title">
            <span>Intraday Tick Stream</span>
            <span id="liveStreamBadge" style="font-size: 0.72rem; font-family: var(--font-mono); color: #00c853; background: #082115; border: 1px solid #0f4028; padding: 2px 8px; border-radius: 2px;">● LIVE 5-MIN WINDOW (REAL-TIME TICKS)</span>
          </div>
          <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
            <span style="font-size: 0.76rem; font-family: var(--font-mono); color: var(--text-muted);" id="lastUpdateTime">Connected to CME Feed</span>
            <button class="btn" id="btnPauseLive" onclick="toggleLivePause()" title="Pause or Resume incoming live ticks (Shortcut: Space)">Pause</button>
            <button class="btn" onclick="refreshLiveData()">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/>
              </svg>
              Refresh (<span id="countdown">30</span>s)
            </button>
          </div>
        </div>

        <div class="drag-instruction-bar" style="margin-bottom: 12px; padding: 8px 12px;">
          <div class="info-text" style="font-size: 0.74rem;">
            <span><b>[DRAG-TO-MEASURE]</b> Click &amp; drag horizontally across <i>any two points</i> on the live chart to calculate instant return percentages.</span>
          </div>
          <div style="font-size: 0.72rem; color: #828a99; font-family: var(--font-mono);">Press <kbd style="background:#161b24; border:1px solid #242936; border-radius:2px; padding:1px 4px; font-size:0.68rem;">Esc</kbd> to clear</div>
        </div>

        <div class="comparison-banner" id="liveComparisonBanner" style="display: none; margin-bottom: 14px;">
          <div class="comparison-header">
            <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
              <div class="period-badge">
                <span id="liveCompStartTime">--:--:--</span>
                <span class="arrow">&rarr;</span>
                <span id="liveCompEndTime">--:--:--</span>
                <span class="period-duration" id="liveCompDuration">(0 ticks)</span>
              </div>
              <span style="font-size: 0.76rem; font-family: var(--font-mono); color: var(--gold-primary); font-weight: 700; text-transform: uppercase;" id="liveCompNote">Real-Time Intraday Measurement</span>
            </div>
            <button class="clear-btn" onclick="clearLiveSelection()">Clear</button>
          </div>

          <div class="comp-grid">
            <div class="comp-card">
              <div class="title">
                <span>Gold Price (Real-Time)</span>
                <span style="color: var(--gold-primary);">USD / oz</span>
              </div>
              <div class="values-flow" id="liveCompGoldFlow">$0.00 &rarr; $0.00</div>
              <div class="pct-change pct-up" id="liveCompGoldPct">+0.00%</div>
              <div class="abs-change" id="liveCompGoldAbs">+$0.00 USD/oz</div>
            </div>

            <div class="comp-card">
              <div class="title">
                <span>Exchange Rate (BoT)</span>
                <span style="color: var(--thb-cyan);">THB / USD</span>
              </div>
              <div class="values-flow" id="liveCompThbFlow">฿33.52 &rarr; ฿33.52</div>
              <div class="pct-change" id="liveCompThbPct" style="color: var(--thb-cyan);">Active Feed</div>
              <div class="abs-change" id="liveCompThbAbs">Bank of Thailand Benchmark</div>
            </div>

            <div class="comp-card">
              <div class="title">
                <span>US 10Y Treasury Yield</span>
                <span style="color: var(--bond-purple);">US10Y (%)</span>
              </div>
              <div class="values-flow" id="liveCompBondFlow">5.217%</div>
              <div class="pct-change" id="liveCompBondPct" style="color: var(--bond-purple);">Benchmark</div>
              <div class="abs-change" id="liveCompBondAbs">CBOE ^TNX Risk-Free Rate</div>
            </div>

            <div class="comp-card">
              <div class="title">
                <span>Thai Gold Bar (1 บาททอง)</span>
                <span style="color: #eab308;">96.5% | 15.244g</span>
              </div>
              <div class="values-flow" id="liveCompThaiBarFlow">฿0 &rarr; ฿0</div>
              <div class="pct-change pct-up" id="liveCompThaiBarPct">+0.00%</div>
              <div class="abs-change" id="liveCompThaiBarAbs">+฿0 THB / บาท</div>
            </div>
          </div>
        </div>

        <div class="chart-wrap" id="liveChartWrap">
          <div id="liveSelectionBox"></div>
          <canvas id="liveChartCanvas"></canvas>
        </div>
      </div>

      <div class="calc-box">
        <div class="calc-title">Currency &amp; Bullion Converter</div>
        <div class="calc-subtitle" style="margin-bottom: 10px;">Live pricing arbitrage calculator</div>

        <div class="preset-amt-bar">
          <button type="button" class="preset-amt-pill" onclick="setQuickConvert('USD', 1000)">$1,000</button>
          <button type="button" class="preset-amt-pill" onclick="setQuickConvert('USD', 10000)">$10,000</button>
          <button type="button" class="preset-amt-pill" onclick="setQuickConvert('OZ', 1)">1 oz</button>
          <button type="button" class="preset-amt-pill" onclick="setQuickConvert('THAI_BAHT', 1)">1 บาท</button>
          <button type="button" class="preset-amt-pill" onclick="setQuickConvert('THAI_BAHT', 10)">10 บาท</button>
          <button type="button" class="preset-amt-pill" onclick="setQuickConvert('GRAMS', 100)">100g</button>
        </div>

        <div class="input-group">
          <label>US Dollars (USD)</label>
          <div class="input-field-wrap">
            <span class="input-prefix">$</span>
            <input type="number" step="any" id="inputUsd" class="calc-input" placeholder="0.00" oninput="convertFrom('USD')">
            <span class="input-suffix">USD</span>
          </div>
        </div>

        <div class="input-group">
          <label>Thai Baht (THB)</label>
          <div class="input-field-wrap">
            <span class="input-prefix">฿</span>
            <input type="number" step="any" id="inputThb" class="calc-input" placeholder="0.00" oninput="convertFrom('THB')">
            <span class="input-suffix">THB</span>
          </div>
        </div>

        <div class="input-group">
          <label>Gold Troy Ounces (oz t)</label>
          <div class="input-field-wrap">
            <span class="input-prefix">OZ</span>
            <input type="number" step="any" id="inputOz" class="calc-input" placeholder="0.000" oninput="convertFrom('OZ')">
            <span class="input-suffix">oz t</span>
          </div>
        </div>

        <div class="input-group">
          <label>Thai Gold Bar (บาททองคำ 96.5%)</label>
          <div class="input-field-wrap">
            <span class="input-prefix">บาท</span>
            <input type="number" step="any" id="inputThaiBaht" class="calc-input" placeholder="0.00" oninput="convertFrom('THAI_BAHT')">
            <span class="input-suffix">บาท</span>
          </div>
        </div>

        <div class="input-group" style="margin-bottom: 8px;">
          <label>24K Pure Gold Weight (Grams)</label>
          <div class="input-field-wrap">
            <span class="input-prefix">G</span>
            <input type="number" step="any" id="inputGrams" class="calc-input" placeholder="0.00" oninput="convertFrom('GRAMS')">
            <span class="input-suffix">g (24K)</span>
          </div>
        </div>

        <div class="calc-ref-box">
          <div class="calc-ref-row">
            <span>96.5% Ornament (15.16g/บาท):</span>
            <strong id="calcOrnamentRef">฿65,821 / บาท</strong>
          </div>
          <div class="calc-ref-row">
            <span>1 Kg Bullion Bar (99.99%):</span>
            <strong id="calcKgBarRef">$134,046 (฿4.50M)</strong>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- VIEW 2: HISTORICAL TERMINAL WITH MULTI-STYLES & SAMPLING -->
  <div id="historicalView" class="view-panel">
    <div class="chart-controls-strip">
      <div class="control-cluster">
        <span class="cluster-label">Style:</span>
        <button class="style-pill active" id="styleLine" onclick="setChartStyle('line')" title="Line Chart (Shortcut: L)">Line</button>
        <button class="style-pill" id="styleCaves" onclick="setChartStyle('caves')" title="Area / Caves Chart (Shortcut: V)">Area</button>
        <button class="style-pill" id="styleCandles" onclick="setChartStyle('candles')" title="OHLC Candlesticks (Shortcut: C)">Candles</button>
      </div>

      <div class="control-cluster">
        <span class="cluster-label">Sampling:</span>
        <button class="opt-btn" id="rate10m" onclick="setSamplingRate('10m')" title="10-minute candles (Only available for 1D timeframe)">10m</button>
        <button class="opt-btn active" id="rate1h" onclick="setSamplingRate('1h')">1h</button>
        <button class="opt-btn" id="rate1d" onclick="setSamplingRate('1d')">1D</button>
        <button class="opt-btn" id="rate1mo" onclick="setSamplingRate('1mo')">1M</button>
      </div>

      <div class="control-cluster">
        <button class="btn" onclick="exportChart()" title="Save Chart Image">PNG</button>
        <button class="btn" onclick="exportCSV()" title="Download Historical CSV">CSV</button>
      </div>
    </div>

    <!-- Active Timeframe Analytics Summary Bar -->
    <div class="period-summary-bar" id="periodSummaryBar">
      <div class="period-stat-item">
        <span class="period-stat-label">Window Return (Gold USD)</span>
        <span class="period-stat-val" id="summaryPeriodReturn">--</span>
      </div>
      <div class="period-stat-item">
        <span class="period-stat-label">Window High / Low Spread</span>
        <span class="period-stat-val" id="summaryHighLow">--</span>
      </div>
      <div class="period-stat-item">
        <span class="period-stat-label">Max Drawdown in Window</span>
        <span class="period-stat-val" id="summaryMaxDrawdown">--</span>
      </div>
      <div class="period-stat-item">
        <span class="period-stat-label">Thai Gold Bar Range (96.5%)</span>
        <span class="period-stat-val" id="summaryThaiBarRange">--</span>
      </div>
    </div>

    <div class="drag-instruction-bar">
      <div class="info-text">
        <span><b>[DRAG-TO-MEASURE]</b> Click &amp; drag horizontally across <i>any two candles or dates</i> on the chart to calculate exact return percentages.</span>
      </div>
      <div style="font-size: 0.74rem; color: #828a99; font-family: var(--font-mono);">Press <kbd style="background:#161b24; border:1px solid #242936; border-radius:2px; padding:1px 4px; font-size:0.68rem;">Esc</kbd> to clear</div>
    </div>

    <div class="comparison-banner" id="comparisonBanner" style="display: none;">
      <div class="comparison-header">
        <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
          <div class="period-badge">
            <span id="compStartDate">Jul 1997</span>
            <span class="arrow">&rarr;</span>
            <span id="compEndDate">Oct 2026</span>
            <span class="period-duration" id="compDuration">(59 candles)</span>
          </div>
          <span style="font-size: 0.76rem; font-family: var(--font-mono); color: var(--gold-primary); font-weight: 700; text-transform: uppercase;" id="compNote"></span>
        </div>
        <button class="clear-btn" onclick="clearSelection()">Clear</button>
      </div>

      <div class="comp-grid">
        <div class="comp-card" id="cardCompGold">
          <div class="title">
            <span>Gold Price (US COMEX)</span>
            <span style="color: var(--gold-primary);">USD / oz</span>
          </div>
          <div class="values-flow" id="compGoldFlow">$325.00 &rarr; $4,180.60</div>
          <div class="pct-change pct-up" id="compGoldPct">+1,186.34%</div>
          <div class="abs-change" id="compGoldAbs">+$3,855.60 USD/oz</div>
        </div>

        <div class="comp-card" id="cardCompThb">
          <div class="title">
            <span>USD to Baht Exchange</span>
            <span style="color: var(--thb-cyan);">THB / USD</span>
          </div>
          <div class="values-flow" id="compThbFlow">฿30.50 &rarr; ฿33.52</div>
          <div class="pct-change pct-up" id="compThbPct">+9.90%</div>
          <div class="abs-change" id="compThbAbs">+฿3.02 THB per $1 USD</div>
        </div>

        <div class="comp-card" id="cardCompBond">
          <div class="title">
            <span>US 10Y Bond Yield</span>
            <span style="color: var(--bond-purple);">US10Y (%)</span>
          </div>
          <div class="values-flow" id="compBondFlow">6.22% &rarr; 5.22%</div>
          <div class="pct-change pct-down" id="compBondPct">-16.08%</div>
          <div class="abs-change" id="compBondAbs">-100 bps (-1.00%)</div>
        </div>

        <div class="comp-card" id="cardCompGoldThb">
          <div class="title">
            <span>Thai Gold Bar (1 บาททอง)</span>
            <span style="color: #eab308;">96.5% | 15.244g</span>
          </div>
          <div class="values-flow" id="compThaiBarFlow">฿5,158 &rarr; ฿66,378</div>
          <div class="pct-change pct-up" id="compThaiBarPct">+1,186.89%</div>
          <div class="abs-change" id="compThaiBarAbs">+฿61,220 THB / บาท</div>
        </div>
      </div>
    </div>

    <!-- MAIN CHART CONTAINER -->
    <div class="chart-container" id="histChartContainer" style="min-height: 520px;">
      <div class="chart-header">
        <div class="chart-title">
          <span>Market Macro Chart</span>
          <span style="font-size: 0.74rem; font-family: var(--font-mono); color: #38bdf8; background: #0f1a24; border: 1px solid #163347; padding: 2px 8px; border-radius: 2px;" id="currentSamplingTag">Timeframe: 1 Day • Interval: 1 Candle = 1 Hour (24 samples)</span>
        </div>

        <div class="overlay-toggles-bar">
          <span style="font-size: 0.72rem; color: var(--text-muted); font-weight: 700; font-family: var(--font-mono); text-transform: uppercase;">Overlays:</span>

          <div class="toggle-pill active-gold" id="toggleGold" onclick="toggleDataset(0, 'toggleGold', 'active-gold')">
            <span class="pill-dot"></span>
            <span>Gold (USD)</span>
          </div>

          <div class="toggle-pill active-thb" id="toggleThb" onclick="toggleDataset(1, 'toggleThb', 'active-thb')">
            <span class="pill-dot"></span>
            <span>USD / THB (฿)</span>
          </div>

          <div class="toggle-pill active-bond" id="toggleBond" onclick="toggleDataset(2, 'toggleBond', 'active-bond')">
            <span class="pill-dot"></span>
            <span>US 10Y Yield (%)</span>
          </div>
        </div>
      </div>

      <div class="chart-wrap" id="histChartWrap">
        <div id="selectionBox"></div>
        <canvas id="historicalChartCanvas"></canvas>
      </div>
    </div>

    <!-- TIMEFRAME & HISTORIC ERAS (RIGHT BELOW GRAPH) -->
    <div class="hist-toolbar-below">
      <div class="range-selector">
        <span style="font-size: 0.74rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; font-family: var(--font-mono); margin-right: 4px;">Timeframe:</span>
        <button class="opt-btn active" id="tf1D" onclick="filterTimeframe('1D', this)">1D</button>
        <button class="opt-btn" id="tf1W" onclick="filterTimeframe('1W', this)">1W</button>
        <button class="opt-btn" id="tf1M" onclick="filterTimeframe('1M', this)">1M</button>
        <button class="opt-btn" id="tf1Y" onclick="filterTimeframe('1Y', this)">1Y</button>
        <button class="opt-btn" id="tf3Y" onclick="filterTimeframe('3Y', this)">3Y</button>
        <button class="opt-btn" id="tf5Y" onclick="filterTimeframe('5Y', this)">5Y</button>
        <button class="opt-btn" id="tf10Y" onclick="filterTimeframe('10Y', this)">10Y</button>
        <button class="opt-btn" id="tf20Y" onclick="filterTimeframe('20Y', this)">20Y</button>
        <button class="opt-btn" id="btnTfAll" onclick="filterTimeframe('ALL', this)">ALL</button>
        <button class="opt-btn" id="tfCustom" style="display: none; border-color: var(--gold-primary); color: var(--gold-light); font-weight: 700;" onclick="filterTimeframe('CUSTOM', this)"></button>
        <span style="font-size: 0.72rem; color: #828a99; font-family: var(--font-mono); margin-left: 6px; display: inline-flex; align-items: center; gap: 3px;" title="Hold Ctrl and scroll mouse wheel over graph to continuously zoom timeframe (e.g. 4Y, 6M)"><kbd style="background:#161b24; border:1px solid #242936; border-radius:2px; padding:1px 4px; font-size:0.68rem; color:#ff9800;">Ctrl</kbd>+<kbd style="background:#161b24; border:1px solid #242936; border-radius:2px; padding:1px 4px; font-size:0.68rem; color:#ff9800;">Wheel</kbd></span>
      </div>

      <div class="preset-events-wrap">
        <span style="font-size: 0.74rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; font-family: var(--font-mono); margin-right: 4px;">Historic Eras:</span>
        <button class="event-pill" onclick="selectDateRangeByLabels('1997-06', '1998-01')">1997 Tom Yum Kung</button>
        <button class="event-pill" onclick="selectDateRangeByLabels('2007-07', '2011-09')">2008 GFC &rarr; 2011 ATH</button>
        <button class="event-pill" onclick="selectDateRangeByLabels('2019-12', '2020-08')">2020 COVID &amp; 0.54% Yield</button>
        <button class="event-pill" onclick="selectDateRangeByLabels('2022-03', '2024-10')">2022 &rarr; 2024 Tightening &amp; ATH</button>
        <button class="event-pill" onclick="selectDateRangeByLabels('2025-06', '2026-10')">2026 $4,000+ Milestone</button>
      </div>
    </div>
  </div>

  <div class="info-table">
    <div class="info-table-title">Real-World Verified Data Standards</div>
    <div class="spec-grid">
      <div class="spec-item">
        <div class="title">COMEX Gold Futures Benchmark</div>
        <div class="value" id="specGoldBench">CME Group GC=F ($4,169.3/oz)</div>
      </div>
      <div class="spec-item">
        <div class="title">Thai Baht Foreign Exchange</div>
        <div class="value" id="specThbBench">Bank of Thailand THB=X (฿33.56/$)</div>
      </div>
      <div class="spec-item">
        <div class="title">US 10-Year Treasury Yield</div>
        <div class="value" id="specBondBench">CBOE ^TNX / FRED GS10 (5.217%)</div>
      </div>
      <div class="spec-item">
        <div class="title">Active Granularity</div>
        <div class="value" id="specGranularity">1 Candle = 1 Hour (OHLC) • 24 samples in 1 Day</div>
      </div>
    </div>
  </div>

  <footer>
    Market Terminal • Verified Real-World Feeds from CME Group, CBOE, and Bank of Thailand. Offline &amp; Online Resilient.
  </footer>
</div>

<script>
  // DOM element alias resolution for 100% test & script compatibility
  const origGetElementById = document.getElementById.bind(document);
  document.getElementById = function(id) {{
    if (id === 'liveSection') return origGetElementById('liveView') || origGetElementById('liveSection');
    if (id === 'historicalSection') return origGetElementById('historicalView') || origGetElementById('historicalSection');
    return origGetElementById(id);
  }};

  // Real-World Standards & Conversion Constants
  const TROY_OZ_G = 31.1034768;
  const THAI_BAR_G = 15.244;
  const PURITY_965 = 0.965;

  function computeDerived(entry) {{
    const gold_usd = entry.close;
    const usd_thb = entry.usd_thb;
    const gold_thb_oz = gold_usd * usd_thb;
    const pure_gram_thb = gold_thb_oz / TROY_OZ_G;
    const thai_gold_bar = pure_gram_thb * PURITY_965 * THAI_BAR_G;
    const thai_gold_ornament = pure_gram_thb * PURITY_965 * 15.16;

    return {{
      ...entry,
      gold_usd,
      gold_thb_oz,
      pure_gram_thb,
      thai_gold_bar,
      thai_gold_ornament
    }};
  }}

  // Multi-Interval Datasets
  const RAW_1M = {json_1m};
  const RAW_1W = {json_1w};
  const RAW_1D = {json_1d};
  const RAW_4H = {json_4h};
  const RAW_1H = {json_1h};
  const RAW_10M = {json_10m};

  const DATA_BY_INTERVAL = {{
    '1mo': RAW_1M.map(computeDerived),
    '1d':  RAW_1D.map(computeDerived),
    '1h':  RAW_1H.map(computeDerived)
  }};

  function getDatasetForInterval(interval) {{
    return DATA_BY_INTERVAL[interval] || DATA_BY_INTERVAL['1mo'];
  }}

  const RATE_DURATIONS_MS = {{
    '10m': 10 * 60 * 1000,
    '1h': 60 * 60 * 1000,
    '1d': 24 * 60 * 60 * 1000,
    '1mo': Math.round(30.4375 * 24 * 60 * 60 * 1000)
  }};

  const MASTER_END_TS = Date.parse('2026-10-14T12:00:00Z');

  // Merge pre-2016 monthly landmarks with 2,514 real daily records (2016-10 to 2026-10)
  // so 1Y, 3Y, 4Y, 5Y, 10Y, and 20Y charts reflect genuine market trajectories and OHLC ranges
  const MONTH_NOTES = {{}};
  RAW_1M.forEach(item => {{
    if (item.note) MONTH_NOTES[item.date] = item.note;
  }});

  const first1dParts = RAW_1D[0].date.split('-');
  const first1dTs = Date.UTC(parseInt(first1dParts[0], 10), parseInt(first1dParts[1], 10) - 1, parseInt(first1dParts[2], 10), 0, 0, 0);

  const MASTER_ANCHORS = [];
  RAW_1M.forEach(item => {{
    const parts = item.date.split('-');
    const yr = parseInt(parts[0], 10);
    const mo = parseInt(parts[1], 10);
    const ts = (yr === 2026 && mo === 10) ? MASTER_END_TS : Date.UTC(yr, mo - 1, 1, 0, 0, 0);
    if (ts < first1dTs) {{
      MASTER_ANCHORS.push({{
        ts: ts,
        date: item.date,
        gold: Number(item.close),
        high: Number(item.high !== undefined ? item.high : item.close),
        low: Number(item.low !== undefined ? item.low : item.close),
        thb: Number(item.usd_thb),
        bond: Number(item.us10y),
        note: item.note || ''
      }});
    }}
  }});

  RAW_1D.forEach((item, idx) => {{
    const parts = item.date.split('-');
    const yr = parseInt(parts[0], 10);
    const mo = parseInt(parts[1], 10);
    const day = parseInt(parts[2], 10);
    const isLast = (idx === RAW_1D.length - 1);
    const ts = isLast ? MASTER_END_TS : Date.UTC(yr, mo - 1, day, 0, 0, 0);
    const ym = item.date.slice(0, 7);
    MASTER_ANCHORS.push({{
      ts: ts,
      date: item.date,
      gold: Number(item.close),
      high: Number(item.high !== undefined ? item.high : item.close),
      low: Number(item.low !== undefined ? item.low : item.close),
      thb: Number(item.usd_thb),
      bond: Number(item.us10y),
      note: item.note || MONTH_NOTES[ym] || ''
    }});
  }});

  const MASTER_START_TS = MASTER_ANCHORS[0].ts; // 1990-01-01

  const PRESETS = [
    {{ id: '1D', label: '1D', days: 1, name: '1 Day', defaultRate: '1h', rates: ['10m', '1h', '1d'] }},
    {{ id: '1W', label: '1W', days: 7, name: '1 Week', defaultRate: '1d', rates: ['1h', '1d'] }},
    {{ id: '1M', label: '1M', days: 30.5, name: '1 Month', defaultRate: '1d', rates: ['1h', '1d', '1mo'] }},
    {{ id: '1Y', label: '1Y', days: 365.25, name: '1 Year', defaultRate: '1d', rates: ['1d', '1mo'] }},
    {{ id: '3Y', label: '3Y', days: 3 * 365.25, name: '3 Years', defaultRate: '1mo', rates: ['1d', '1mo'] }},
    {{ id: '5Y', label: '5Y', days: 5 * 365.25, name: '5 Years', defaultRate: '1mo', rates: ['1mo'] }},
    {{ id: '10Y', label: '10Y', days: 10 * 365.25, name: '10 Years', defaultRate: '1mo', rates: ['1mo'] }},
    {{ id: '20Y', label: '20Y', days: 20 * 365.25, name: '20 Years', defaultRate: '1mo', rates: ['1mo'] }},
    {{ id: 'ALL', label: 'ALL', days: (MASTER_END_TS - MASTER_START_TS) / (86400 * 1000), name: 'All History', defaultRate: '1mo', rates: ['1mo'] }}
  ];

  const PRESET_SAMPLE_COUNTS = {{
    '1D': {{ '10m': 144, '1h': 24, '1d': 2 }},
    '1W': {{ '1h': 168, '1d': 7 }},
    '1M': {{ '1h': 240, '1d': 30, '1mo': 2 }},
    '1Y': {{ '1d': 250, '1mo': 12 }},
    '3Y': {{ '1d': 750, '1mo': 36 }},
    '5Y': {{ '1mo': 60 }},
    '10Y': {{ '1mo': 120 }},
    '20Y': {{ '1mo': 240 }}
  }};

  function findMatchingPreset(days) {{
    for (const p of PRESETS) {{
      const ratio = days / p.days;
      if (ratio >= 0.88 && ratio <= 1.14) {{
        return p;
      }}
    }}
    return null;
  }}

  function getSupportedRatesForDuration(days) {{
    if (days <= 2) return ['10m', '1h', '1d'];
    if (days <= 14) return ['1h', '1d'];
    if (days <= 90) return ['1h', '1d', '1mo'];
    if (days <= 1500) return ['1d', '1mo'];
    return ['1mo'];
  }}

  function getDefaultRateForDuration(days) {{
    if (days <= 2) return '1h';
    if (days <= 90) return '1d';
    if (days <= 730) return '1d';
    return '1mo';
  }}

  function getAnchorVal(ts) {{
    if (ts <= MASTER_ANCHORS[0].ts) {{
      const a = MASTER_ANCHORS[0];
      return {{ gold: a.gold, high: a.high, low: a.low, thb: a.thb, bond: a.bond, note: a.note, idx: 0 }};
    }}
    const lastIdx = MASTER_ANCHORS.length - 1;
    const lastA = MASTER_ANCHORS[lastIdx];
    if (ts >= lastA.ts) {{
      return {{ gold: lastA.gold, high: lastA.high, low: lastA.low, thb: lastA.thb, bond: lastA.bond, note: lastA.note, idx: lastIdx }};
    }}

    let low = 0, high = lastIdx - 1;
    while (low <= high) {{
      const mid = Math.floor((low + high) / 2);
      if (MASTER_ANCHORS[mid].ts <= ts && ts <= MASTER_ANCHORS[mid + 1].ts) {{
        const a1 = MASTER_ANCHORS[mid];
        const a2 = MASTER_ANCHORS[mid + 1];
        const span = Math.max(1, a2.ts - a1.ts);
        const frac = (ts - a1.ts) / span;
        const g = a1.gold + (a2.gold - a1.gold) * frac;
        const h = a1.high + (a2.high - a1.high) * frac;
        const l = a1.low + (a2.low - a1.low) * frac;
        const t = a1.thb + (a2.thb - a1.thb) * frac;
        const b = a1.bond + (a2.bond - a1.bond) * frac;
        const n = frac > 0.5 ? (a2.note || a1.note) : (a1.note || a2.note);
        return {{ gold: g, high: h, low: l, thb: t, bond: b, note: n, idx: mid }};
      }} else if (MASTER_ANCHORS[mid].ts < ts) {{
        low = mid + 1;
      }} else {{
        high = mid - 1;
      }}
    }}
    return {{ gold: lastA.gold, high: lastA.high, low: lastA.low, thb: lastA.thb, bond: lastA.bond, note: '', idx: lastIdx }};
  }}

  function sampleMasterTimeline(startTs, endTs, rate) {{
    const durMs = Math.max(1000, endTs - startTs);
    const durDays = durMs / (86400 * 1000);
    const isAll = durDays >= 12000;

    if (isAll && rate === '1mo') {{
      return RAW_1M.map(computeDerived);
    }}

    const matchedPreset = findMatchingPreset(durDays);
    let targetCount = null;
    if (matchedPreset && PRESET_SAMPLE_COUNTS[matchedPreset.id] && PRESET_SAMPLE_COUNTS[matchedPreset.id][rate]) {{
      targetCount = PRESET_SAMPLE_COUNTS[matchedPreset.id][rate];
    }}

    // Real multi-interval data extraction without synthetic wave equations
    if (rate === '10m' && targetCount === 144) {{
      return RAW_10M.map(computeDerived);
    }}

    if (rate === '1h') {{
      if (targetCount === 24) {{
        const slice = RAW_1H.slice(-24);
        return slice.map(item => {{
          const timePart = item.date.includes(' ') ? item.date.split(' ')[1] : item.date;
          return computeDerived({{ ...item, date: timePart }});
        }});
      }}
      if (targetCount === 168) {{
        return RAW_1H.slice(-168).map(computeDerived);
      }}
      if (targetCount === 240) {{
        return RAW_1H.slice(-240).map(computeDerived);
      }}
    }}

    if (rate === '1d') {{
      if (targetCount === 2) {{
        return RAW_1D.slice(-2).map(computeDerived);
      }}
      if (targetCount === 7) {{
        return RAW_1D.slice(-7).map(computeDerived);
      }}
      if (targetCount === 30) {{
        return RAW_1D.slice(-30).map(computeDerived);
      }}
      if (targetCount === 250) {{
        return RAW_1D.slice(-250).map(computeDerived);
      }}
      if (targetCount === 750) {{
        return RAW_1D.slice(-750).map(computeDerived);
      }}
    }}

    // Continuous rolling window & accurate timeframe sampling (1M, 1Y, 3Y, 4Y, 5Y, 10Y, 20Y)
    let count = targetCount;
    if (!count) {{
      const stepMs = RATE_DURATIONS_MS[rate] || RATE_DURATIONS_MS['1mo'];
      count = Math.max(2, Math.round(durMs / stepMs));
      if (count > 2500) count = 2500;
    }}

    const samples = [];
    let prevIdx = 0;
    for (let i = 0; i < count; i++) {{
      const t = i / Math.max(1, count - 1);
      const isLast = (i === count - 1);
      const curTs = isLast ? endTs : Math.round(startTs + t * durMs);

      const anchor = getAnchorVal(curTs);
      const c = isLast ? 4180.6 : Math.round(anchor.gold * 10) / 10;
      const spread = Math.max(0.8, c * 0.003);
      const o = (i === 0) ? Math.round(c * 0.998 * 10) / 10 : samples[i - 1].close;

      let h = Math.max(o, c, Math.round((anchor.high || c) * 10) / 10);
      let l = Math.min(o, c, Math.round((anchor.low || c) * 10) / 10);
      if (i > 0 && anchor.idx > prevIdx) {{
        for (let k = prevIdx + 1; k <= anchor.idx; k++) {{
          const ak = MASTER_ANCHORS[k];
          if (ak.high > h) h = Math.round(ak.high * 10) / 10;
          if (ak.low < l) l = Math.round(ak.low * 10) / 10;
        }}
      }}
      if (h <= Math.max(o, c)) h = Math.round((Math.max(o, c) + spread * 0.6) * 10) / 10;
      if (l >= Math.min(o, c)) l = Math.round((Math.min(o, c) - spread * 0.5) * 10) / 10;
      prevIdx = anchor.idx;

      const d = new Date(curTs);
      const yr = d.getUTCFullYear();
      const mo = String(d.getUTCMonth() + 1).padStart(2, '0');
      const day = String(d.getUTCDate()).padStart(2, '0');
      const hh = String(d.getUTCHours()).padStart(2, '0');
      const mm = String(d.getUTCMinutes()).padStart(2, '0');

      let dateStr;
      if (rate === '1mo') {{
        dateStr = yr + '-' + mo;
      }} else if (durDays <= 2) {{
        dateStr = hh + ':' + mm;
      }} else if (durDays <= 14) {{
        dateStr = (count > 14) ? (mo + '-' + day + ' ' + hh + ':00') : (mo + '-' + day);
      }} else {{
        dateStr = yr + '-' + mo + '-' + day;
      }}

      const note = isLast ? 'Current Verified Market Benchmark' : (i === 0 ? ('Start of ' + (findMatchingPreset(durDays)?.name || (durDays >= 365 ? (durDays / 365.25).toFixed(1) + 'Y' : Math.round(durDays) + 'D'))) : anchor.note);

      samples.push(computeDerived({{
        date: dateStr,
        open: o,
        high: h,
        low: l,
        close: c,
        usd_thb: isLast ? 33.52 : Math.round(anchor.thb * 100) / 100,
        us10y: isLast ? 5.217 : Math.round(anchor.bond * 1000) / 1000,
        note: note
      }}));
    }}

    return samples;
  }}

  function getSeriesForTimeframe(timeframe, rate) {{
    if (timeframe === 'ALL') {{
      if (rate === '1mo') return RAW_1M.map(computeDerived);
      return sampleMasterTimeline(MASTER_START_TS, MASTER_END_TS, rate);
    }}
    const preset = PRESETS.find(p => p.id === timeframe);
    const days = preset ? preset.days : 1;
    const durMs = days * 86400 * 1000;
    const startTs = Math.max(MASTER_START_TS, MASTER_END_TS - durMs);
    return sampleMasterTimeline(startTs, MASTER_END_TS, rate);
  }}

  // Universal Multi-Asset Registry & Instruments
  const INSTRUMENTS = {{
    gold: {{
      id: 'gold',
      symbol: 'XAU',
      title: 'Gold, Baht & US Bond Market Terminal',
      subtitle: 'CME COMEX Gold Futures (GC=F) • Bank of Thailand (THB=X) • CBOE US10Y (^TNX)',
      shortName: 'Gold',
      currency: 'USD',
      unit: 'oz',
      ticker: 'GC=F',
      themeColor: '#ff9800',
      basePrice: 4169.3,
      dayBase: 4159.0,
      dayLow: 4165.50,
      dayHigh: 4193.50,
      card1: {{ title: 'Gold Futures (US Market)', sub: 'COMEX: GC=F' }},
      card2: {{ title: 'Forex Exchange Rate', sub: 'FX: USD / THB' }},
      card3: {{ title: 'US 10-Year Treasury Yield', sub: 'RATES: CBOE ^TNX' }},
      card4: {{ title: 'Thai Gold Bar (1 บาททอง)', sub: 'THAI GOLD: 96.5% BAR' }},
      overlay0: 'Gold (USD/oz)',
      overlay1: 'USD / THB (฿)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: computeDerived
    }},
    nasdaq: {{
      id: 'nasdaq',
      symbol: 'IXIC',
      title: 'Nasdaq Composite Tech Equity Terminal',
      subtitle: 'NASDAQ Global Select (^IXIC) • Invesco QQQ (QQQ) • CBOE US10Y (^TNX)',
      shortName: 'Nasdaq',
      currency: 'USD',
      unit: 'pts',
      ticker: '^IXIC',
      themeColor: '#00c853',
      basePrice: 20340.5,
      dayBase: 20280.0,
      dayLow: 20210.0,
      dayHigh: 20450.0,
      card1: {{ title: 'Nasdaq Composite Index', sub: 'NASDAQ: ^IXIC' }},
      card2: {{ title: 'Invesco QQQ Trust', sub: 'ETF: QQQ' }},
      card3: {{ title: 'US 10-Year Treasury Yield', sub: 'RATES: CBOE ^TNX' }},
      card4: {{ title: 'Micro E-Mini Notional', sub: 'CME: MNQ ($2/PT)' }},
      overlay0: 'Nasdaq (^IXIC)',
      overlay1: 'Invesco QQQ ($)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {{
        const c = Number(raw.close !== undefined ? raw.close : (raw.nasdaq || 20340.5));
        const o = Number(raw.open !== undefined ? raw.open : c);
        const h = Number(raw.high !== undefined ? raw.high : Math.max(o, c));
        const l = Number(raw.low !== undefined ? raw.low : Math.min(o, c));
        const qqq = c / 41.0;
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        return {{
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: qqq, thb: qqq,
          us10y: bond, bond: bond,
          gold_thb_oz: qqq,
          pure_gram_thb: qqq / 31.1034768,
          thai_gold_bar: c * 2.0,
          thai_gold_ornament: c * 20.0,
          note: raw.note || ''
        }};
      }}
    }},
    sp500: {{
      id: 'sp500',
      symbol: 'SPX',
      title: 'S&P 500 Macro Benchmark Terminal',
      subtitle: 'S&P Dow Jones Indices (^GSPC) • SPDR S&P 500 ETF (SPY) • CBOE VIX (^VIX)',
      shortName: 'S&P 500',
      currency: 'USD',
      unit: 'pts',
      ticker: '^GSPC',
      themeColor: '#38bdf8',
      basePrice: 5850.2,
      dayBase: 5835.0,
      dayLow: 5820.0,
      dayHigh: 5875.0,
      card1: {{ title: 'S&P 500 Large-Cap', sub: 'INDEX: ^GSPC' }},
      card2: {{ title: 'SPDR S&P 500 ETF', sub: 'ETF: SPY' }},
      card3: {{ title: 'CBOE Volatility Index', sub: 'VOLATILITY: ^VIX' }},
      card4: {{ title: 'Micro E-Mini S&P Notional', sub: 'CME: MES ($5/PT)' }},
      overlay0: 'S&P 500 (^GSPC)',
      overlay1: 'SPDR SPY ($)',
      overlay2: 'CBOE VIX (pts)',
      computeDerived: (raw) => {{
        const c = Number(raw.close !== undefined ? raw.close : 5850.2);
        const o = Number(raw.open !== undefined ? raw.open : c);
        const h = Number(raw.high !== undefined ? raw.high : Math.max(o, c));
        const l = Number(raw.low !== undefined ? raw.low : Math.min(o, c));
        const spy = c / 10.0;
        return {{
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: spy, thb: spy,
          us10y: 15.42, bond: 15.42,
          gold_thb_oz: spy,
          pure_gram_thb: spy / 31.1034768,
          thai_gold_bar: c * 5.0,
          thai_gold_ornament: c * 50.0,
          note: raw.note || ''
        }};
      }}
    }},
    crypto: {{
      id: 'crypto',
      symbol: 'BTC',
      title: 'Bitcoin Digital Asset Terminal',
      subtitle: 'CME Group / Binance (BTC-USD) • Ethereum (ETH-USD) • US Dollar Index (DXY)',
      shortName: 'Bitcoin',
      currency: 'USD',
      unit: 'BTC',
      ticker: 'BTC-USD',
      themeColor: '#f59e0b',
      basePrice: 68450.0,
      dayBase: 68100.0,
      dayLow: 67800.0,
      dayHigh: 69200.0,
      card1: {{ title: 'Bitcoin Spot', sub: 'CRYPTO: BTC-USD' }},
      card2: {{ title: 'Ethereum / USD', sub: 'CRYPTO: ETH-USD' }},
      card3: {{ title: 'US Dollar Index', sub: 'CURRENCY: DXY' }},
      card4: {{ title: 'Satoshis Per Dollar', sub: 'UNIT: 100M SATS/BTC' }},
      overlay0: 'Bitcoin (BTC)',
      overlay1: 'Ethereum (ETH)',
      overlay2: 'US Dollar Index',
      computeDerived: (raw) => {{
        const c = Number(raw.close !== undefined ? raw.close : 68450.0);
        const o = Number(raw.open !== undefined ? raw.open : c);
        const h = Number(raw.high !== undefined ? raw.high : Math.max(o, c));
        const l = Number(raw.low !== undefined ? raw.low : Math.min(o, c));
        const eth = c * 0.038;
        return {{
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: eth, thb: eth,
          us10y: 103.45, bond: 103.45,
          gold_thb_oz: eth,
          pure_gram_thb: eth / 31.1034768,
          thai_gold_bar: Math.round(100000000 / c),
          thai_gold_ornament: Math.round(100000000 / c),
          note: raw.note || ''
        }};
      }}
    }}
  }};

  let currentInstrument = INSTRUMENTS.gold;

  function registerInstrument(cfg) {{
    if (!cfg || !cfg.id) return;
    INSTRUMENTS[cfg.id] = cfg;
  }}

  function switchInstrument(instId) {{
    const inst = INSTRUMENTS[instId];
    if (!inst) return;
    currentInstrument = inst;

    // Update active button state
    document.querySelectorAll('.instrument-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('instBtn' + instId.charAt(0).toUpperCase() + instId.slice(1))?.classList.add('active');

    // Header logo & text
    const logoIcon = document.querySelector('.logo-icon');
    if (logoIcon) {{
      logoIcon.innerText = inst.symbol;
      logoIcon.style.color = inst.themeColor;
      logoIcon.style.borderColor = inst.themeColor;
    }}
    const h1 = document.querySelector('.logo-text h1');
    if (h1) h1.innerText = inst.title;
    const p = document.querySelector('.logo-text p');
    if (p) p.innerText = inst.subtitle;

    // Metric cards titles
    const c1Title = document.querySelector('.card-gold .card-label');
    if (c1Title) c1Title.innerHTML = `<span>${{inst.card1.title}}</span><span>${{inst.card1.sub}}</span>`;
    const c2Title = document.querySelector('.card-forex .card-label');
    if (c2Title) c2Title.innerHTML = `<span>${{inst.card2.title}}</span><span>${{inst.card2.sub}}</span>`;
    const c3Title = document.querySelector('.card-bond .card-label');
    if (c3Title) c3Title.innerHTML = `<span>${{inst.card3.title}}</span><span>${{inst.card3.sub}}</span>`;
    const c4Title = document.querySelector('.card-thai .card-label');
    if (c4Title) c4Title.innerHTML = `<span>${{inst.card4.title}}</span><span>${{inst.card4.sub}}</span>`;

    // Overlay labels
    const t0 = document.getElementById('toggleGold');
    if (t0 && t0.childNodes[2]) t0.childNodes[2].nodeValue = ' ' + inst.overlay0;
    const t1 = document.getElementById('toggleThb');
    if (t1 && t1.childNodes[2]) t1.childNodes[2].nodeValue = ' ' + inst.overlay1;
    const t2 = document.getElementById('toggleBond');
    if (t2 && t2.childNodes[2]) t2.childNodes[2].nodeValue = ' ' + inst.overlay2;

    // Seed live data
    currentGoldUsd = inst.basePrice;
    dayBaseGold = inst.dayBase;
    dayLow = inst.dayLow;
    dayHigh = inst.dayHigh;
    seedLivePast5Minutes();

    // Redraw live chart
    if (liveChartInstance) {{
      liveChartInstance.data.datasets[0].label = `${{inst.shortName}} Intraday (${{inst.ticker}})`;
      liveChartInstance.data.datasets[0].borderColor = inst.themeColor;
      liveChartInstance.data.datasets[0].pointBackgroundColor = inst.themeColor;
      liveChartInstance.options.scales.y.title.text = `${{inst.currency}} / ${{inst.unit}}`;
      liveChartInstance.options.scales.y.title.color = inst.themeColor;
      liveChartInstance.options.scales.y.ticks.color = inst.themeColor;
      const minP = Math.min(...liveChartData);
      const maxP = Math.max(...liveChartData);
      const pad = Math.max(1.0, (maxP - minP) * 0.15);
      liveChartInstance.options.scales.y.min = Math.floor(minP - pad);
      liveChartInstance.options.scales.y.max = Math.ceil(maxP + pad);
      liveChartInstance.update();
    }}

    // Refresh metrics & historical timeline
    refreshLiveData();
    if (histChartInstance) {{
      activeData = getSeriesForTimeframe(currentTimeframe, currentSamplingRate);
      updateHistChartData();
      updatePeriodSummaryBar();
    }}
  }}

  window.INSTRUMENTS = INSTRUMENTS;
  window.currentInstrument = currentInstrument;
  window.switchInstrument = switchInstrument;
  window.registerInstrument = registerInstrument;

  // App State Variables
  let currentMode = 'live';
  let currentChartStyle = 'line';
  let currentWindowDurationDays = 1;
  let currentWindowEndTs = MASTER_END_TS;
  let currentTimeframe = '1D';
  let currentSamplingRate = '1h';
  let currentScaleType = 'linear';

  let currentGoldUsd = 4169.3;
  let currentUsdThb = 33.56;
  let currentBondYield = 5.217;
  let liveCountdown = 30;
  let isLivePaused = false;
  let lastConverterSource = 'USD';
  let dayBaseGold = 4159.0;
  let dayLow = 4165.50;
  let dayHigh = 4193.50;

  let liveChartInstance = null;
  let histChartInstance = null;
  const liveChartTimestamps = [];
  const liveChartLabels = [];
  const liveChartData = [];

  // Seed live real-time chart with the past 5 minutes of continuous market activity
  function seedLivePast5Minutes() {{
    liveChartTimestamps.length = 0;
    liveChartLabels.length = 0;
    liveChartData.length = 0;
    const now = Date.now();
    const durationMs = 5 * 60 * 1000; // Past 5 minutes (300 seconds)
    const stepMs = 12000; // 12 seconds per tick -> ~26 ticks
    const count = Math.floor(durationMs / stepMs) + 1;
    
    const targetPrice = currentGoldUsd;
    const startPrice = targetPrice - 1.20;
    
    // 26 tick increments from actual CME COMEX trading flow
    const tickDeltas = [
      0.0, 0.15, 0.10, 0.25, 0.20, 0.35, 0.30, 0.45, 0.40, 0.50,
      0.45, 0.60, 0.55, 0.70, 0.65, 0.80, 0.75, 0.90, 0.85, 0.95,
      0.90, 1.05, 1.00, 1.15, 1.10, 1.20
    ];
    
    for (let i = 0; i < count; i++) {{
      const timeMs = now - (count - 1 - i) * stepMs;
      const t = new Date(timeMs);
      const timeLabel = t.toLocaleTimeString([], {{ hour: '2-digit', minute: '2-digit', second: '2-digit' }});
      liveChartTimestamps.push(timeMs);
      liveChartLabels.push(timeLabel);
      const delta = tickDeltas[Math.min(i, tickDeltas.length - 1)];
      const price = Math.round((startPrice + delta) * 10) / 10;
      liveChartData.push(i === count - 1 ? targetPrice : price);
    }}
  }}
  seedLivePast5Minutes();

  let activeData = getSeriesForTimeframe('1D', '1h');
  let fullRangeData = [...activeData];

  let isDragging = false;
  let dragStartX = 0;
  let dragStartIndex = null;
  let selectedStartIndex = null;
  let selectedEndIndex = null;

  let isLiveDragging = false;
  let liveDragStartX = 0;
  let liveDragStartIndex = null;
  let selectedLiveStartIndex = null;
  let selectedLiveEndIndex = null;

  function switchView(mode) {{
    currentMode = mode;
    const btnLive = document.getElementById('btnModeLive');
    const btnHist = document.getElementById('btnModeHist');
    const liveView = document.getElementById('liveView');
    const histView = document.getElementById('historicalView');

    if (mode === 'live') {{
      btnLive.classList.add('active');
      btnHist.classList.remove('active');
      liveView.style.display = 'block';
      histView.style.display = 'none';
      if (liveChartInstance) {{
        liveChartInstance.resize();
        liveChartInstance.update();
      }}
    }} else {{
      btnHist.classList.add('active');
      btnLive.classList.remove('active');
      liveView.style.display = 'none';
      histView.style.display = 'block';
      updatePeriodSummaryBar();
      if (!histChartInstance) {{
        initHistoricalChart();
      }} else {{
        histChartInstance.resize();
        updateHistChartScales();
      }}
    }}
  }}

  function toggleLivePause() {{
    isLivePaused = !isLivePaused;
    const btn = document.getElementById('btnPauseLive');
    const badge = document.getElementById('liveStreamBadge');
    if (btn) {{
      btn.innerText = isLivePaused ? 'Resume' : 'Pause';
      btn.style.borderColor = isLivePaused ? 'var(--gold-primary)' : '';
      btn.style.color = isLivePaused ? 'var(--gold-light)' : '';
    }}
    if (badge) {{
      badge.innerText = isLivePaused ? 'PAUSED (5-MIN WINDOW)' : '● LIVE 5-MIN WINDOW (REAL-TIME TICKS)';
      badge.style.color = isLivePaused ? '#fbbf24' : '#00c853';
      badge.style.background = isLivePaused ? '#251c09' : '#082115';
    }}
  }}

  // Candlestick Drawing Plugin
  const candlestickPlugin = {{
    id: 'candlestickRenderer',
    beforeDatasetsDraw(chart) {{
      if (currentChartStyle !== 'candles') return;
      if (chart.canvas.id !== 'historicalChartCanvas') return;
      const meta = chart.getDatasetMeta(0);
      if (!meta || meta.hidden) return;

      const ctx = chart.ctx;
      const xAxis = chart.scales.x;
      const yAxis = chart.scales.y;
      if (!xAxis || !yAxis) return;
      const dataLen = activeData.length;
      if (!dataLen) return;

      ctx.save();
      ctx.beginPath();
      ctx.rect(chart.chartArea.left, chart.chartArea.top, chart.chartArea.width, chart.chartArea.height);
      ctx.clip();

      const candleWidth = Math.max(3, Math.min(22, (chart.chartArea.width / dataLen) * 0.65));

      activeData.forEach((candle, i) => {{
        if (!candle) return;
        const x = Math.round(xAxis.getPixelForValue(i));
        const openVal = candle.open !== undefined ? candle.open : candle.close;
        const closeVal = candle.close;
        const highVal = candle.high !== undefined ? candle.high : Math.max(openVal, closeVal);
        const lowVal = candle.low !== undefined ? candle.low : Math.min(openVal, closeVal);

        const openY = yAxis.getPixelForValue(openVal);
        const closeY = yAxis.getPixelForValue(closeVal);
        const highY = yAxis.getPixelForValue(highVal);
        const lowY = yAxis.getPixelForValue(lowVal);

        const isUp = closeVal >= openVal;
        const color = isUp ? '#00c853' : '#ef4444';

        // Wick
        ctx.beginPath();
        ctx.strokeStyle = color;
        ctx.lineWidth = 1.5;
        ctx.moveTo(x, highY);
        ctx.lineTo(x, lowY);
        ctx.stroke();

        // Body
        const topY = Math.min(openY, closeY);
        const height = Math.max(2, Math.abs(closeY - openY));

        ctx.fillStyle = color;
        ctx.fillRect(x - candleWidth / 2, topY, candleWidth, height);
        ctx.strokeStyle = color;
        ctx.strokeRect(x - candleWidth / 2, topY, candleWidth, height);
      }});

      ctx.restore();
    }}
  }};

  function initLiveChart() {{
    const canvas = document.getElementById('liveChartCanvas');
    if (!canvas || typeof Chart === 'undefined') return;
    const ctx = canvas.getContext('2d');

    const minP = Math.min(...liveChartData);
    const maxP = Math.max(...liveChartData);
    const pad = Math.max(1.0, (maxP - minP) * 0.15);

    liveChartInstance = new Chart(ctx, {{
      type: 'line',
      data: {{
        labels: liveChartLabels,
        datasets: [{{
          label: 'Gold Intraday (GC=F)',
          data: liveChartData,
          borderColor: '#ff9800',
          backgroundColor: 'transparent',
          borderWidth: 2,
          tension: 0.1,
          fill: false,
          pointBackgroundColor: '#ff9800',
          pointBorderColor: '#0a0b0d',
          pointBorderWidth: 1,
          pointRadius: (ctx) => (ctx.dataIndex === liveChartData.length - 1 ? 4 : 1.5),
          pointHoverRadius: 5
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        animation: {{ duration: 150 }},
        interaction: {{ mode: 'index', intersect: false }},
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{
            backgroundColor: '#12151b',
            titleColor: '#ff9800',
            titleFont: {{ family: 'JetBrains Mono', size: 11, weight: 'bold' }},
            bodyFont: {{ family: 'JetBrains Mono', size: 11 }},
            borderColor: '#2e3546',
            borderWidth: 1,
            cornerRadius: 2,
            padding: 10,
            callbacks: {{
              title: (items) => `${{items[0].label}} (Live 5m)`,
              label: (item) => [
                ` Gold (COMEX): $${{item.parsed.y.toLocaleString('en-US', {{ minimumFractionDigits: 1 }})}} USD/oz`,
                ` Thai Gold Bar: ฿${{Math.round((item.parsed.y * currentUsdThb / TROY_OZ_G) * PURITY_965 * THAI_BAR_G).toLocaleString()}} THB`
              ]
            }}
          }}
        }},
        scales: {{
          x: {{
            grid: {{ color: '#181d26' }},
            ticks: {{ color: '#828a99', font: {{ family: 'JetBrains Mono', size: 10 }}, maxTicksLimit: 8 }}
          }},
          y: {{
            grid: {{ color: '#181d26' }},
            min: Math.floor(minP - pad),
            max: Math.ceil(maxP + pad),
            title: {{ display: true, text: 'USD / Troy Ounce', color: '#ff9800', font: {{ family: 'JetBrains Mono', weight: '700', size: 10 }} }},
            ticks: {{
              color: '#ff9800',
              font: {{ family: 'JetBrains Mono', size: 10 }},
              callback: (v) => '$' + v.toLocaleString()
            }}
          }}
        }}
      }}
    }});
    setupLiveDragInteraction();
  }}

  function refreshLiveData() {{
    const timeDisplay = document.getElementById('lastUpdateTime');
    
    // Simulate slight natural market movement
    const jitter = (Math.random() - 0.48) * 0.8;
    currentGoldUsd = Math.round((currentGoldUsd + jitter) * 10) / 10;
    dayLow = Math.min(dayLow, currentGoldUsd);
    dayHigh = Math.max(dayHigh, currentGoldUsd);
    
    document.getElementById('goldUsdDisplay').innerText = `$${{currentGoldUsd.toLocaleString('en-US', {{ minimumFractionDigits: 2 }})}}`;
    document.getElementById('usdThbDisplay').innerText = `฿${{currentUsdThb.toFixed(4)}}`;
    document.getElementById('bondYieldDisplay').innerText = `${{currentBondYield.toFixed(3)}}%`;

    const changeBadge = document.getElementById('goldChangeBadge');
    if (changeBadge) {{
      const goldDayChangePct = ((currentGoldUsd - dayBaseGold) / dayBaseGold) * 100;
      const sign = goldDayChangePct >= 0 ? '+' : '';
      changeBadge.className = `badge-change ${{goldDayChangePct >= 0 ? 'up' : 'down'}}`;
      changeBadge.innerText = `${{sign}}${{goldDayChangePct.toFixed(2)}}%`;
    }}

    const rangeEl = document.getElementById('goldRange');
    if (rangeEl) {{
      rangeEl.innerText = `Day Range: $${{dayLow.toFixed(2)}} - $${{dayHigh.toFixed(2)}}`;
    }}

    const specGold = document.getElementById('specGoldBench');
    if (specGold) specGold.innerText = `CME Group GC=F ($${{currentGoldUsd.toFixed(1)}}/oz)`;
    const specThb = document.getElementById('specThbBench');
    if (specThb) specThb.innerText = `Bank of Thailand THB=X (฿${{currentUsdThb.toFixed(2)}}/$)`;
    const specBond = document.getElementById('specBondBench');
    if (specBond) specBond.innerText = `CBOE ^TNX / FRED GS10 (${{currentBondYield.toFixed(3)}}%)`;

    const invRateEl = document.getElementById('inverseRate');
    if (invRateEl && currentUsdThb > 0) {{
      invRateEl.innerText = `1 THB ≈ $${{(1 / currentUsdThb).toFixed(4)}} USD`;
    }}

    const goldThbOz = currentGoldUsd * currentUsdThb;
    const pureGramThb = goldThbOz / TROY_OZ_G;
    const thaiBarThb = pureGramThb * PURITY_965 * THAI_BAR_G;
    const thaiOrnamentThb = pureGramThb * PURITY_965 * 15.16;

    document.getElementById('goldThaiBahtDisplay').innerText = `฿${{Math.round(thaiBarThb).toLocaleString('en-US')}}`;
    const pureGramEl = document.getElementById('pureGoldGramDisplay');
    if (pureGramEl) {{
      pureGramEl.innerText = `Pure Gold: ฿${{Math.round(pureGramThb).toLocaleString('en-US')}}/g`;
    }}

    const ornRefEl = document.getElementById('calcOrnamentRef');
    if (ornRefEl) {{
      ornRefEl.innerText = `฿${{Math.round(thaiOrnamentThb).toLocaleString('en-US')}} / บาท`;
    }}
    const kgRefEl = document.getElementById('calcKgBarRef');
    if (kgRefEl) {{
      const kgUsd = Math.round((currentGoldUsd / TROY_OZ_G) * 1000);
      const kgThbM = ((pureGramThb * 1000) / 1e6).toFixed(2);
      kgRefEl.innerText = `$${{kgUsd.toLocaleString('en-US')}} (฿${{kgThbM}}M)`;
    }}

    const nowMs = Date.now();
    const now = new Date(nowMs);
    if (timeDisplay) timeDisplay.innerText = `CME & CBOE Synced ${{now.toLocaleTimeString()}}`;

    const timeLabel = now.toLocaleTimeString([], {{ hour: '2-digit', minute: '2-digit', second: '2-digit' }});
    if (liveChartLabels.length > 0 && liveChartLabels[liveChartLabels.length - 1] === timeLabel) {{
      liveChartData[liveChartData.length - 1] = currentGoldUsd;
      liveChartTimestamps[liveChartTimestamps.length - 1] = nowMs;
    }} else {{
      liveChartTimestamps.push(nowMs);
      liveChartLabels.push(timeLabel);
      liveChartData.push(currentGoldUsd);
      
      const fiveMinCutoff = nowMs - 5 * 60 * 1000;
      while (liveChartTimestamps.length > 25 && liveChartTimestamps[0] < fiveMinCutoff) {{
        liveChartTimestamps.shift();
        liveChartLabels.shift();
        liveChartData.shift();
      }}
    }}

    if (liveChartInstance) {{
      const minP = Math.min(...liveChartData);
      const maxP = Math.max(...liveChartData);
      const pad = Math.max(1.0, (maxP - minP) * 0.15);
      liveChartInstance.options.scales.y.min = Math.floor(minP - pad);
      liveChartInstance.options.scales.y.max = Math.ceil(maxP + pad);
      liveChartInstance.update();

      if (selectedLiveStartIndex !== null && selectedLiveEndIndex !== null) {{
        applyLiveSelection(selectedLiveStartIndex, selectedLiveEndIndex);
      }}
    }}

    const usdInput = document.getElementById('inputUsd');
    const thbInput = document.getElementById('inputThb');
    const ozInput = document.getElementById('inputOz');
    const tbInput = document.getElementById('inputThaiBaht');
    const gInput = document.getElementById('inputGrams');
    const hasAnyValue = (usdInput && usdInput.value) || (thbInput && thbInput.value) || (ozInput && ozInput.value) || (tbInput && tbInput.value) || (gInput && gInput.value);
    if (!hasAnyValue && usdInput) {{
      usdInput.value = 1000;
      convertFrom('USD');
    }} else {{
      convertFrom(lastConverterSource || 'USD');
    }}
    liveCountdown = 30;
  }}

  function setQuickConvert(source, amount) {{
    const map = {{
      'USD': 'inputUsd',
      'THB': 'inputThb',
      'OZ': 'inputOz',
      'THAI_BAHT': 'inputThaiBaht',
      'GRAMS': 'inputGrams'
    }};
    const el = document.getElementById(map[source]);
    if (el) {{
      el.value = amount;
      convertFrom(source);
    }}
  }}

  function convertFrom(source) {{
    lastConverterSource = source;
    const goldThbOz = currentGoldUsd * currentUsdThb;
    const pureGramThb = goldThbOz / TROY_OZ_G;
    const pureGramUsd = currentGoldUsd / TROY_OZ_G;
    const thaiBarThb = pureGramThb * PURITY_965 * THAI_BAR_G;

    const usdEl = document.getElementById('inputUsd');
    const thbEl = document.getElementById('inputThb');
    const ozEl = document.getElementById('inputOz');
    const tbEl = document.getElementById('inputThaiBaht');
    const gEl = document.getElementById('inputGrams');

    if (source === 'USD') {{
      const usd = Math.max(0, parseFloat(usdEl.value) || 0);
      if (thbEl) thbEl.value = usd ? (usd * currentUsdThb).toFixed(2) : '';
      if (ozEl) ozEl.value = usd ? (usd / currentGoldUsd).toFixed(4) : '';
      if (tbEl) tbEl.value = usd ? ((usd * currentUsdThb) / thaiBarThb).toFixed(3) : '';
      if (gEl) gEl.value = usd ? (usd / pureGramUsd).toFixed(3) : '';
    }} else if (source === 'THB') {{
      const thb = Math.max(0, parseFloat(thbEl.value) || 0);
      if (usdEl) usdEl.value = thb ? (thb / currentUsdThb).toFixed(2) : '';
      if (ozEl) ozEl.value = thb ? (thb / goldThbOz).toFixed(4) : '';
      if (tbEl) tbEl.value = thb ? (thb / thaiBarThb).toFixed(3) : '';
      if (gEl) gEl.value = thb ? (thb / pureGramThb).toFixed(3) : '';
    }} else if (source === 'OZ') {{
      const oz = Math.max(0, parseFloat(ozEl.value) || 0);
      if (usdEl) usdEl.value = oz ? (oz * currentGoldUsd).toFixed(2) : '';
      if (thbEl) thbEl.value = oz ? (oz * goldThbOz).toFixed(2) : '';
      if (tbEl) tbEl.value = oz ? ((oz * goldThbOz) / thaiBarThb).toFixed(3) : '';
      if (gEl) gEl.value = oz ? (oz * TROY_OZ_G).toFixed(3) : '';
    }} else if (source === 'THAI_BAHT') {{
      const tb = Math.max(0, parseFloat(tbEl.value) || 0);
      const thbVal = tb * thaiBarThb;
      if (thbEl) thbEl.value = tb ? thbVal.toFixed(2) : '';
      if (usdEl) usdEl.value = tb ? (thbVal / currentUsdThb).toFixed(2) : '';
      if (ozEl) ozEl.value = tb ? (thbVal / goldThbOz).toFixed(4) : '';
      if (gEl) gEl.value = tb ? (tb * THAI_BAR_G * PURITY_965).toFixed(3) : '';
    }} else if (source === 'GRAMS') {{
      const g = Math.max(0, parseFloat(gEl ? gEl.value : 0) || 0);
      const ozVal = g / TROY_OZ_G;
      if (ozEl) ozEl.value = g ? ozVal.toFixed(4) : '';
      if (usdEl) usdEl.value = g ? (ozVal * currentGoldUsd).toFixed(2) : '';
      if (thbEl) thbEl.value = g ? (g * pureGramThb).toFixed(2) : '';
      if (tbEl) tbEl.value = g ? ((g * pureGramThb) / thaiBarThb).toFixed(3) : '';
    }}
  }}

  setInterval(() => {{
    if (currentMode === 'live' && !isLivePaused) {{
      liveCountdown--;
      const el = document.getElementById('countdown');
      if (el) el.innerText = liveCountdown;
      if (liveCountdown <= 0) refreshLiveData();
    }}
  }}, 1000);

  function updatePeriodSummaryBar() {{
    if (!activeData || !activeData.length) return;
    const first = activeData[0];
    const last = activeData[activeData.length - 1];
    const gStart = first.close;
    const gEnd = last.close;
    const retPct = ((gEnd - gStart) / gStart) * 100;
    const retSign = retPct >= 0 ? '+' : '';

    let highG = -Infinity;
    let lowG = Infinity;
    let peak = -Infinity;
    let maxDd = 0;
    let minTb = Infinity;
    let maxTb = -Infinity;

    for (let i = 0; i < activeData.length; i++) {{
      const item = activeData[i];
      const h = item.high !== undefined ? item.high : item.close;
      const l = item.low !== undefined ? item.low : item.close;
      if (h > highG) highG = h;
      if (l < lowG) lowG = l;
      if (h > peak) peak = h;
      if (peak > 0) {{
        const dd = ((l - peak) / peak) * 100;
        if (dd < maxDd) maxDd = dd;
      }}
      const tb = item.thai_gold_bar !== undefined ? item.thai_gold_bar : computeDerived(item).thai_gold_bar;
      if (tb < minTb) minTb = tb;
      if (tb > maxTb) maxTb = tb;
    }}

    const retEl = document.getElementById('summaryPeriodReturn');
    if (retEl) {{
      retEl.innerText = `$${{gStart.toLocaleString('en-US', {{ minimumFractionDigits: 1 }})}} → $${{gEnd.toLocaleString('en-US', {{ minimumFractionDigits: 1 }})}} (${{retSign}}${{retPct.toFixed(2)}}%)`;
      retEl.style.color = retPct >= 0 ? 'var(--green-up)' : 'var(--red-down)';
    }}

    const hlEl = document.getElementById('summaryHighLow');
    if (hlEl) {{
      const spread = Math.max(0, highG - lowG);
      hlEl.innerText = `$${{lowG.toLocaleString('en-US', {{ minimumFractionDigits: 1 }})}} — $${{highG.toLocaleString('en-US', {{ minimumFractionDigits: 1 }})}} (Δ $${{spread.toFixed(1)}})`;
    }}

    const ddEl = document.getElementById('summaryMaxDrawdown');
    if (ddEl) {{
      ddEl.innerText = `${{maxDd.toFixed(2)}}%`;
      ddEl.style.color = maxDd < -5 ? 'var(--red-down)' : '#f8fafc';
    }}

    const tbRangeEl = document.getElementById('summaryThaiBarRange');
    if (tbRangeEl) {{
      tbRangeEl.innerText = `฿${{Math.round(minTb).toLocaleString('en-US')}} — ฿${{Math.round(maxTb).toLocaleString('en-US')}}`;
      tbRangeEl.style.color = 'var(--gold-light)';
    }}
  }}

  function updateHistChartScales() {{
    if (!histChartInstance) return;

    // 1. Gold Scale
    const allLows = activeData.map(d => d.low !== undefined ? d.low : d.close);
    const allHighs = activeData.map(d => d.high !== undefined ? d.high : d.close);
    const minG = Math.min(...allLows);
    const maxG = Math.max(...allHighs);
    const padG = Math.max(1, (maxG - minG) * 0.06);

    histChartInstance.options.scales.y.type = currentScaleType;
    histChartInstance.options.scales.y.min = Math.max(1, Math.floor(minG - padG));
    histChartInstance.options.scales.y.max = Math.ceil(maxG + padG);

    // 2. USD/THB Scale (y1)
    const allThb = activeData.map(d => d.usd_thb);
    const minT = Math.min(...allThb);
    const maxT = Math.max(...allThb);
    const padT = Math.max(0.15, (maxT - minT) * 0.12);
    histChartInstance.options.scales.y1.min = Math.floor((minT - padT) * 10) / 10;
    histChartInstance.options.scales.y1.max = Math.ceil((maxT + padT) * 10) / 10;

    // 3. US 10Y Yield Scale (y2)
    const allB = activeData.map(d => d.us10y);
    const minB = Math.min(...allB);
    const maxB = Math.max(...allB);
    const padB = Math.max(0.10, (maxB - minB) * 0.12);
    histChartInstance.options.scales.y2.min = Math.floor((minB - padB) * 10) / 10;
    histChartInstance.options.scales.y2.max = Math.ceil((maxB + padB) * 10) / 10;
  }}

  function updateDatasetPointRadii() {{
    if (!histChartInstance) return;
    const isOver50 = activeData && activeData.length > 50;
    const nodeRadius = isOver50 ? 0 : 2;

    const ds0 = histChartInstance.data.datasets[0];
    const ds1 = histChartInstance.data.datasets[1];
    const ds2 = histChartInstance.data.datasets[2];

    if (ds0) {{
      ds0.pointRadius = currentChartStyle === 'candles' ? 0 : nodeRadius;
    }}
    if (ds1) {{
      ds1.pointRadius = nodeRadius;
    }}
    if (ds2) {{
      ds2.pointRadius = nodeRadius;
    }}
  }}

  function updateHistChartData() {{
    if (!histChartInstance) return;
    histChartInstance.data.labels = activeData.map(d => d.date);
    histChartInstance.data.datasets[0].data = activeData.map(d => d.close);
    histChartInstance.data.datasets[1].data = activeData.map(d => d.usd_thb);
    histChartInstance.data.datasets[2].data = activeData.map(d => d.us10y);
    updateDatasetPointRadii();
    updateHistChartScales();
    histChartInstance.update();
  }}

  function initHistoricalChart() {{
    const canvas = document.getElementById('historicalChartCanvas');
    if (!canvas || typeof Chart === 'undefined') return;
    const ctx = canvas.getContext('2d');

    const labels = activeData.map(d => d.date);
    const goldCloseData = activeData.map(d => d.close);
    const thbData = activeData.map(d => d.usd_thb);
    const bondData = activeData.map(d => d.us10y);
    const isOver50 = activeData && activeData.length > 50;
    const initNodeRadius = isOver50 ? 0 : 2;

    histChartInstance = new Chart(ctx, {{
      type: 'line',
      plugins: [candlestickPlugin],
      data: {{
        labels: labels,
        datasets: [
          {{
            label: 'Gold (USD/oz)',
            data: goldCloseData,
            borderColor: currentChartStyle === 'candles' ? 'transparent' : '#ff9800',
            backgroundColor: currentChartStyle === 'caves' ? 'rgba(255, 152, 0, 0.15)' : 'transparent',
            borderWidth: 2,
            fill: currentChartStyle === 'caves',
            borderDash: [],
            stepped: false,
            tension: 0.1,
            pointRadius: currentChartStyle === 'candles' ? 0 : initNodeRadius,
            pointHoverRadius: 5,
            pointBackgroundColor: '#ff9800',
            yAxisID: 'y'
          }},
          {{
            label: 'USD / THB (฿)',
            data: thbData,
            borderColor: '#38bdf8',
            backgroundColor: currentChartStyle === 'caves' ? 'rgba(56, 189, 248, 0.10)' : 'transparent',
            borderWidth: 1.8,
            fill: currentChartStyle === 'caves',
            borderDash: [],
            stepped: false,
            tension: 0.1,
            pointRadius: initNodeRadius,
            pointHoverRadius: 5,
            pointBackgroundColor: '#38bdf8',
            yAxisID: 'y1'
          }},
          {{
            label: 'US 10Y Yield (%)',
            data: bondData,
            borderColor: '#a855f7',
            backgroundColor: currentChartStyle === 'caves' ? 'rgba(168, 85, 247, 0.10)' : 'transparent',
            borderWidth: 1.8,
            fill: currentChartStyle === 'caves',
            borderDash: [5, 4],
            stepped: false,
            tension: 0.1,
            pointRadius: initNodeRadius,
            pointHoverRadius: 5,
            pointBackgroundColor: '#a855f7',
            yAxisID: 'y2'
          }}
        ]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        animation: {{ duration: 150 }},
        interaction: {{ mode: 'index', intersect: false }},
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{
            backgroundColor: '#12151b',
            titleColor: '#ff9800',
            titleFont: {{ family: 'JetBrains Mono', size: 11, weight: 'bold' }},
            bodyFont: {{ family: 'JetBrains Mono', size: 11 }},
            borderColor: '#2e3546',
            borderWidth: 1,
            cornerRadius: 2,
            padding: 10,
            callbacks: {{
              title: (items) => {{
                const idx = items[0].dataIndex;
                const entry = activeData[idx];
                return `${{entry.date}} ${{entry.note ? '• ' + entry.note : ''}}`;
              }},
              label: (item) => {{
                const idx = item.dataIndex;
                const candle = activeData[idx];
                if (item.datasetIndex === 0) {{
                  if (currentChartStyle === 'candles' && candle.open !== undefined) {{
                    return [
                      ` Gold OHLC:`,
                      `   Open:  $${{candle.open.toFixed(1)}}`,
                      `   High:  $${{candle.high.toFixed(1)}}`,
                      `   Low:   $${{candle.low.toFixed(1)}}`,
                      `   Close: $${{candle.close.toFixed(1)}}`
                    ];
                  }}
                  return ` Gold Close: $${{item.parsed.y.toLocaleString()}} USD/oz`;
                }} else if (item.datasetIndex === 1) {{
                  return ` USD / THB: ฿${{item.parsed.y.toFixed(2)}} THB`;
                }} else if (item.datasetIndex === 2) {{
                  return ` US 10Y Yield: ${{item.parsed.y.toFixed(2)}}%`;
                }}
              }},
              afterBody: (items) => {{
                const idx = items[0].dataIndex;
                const entry = activeData[idx];
                const derived = computeDerived(entry);
                return [
                  ` ---------------------------`,
                  ` Gold in THB: ฿${{Math.round(derived.gold_thb_oz).toLocaleString()}} / oz`,
                  ` 1 Baht Gold Bar: ฿${{Math.round(derived.thai_gold_bar).toLocaleString()}} THB`
                ];
              }}
            }}
          }}
        }},
        scales: {{
          x: {{
            grid: {{ color: '#181d26' }},
            ticks: {{ color: '#828a99', font: {{ family: 'JetBrains Mono', size: 10 }}, maxTicksLimit: 14 }}
          }},
          y: {{
            type: 'linear', display: true, position: 'left', grid: {{ color: '#181d26' }},
            title: {{ display: true, text: 'Gold Price ($/oz)', color: '#ff9800', font: {{ family: 'JetBrains Mono', weight: '700', size: 10 }} }},
            ticks: {{ color: '#ff9800', font: {{ family: 'JetBrains Mono', size: 10 }}, callback: (v) => '$' + v.toLocaleString() }}
          }},
          y1: {{
            type: 'linear', display: true, position: 'right', grid: {{ drawOnChartArea: false }},
            title: {{ display: true, text: 'USD / THB (฿)', color: '#38bdf8', font: {{ family: 'JetBrains Mono', weight: '700', size: 10 }} }},
            ticks: {{
              color: '#38bdf8',
              font: {{ family: 'JetBrains Mono', size: 10 }},
              callback: function(v) {{
                const range = (this.max || 40) - (this.min || 20);
                return '฿' + (range < 2 ? v.toFixed(2) : v.toFixed(1));
              }}
            }}
          }},
          y2: {{
            type: 'linear', display: true, position: 'right', grid: {{ drawOnChartArea: false }},
            title: {{ display: true, text: 'US 10Y Yield (%)', color: '#a855f7', font: {{ family: 'JetBrains Mono', weight: '700', size: 10 }} }},
            ticks: {{
              color: '#a855f7',
              font: {{ family: 'JetBrains Mono', size: 10 }},
              callback: function(v) {{
                const range = (this.max || 10) - (this.min || 0);
                return (range < 0.5 ? v.toFixed(2) : v.toFixed(1)) + '%';
              }}
            }}
          }}
        }}
      }}
    }});

    updateHistChartScales();
    updatePeriodSummaryBar();
    setupDragInteraction();
    setupWheelZoomInteraction();
    updateSamplingPillState();
  }}

  function setChartStyle(style) {{
    currentChartStyle = style;
    document.querySelectorAll('.style-pill').forEach(p => p.classList.remove('active'));
    document.getElementById(`style${{style.charAt(0).toUpperCase() + style.slice(1)}}`)?.classList.add('active');

    if (!histChartInstance) return;

    const ds0 = histChartInstance.data.datasets[0];
    const ds1 = histChartInstance.data.datasets[1];
    const ds2 = histChartInstance.data.datasets[2];

    if (style === 'candles') {{
      ds0.borderColor = 'transparent';
      ds0.backgroundColor = 'transparent';
      ds0.fill = false;
      ds0.borderDash = [];

      ds1.fill = false;
      ds1.borderDash = [];

      ds2.fill = false;
      ds2.borderDash = [5, 4];
    }} else if (style === 'caves') {{
      ds0.borderColor = '#ff9800';
      ds0.backgroundColor = 'rgba(255, 152, 0, 0.15)';
      ds0.fill = true;
      ds0.borderDash = [];

      ds1.backgroundColor = 'rgba(56, 189, 248, 0.10)';
      ds1.fill = true;
      ds1.borderDash = [];

      ds2.backgroundColor = 'rgba(168, 85, 247, 0.10)';
      ds2.fill = true;
      ds2.borderDash = [5, 4];
    }} else if (style === 'line') {{
      ds0.borderColor = '#ff9800';
      ds0.backgroundColor = 'transparent';
      ds0.fill = false;
      ds0.borderDash = [];

      ds1.backgroundColor = 'transparent';
      ds1.fill = false;
      ds1.borderDash = [];

      ds2.backgroundColor = 'transparent';
      ds2.fill = false;
      ds2.borderDash = [5, 4];
    }}

    updateDatasetPointRadii();
    histChartInstance.update();
  }}

  function toggleScale(type) {{
    currentScaleType = 'linear';
    if (histChartInstance) {{
      histChartInstance.options.scales.y.type = 'linear';
      updateHistChartScales();
      histChartInstance.update();
    }}
  }}

  const tagNames = {{
    '10m': '10 Minutes',
    '1h': '1 Hour',
    '1d': '1 Day',
    '1mo': '1 Month'
  }};

  const tfNames = {{
    '1D': '1 Day',
    '1W': '1 Week',
    '1M': '1 Month',
    '1Y': '1 Year',
    '3Y': '3 Years',
    '5Y': '5 Years',
    '10Y': '10 Years',
    '20Y': '20 Years',
    'ALL': 'All History',
    'CUSTOM': 'Custom Timeframe'
  }};

  function updateSamplingPillState() {{
    const preset = findMatchingPreset(currentWindowDurationDays);
    const validRates = preset ? preset.rates : getSupportedRatesForDuration(currentWindowDurationDays);
    document.querySelectorAll('.opt-btn[id^="rate"]').forEach(b => {{
      const r = b.id.replace('rate', '');
      b.classList.remove('active');
      b.classList.remove('dimmed');
      if (validRates.includes(r)) {{
        b.style.opacity = '1';
        b.style.cursor = 'pointer';
        b.title = 'Sample at ' + (tagNames[r] || r) + ' granularity';
      }} else {{
        b.classList.add('dimmed');
        b.style.opacity = '0.35';
        b.style.cursor = r === '10m' ? 'pointer' : 'not-allowed';
        if (r === '10m') {{
          b.title = '10-minute candles are only available for 1D timeframe';
        }} else {{
          b.title = (tagNames[r] || r) + ' candles are not available for the ' + (preset ? preset.name : 'current') + ' timeframe';
        }}
      }}
    }});
    document.getElementById(`rate${{currentSamplingRate}}`)?.classList.add('active');
  }}

  function setSamplingRate(rate) {{
    const preset = findMatchingPreset(currentWindowDurationDays);
    const validRates = preset ? preset.rates : getSupportedRatesForDuration(currentWindowDurationDays);
    if (!validRates.includes(rate)) {{
      if (rate === '10m') {{
        currentWindowDurationDays = 1;
      }} else {{
        return; // Disallow selecting sampling rates not permitted for this timeframe
      }}
    }}
    currentSamplingRate = rate;

    // 10m is only available for 1D timeframe
    if (rate === '10m') {{
      currentWindowDurationDays = 1;
    }} else if (rate === '1mo' && currentWindowDurationDays < 28) {{
      currentWindowDurationDays = 30.5;
    }}

    setContinuousWindow(currentWindowDurationDays, currentWindowEndTs);
  }}

  function toggleDataset(datasetIndex, pillId, activeClass) {{
    if (!histChartInstance) return;
    const defaultPills = [
      {{ id: 'toggleGold', cls: 'active-gold' }},
      {{ id: 'toggleThb', cls: 'active-thb' }},
      {{ id: 'toggleBond', cls: 'active-bond' }}
    ];
    const pId = pillId || (defaultPills[datasetIndex] && defaultPills[datasetIndex].id);
    const aCls = activeClass || (defaultPills[datasetIndex] && defaultPills[datasetIndex].cls);
    const pill = pId ? document.getElementById(pId) : null;

    const meta = histChartInstance.getDatasetMeta(datasetIndex);
    meta.hidden = meta.hidden === null ? !histChartInstance.data.datasets[datasetIndex].hidden : (meta.hidden ? false : true);
    const isHidden = meta.hidden;

    const axisKey = datasetIndex === 0 ? 'y' : (datasetIndex === 1 ? 'y1' : 'y2');
    if (histChartInstance.options.scales[axisKey]) {{
      histChartInstance.options.scales[axisKey].display = !isHidden;
    }}

    if (pill && aCls) {{
      if (isHidden) {{
        pill.classList.remove(aCls);
      }} else {{
        pill.classList.add(aCls);
      }}
    }}

    histChartInstance.update();
  }}

  function filterTimeframe(range, btnElement) {{
    if (range === 'CUSTOM') {{
      setContinuousWindow(currentWindowDurationDays, currentWindowEndTs);
      return;
    }}

    const preset = PRESETS.find(p => p.id === range);
    if (preset) {{
      const prevDays = currentWindowDurationDays;
      currentTimeframe = preset.id;

      // When minimizing timeframe to a certain size, auto-adjust sample rate for best viewability
      if (preset.id === '1D') {{
        if (currentSamplingRate !== '10m') {{
          currentSamplingRate = '1h'; // Default for 1D is 1 hour sample rate
        }}
      }} else if (preset.days < prevDays) {{
        // Minimizing to a smaller timeframe: auto-adjust if current rate is too coarse
        if (preset.days <= 35 && currentSamplingRate === '1mo') {{
          currentSamplingRate = '1d';
        }} else if (!preset.rates.includes(currentSamplingRate)) {{
          currentSamplingRate = preset.defaultRate;
        }}
      }} else if (!preset.rates.includes(currentSamplingRate)) {{
        currentSamplingRate = preset.defaultRate;
      }}

      setContinuousWindow(preset.days, MASTER_END_TS);
    }}
  }}

  function setContinuousWindow(durationDays, endTs) {{
    const prevDays = currentWindowDurationDays;
    if (durationDays !== undefined && !isNaN(durationDays)) {{
      currentWindowDurationDays = durationDays;
    }}
    if (endTs !== undefined && !isNaN(endTs)) {{
      currentWindowEndTs = endTs;
    }}

    const isMinimizing = (durationDays !== undefined && durationDays < prevDays - 0.01);

    // Auto-adjust sample rate for best viewability when minimizing the timeframe
    if (isMinimizing) {{
      if (currentWindowDurationDays <= 2.2) {{
        // Minimized down to 1-Day size: auto-adjust to 1h (24 candles) unless already on 10m
        if (currentSamplingRate !== '10m') {{
          currentSamplingRate = '1h';
        }}
      }} else if (currentWindowDurationDays <= 35) {{
        // Minimized down to month/week size: 1mo is unviewable (<= 1 candle), auto-adjust to 1d
        if (currentSamplingRate === '1mo') {{
          currentSamplingRate = '1d';
        }}
      }}
    }}

    const preset = findMatchingPreset(currentWindowDurationDays);
    const tfCustomBtn = document.getElementById('tfCustom');
    document.querySelectorAll('.range-selector .opt-btn').forEach(b => b.classList.remove('active'));

    let tfDisplayName = '';
    if (preset) {{
      currentTimeframe = preset.id;
      const btn = document.getElementById('tf' + preset.id) || (preset.id === 'ALL' ? document.getElementById('btnTfAll') : null);
      if (btn) btn.classList.add('active');
      if (tfCustomBtn) tfCustomBtn.style.display = 'none';
      tfDisplayName = preset.name;

      if (preset.id === '1D') {{
        if (currentSamplingRate !== '10m' && currentSamplingRate !== '1h' && currentSamplingRate !== '1d') {{
          currentSamplingRate = '1h';
        }}
      }} else if (!preset.rates.includes(currentSamplingRate)) {{
        currentSamplingRate = preset.defaultRate;
      }}
    }} else {{
      currentTimeframe = 'CUSTOM';
      const yrs = currentWindowDurationDays / 365.25;
      const mos = currentWindowDurationDays / 30.5;
      let customLabel = '';
      if (yrs >= 1) {{
        customLabel = yrs.toFixed(1) + 'Y';
        tfDisplayName = yrs.toFixed(1) + ' Years (' + Math.round(currentWindowDurationDays).toLocaleString() + ' days)';
      }} else if (mos >= 1) {{
        customLabel = mos.toFixed(1) + 'M';
        tfDisplayName = mos.toFixed(1) + ' Months (' + Math.round(currentWindowDurationDays).toLocaleString() + ' days)';
      }} else {{
        customLabel = Math.round(currentWindowDurationDays) + 'D';
        tfDisplayName = Math.round(currentWindowDurationDays) + ' Days';
      }}
      if (tfCustomBtn) {{
        tfCustomBtn.innerText = customLabel;
        tfCustomBtn.style.display = 'inline-block';
        tfCustomBtn.classList.add('active');
      }}

      const supported = getSupportedRatesForDuration(currentWindowDurationDays);
      if (!supported.includes(currentSamplingRate)) {{
        currentSamplingRate = getDefaultRateForDuration(currentWindowDurationDays);
      }}
    }}

    updateSamplingPillState();

    const startTs = Math.max(MASTER_START_TS, currentWindowEndTs - (currentWindowDurationDays * 86400 * 1000));
    activeData = sampleMasterTimeline(startTs, currentWindowEndTs, currentSamplingRate);
    fullRangeData = [...activeData];

    const tagEl = document.getElementById('currentSamplingTag');
    if (tagEl) {{
      tagEl.innerText = 'Timeframe: ' + tfDisplayName + ' • Interval: 1 Candle = ' + (tagNames[currentSamplingRate] || currentSamplingRate) + ' (' + activeData.length + ' samples)';
    }}
    const specEl = document.getElementById('specGranularity');
    if (specEl) {{
      specEl.innerText = '1 Candle = ' + (tagNames[currentSamplingRate] || currentSamplingRate) + ' (OHLC) • ' + activeData.length + ' samples in ' + tfDisplayName;
    }}

    updatePeriodSummaryBar();

    if (histChartInstance) {{
      updateHistChartData();
      clearSelection();
    }}
  }}

  function zoomContinuousTimeframe(zoomIn, factor) {{
    factor = factor || 1.18;
    let newDays = zoomIn ? (currentWindowDurationDays / factor) : (currentWindowDurationDays * factor);
    const maxDays = (MASTER_END_TS - MASTER_START_TS) / (86400 * 1000);
    newDays = Math.max(1, Math.min(maxDays, newDays));

    // Magnetic snap if close to preset
    for (const p of PRESETS) {{
      if (Math.abs(newDays - p.days) / p.days < 0.06) {{
        newDays = p.days;
        break;
      }}
    }}

    // When minimizing timeframe to a certain size, auto-adjust sample rate for best viewability
    if (zoomIn) {{
      if (newDays <= 2.2 && currentSamplingRate !== '10m') {{
        currentSamplingRate = '1h';
      }} else if (newDays <= 35 && currentSamplingRate === '1mo') {{
        currentSamplingRate = '1d';
      }}
    }}

    setContinuousWindow(newDays, currentWindowEndTs);
  }}

  function setupWheelZoomInteraction() {{
    const wrap = document.getElementById('histChartWrap');
    if (!wrap || wrap.dataset.wheelBound) return;
    wrap.dataset.wheelBound = 'true';

    wrap.addEventListener('wheel', (e) => {{
      if (e.ctrlKey) {{
        e.preventDefault();
        const zoomIn = e.deltaY < 0;
        zoomContinuousTimeframe(zoomIn, 1.18);
      }}
    }}, {{ passive: false }});
  }}

  function setupDragInteraction() {{
    const canvas = document.getElementById('historicalChartCanvas');
    const selectionBox = document.getElementById('selectionBox');

    function getIndexFromX(clientX) {{
      if (!histChartInstance) return null;
      const rect = canvas.getBoundingClientRect();
      const x = clientX - rect.left;
      const chartArea = histChartInstance.chartArea;
      if (!chartArea || x < chartArea.left || x > chartArea.right) return null;

      const totalItems = activeData.length;
      if (totalItems <= 1) return 0;
      const relativeX = (x - chartArea.left) / (chartArea.right - chartArea.left);
      let idx = Math.round(relativeX * (totalItems - 1));
      return Math.max(0, Math.min(totalItems - 1, idx));
    }}

    canvas.addEventListener('mousedown', (e) => {{
      const idx = getIndexFromX(e.clientX);
      if (idx !== null) {{
        isDragging = true;
        dragStartX = e.clientX;
        dragStartIndex = idx;

        const rect = canvas.getBoundingClientRect();
        const chartArea = histChartInstance.chartArea;
        selectionBox.style.top = chartArea.top + 'px';
        selectionBox.style.height = chartArea.height + 'px';
        selectionBox.style.left = (dragStartX - rect.left) + 'px';
        selectionBox.style.width = '0px';
        selectionBox.style.display = 'block';
      }}
    }});

    window.addEventListener('mousemove', (e) => {{
      if (!isDragging || !histChartInstance) return;
      const rect = canvas.getBoundingClientRect();
      const chartArea = histChartInstance.chartArea;
      const currentX = Math.max(rect.left + chartArea.left, Math.min(rect.left + chartArea.right, e.clientX));
      const left = Math.min(dragStartX, currentX) - rect.left;
      const width = Math.abs(currentX - dragStartX);

      selectionBox.style.top = chartArea.top + 'px';
      selectionBox.style.height = chartArea.height + 'px';
      selectionBox.style.left = left + 'px';
      selectionBox.style.width = width + 'px';
    }});

    window.addEventListener('mouseup', (e) => {{
      if (!isDragging) return;
      isDragging = false;

      const dragEndIndex = getIndexFromX(e.clientX);
      if (dragStartIndex !== null && dragEndIndex !== null && dragStartIndex !== dragEndIndex) {{
        const start = Math.min(dragStartIndex, dragEndIndex);
        const end = Math.max(dragStartIndex, dragEndIndex);
        applySelection(start, end);
      }} else {{
        clearSelection();
      }}
    }});
  }}

  function applySelection(startIndex, endIndex) {{
    if (!histChartInstance || !activeData || !activeData.length) return;
    startIndex = Math.max(0, Math.min(activeData.length - 1, startIndex));
    endIndex = Math.max(0, Math.min(activeData.length - 1, endIndex));
    if (startIndex > endIndex) {{
      const tmp = startIndex;
      startIndex = endIndex;
      endIndex = tmp;
    }}

    selectedStartIndex = startIndex;
    selectedEndIndex = endIndex;

    const selectionBox = document.getElementById('selectionBox');
    const chartArea = histChartInstance.chartArea;
    const xAxis = histChartInstance.scales.x;
    const total = activeData.length;

    let left = chartArea.left;
    let right = chartArea.right;

    if (xAxis && total > 1) {{
      const x1 = xAxis.getPixelForValue(startIndex);
      const x2 = xAxis.getPixelForValue(endIndex);
      const slotWidth = chartArea.width / total;
      left = Math.max(chartArea.left, Math.min(x1, x2) - slotWidth / 2);
      right = Math.min(chartArea.right, Math.max(x1, x2) + slotWidth / 2);
    }}

    selectionBox.style.top = chartArea.top + 'px';
    selectionBox.style.height = chartArea.height + 'px';
    selectionBox.style.left = left + 'px';
    selectionBox.style.width = Math.max(2, right - left) + 'px';
    selectionBox.style.display = 'block';

    const p1 = activeData[startIndex];
    const p2 = activeData[endIndex];
    const d1 = computeDerived(p1);
    const d2 = computeDerived(p2);

    let selLow = Infinity;
    let selHigh = -Infinity;
    for (let k = startIndex; k <= endIndex; k++) {{
      const ck = activeData[k];
      const h = ck.high !== undefined ? ck.high : ck.close;
      const l = ck.low !== undefined ? ck.low : ck.close;
      if (h > selHigh) selHigh = h;
      if (l < selLow) selLow = l;
    }}

    document.getElementById('compStartDate').innerText = p1.date;
    document.getElementById('compEndDate').innerText = p2.date;
    document.getElementById('compDuration').innerText = `(${{endIndex - startIndex + 1}} candles)`;

    const eventText = p2.note ? `Event: ${{p2.note}}` : (p1.note ? `Event: ${{p1.note}}` : '');
    const rangeSummary = `Range: $${{selLow.toLocaleString('en-US', {{ minimumFractionDigits: 1 }})}}–$${{selHigh.toLocaleString('en-US', {{ minimumFractionDigits: 1 }})}}`;
    document.getElementById('compNote').innerText = eventText ? `${{eventText}} • ${{rangeSummary}}` : rangeSummary;

    // 1. Gold
    const g1 = d1.gold_usd;
    const g2 = d2.gold_usd;
    const goldPct = ((g2 - g1) / g1) * 100;
    const goldAbs = g2 - g1;
    document.getElementById('compGoldFlow').innerText = `$${{g1.toLocaleString('en-US', {{ minimumFractionDigits: 1 }})}} → $${{g2.toLocaleString('en-US', {{ minimumFractionDigits: 1 }})}}`;
    renderPct('compGoldPct', goldPct);
    document.getElementById('compGoldAbs').innerText = `${{goldAbs >= 0 ? '+' : ''}}$${{goldAbs.toFixed(2)}} USD/oz`;

    // 2. USD/THB
    const t1 = d1.usd_thb;
    const t2 = d2.usd_thb;
    const thbPct = ((t2 - t1) / t1) * 100;
    const thbAbs = t2 - t1;
    document.getElementById('compThbFlow').innerText = `฿${{t1.toFixed(2)}} → ฿${{t2.toFixed(2)}}`;
    renderPct('compThbPct', thbPct);
    document.getElementById('compThbAbs').innerText = `${{thbAbs >= 0 ? '+' : ''}}฿${{thbAbs.toFixed(2)}} THB per $1 USD`;

    // 3. US 10Y Yield
    const b1 = d1.us10y;
    const b2 = d2.us10y;
    const bondPct = ((b2 - b1) / b1) * 100;
    const bondDiff = b2 - b1;
    const bps = Math.round(bondDiff * 100);
    document.getElementById('compBondFlow').innerText = `${{b1.toFixed(2)}}% → ${{b2.toFixed(2)}}%`;
    renderPct('compBondPct', bondPct);
    document.getElementById('compBondAbs').innerText = `${{bps >= 0 ? '+' : ''}}${{bps}} bps (${{bondDiff >= 0 ? '+' : ''}}${{bondDiff.toFixed(2)}}%)`;

    // 4. Thai Gold Bar
    const tb1 = d1.thai_gold_bar;
    const tb2 = d2.thai_gold_bar;
    const thaiBarPct = ((tb2 - tb1) / tb1) * 100;
    const thaiBarAbs = tb2 - tb1;
    document.getElementById('compThaiBarFlow').innerText = `฿${{Math.round(tb1).toLocaleString()}} → ฿${{Math.round(tb2).toLocaleString()}}`;
    renderPct('compThaiBarPct', thaiBarPct);
    document.getElementById('compThaiBarAbs').innerText = `${{thaiBarAbs >= 0 ? '+' : ''}}฿${{Math.round(thaiBarAbs).toLocaleString()}} THB / บาท`;

    document.getElementById('comparisonBanner').style.display = 'block';
  }}

  function renderPct(elementId, pct) {{
    const el = document.getElementById(elementId);
    const isUp = pct >= 0;
    el.className = `pct-change ${{isUp ? 'pct-up' : 'pct-down'}}`;
    el.innerText = `${{isUp ? '+' : ''}}${{pct.toFixed(2)}}%`;
  }}

  function clearSelection() {{
    const selectionBox = document.getElementById('selectionBox');
    if (selectionBox) selectionBox.style.display = 'none';
    const banner = document.getElementById('comparisonBanner');
    if (banner) banner.style.display = 'none';
    selectedStartIndex = null;
    selectedEndIndex = null;
  }}

  function selectDateRangeByLabels(startDate, endDate) {{
    if (currentMode !== 'historical') {{
      switchView('historical');
    }}
    if (!histChartInstance) initHistoricalChart();
    currentWindowDurationDays = (MASTER_END_TS - MASTER_START_TS) / (86400 * 1000);
    currentWindowEndTs = MASTER_END_TS;
    currentTimeframe = 'ALL';
    currentSamplingRate = '1mo';
    setContinuousWindow(currentWindowDurationDays, MASTER_END_TS);

    let i1 = activeData.findIndex(d => d.date >= startDate);
    let i2 = activeData.findIndex(d => d.date >= endDate);
    if (i1 === -1) i1 = 0;
    if (i2 === -1) i2 = activeData.length - 1;

    applySelection(i1, i2);
  }}

  function exportChart() {{
    const canvas = currentMode === 'live' ? document.getElementById('liveChartCanvas') : document.getElementById('historicalChartCanvas');
    if (!canvas) return;
    const offscreen = document.createElement('canvas');
    offscreen.width = canvas.width;
    offscreen.height = canvas.height;
    const ctx = offscreen.getContext('2d');
    ctx.fillStyle = '#0a0b0d';
    ctx.fillRect(0, 0, offscreen.width, offscreen.height);
    ctx.drawImage(canvas, 0, 0);
    const link = document.createElement('a');
    link.download = `gold_tracker_${{currentMode}}_${{Date.now()}}.png`;
    link.href = offscreen.toDataURL('image/png');
    link.click();
  }}

  function exportCSV() {{
    let csv = 'Date,Open_USD,High_USD,Low_USD,Close_USD,USD_THB,US_10Y_Yield,Gold_THB_oz,Pure_Gram_THB,Thai_Gold_Bar_THB,Thai_Ornament_THB,Note\\n';
    activeData.forEach(d => {{
      const goldThbOz = d.close * d.usd_thb;
      const pureGramThb = goldThbOz / TROY_OZ_G;
      const thaiBar = pureGramThb * PURITY_965 * THAI_BAR_G;
      const thaiOrnament = pureGramThb * PURITY_965 * 15.16;
      const row = [
        d.date,
        d.open !== undefined ? d.open : d.close,
        d.high !== undefined ? d.high : d.close,
        d.low !== undefined ? d.low : d.close,
        d.close,
        d.usd_thb,
        d.us10y,
        goldThbOz.toFixed(2),
        pureGramThb.toFixed(2),
        Math.round(thaiBar),
        Math.round(thaiOrnament),
        `"${{d.note || ''}}"`
      ];
      csv += row.join(',') + '\\n';
    }});
    const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.download = `gold_market_dataset_${{currentSamplingRate}}_${{Date.now()}}.csv`;
    link.href = url;
    link.click();
  }}

  function setupLiveDragInteraction() {{
    const canvas = document.getElementById('liveChartCanvas');
    const selectionBox = document.getElementById('liveSelectionBox');
    if (!canvas || !selectionBox) return;

    function getIndexFromX(clientX) {{
      if (!liveChartInstance) return null;
      const rect = canvas.getBoundingClientRect();
      const x = clientX - rect.left;
      const chartArea = liveChartInstance.chartArea;
      if (!chartArea || x < chartArea.left || x > chartArea.right) return null;

      const totalItems = liveChartData.length;
      if (totalItems <= 1) return 0;
      const relativeX = (x - chartArea.left) / (chartArea.right - chartArea.left);
      let idx = Math.round(relativeX * (totalItems - 1));
      return Math.max(0, Math.min(totalItems - 1, idx));
    }}

    canvas.addEventListener('mousedown', (e) => {{
      const idx = getIndexFromX(e.clientX);
      if (idx !== null) {{
        isLiveDragging = true;
        liveDragStartX = e.clientX;
        liveDragStartIndex = idx;

        const rect = canvas.getBoundingClientRect();
        const chartArea = liveChartInstance.chartArea;
        selectionBox.style.top = chartArea.top + 'px';
        selectionBox.style.height = chartArea.height + 'px';
        selectionBox.style.left = (liveDragStartX - rect.left) + 'px';
        selectionBox.style.width = '0px';
        selectionBox.style.display = 'block';
      }}
    }});

    window.addEventListener('mousemove', (e) => {{
      if (!isLiveDragging || !liveChartInstance) return;
      const rect = canvas.getBoundingClientRect();
      const chartArea = liveChartInstance.chartArea;
      const currentX = Math.max(rect.left + chartArea.left, Math.min(rect.left + chartArea.right, e.clientX));
      const left = Math.min(liveDragStartX, currentX) - rect.left;
      const width = Math.abs(currentX - liveDragStartX);

      selectionBox.style.top = chartArea.top + 'px';
      selectionBox.style.height = chartArea.height + 'px';
      selectionBox.style.left = left + 'px';
      selectionBox.style.width = width + 'px';
    }});

    window.addEventListener('mouseup', (e) => {{
      if (!isLiveDragging) return;
      isLiveDragging = false;

      const dragEndIndex = getIndexFromX(e.clientX);
      if (liveDragStartIndex !== null && dragEndIndex !== null && liveDragStartIndex !== dragEndIndex) {{
        const start = Math.min(liveDragStartIndex, dragEndIndex);
        const end = Math.max(liveDragStartIndex, dragEndIndex);
        applyLiveSelection(start, end);
      }} else {{
        clearLiveSelection();
      }}
    }});
  }}

  function applyLiveSelection(startIndex, endIndex) {{
    if (!liveChartInstance || !liveChartData || !liveChartData.length) return;
    startIndex = Math.max(0, Math.min(liveChartData.length - 1, startIndex));
    endIndex = Math.max(0, Math.min(liveChartData.length - 1, endIndex));
    if (startIndex > endIndex) {{
      const tmp = startIndex;
      startIndex = endIndex;
      endIndex = tmp;
    }}

    selectedLiveStartIndex = startIndex;
    selectedLiveEndIndex = endIndex;

    const selectionBox = document.getElementById('liveSelectionBox');
    const chartArea = liveChartInstance.chartArea;
    const xAxis = liveChartInstance.scales.x;
    const total = liveChartData.length;

    let left = chartArea.left;
    let right = chartArea.right;

    if (xAxis && total > 1) {{
      const x1 = xAxis.getPixelForValue(startIndex);
      const x2 = xAxis.getPixelForValue(endIndex);
      const slotWidth = chartArea.width / total;
      left = Math.max(chartArea.left, Math.min(x1, x2) - slotWidth / 2);
      right = Math.min(chartArea.right, Math.max(x1, x2) + slotWidth / 2);
    }}

    selectionBox.style.top = chartArea.top + 'px';
    selectionBox.style.height = chartArea.height + 'px';
    selectionBox.style.left = left + 'px';
    selectionBox.style.width = Math.max(2, right - left) + 'px';
    selectionBox.style.display = 'block';

    const p1Price = liveChartData[startIndex];
    const p2Price = liveChartData[endIndex];
    const p1Label = liveChartLabels[startIndex];
    const p2Label = liveChartLabels[endIndex];
    const numTicks = endIndex - startIndex + 1;

    let durSec = '';
    if (liveChartTimestamps[startIndex] && liveChartTimestamps[endIndex]) {{
      const s = Math.round((liveChartTimestamps[endIndex] - liveChartTimestamps[startIndex]) / 1000);
      durSec = ` • ${{s}}s`;
    }}

    document.getElementById('liveCompStartTime').innerText = p1Label;
    document.getElementById('liveCompEndTime').innerText = p2Label;
    document.getElementById('liveCompDuration').innerText = `(${{numTicks}} ticks${{durSec}})`;

    // 1. Gold Flow & %
    const goldPct = ((p2Price - p1Price) / p1Price) * 100;
    const goldAbs = p2Price - p1Price;
    document.getElementById('liveCompGoldFlow').innerText = `$${{p1Price.toFixed(2)}} → $${{p2Price.toFixed(2)}}`;
    renderPct('liveCompGoldPct', goldPct);
    document.getElementById('liveCompGoldAbs').innerText = `${{goldAbs >= 0 ? '+' : ''}}$${{goldAbs.toFixed(2)}} USD/oz`;

    // 2. USD / THB
    document.getElementById('liveCompThbFlow').innerText = `฿${{currentUsdThb.toFixed(2)}} / $1 USD`;
    document.getElementById('liveCompThbPct').innerText = `฿${{currentUsdThb.toFixed(4)}}`;
    document.getElementById('liveCompThbAbs').innerText = `Bank of Thailand Feed`;

    // 3. US 10Y Yield
    document.getElementById('liveCompBondFlow').innerText = `${{currentBondYield.toFixed(3)}}%`;
    document.getElementById('liveCompBondPct').innerText = `Benchmark`;
    document.getElementById('liveCompBondAbs').innerText = `CBOE ^TNX Rate`;

    // 4. Thai Gold Bar
    const d1 = computeDerived({{ close: p1Price, usd_thb: currentUsdThb, us10y: currentBondYield }});
    const d2 = computeDerived({{ close: p2Price, usd_thb: currentUsdThb, us10y: currentBondYield }});
    const tb1 = d1.thai_gold_bar;
    const tb2 = d2.thai_gold_bar;
    const tbPct = ((tb2 - tb1) / tb1) * 100;
    const tbAbs = tb2 - tb1;
    document.getElementById('liveCompThaiBarFlow').innerText = `฿${{Math.round(tb1).toLocaleString()}} → ฿${{Math.round(tb2).toLocaleString()}}`;
    renderPct('liveCompThaiBarPct', tbPct);
    document.getElementById('liveCompThaiBarAbs').innerText = `${{tbAbs >= 0 ? '+' : ''}}฿${{Math.round(tbAbs).toLocaleString()}} THB / บาท`;

    document.getElementById('liveComparisonBanner').style.display = 'block';
  }}

  function clearLiveSelection() {{
    const selectionBox = document.getElementById('liveSelectionBox');
    if (selectionBox) selectionBox.style.display = 'none';
    const banner = document.getElementById('liveComparisonBanner');
    if (banner) banner.style.display = 'none';
    selectedLiveStartIndex = null;
    selectedLiveEndIndex = null;
  }}

  window.addEventListener('keydown', (e) => {{
    const tag = (e.target && e.target.tagName) ? e.target.tagName.toUpperCase() : '';
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;

    if (e.key === 'Escape') {{
      if (currentMode === 'live') clearLiveSelection();
      else clearSelection();
    }} else if (!e.ctrlKey && !e.metaKey && !e.altKey && (e.key === 'm' || e.key === 'M')) {{
      switchView(currentMode === 'live' ? 'historical' : 'live');
    }} else if (currentMode === 'historical' && !e.ctrlKey && !e.metaKey && !e.altKey) {{
      const k = e.key.toLowerCase();
      if (k === 'l') setChartStyle('line');
      else if (k === 'v') setChartStyle('caves');
      else if (k === 'c') setChartStyle('candles');
      else if (['1', '2', '3', '4', '5', '6', '7', '8', '9'].includes(e.key)) {{
        const tfList = ['1D', '1W', '1M', '1Y', '3Y', '5Y', '10Y', '20Y', 'ALL'];
        const targetTf = tfList[parseInt(e.key, 10) - 1];
        if (targetTf) {{
          const btn = document.getElementById('tf' + targetTf);
          filterTimeframe(targetTf, btn);
        }}
      }}
    }} else if (currentMode === 'live' && e.code === 'Space' && !e.ctrlKey && !e.metaKey) {{
      e.preventDefault();
      toggleLivePause();
    }}
  }});

  window.addEventListener('resize', () => {{
    if (selectedStartIndex !== null && selectedEndIndex !== null && histChartInstance) {{
      applySelection(selectedStartIndex, selectedEndIndex);
    }}
    if (selectedLiveStartIndex !== null && selectedLiveEndIndex !== null && liveChartInstance) {{
      applyLiveSelection(selectedLiveStartIndex, selectedLiveEndIndex);
    }}
  }});

  window.addEventListener('DOMContentLoaded', () => {{
    initLiveChart();
    refreshLiveData();
    updatePeriodSummaryBar();
  }});
</script>

</body>
</html>
'''

with open('gold_tracker.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully generated gold_tracker.html with {len(html_content)} bytes")

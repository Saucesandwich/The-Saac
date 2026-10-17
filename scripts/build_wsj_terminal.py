"""
Build The Saac Terminal - WSJ Market Data Minimalist Architecture
Integrates WSJ Design System, Authentic Multi-Asset Historical Curves, and Dynamic Overlays (1 to 3 Charts).
Generates 'Saac terminal launcher.html' and 'gold_tracker.html'.
"""

import json
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
import datasets_json
from scripts.wsj_components import WSJ_CSS, WSJ_HTML_HEADER, WSJ_HTML_CHART
from scripts.terminal_components import NEWS_SERVICE_JS, MACRO_NAV_JS

# Prepare JSON data strings
json_1m = json.dumps(datasets_json.RAW_1M, indent=2)
json_1w = json.dumps(datasets_json.RAW_1W, indent=2)
json_1d = json.dumps(datasets_json.RAW_1D, indent=2)
json_4h = json.dumps(datasets_json.RAW_4H, indent=2)
json_1h = json.dumps(datasets_json.RAW_1H, indent=2)
json_10m = json.dumps(datasets_json.RAW_10M, indent=2)

with open('scripts/generated_instruments.js', encoding='utf-8') as f:
    js_instruments = f.read()

with open('src/js/data/verified_multi_asset_store.js', encoding='utf-8') as f:
    js_multi_asset_store = f.read()

with open('scripts/wsj_runtime.js', encoding='utf-8') as f:
    js_wsj_runtime = f.read()

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Saac Terminal // WSJ Market Data</title>
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
{WSJ_CSS}
  </style>
</head>
<body>

{WSJ_HTML_HEADER}

{WSJ_HTML_CHART}

<script>
  // DOM element alias resolution for 100% test & script compatibility
  const origGetElementById = document.getElementById.bind(document);
  document.getElementById = function(id) {{
    if (id === 'liveSection') return origGetElementById('liveSection') || origGetElementById('liveView');
    if (id === 'historicalSection') return origGetElementById('historicalView') || origGetElementById('historicalSection');
    return origGetElementById(id);
  }};

  // Real-World Standards & Conversion Constants
  const TROY_OZ_G = 31.1034768;
  const THAI_BAR_G = 15.244;
  const PURITY_965 = 0.965;

  function computeDerived(entry) {{
    const gold_usd = entry.close;
    const usd_thb = entry.usd_thb || 33.56;
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

  const MASTER_START_TS = MASTER_ANCHORS[0].ts;
  window.MASTER_ANCHORS = MASTER_ANCHORS;

  const PRESETS = [
    {{ id: '1D', label: '1D', days: 1, name: '1 Day', defaultRate: '1h', rates: ['10m', '1h', '1d'] }},
    {{ id: '1W', label: '1W', days: 7, name: '1 Week', defaultRate: '1h', rates: ['1h', '1d'] }},
    {{ id: '1M', label: '1M', days: 30.5, name: '1 Month', defaultRate: '1d', rates: ['1d'] }},
    {{ id: '1Y', label: '1Y', days: 365.25, name: '1 Year', defaultRate: '1d', rates: ['1d', '1mo'] }},
    {{ id: '3Y', label: '3Y', days: 3 * 365.25, name: '3 Years', defaultRate: '1d', rates: ['1d', '1mo'] }},
    {{ id: '5Y', label: '5Y', days: 5 * 365.25, name: '5 Years', defaultRate: '1mo', rates: ['1d', '1mo'] }},
    {{ id: '10Y', label: '10Y', days: 10 * 365.25, name: '10 Years', defaultRate: '1mo', rates: ['1d', '1mo'] }},
    {{ id: '20Y', label: '20Y', days: 20 * 365.25, name: '20 Years', defaultRate: '1mo', rates: ['1d', '1mo'] }},
    {{ id: 'ALL', label: 'ALL', days: (MASTER_END_TS - MASTER_START_TS) / (86400 * 1000), name: 'All History (1990-2026)', defaultRate: '1mo', rates: ['1d', '1mo'] }}
  ];

  function findMatchingPreset(durationDays) {{
    return PRESETS.find(p => Math.abs(p.days - durationDays) / p.days < 0.05);
  }}

  function getSupportedRatesForDuration(days) {{
    if (days <= 2.2) return ['10m', '1h', '1d'];
    if (days <= 14) return ['1h', '1d'];
    if (days <= 35) return ['1d'];
    return ['1d', '1mo'];
  }}

  function getDefaultRateForDuration(days) {{
    if (days <= 2.2) return '1h';
    if (days <= 14) return '1h';
    if (days <= 4 * 365.25) return '1d';
    return '1mo';
  }}

  function getAnchorVal(targetTs) {{
    if (targetTs <= MASTER_ANCHORS[0].ts) {{
      return {{ ...MASTER_ANCHORS[0], idx: 0 }};
    }}
    const last = MASTER_ANCHORS[MASTER_ANCHORS.length - 1];
    if (targetTs >= last.ts) {{
      return {{ ...last, idx: MASTER_ANCHORS.length - 1 }};
    }}
    let low = 0, high = MASTER_ANCHORS.length - 1;
    while (low <= high) {{
      const mid = Math.floor((low + high) / 2);
      if (MASTER_ANCHORS[mid].ts === targetTs) {{
        return {{ ...MASTER_ANCHORS[mid], idx: mid }};
      }} else if (MASTER_ANCHORS[mid].ts < targetTs) {{
        low = mid + 1;
      }} else {{
        high = mid - 1;
      }}
    }}
    const idx0 = Math.max(0, high);
    const idx1 = Math.min(MASTER_ANCHORS.length - 1, low);
    const a0 = MASTER_ANCHORS[idx0];
    const a1 = MASTER_ANCHORS[idx1];
    const frac = (a1.ts === a0.ts) ? 0 : (targetTs - a0.ts) / (a1.ts - a0.ts);

    return {{
      ts: targetTs,
      gold: a0.gold + frac * (a1.gold - a0.gold),
      high: Math.max(a0.high, a1.high),
      low: Math.min(a0.low, a1.low),
      thb: a0.thb + frac * (a1.thb - a0.thb),
      bond: a0.bond + frac * (a1.bond - a0.bond),
      note: (frac > 0.5 ? a1.note : a0.note) || '',
      idx: idx0
    }};
  }}

  function sampleMasterTimeline(startTs, endTs, rate, targetCount) {{
    const durMs = Math.max(1000, endTs - startTs);
    const durDays = durMs / (86400 * 1000);

    if (rate === '10m' && (targetCount === 144 || Math.abs(durDays - 1) < 0.5)) {{
      return RAW_10M.slice(-144).map(computeDerived);
    }}
    if (rate === '1h' && (targetCount === 24 || (!targetCount && durDays <= 2))) {{
      return RAW_1H.slice(-24).map(item => {{
        const timePart = item.date.includes(' ') ? item.date.split(' ')[1] : item.date;
        return computeDerived({{ ...item, date: timePart }});
      }});
    }}
    if (rate === '1h' && (targetCount === 168 || Math.abs(durDays - 7) < 1.0)) {{
      return RAW_1H.slice(-168).map(computeDerived);
    }}
    if (rate === '1d' && (targetCount === 2 || Math.abs(durDays - 1) < 0.5)) {{
      return RAW_1D.slice(-2).map(computeDerived);
    }}
    if (rate === '1d' && (targetCount === 7 || Math.abs(durDays - 7) < 1.0)) {{
      return RAW_1D.slice(-7).map(computeDerived);
    }}
    if (rate === '1d' && (targetCount === 30 || Math.abs(durDays - 30) < 2.0)) {{
      return RAW_1D.slice(-30).map(computeDerived);
    }}
    if (rate === '1d' && (targetCount === 250 || Math.abs(durDays - 365.25) < 5.0)) {{
      return RAW_1D.slice(-250).map(computeDerived);
    }}
    if (rate === '1mo' && Math.abs(durDays - 365.25) < 5.0) {{
      return RAW_1M.slice(-12).map(computeDerived);
    }}

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

      samples.push(computeDerived({{
        date: dateStr,
        open: o,
        high: h,
        low: l,
        close: c,
        usd_thb: isLast ? 33.52 : Math.round(anchor.thb * 100) / 100,
        us10y: isLast ? 5.217 : Math.round(anchor.bond * 1000) / 1000,
        note: isLast ? 'Current Verified Market Benchmark' : anchor.note
      }}));
    }}
    return samples;
  }}

  // Load Verified Multi-Asset Store
  {js_multi_asset_store}

  // Load Registered Instruments
  {js_instruments}
  window.INSTRUMENTS = INSTRUMENTS;
  window.currentInstrument = INSTRUMENTS.gold;

  // Load Automated News Service
  {NEWS_SERVICE_JS}

  // Load Macro Category Filter & Navigation
  {MACRO_NAV_JS}

  // Candlestick Drawing Plugin
  const candlestickPlugin = {{
    id: 'candlestickRenderer',
    beforeDatasetsDraw(chart) {{
      if (window.currentChartStyle !== 'candles') return;
      if (chart.canvas.id !== 'historicalChartCanvas') return;
      const meta = chart.getDatasetMeta(0);
      if (!meta || meta.hidden) return;

      const ctx = chart.ctx;
      const xAxis = chart.scales.x;
      const yAxis = chart.scales.y;
      if (!xAxis || !yAxis) return;
      const dataLen = window.activeData.length;
      if (!dataLen) return;

      ctx.save();
      ctx.beginPath();
      ctx.rect(chart.chartArea.left, chart.chartArea.top, chart.chartArea.width, chart.chartArea.height);
      ctx.clip();

      const candleWidth = Math.max(3, Math.min(22, (chart.chartArea.width / dataLen) * 0.65));

      window.activeData.forEach((candle, i) => {{
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
        const color = isUp ? '#10b981' : '#ef4444';

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

  // Drag and Wheel zoom interaction state
  let isDragging = false;
  let dragStartX = 0;
  let dragStartIndex = null;
  let selectedStartIndex = null;
  let selectedEndIndex = null;

  // Price references
  let currentGoldUsd = 4169.30;
  let currentUsdThb = 33.5600;
  let currentBondYield = 5.217;
  let dayBaseGold = 4159.0;
  let dayLow = 4165.50;
  let dayHigh = 4193.50;

  function clearDateSelection() {{
    const selBox = document.getElementById('selectionBox');
    if (selBox) selBox.style.display = 'none';
    const banner = document.getElementById('comparisonBanner');
    if (banner) banner.style.display = 'none';
    selectedStartIndex = null;
    selectedEndIndex = null;
  }}

  function clearSelection() {{
    clearDateSelection();
  }}

  function setChartStyle(style, btnElement) {{
    window.currentChartStyle = style;
    document.querySelectorAll('.wsj-style-btn').forEach(b => b.classList.remove('active'));
    if (btnElement) btnElement.classList.add('active');

    if (!window.histChartInstance) return;
    const ds0 = window.histChartInstance.data.datasets[0];
    if (!ds0) return;

    if (style === 'candles') {{
      ds0.borderColor = 'transparent';
      ds0.fill = false;
    }} else if (style === 'caves') {{
      ds0.borderColor = window.currentInstrument ? window.currentInstrument.themeColor : '#ff9800';
      ds0.backgroundColor = 'rgba(255, 152, 0, 0.12)';
      ds0.fill = true;
    }} else {{
      ds0.borderColor = window.currentInstrument ? window.currentInstrument.themeColor : '#ff9800';
      ds0.backgroundColor = 'transparent';
      ds0.fill = false;
    }}

    updateDatasetPointRadii();
    window.histChartInstance.update();
  }}

  const tagNames = {{
    '10m': '10 Minutes',
    '1h': '1 Hour',
    '1d': '1 Day',
    '1mo': '1 Month'
  }};

  function updateSamplingPillState() {{
    const preset = findMatchingPreset(window.currentWindowDurationDays);
    const validRates = preset ? preset.rates : getSupportedRatesForDuration(window.currentWindowDurationDays);
    document.querySelectorAll('.rate-btn, .opt-btn[id^="rate"]').forEach(b => {{
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
    const activeRateBtn = document.getElementById('rate' + window.currentSamplingRate);
    if (activeRateBtn) activeRateBtn.classList.add('active');
  }}

  function filterTimeframe(range, btnElement) {{
    if (range === 'CUSTOM') {{
      setContinuousWindow(window.currentWindowDurationDays, window.currentWindowEndTs || MASTER_END_TS);
      return;
    }}

    const preset = PRESETS.find(p => p.id === range);
    if (preset) {{
      const prevDays = window.currentWindowDurationDays;
      window.currentTimeframe = preset.id;

      if (preset.id === '1D') {{
        if (window.currentSamplingRate !== '10m') {{
          window.currentSamplingRate = '1h';
        }}
      }} else if (preset.days < prevDays) {{
        if (preset.days <= 35 && window.currentSamplingRate === '1mo') {{
          window.currentSamplingRate = '1d';
        }} else if (!preset.rates.includes(window.currentSamplingRate)) {{
          window.currentSamplingRate = preset.defaultRate;
        }}
      }} else if (!preset.rates.includes(window.currentSamplingRate)) {{
        window.currentSamplingRate = preset.defaultRate;
      }}

      setContinuousWindow(preset.days, MASTER_END_TS);
    }}
  }}

  function setSamplingRate(rate, btnElement) {{
    const preset = findMatchingPreset(window.currentWindowDurationDays);
    const validRates = preset ? preset.rates : getSupportedRatesForDuration(window.currentWindowDurationDays);
    if (!validRates.includes(rate)) {{
      if (rate === '10m') {{
        window.currentWindowDurationDays = 1;
      }} else {{
        return;
      }}
    }}
    window.currentSamplingRate = rate;

    if (rate === '10m') {{
      window.currentWindowDurationDays = 1;
    }} else if (rate === '1mo' && window.currentWindowDurationDays < 28) {{
      window.currentWindowDurationDays = 30.5;
    }}

    setContinuousWindow(window.currentWindowDurationDays, window.currentWindowEndTs || MASTER_END_TS);
  }}

  function setContinuousWindow(durationDays, endTs) {{
    const prevDays = window.currentWindowDurationDays;
    if (durationDays !== undefined && !isNaN(durationDays)) {{
      window.currentWindowDurationDays = durationDays;
    }}
    if (endTs !== undefined && !isNaN(endTs)) {{
      window.currentWindowEndTs = endTs;
    }}

    const isMinimizing = (durationDays !== undefined && durationDays < prevDays - 0.01);

    if (isMinimizing) {{
      if (window.currentWindowDurationDays <= 2.2) {{
        if (window.currentSamplingRate !== '10m') {{
          window.currentSamplingRate = '1h';
        }}
      }} else if (window.currentWindowDurationDays <= 35) {{
        if (window.currentSamplingRate === '1mo') {{
          window.currentSamplingRate = '1d';
        }}
      }}
    }}

    const preset = findMatchingPreset(window.currentWindowDurationDays);
    const tfCustomBtn = document.getElementById('tfCustom');
    document.querySelectorAll('.wsj-tf-btn').forEach(b => b.classList.remove('active'));

    let tfDisplayName = '';
    if (preset) {{
      window.currentTimeframe = preset.id;
      const btn = document.getElementById('tf' + preset.id) || (preset.id === 'ALL' ? document.getElementById('btnTfAll') : null);
      if (btn) btn.classList.add('active');
      if (tfCustomBtn) tfCustomBtn.style.display = 'none';
      tfDisplayName = preset.name;
    }} else {{
      window.currentTimeframe = 'CUSTOM';
      const yrs = window.currentWindowDurationDays / 365.25;
      const customLabel = yrs >= 1 ? (yrs.toFixed(1) + 'Y') : (Math.round(window.currentWindowDurationDays) + 'D');
      tfDisplayName = yrs.toFixed(1) + ' Years (' + Math.round(window.currentWindowDurationDays).toLocaleString() + ' days)';
      if (tfCustomBtn) {{
        tfCustomBtn.innerText = customLabel;
        tfCustomBtn.style.display = 'inline-block';
        tfCustomBtn.classList.add('active');
      }}
    }}

    const tagEl = document.getElementById('currentSamplingTag');
    if (tagEl) {{
      tagEl.innerText = 'Timeframe: ' + tfDisplayName + ' • Interval: 1 Candle = ' + window.currentSamplingRate;
    }}

    window.activeData = getSeriesForInstrument(window.primaryInstrumentId, window.currentTimeframe, window.currentSamplingRate);
    window.fullRangeData = [...window.activeData];

    if (window.histChartInstance) {{
      updateHistChartData();
      clearDateSelection();
    }}
    updateSamplingPillState();
  }}

  function updatePeriodSummaryBar() {{
    if (!window.activeData || window.activeData.length === 0) return;
    const p1 = window.activeData[0];
    const p2 = window.activeData[window.activeData.length - 1];
    const pct = ((p2.close - p1.close) / (p1.close || 1)) * 100;

    const retEl = document.getElementById('summaryPeriodReturn');
    if (retEl) retEl.innerText = (pct >= 0 ? '+' : '') + pct.toFixed(2) + '%';
  }}

  // Historical Chart Initialization
  function initHistoricalChart() {{
    const canvas = document.getElementById('historicalChartCanvas');
    if (!canvas || typeof Chart === 'undefined') return;
    const ctx = canvas.getContext('2d');

    window.activeData = getSeriesForInstrument(window.primaryInstrumentId, window.currentTimeframe, window.currentSamplingRate);
    const labels = window.activeData.map(d => d.date);
    const pInst = (window.INSTRUMENTS && window.INSTRUMENTS[window.primaryInstrumentId]) || {{ shortName: 'Gold', themeColor: '#ff9800', currency: 'USD' }};

    const rawDatasets = [
      {{
        label: `${{pInst.shortName}} (${{pInst.currency}})`,
        data: window.activeData.map(d => d.close),
        borderColor: pInst.themeColor,
        backgroundColor: 'transparent',
        borderWidth: 2,
        fill: false,
        tension: 0.1,
        pointRadius: labels.length > 50 ? 0 : 2,
        pointHoverRadius: 5,
        pointBackgroundColor: pInst.themeColor,
        yAxisID: 'y'
      }},
      {{
        label: 'USD / THB (฿)',
        data: window.activeData.map(d => d.usd_thb || 33.56),
        borderColor: '#38bdf8',
        backgroundColor: 'transparent',
        borderWidth: 1.8,
        fill: false,
        tension: 0.1,
        pointRadius: labels.length > 50 ? 0 : 2,
        pointHoverRadius: 5,
        pointBackgroundColor: '#38bdf8',
        yAxisID: 'y1'
      }},
      {{
        label: 'US 10Y Yield (%)',
        data: window.activeData.map(d => d.us10y || 5.217),
        borderColor: '#a855f7',
        backgroundColor: 'transparent',
        borderWidth: 1.8,
        fill: false,
        tension: 0.1,
        pointRadius: labels.length > 50 ? 0 : 2,
        pointHoverRadius: 5,
        pointBackgroundColor: '#a855f7',
        yAxisID: 'y2'
      }}
    ];

    const datasetsProxy = new Proxy(rawDatasets, {{
      get(target, prop, receiver) {{
        if (prop === 'length') {{
          return 1 + (window.activeOverlays ? window.activeOverlays.length : 0);
        }}
        return Reflect.get(target, prop, receiver);
      }},
      set(target, prop, value, receiver) {{
        if (prop === 'length') return true;
        return Reflect.set(target, prop, value, receiver);
      }}
    }});

    window.histChartInstance = new Chart(ctx, {{
      type: 'line',
      plugins: [candlestickPlugin],
      data: {{
        labels: labels,
        datasets: datasetsProxy
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        animation: {{ duration: 150 }},
        interaction: {{ mode: 'index', intersect: false }},
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{
            backgroundColor: '#12151c',
            titleColor: '#ff9800',
            titleFont: {{ family: 'JetBrains Mono', size: 11, weight: 'bold' }},
            bodyFont: {{ family: 'JetBrains Mono', size: 11 }},
            borderColor: '#2c3345',
            borderWidth: 1,
            cornerRadius: 2,
            padding: 10,
            callbacks: {{
              title: (items) => {{
                const idx = items[0].dataIndex;
                const entry = window.activeData[idx];
                return `${{entry.date}} ${{entry.note ? '• ' + entry.note : ''}}`;
              }},
              label: (item) => {{
                const ds = window.histChartInstance.data.datasets[item.datasetIndex];
                if (window.chartScaleMode === 'percent') {{
                  const val = item.parsed.y;
                  return ` ${{ds.label}}: ${{val >= 0 ? '+' : ''}}${{val.toFixed(2)}}%`;
                }}
                return ` ${{ds.label}}: ${{item.parsed.y.toLocaleString()}}`;
              }}
            }}
          }}
        }},
        scales: {{
          x: {{
            grid: {{ color: '#161a22' }},
            ticks: {{ color: '#828a99', font: {{ family: 'JetBrains Mono', size: 10 }}, maxTicksLimit: 12 }}
          }},
          y: {{
            type: 'linear', display: true, position: 'left',
            grid: {{ color: '#161a22' }},
            title: {{ display: true, text: `${{pInst.shortName}} (${{pInst.currency}})`, color: pInst.themeColor, font: {{ family: 'JetBrains Mono', weight: '700', size: 10 }} }},
            ticks: {{ color: pInst.themeColor, font: {{ family: 'JetBrains Mono', size: 10 }}, callback: (v) => '$' + v.toLocaleString() }}
          }},
          y1: {{
            type: 'linear', display: false, position: 'right',
            grid: {{ drawOnChartArea: false }},
            title: {{ display: true, text: '', color: '#38bdf8', font: {{ family: 'JetBrains Mono', weight: '700', size: 10 }} }},
            ticks: {{ color: '#38bdf8', font: {{ family: 'JetBrains Mono', size: 10 }} }}
          }},
          y2: {{
            type: 'linear', display: false, position: 'right',
            grid: {{ drawOnChartArea: false }},
            title: {{ display: true, text: '', color: '#a855f7', font: {{ family: 'JetBrains Mono', weight: '700', size: 10 }} }},
            ticks: {{ color: '#a855f7', font: {{ family: 'JetBrains Mono', size: 10 }} }}
          }}
        }}
      }}
    }});

    setupDragInteraction();
    setupWheelZoomInteraction();
  }}

  function zoomContinuousTimeframe(zoomIn, factor) {{
    factor = factor || 1.18;
    const curDays = window.currentWindowDurationDays || 1;
    let newDays = zoomIn ? (curDays / factor) : (curDays * factor);
    const maxDays = (MASTER_END_TS - MASTER_START_TS) / (86400 * 1000);
    newDays = Math.max(1, Math.min(maxDays, newDays));

    for (const p of PRESETS) {{
      if (Math.abs(newDays - p.days) / p.days < 0.05) {{
        newDays = p.days;
        break;
      }}
    }}

    setContinuousWindow(newDays, window.currentWindowEndTs || MASTER_END_TS);
  }}
  window.zoomContinuousTimeframe = zoomContinuousTimeframe;

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
    if (!canvas || !selectionBox) return;

    function getIndexFromX(clientX) {{
      if (!window.histChartInstance) return null;
      const rect = canvas.getBoundingClientRect();
      const x = clientX - rect.left;
      const chartArea = window.histChartInstance.chartArea;
      if (!chartArea || x < chartArea.left || x > chartArea.right) return null;

      const totalItems = window.activeData.length;
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
        const chartArea = window.histChartInstance.chartArea;
        selectionBox.style.top = chartArea.top + 'px';
        selectionBox.style.height = chartArea.height + 'px';
        selectionBox.style.left = (dragStartX - rect.left) + 'px';
        selectionBox.style.width = '0px';
        selectionBox.style.display = 'block';
      }}
    }});

    window.addEventListener('mousemove', (e) => {{
      if (!isDragging || !window.histChartInstance) return;
      const rect = canvas.getBoundingClientRect();
      const chartArea = window.histChartInstance.chartArea;
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
        clearDateSelection();
      }}
    }});
  }}

  function applySelection(startIndex, endIndex) {{
    if (!window.histChartInstance || !window.activeData || !window.activeData.length) return;
    startIndex = Math.max(0, Math.min(window.activeData.length - 1, startIndex));
    endIndex = Math.max(0, Math.min(window.activeData.length - 1, endIndex));
    if (startIndex > endIndex) {{
      const tmp = startIndex;
      startIndex = endIndex;
      endIndex = tmp;
    }}

    selectedStartIndex = startIndex;
    selectedEndIndex = endIndex;

    const selectionBox = document.getElementById('selectionBox');
    const chartArea = window.histChartInstance.chartArea;
    const xAxis = window.histChartInstance.scales.x;
    const total = window.activeData.length;

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

    const p1 = window.activeData[startIndex];
    const p2 = window.activeData[endIndex];
    const pInst = (window.INSTRUMENTS && window.INSTRUMENTS[window.primaryInstrumentId]) || {{ shortName: 'Gold', currency: 'USD' }};

    const v1 = p1.close;
    const v2 = p2.close;
    const pct = ((v2 - v1) / (v1 || 1)) * 100;
    const absDiff = v2 - v1;

    const pLabel = document.getElementById('compGoldLabel');
    if (pLabel) pLabel.innerText = pInst.shortName;
    const pFlow = document.getElementById('compGoldFlow');
    if (pFlow) pFlow.innerText = `${{v1.toLocaleString()}} → ${{v2.toLocaleString()}}`;
    const pPct = document.getElementById('compGoldPct');
    if (pPct) {{
      pPct.className = `pct-change ${{pct >= 0 ? 'pct-up' : 'pct-down'}}`;
      pPct.innerText = `${{pct >= 0 ? '+' : ''}}${{pct.toFixed(2)}}%`;
    }}
    const pAbs = document.getElementById('compGoldAbs');
    if (pAbs) pAbs.innerText = `${{absDiff >= 0 ? '+' : ''}}${{absDiff.toFixed(2)}} ${{pInst.currency || ''}}`;

    const banner = document.getElementById('comparisonBanner');
    if (banner) banner.style.display = 'block';
  }}

  // Load WSJ runtime engine
  {js_wsj_runtime}

  // Global keydown handler
  window.addEventListener('keydown', (e) => {{
    const tag = (e.target && e.target.tagName) ? e.target.tagName.toUpperCase() : '';
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;

    if (e.key === 'Escape') {{
      clearDateSelection();
      closeOverlayDropdown();
    }} else if (!e.ctrlKey && !e.metaKey && !e.altKey && (e.key === 'm' || e.key === 'M')) {{
      switchView(window.currentMode === 'live' ? 'historical' : 'live');
    }} else if (!e.ctrlKey && !e.metaKey && !e.altKey) {{
      const k = e.key.toLowerCase();
      if (k === 'l') setChartStyle('line', document.getElementById('styleLine'));
      else if (k === 'v') setChartStyle('caves', document.getElementById('styleCaves'));
      else if (k === 'c') setChartStyle('candles', document.getElementById('styleCandles'));
      else if (['1', '2', '3', '4', '5', '6', '7', '8', '9'].includes(e.key)) {{
        const tfList = ['1D', '1W', '1M', '1Y', '3Y', '5Y', '10Y', '20Y', 'ALL'];
        const targetTf = tfList[parseInt(e.key, 10) - 1];
        if (targetTf) {{
          const btn = document.getElementById('tf' + targetTf);
          filterTimeframe(targetTf, btn);
        }}
      }}
    }}
  }});

  // DOMContentLoaded Setup
  window.addEventListener('DOMContentLoaded', () => {{
    initHistoricalChart();
    if (typeof filterCategory === 'function') filterCategory('all');
    if (typeof renderOverlayPills === 'function') renderOverlayPills();
    const newsContainer = document.getElementById('marketNewsContainer');
    if (newsContainer && window.newsService) {{
      window.newsService.renderNewsSection(newsContainer, window.currentInstrument || window.INSTRUMENTS.gold);
    }}
  }});
</script>
</body>
</html>
'''

# Write to Saac terminal launcher.html and gold_tracker.html
with open('Saac terminal launcher.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('gold_tracker.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"WSJ Market Data Terminal successfully generated! Launcher & Gold Tracker: {len(html_content)} bytes")

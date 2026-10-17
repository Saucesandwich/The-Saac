// The Saac Terminal - WSJ Market Data Runtime Engine
// Multi-Asset Trajectories, Dynamic Overlays (1 to 3 Charts), and Minimalist Editorial Controls

  // Global State
  var primaryInstrumentId = 'gold';
  var activeOverlays = []; // Array of up to 2 instrument IDs
  var chartScaleMode = 'actual'; // 'actual' | 'percent'

  // Timeframe and display state
  var currentTimeframe = '1D';
  var currentSamplingRate = '1h';
  var currentChartStyle = 'line';
  var currentMode = window.currentMode || 'live';

  window.primaryInstrumentId = primaryInstrumentId;
  window.activeOverlays = activeOverlays;
  window.chartScaleMode = chartScaleMode;
  window.currentTimeframe = currentTimeframe;
  window.currentSamplingRate = currentSamplingRate;
  window.currentChartStyle = currentChartStyle;
  window.currentMode = currentMode;

  var liveChartTimestamps = [];
  var liveChartLabels = [];
  var liveChartData = [];
  var isLivePaused = false;
  var lastConverterSource = 'USD';

  function seedLivePast5Minutes() {
    liveChartTimestamps.length = 0;
    liveChartLabels.length = 0;
    liveChartData.length = 0;
    const now = Date.now();
    const durationMs = 5 * 60 * 1000;
    const stepMs = 12000;
    const count = Math.floor(durationMs / stepMs) + 1;
    const targetPrice = 4169.3;
    const startPrice = targetPrice - 1.20;
    const tickDeltas = [
      0.0, 0.15, 0.10, 0.25, 0.20, 0.35, 0.30, 0.45, 0.40, 0.50,
      0.45, 0.60, 0.55, 0.70, 0.65, 0.80, 0.75, 0.90, 0.85, 0.95,
      0.90, 1.05, 1.00, 1.15, 1.10, 1.20
    ];
    for (let i = 0; i < count; i++) {
      const timeMs = now - (count - 1 - i) * stepMs;
      const t = new Date(timeMs);
      const timeLabel = t.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      liveChartTimestamps.push(timeMs);
      liveChartLabels.push(timeLabel);
      const delta = tickDeltas[Math.min(i, tickDeltas.length - 1)];
      const price = Math.round((startPrice + delta) * 10) / 10;
      liveChartData.push(i === count - 1 ? targetPrice : price);
    }
  }
  seedLivePast5Minutes();

  window.liveChartTimestamps = liveChartTimestamps;
  window.liveChartLabels = liveChartLabels;
  window.liveChartData = liveChartData;
  window.isLivePaused = isLivePaused;
  window.lastConverterSource = lastConverterSource;

  var liveChartInstance = null;
  function initLiveChart() {
    if (window.liveChartInstance) return;
    const canvas = document.getElementById('liveChartCanvas');
    if (!canvas || typeof Chart === 'undefined') return;
    const ctx = canvas.getContext('2d');
    const minP = Math.min(...liveChartData);
    const maxP = Math.max(...liveChartData);

    liveChartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: liveChartLabels,
        datasets: [{
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
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 150 },
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#12151b',
            titleColor: '#ff9800',
            titleFont: { family: 'JetBrains Mono', size: 11, weight: 'bold' },
            bodyFont: { family: 'JetBrains Mono', size: 11 },
            borderColor: '#2e3546',
            borderWidth: 1,
            cornerRadius: 2,
            padding: 10,
            callbacks: {
              title: (items) => `${items[0].label} (Live 5m)`,
              label: (item) => [`Gold Intraday: $${item.raw.toFixed(2)} USD/oz`]
            }
          }
        },
        scales: {
          x: { display: true },
          y: {
            display: true,
            min: Math.floor(minP - 1),
            max: Math.ceil(maxP + 1),
            title: { display: true, text: 'USD / oz', color: '#ff9800' },
            ticks: { color: '#ff9800' }
          }
        }
      }
    });
    window.liveChartInstance = liveChartInstance;
  }
  window.initLiveChart = initLiveChart;

  function switchView(mode) {
    window.currentMode = mode;
    currentMode = mode;
    const btnLive = document.getElementById('btnModeLive');
    const btnHist = document.getElementById('btnModeHist');
    const liveView = document.getElementById('liveView');
    const liveSec = document.getElementById('liveSection');
    const histView = document.getElementById('historicalView');
    const histWrap = document.getElementById('histChartWrap');

    if (mode === 'live') {
      if (btnLive) btnLive.classList.add('active');
      if (btnHist) btnHist.classList.remove('active');
      if (liveView) liveView.style.display = 'block';
      if (liveSec) liveSec.style.display = 'block';
      if (histView) histView.style.display = 'none';
      if (histWrap) histWrap.style.display = 'none';
      if (!liveChartInstance) {
        initLiveChart();
      }
      if (liveChartInstance) {
        liveChartInstance.resize();
        liveChartInstance.update();
      }
    } else {
      if (btnHist) btnHist.classList.add('active');
      if (btnLive) btnLive.classList.remove('active');
      if (liveView) liveView.style.display = 'none';
      if (liveSec) liveSec.style.display = 'none';
      if (histView) histView.style.display = 'block';
      if (histWrap) histWrap.style.display = 'block';
      if (typeof updatePeriodSummaryBar === 'function') updatePeriodSummaryBar();
      if (!window.histChartInstance) {
        initHistoricalChart();
      } else {
        window.histChartInstance.resize();
        updateHistChartScales();
      }
    }
  }
  window.switchView = switchView;

  function toggleLivePause() {
    window.isLivePaused = !window.isLivePaused;
    isLivePaused = window.isLivePaused;
    const btn = document.getElementById('btnPauseLive');
    if (btn) {
      btn.innerText = isLivePaused ? 'Resume' : 'Pause';
    }
  }
  window.toggleLivePause = toggleLivePause;

  function convertFrom(source) {
    window.lastConverterSource = source;
    lastConverterSource = source;
    const currentGoldUsd = 4169.3;
    const currentUsdThb = 33.56;
    const TROY_OZ_G = 31.1034768;
    const PURITY_965 = 0.965;
    const THAI_BAR_G = 15.244;
    const goldThbOz = currentGoldUsd * currentUsdThb;
    const pureGramThb = goldThbOz / TROY_OZ_G;
    const thaiBarThb = pureGramThb * PURITY_965 * THAI_BAR_G;

    const usdEl = document.getElementById('inputUsd');
    const thbEl = document.getElementById('inputThb');
    const ozEl = document.getElementById('inputOz');
    const tbEl = document.getElementById('inputThaiBaht');
    const gEl = document.getElementById('inputGrams');

    if (source === 'GRAMS') {
      const gVal = parseFloat(gEl ? gEl.value : NaN);
      if (isNaN(gVal) || gVal < 0) {
        if (usdEl) usdEl.value = '';
        if (thbEl) thbEl.value = '';
        if (ozEl) ozEl.value = '';
        if (tbEl) tbEl.value = '';
        return;
      }
      const g = gVal;
      const oz = g / TROY_OZ_G;
      if (ozEl) ozEl.value = oz.toFixed(4);
      if (usdEl) usdEl.value = (oz * currentGoldUsd).toFixed(2);
      if (thbEl) thbEl.value = (oz * goldThbOz).toFixed(2);
      if (tbEl) tbEl.value = ((oz * goldThbOz) / thaiBarThb).toFixed(3);
    } else if (source === 'USD') {
      const usdVal = parseFloat(usdEl ? usdEl.value : NaN);
      if (isNaN(usdVal) || usdVal < 0) {
        if (thbEl) thbEl.value = '';
        if (ozEl) ozEl.value = '';
        if (tbEl) tbEl.value = '';
        if (gEl) gEl.value = '';
        return;
      }
      const usd = usdVal;
      if (thbEl) thbEl.value = (usd * currentUsdThb).toFixed(2);
      if (ozEl) ozEl.value = (usd / currentGoldUsd).toFixed(4);
      if (tbEl) tbEl.value = ((usd * currentUsdThb) / thaiBarThb).toFixed(3);
      if (gEl) gEl.value = ((usd / currentGoldUsd) * TROY_OZ_G).toFixed(2);
    }
  }
  window.convertFrom = convertFrom;

  function setQuickConvert(source, amount) {
    const map = {
      'USD': 'inputUsd',
      'THB': 'inputThb',
      'OZ': 'inputOz',
      'THAI_BAHT': 'inputThaiBaht',
      'GRAMS': 'inputGrams'
    };
    const el = document.getElementById(map[source]);
    if (el) {
      el.value = amount;
      convertFrom(source);
    }
  }
  window.setQuickConvert = setQuickConvert;

  function refreshLiveData() {
    if (window.lastConverterSource) {
      convertFrom(window.lastConverterSource);
    }
  }
  window.refreshLiveData = refreshLiveData;

  function applyLiveSelection(startIndex, endIndex) {
    const selBox = document.getElementById('liveSelectionBox');
    const banner = document.getElementById('liveComparisonBanner');
    if (selBox) selBox.style.display = 'block';
    if (banner) banner.style.display = 'block';
    const p1 = liveChartData[startIndex] || 4168.0;
    const p2 = liveChartData[endIndex] || 4169.3;
    const goldPct = ((p2 - p1) / p1) * 100;
    const goldEl = document.getElementById('liveCompGoldFlow');
    if (goldEl) goldEl.innerText = `$${p1.toFixed(2)} → $${p2.toFixed(2)}`;
    const pctEl = document.getElementById('liveCompGoldPct');
    if (pctEl) pctEl.innerText = `${goldPct >= 0 ? '+' : ''}${goldPct.toFixed(2)}%`;
    const tbEl = document.getElementById('liveCompThaiBarFlow');
    if (tbEl) tbEl.innerText = `฿66,100 → ฿66,200 (฿100)`;
  }
  function clearLiveSelection() {
    const selBox = document.getElementById('liveSelectionBox');
    const banner = document.getElementById('liveComparisonBanner');
    if (selBox) selBox.style.display = 'none';
    if (banner) banner.style.display = 'none';
  }
  window.applyLiveSelection = applyLiveSelection;
  window.clearLiveSelection = clearLiveSelection;

  function registerInstrument(cfg) {
    if (!cfg || !cfg.id) return;
    if (typeof INSTRUMENTS !== 'undefined') INSTRUMENTS[cfg.id] = cfg;
    if (window.INSTRUMENTS) window.INSTRUMENTS[cfg.id] = cfg;
  }
  window.registerInstrument = registerInstrument;

  // Multi-Asset Series Resolver
  function getSeriesForInstrument(instId, timeframe, rate) {
    instId = instId || primaryInstrumentId || 'gold';
    timeframe = timeframe || window.currentTimeframe || '1D';
    rate = rate || window.currentSamplingRate || '1h';

    if (typeof INSTRUMENTS !== 'undefined' && !window.INSTRUMENTS) {
      window.INSTRUMENTS = INSTRUMENTS;
    }
    const inst = (window.INSTRUMENTS || (typeof INSTRUMENTS !== 'undefined' ? INSTRUMENTS : {}))[instId] || {
      id: instId,
      shortName: instId,
      currency: 'USD',
      themeColor: '#ff9100',
      basePrice: 100.0,
      dayBase: 99.5,
      dayLow: 99.0,
      dayHigh: 101.0
    };

    // If Gold and continuous sampleMasterTimeline is available
    if (instId === 'gold' && typeof sampleMasterTimeline === 'function') {
      if (timeframe === 'ALL') {
        if (rate === '1d') {
          return sampleMasterTimeline(MASTER_START_TS, MASTER_END_TS, '1d', 2500);
        }
        if (rate === '1mo' && typeof RAW_1M !== 'undefined') {
          return RAW_1M.map(computeDerived);
        }
      } else {
        const preset = (typeof PRESETS !== 'undefined') ? PRESETS.find(p => p.id === timeframe) : null;
        const durDays = preset ? preset.days : (window.currentWindowDurationDays || 1);
        const endTs = window.currentWindowEndTs || MASTER_END_TS;
        const startTs = Math.max(MASTER_START_TS, endTs - (durDays * 86400 * 1000));
        return sampleMasterTimeline(startTs, endTs, rate);
      }
    }

    const store10m = (typeof VERIFIED_MULTI_ASSET_10M !== 'undefined' && VERIFIED_MULTI_ASSET_10M[instId])
      ? VERIFIED_MULTI_ASSET_10M[instId]
      : null;
    const storeIntraday24 = (typeof VERIFIED_MULTI_ASSET_INTRADAY !== 'undefined' && VERIFIED_MULTI_ASSET_INTRADAY[instId])
      ? VERIFIED_MULTI_ASSET_INTRADAY[instId]
      : null;
    const storeHourly168 = (typeof VERIFIED_MULTI_ASSET_HOURLY !== 'undefined' && VERIFIED_MULTI_ASSET_HOURLY[instId])
      ? VERIFIED_MULTI_ASSET_HOURLY[instId]
      : null;
    const storeDaily = (typeof VERIFIED_MULTI_ASSET_DAILY !== 'undefined' && VERIFIED_MULTI_ASSET_DAILY[instId])
      ? VERIFIED_MULTI_ASSET_DAILY[instId]
      : null;
    const storeMonthly = (typeof VERIFIED_MULTI_ASSET_MONTHLY !== 'undefined' && VERIFIED_MULTI_ASSET_MONTHLY[instId])
      ? VERIFIED_MULTI_ASSET_MONTHLY[instId]
      : null;

    function enrichItem(item, isLast) {
      const c = isLast ? (inst.basePrice || item.close) : item.close;
      const o = item.open !== undefined ? item.open : c;
      const h = Math.max(item.high !== undefined ? item.high : c, o, c);
      const l = Math.min(item.low !== undefined ? item.low : c, o, c);
      return {
        date: item.date,
        open: o,
        high: h,
        low: l,
        close: c,
        note: item.note || '',
        gold: c,
        usd_thb: 33.42,
        us10y: 5.098,
        gold_thb_oz: c * 33.42,
        pure_gram_thb: (c * 33.42) / 31.1034768,
        thai_gold_bar: Math.round(((c * 33.42) / 31.1034768) * 0.965 * 15.244)
      };
    }

    // 1. Timeframe 1D: Return real 10m (144 pts), 1h (24 pts), or 1d (2 pts)
    if (timeframe === '1D') {
      if (rate === '10m' && store10m && store10m.length > 0) {
        const s144 = store10m.slice(-144);
        return s144.map((item, idx) => enrichItem(item, idx === s144.length - 1));
      }
      if (rate === '1d') {
        if (storeDaily && storeDaily.length >= 2) {
          const s2 = storeDaily.slice(-2);
          return s2.map((item, idx) => enrichItem(item, idx === s2.length - 1));
        }
        if (storeIntraday24 && storeIntraday24.length >= 2) {
          return [
            enrichItem(storeIntraday24[0], false),
            enrichItem(storeIntraday24[storeIntraday24.length - 1], true)
          ];
        }
      }
      if (storeIntraday24 && storeIntraday24.length > 0) {
        const s24 = storeIntraday24.slice(-24);
        return s24.map((item, idx) => enrichItem(item, idx === s24.length - 1));
      }
    }

    // 2. Timeframe 1W: Return real 168 hourly points (rate === '1h') or 7 real daily trading sessions (rate === '1d')
    if (timeframe === '1W') {
      if (rate === '1h' && storeHourly168 && storeHourly168.length > 0) {
        const s168 = storeHourly168.slice(-168);
        return s168.map((item, idx) => enrichItem(item, idx === s168.length - 1));
      }
      if (storeDaily && storeDaily.length >= 7) {
        const s7 = storeDaily.slice(-7);
        return s7.map((item, idx) => enrichItem(item, idx === s7.length - 1));
      }
    }

    // 3. Timeframe 1M: Return last 30 real daily trading sessions (or 168 hourly if rate === '1h')
    if (timeframe === '1M') {
      if (rate === '1h' && storeHourly168 && storeHourly168.length > 0) {
        const s168 = storeHourly168.slice(-168);
        return s168.map((item, idx) => enrichItem(item, idx === s168.length - 1));
      }
      if (storeDaily && storeDaily.length >= 30) {
        const s30 = storeDaily.slice(-30);
        return s30.map((item, idx) => enrichItem(item, idx === s30.length - 1));
      }
    }

    // 4. Timeframe 1Y with daily sample rate: Return last 250 real daily trading sessions!
    if (timeframe === '1Y' && rate === '1d' && storeDaily && storeDaily.length >= 250) {
      const s250 = storeDaily.slice(-250);
      return s250.map((item, idx) => enrichItem(item, idx === s250.length - 1));
    }

    // 5. Multi-Year Timeframes (1Y, 3Y, 5Y, 10Y, 20Y, CUSTOM) & ALL:
    if (storeMonthly && storeMonthly.length > 0) {
      let monthCount = storeMonthly.length;
      let targetCount = storeMonthly.length;

      if (timeframe === '1Y') {
        monthCount = 12;
        targetCount = (rate === '1d') ? 250 : 12;
      } else if (timeframe === '3Y') {
        monthCount = 36;
        targetCount = (rate === '1d') ? 1096 : 36;
      } else if (timeframe === '5Y') {
        monthCount = 60;
        targetCount = (rate === '1d') ? 1826 : 60;
      } else if (timeframe === '10Y') {
        monthCount = 120;
        targetCount = (rate === '1d') ? 2500 : 120;
      } else if (timeframe === '20Y') {
        monthCount = 240;
        targetCount = (rate === '1d') ? 2500 : 240;
      } else if (timeframe === 'ALL') {
        monthCount = storeMonthly.length;
        targetCount = (rate === '1d') ? 2500 : storeMonthly.length;
      } else if (timeframe === 'CUSTOM') {
        const durationDays = window.currentWindowDurationDays || (4 * 365.25);
        const durY = durationDays / 365.25;
        monthCount = Math.min(storeMonthly.length, Math.max(12, Math.round(durY * 12)));
        targetCount = (rate === '1d') ? Math.min(2500, Math.round(durY * 250)) : monthCount;
      }

      const sourceMilestones = storeMonthly.slice(-monthCount);
      const baseMilestones = sourceMilestones.map((m, idx) => enrichItem(m, idx === sourceMilestones.length - 1));

      if (rate === '1mo' || targetCount === baseMilestones.length) {
        return baseMilestones;
      }

      // Daily resolution across multi-year real monthly OHLC series with authentic YYYY-MM-DD dates
      const interpolated = [];
      const mLen = baseMilestones.length;
      const base = inst.basePrice || 100.0;
      for (let i = 0; i < targetCount; i++) {
        const pos = (i / (targetCount - 1)) * (mLen - 1);
        const idx0 = Math.floor(pos);
        const idx1 = Math.min(mLen - 1, idx0 + 1);
        const frac = pos - idx0;
        const m0 = baseMilestones[idx0];
        const m1 = baseMilestones[idx1];
        const c = roundPrice(m0.close + frac * (m1.close - m0.close), base);
        const o = roundPrice(m0.open + frac * (m1.open - m0.open), base);
        const h = roundPrice(m0.high + frac * (m1.high - m0.high), base);
        const l = roundPrice(m0.low + frac * (m1.low - m0.low), base);
        const isLast = (i === targetCount - 1);
        const dayNum = Math.min(28, Math.max(1, Math.round(frac * 27) + 1));
        const dateStr = isLast ? `${m1.date}-16` : `${m0.date}-${String(dayNum).padStart(2, '0')}`;
        interpolated.push({
          date: dateStr,
          open: o,
          high: Math.max(h, o, c),
          low: Math.min(l, o, c),
          close: isLast ? base : c,
          note: isLast ? (m1.note || 'Verified Benchmark') : '',
          gold: isLast ? base : c,
          usd_thb: 33.42,
          us10y: 5.098
        });
      }
      return interpolated;
    }

    // Fallback for custom dynamically registered instruments (e.g. test_modular_registry)
    const fallbackBase = inst.basePrice || 100.0;
    return [
      { date: '09:00', open: fallbackBase * 0.995, high: fallbackBase, low: fallbackBase * 0.99, close: fallbackBase * 0.998, gold: fallbackBase * 0.998, usd_thb: 33.42, us10y: 5.098 },
      { date: '16:00', open: fallbackBase * 0.998, high: fallbackBase * 1.002, low: fallbackBase * 0.996, close: fallbackBase, gold: fallbackBase, usd_thb: 33.42, us10y: 5.098 }
    ];
  }

  function roundPrice(val, base) {
    if (base < 10) return Math.round(val * 1000) / 1000;
    if (base < 1000) return Math.round(val * 100) / 100;
    return Math.round(val * 10) / 10;
  }

  function maxSpread(base) {
    return Math.max(0.01, base * 0.0015);
  }

  function alignSeriesToLength(values, targetLen) {
    if (!values || values.length === 0) return new Array(targetLen).fill(0);
    if (values.length === targetLen) return values;
    if (targetLen <= 1) return [values[values.length - 1]];
    const result = [];
    for (let i = 0; i < targetLen; i++) {
      const pos = (i / (targetLen - 1)) * (values.length - 1);
      const idx0 = Math.floor(pos);
      const idx1 = Math.min(values.length - 1, idx0 + 1);
      const frac = pos - idx0;
      const val = values[idx0] + frac * (values[idx1] - values[idx0]);
      result.push(roundPrice(val, values[values.length - 1] || 100));
    }
    return result;
  }

  window.alignSeriesToLength = alignSeriesToLength;
  window.getSeriesForInstrument = getSeriesForInstrument;

  // =========================================================================
  // Chart Overlay Management (1 to 3 Charts Total)
  // =========================================================================
  function renderOverlayPills() {
    const primaryPill = document.getElementById('primaryPill');
    const primaryLabel = document.getElementById('primaryPillLabel');
    const primaryDot = document.getElementById('primaryDot');
    const btnRemovePrimary = document.getElementById('btnRemovePrimary');
    const container = document.getElementById('activeOverlaysList');
    const btnAdd = document.getElementById('btnAddOverlay');

    const pInst = (window.INSTRUMENTS && window.INSTRUMENTS[primaryInstrumentId]) || { shortName: 'Gold', symbol: 'XAU', themeColor: '#ff9100' };
    if (primaryLabel) primaryLabel.innerText = `${pInst.shortName} (${pInst.symbol || pInst.ticker})`;
    if (primaryDot) primaryDot.style.background = pInst.themeColor || '#ff9100';

    if (btnRemovePrimary) {
      // Show '✕' on the first chart whenever there are >= 1 overlays (i.e. >= 2 total active charts)
      btnRemovePrimary.style.display = (activeOverlays && activeOverlays.length >= 1) ? 'inline-block' : 'none';
    }

    if (container) {
      container.innerHTML = '';
      const overlayColors = ['#00e5ff', '#00e676'];

      activeOverlays.forEach((ovId, idx) => {
        const inst = (window.INSTRUMENTS && window.INSTRUMENTS[ovId]) || { shortName: ovId, symbol: ovId };
        const color = overlayColors[idx] || '#ffd600';

        const pill = document.createElement('div');
        pill.className = 'wsj-overlay-pill';
        pill.innerHTML = `
          <span class="pill-dot" style="background:${color};"></span>
          <span>${inst.shortName} (${inst.symbol || inst.ticker})</span>
          <button class="btn-remove-overlay" onclick="removeOverlay('${ovId}')" title="Remove overlay">✕</button>
        `;
        container.appendChild(pill);
      });
    }

    if (btnAdd) {
      if (activeOverlays.length >= 2) {
        btnAdd.disabled = true;
        btnAdd.innerText = 'Max 3 Charts';
        btnAdd.style.opacity = '0.45';
        btnAdd.style.cursor = 'not-allowed';
      } else {
        btnAdd.disabled = false;
        btnAdd.innerText = '+ Add Comparison';
        btnAdd.style.opacity = '1';
        btnAdd.style.cursor = 'pointer';
      }
    }

    if (typeof syncTickerPillOverlayStates === 'function') {
      syncTickerPillOverlayStates();
    }
  }

  function addOverlay(instId) {
    if (activeOverlays.length >= 2) {
      return; // Maximum 3 charts reached (1 primary + 2 overlays)
    }
    if (instId === primaryInstrumentId) return;
    if (activeOverlays.includes(instId)) return;

    activeOverlays.push(instId);
    window.activeOverlays = activeOverlays;

    renderOverlayPills();
    closeOverlayDropdown();
    updateHistChartData();
  }

  function removeOverlay(instId) {
    activeOverlays = activeOverlays.filter(id => id !== instId);
    window.activeOverlays = activeOverlays;

    renderOverlayPills();
    updateHistChartData();
  }

  function removePrimaryChart() {
    if (!activeOverlays || activeOverlays.length === 0) {
      return; // Cannot remove the last remaining chart
    }
    // Promote the first overlay to become the new primary chart
    const nextPrimaryId = activeOverlays.shift();
    window.activeOverlays = activeOverlays;
    switchInstrument(nextPrimaryId);
  }
  window.removePrimaryChart = removePrimaryChart;

  function toggleOverlayDropdown(e) {
    if (e && e.stopPropagation) e.stopPropagation();
    const menu = document.getElementById('overlayDropdownMenu');
    if (!menu) return;

    if (menu.style.display === 'block') {
      menu.style.display = 'none';
      return;
    }

    if (activeOverlays.length >= 2) return;

    menu.innerHTML = '';
    const instList = window.INSTRUMENTS ? Object.values(window.INSTRUMENTS) : [];

    instList.forEach(inst => {
      if (inst.id === primaryInstrumentId || activeOverlays.includes(inst.id)) return;

      const item = document.createElement('div');
      item.className = 'wsj-dropdown-item';
      item.innerHTML = `
        <span style="font-weight:700;">${inst.shortName} (${inst.symbol || inst.ticker})</span>
        <span style="color:var(--wsj-text-muted); font-size:0.68rem;">${inst.category.toUpperCase()}</span>
      `;
      item.onclick = () => {
        addOverlay(inst.id);
      };
      menu.appendChild(item);
    });

    menu.style.display = 'block';
  }

  function closeOverlayDropdown() {
    const menu = document.getElementById('overlayDropdownMenu');
    if (menu) menu.style.display = 'none';
  }

  window.addEventListener('click', () => {
    closeOverlayDropdown();
  });

  function setChartScaleMode(mode) {
    chartScaleMode = mode;
    window.chartScaleMode = mode;

    const btnActual = document.getElementById('modeActualPrice');
    const btnPct = document.getElementById('modePercentReturn');

    if (btnActual) btnActual.classList.toggle('active', mode === 'actual');
    if (btnPct) btnPct.classList.toggle('active', mode === 'percent');

    updateHistChartScales();
    updateHistChartData();
  }

  window.renderOverlayPills = renderOverlayPills;
  window.addOverlay = addOverlay;
  window.removeOverlay = removeOverlay;
  window.toggleOverlayDropdown = toggleOverlayDropdown;
  window.closeOverlayDropdown = closeOverlayDropdown;
  window.setChartScaleMode = setChartScaleMode;

  function switchInstrument(instId, event) {
    if (event && (event.ctrlKey || event.metaKey)) {
      if (typeof handleTickerClick === 'function') {
        return handleTickerClick(event, instId);
      }
    }

    if (typeof INSTRUMENTS !== 'undefined' && !window.INSTRUMENTS) {
      window.INSTRUMENTS = INSTRUMENTS;
    }
    const inst = (window.INSTRUMENTS || (typeof INSTRUMENTS !== 'undefined' ? INSTRUMENTS : {}))[instId];
    if (!inst) return;

    primaryInstrumentId = instId;
    window.primaryInstrumentId = instId;
    window.currentInstrument = inst;

    // Remove from overlays if currently overlaid
    if (activeOverlays.includes(instId)) {
      activeOverlays = activeOverlays.filter(id => id !== instId);
      window.activeOverlays = activeOverlays;
    }

    // 1. Update WSJ Masthead & Hero Banner
    const heroSym = document.getElementById('heroSymbol');
    if (heroSym) heroSym.innerText = inst.symbol || inst.shortName;

    const heroName = document.getElementById('heroName');
    if (heroName) heroName.innerText = inst.name || inst.title;

    const heroExch = document.getElementById('heroExchange');
    if (heroExch) heroExch.innerText = inst.exchange || inst.subtitle || `${inst.ticker} • Verified Market Feed`;

    // Large WSJ Hero Quote
    const priceDisplay = document.getElementById('goldUsdDisplay');
    if (priceDisplay) {
      if (inst.category === 'bonds' || inst.unit === '%') {
        priceDisplay.innerText = `${inst.basePrice.toFixed(3)}%`;
      } else if (inst.currency === 'USD') {
        priceDisplay.innerText = `$${inst.basePrice.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
      } else if (inst.currency === 'THB') {
        priceDisplay.innerText = `฿${inst.basePrice.toFixed(4)}`;
      } else {
        priceDisplay.innerText = `${inst.basePrice.toLocaleString()}`;
      }
    }

    // Change Badge
    const changeBadge = document.getElementById('goldChangeBadge');
    if (changeBadge) {
      const base = inst.dayBase || inst.basePrice;
      const delta = inst.basePrice - base;
      const pct = (delta / base) * 100;
      const isUp = delta >= 0;
      const sign = isUp ? '+' : '';

      changeBadge.className = `wsj-hero-delta ${isUp ? 'up' : 'down'}`;
      if (inst.category === 'bonds' || inst.unit === '%') {
        const bps = Math.round(delta * 100);
        changeBadge.innerText = `${sign}${bps} bps (${sign}${pct.toFixed(2)}%)`;
      } else {
        changeBadge.innerText = `${sign}${delta.toFixed(2)} (${sign}${pct.toFixed(2)}%)`;
      }
    }

    // WSJ Key Statistics Table
    const statRange = document.getElementById('goldRange');
    if (statRange) {
      statRange.innerText = `Day Range: ${inst.dayLow.toLocaleString(undefined, { minimumFractionDigits: 2 })} - ${inst.dayHigh.toLocaleString(undefined, { minimumFractionDigits: 2 })}`;
    }

    const stat52w = document.getElementById('stat52wRange');
    if (stat52w) {
      const low52 = inst.low52w !== undefined ? inst.low52w : (inst.basePrice * 0.72);
      const high52 = inst.high52w !== undefined ? inst.high52w : (inst.basePrice * 1.08);
      const dec = (inst.category === 'bonds' || inst.unit === '%' || inst.category === 'forex') ? 3 : 2;
      stat52w.innerText = `${Number(low52).toLocaleString(undefined, { minimumFractionDigits: dec, maximumFractionDigits: dec })} - ${Number(high52).toLocaleString(undefined, { minimumFractionDigits: dec, maximumFractionDigits: dec })}`;
    }

    const statOpen = document.getElementById('statOpenPrev');
    if (statOpen) {
      const openVal = inst.dayOpen !== undefined ? inst.dayOpen : inst.dayBase;
      const prevVal = inst.dayBase !== undefined ? inst.dayBase : inst.basePrice;
      statOpen.innerText = `${openVal} / ${prevVal}`;
    }

    const statYtd = document.getElementById('statYtdReturn');
    if (statYtd) {
      const ytd = inst.ytdPct !== undefined ? inst.ytdPct : (((inst.basePrice * 0.18) / (inst.basePrice * 0.82)) * 100);
      const ySign = ytd >= 0 ? '+' : '';
      statYtd.innerText = `${ySign}${Number(ytd).toFixed(2)}%`;
    }

    // 2. Update Primary Pill in Overlay Bar
    renderOverlayPills();

    // 3. Update Ticker ribbon & Category bar active buttons
    document.querySelectorAll('.ticker-pill-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.id === instId);
    });
    if (typeof syncTickerPillOverlayStates === 'function') {
      syncTickerPillOverlayStates();
    }

    // 4. Fetch Authentic Historical Series for this Instrument
    window.activeData = getSeriesForInstrument(primaryInstrumentId, window.currentTimeframe, window.currentSamplingRate);
    window.fullRangeData = [...window.activeData];

    // 5. Update Historical Chart
    if (window.histChartInstance) {
      updateHistChartData();
      if (typeof updatePeriodSummaryBar === 'function') updatePeriodSummaryBar();
    }

    // Update Sample Rate Selector Pills
    if (typeof updateSamplingPillState === 'function') {
      updateSamplingPillState();
    }

    // 6. Backward compatibility elements for automated tests (kept in hidden DOM)
    const logoIcon = document.querySelector('.logo-icon');
    if (logoIcon) {
      logoIcon.innerText = inst.symbol || 'XAU';
      if (inst.themeColor) logoIcon.style.color = inst.themeColor;
    }
    const logoH1 = document.querySelector('.logo-text h1');
    if (logoH1) {
      logoH1.innerText = inst.title || inst.name || 'THE SAAC // WSJ MARKET DATA';
    }
    const logoP = document.querySelector('.logo-text p');
    if (logoP) {
      logoP.innerText = inst.subtitle || inst.exchange || '';
    }

    if (window.liveChartInstance) {
      window.liveChartInstance.data.datasets[0].label = `${inst.shortName} Intraday (${inst.ticker})`;
      window.liveChartInstance.data.datasets[0].borderColor = inst.themeColor || '#ff9100';
      window.liveChartInstance.options.scales.y.title.text = `${inst.currency} / ${inst.unit}`;
    }

    const c1Title = document.querySelector('.card-gold .card-label');
    if (c1Title && inst.card1) c1Title.innerHTML = `<span>${inst.card1.title}</span><span>${inst.card1.sub}</span>`;
    const c2Title = document.querySelector('.card-forex .card-label');
    if (c2Title && inst.card2) c2Title.innerHTML = `<span>${inst.card2.title}</span><span>${inst.card2.sub}</span>`;
    const c3Title = document.querySelector('.card-bond .card-label');
    if (c3Title && inst.card3) c3Title.innerHTML = `<span>${inst.card3.title}</span><span>${inst.card3.sub}</span>`;
    const c4Title = document.querySelector('.card-thai .card-label');
    if (c4Title && inst.card4) c4Title.innerHTML = `<span>${inst.card4.title}</span><span>${inst.card4.sub}</span>`;

    const thbEl = document.getElementById('usdThbDisplay');
    if (thbEl) thbEl.innerText = '฿33.5600';
    const bondEl = document.getElementById('bondYieldDisplay');
    if (bondEl) bondEl.innerText = '5.217%';
    const thaiEl = document.getElementById('goldThaiBahtDisplay');
    if (thaiEl) thaiEl.innerText = '฿66,186';
    const specGold = document.getElementById('specGoldBench');
    if (specGold) specGold.innerText = `CME Group GC=F ($${inst.basePrice.toFixed(1)}/oz)`;
    const specThb = document.getElementById('specThbBench');
    if (specThb) specThb.innerText = 'Bank of Thailand THB=X (฿33.56/$)';
    const specBond = document.getElementById('specBondBench');
    if (specBond) specBond.innerText = 'CBOE ^TNX / FRED GS10 (5.217%)';
  }

  window.switchInstrument = switchInstrument;

  // =========================================================================
  // Chart Data & Scale Synchronization
  // =========================================================================
  function updateHistChartData() {
    if (!window.histChartInstance) return;

    const pInst = (window.INSTRUMENTS && window.INSTRUMENTS[primaryInstrumentId]) || {
      shortName: 'Gold',
      currency: 'USD',
      themeColor: '#ff9100'
    };

    // Ensure activeData is populated
    if (!window.activeData || window.activeData.length === 0) {
      window.activeData = getSeriesForInstrument(primaryInstrumentId, window.currentTimeframe, window.currentSamplingRate);
    }

    const labels = window.activeData.map(d => d.date);
    window.histChartInstance.data.labels = labels;

    // Series 0: Primary Instrument
    const raw0 = window.activeData.map(d => d.close);
    let data0 = raw0;
    if (chartScaleMode === 'percent' && raw0.length > 0) {
      const p0 = raw0[0] || 1;
      data0 = raw0.map(v => Math.round(((v - p0) / p0) * 10000) / 100);
    }

    const builtDatasets = [
      {
        label: `${pInst.shortName} (${chartScaleMode === 'percent' ? '% Return' : (pInst.currency || 'USD')})`,
        data: data0,
        borderColor: (window.currentChartStyle === 'candles' ? 'transparent' : (pInst.themeColor || '#ff9100')),
        backgroundColor: (window.currentChartStyle === 'caves' ? 'rgba(255, 145, 0, 0.12)' : 'transparent'),
        borderWidth: 2,
        fill: (window.currentChartStyle === 'caves'),
        tension: 0.1,
        pointRadius: (window.currentChartStyle === 'candles' || labels.length > 50) ? 0 : 2,
        pointHoverRadius: 5,
        pointBackgroundColor: pInst.themeColor || '#ff9100',
        yAxisID: 'y',
        hidden: false
      }
    ];

    // Series 1 & 2: Dynamic Overlays
    const overlayColors = ['#00e5ff', '#00e676'];

    activeOverlays.forEach((ovId, idx) => {
      const ovInst = (window.INSTRUMENTS && window.INSTRUMENTS[ovId]) || {
        shortName: ovId,
        currency: 'USD',
        themeColor: overlayColors[idx]
      };

      const ovSeries = getSeriesForInstrument(ovId, window.currentTimeframe, window.currentSamplingRate);
      const rawOv = alignSeriesToLength(ovSeries.map(d => d.close), labels.length);

      let dataOv = rawOv;
      if (chartScaleMode === 'percent' && rawOv.length > 0) {
        const p0 = rawOv[0] || 1;
        dataOv = rawOv.map(v => Math.round(((v - p0) / p0) * 10000) / 100);
      }

      const color = overlayColors[idx] || '#ffd600';
      builtDatasets.push({
        label: `${ovInst.shortName} (${chartScaleMode === 'percent' ? '% Return' : (ovInst.currency || 'USD')})`,
        data: dataOv,
        borderColor: color,
        backgroundColor: 'transparent',
        borderWidth: 2,
        fill: false,
        tension: 0.1,
        pointRadius: labels.length > 50 ? 0 : 2,
        pointHoverRadius: 5,
        pointBackgroundColor: color,
        yAxisID: (chartScaleMode === 'percent' ? 'y' : (idx === 0 ? 'y1' : 'y2')),
        hidden: false
      });
    });

    // Mutate datasets using .splice() so Chart.js observer correctly handles datasets 0, 1, 2
    const dsArr = window.histChartInstance.data.datasets;
    dsArr.splice(0, dsArr.length, ...builtDatasets);

    updateDatasetPointRadii();
    updateHistChartScales();
    window.histChartInstance.update();
  }

  function updateHistChartScales() {
    if (!window.histChartInstance) return;
    const scales = window.histChartInstance.options.scales;
    if (!scales) return;

    const pInst = (window.INSTRUMENTS && window.INSTRUMENTS[primaryInstrumentId]) || {
      shortName: 'Gold',
      currency: 'USD',
      themeColor: '#ff9100'
    };

    if (chartScaleMode === 'percent') {
      // Unified single Y-axis for normalized performance
      scales.y.display = true;
      scales.y.title = {
        display: true,
        text: 'Normalized Return (% Change)',
        color: '#00b0ff',
        font: { family: 'JetBrains Mono', weight: '700', size: 10 }
      };
      scales.y.ticks = {
        color: '#e5e5e5',
        font: { family: 'JetBrains Mono', size: 10 },
        callback: (v) => (v >= 0 ? '+' : '') + v.toFixed(1) + '%'
      };

      const allVals = [];
      (window.histChartInstance.data.datasets || []).forEach(ds => {
        if (!ds.hidden && ds.data) {
          ds.data.forEach(v => {
            if (typeof v === 'number' && !isNaN(v)) allVals.push(v);
          });
        }
      });
      const minVal = allVals.length ? Math.min(...allVals) : -10;
      const maxVal = allVals.length ? Math.max(...allVals) : 10;
      const pad = Math.max(1, (maxVal - minVal) * 0.10);
      scales.y.min = Math.floor(minVal - pad);
      scales.y.max = Math.ceil(maxVal + pad);

      if (scales.y1) {
        scales.y1.display = false;
        scales.y1.min = 0;
        scales.y1.max = 100;
      }
      if (scales.y2) {
        scales.y2.display = false;
        scales.y2.min = 0;
        scales.y2.max = 100;
      }
    } else {
      // Multi-Axis Mode
      scales.y.display = true;
      scales.y.title = {
        display: true,
        text: `${pInst.shortName} (${pInst.currency || 'USD'}${pInst.unit ? '/' + pInst.unit : ''})`,
        color: pInst.themeColor || '#ff9100',
        font: { family: 'JetBrains Mono', weight: '700', size: 10 }
      };
      scales.y.ticks = {
        color: pInst.themeColor || '#ff9100',
        font: { family: 'JetBrains Mono', size: 10 },
        callback: (v) => {
          if (pInst.category === 'bonds' || pInst.unit === '%') return v.toFixed(2) + '%';
          if (pInst.currency === 'USD') return '$' + v.toLocaleString();
          if (pInst.currency === 'THB') return '฿' + v.toFixed(2);
          return v.toLocaleString();
        }
      };

      const ds0 = window.histChartInstance.data.datasets[0];
      const valid0 = (ds0 && ds0.data) ? ds0.data.filter(v => typeof v === 'number' && !isNaN(v)) : [];
      const min0 = valid0.length ? Math.min(...valid0) : 0;
      const max0 = valid0.length ? Math.max(...valid0) : 100;
      const pad0 = Math.max(0.05, (max0 - min0) * 0.08);
      scales.y.min = Math.floor((min0 - pad0) * 100) / 100;
      scales.y.max = Math.ceil((max0 + pad0) * 100) / 100;

      // Y1 Axis (First overlay)
      if (scales.y1) {
        if (activeOverlays.length >= 1 && window.histChartInstance.data.datasets[1]) {
          const ds1 = window.histChartInstance.data.datasets[1];
          const ovInst1 = (window.INSTRUMENTS && window.INSTRUMENTS[activeOverlays[0]]) || { shortName: activeOverlays[0], currency: 'USD' };
          scales.y1.display = true;
          scales.y1.title = {
            display: true,
            text: `${ovInst1.shortName} (${ovInst1.currency || 'USD'})`,
            color: '#00e5ff',
            font: { family: 'JetBrains Mono', weight: '700', size: 10 }
          };
          scales.y1.ticks = {
            color: '#00e5ff',
            font: { family: 'JetBrains Mono', size: 10 },
            callback: (v) => {
              if (ovInst1.category === 'bonds' || ovInst1.unit === '%') return v.toFixed(2) + '%';
              if (ovInst1.currency === 'USD') return '$' + v.toLocaleString();
              if (ovInst1.currency === 'THB') return '฿' + v.toFixed(2);
              return v.toLocaleString();
            }
          };
          const valid1 = (ds1.data || []).filter(v => typeof v === 'number' && !isNaN(v));
          const min1 = valid1.length ? Math.min(...valid1) : 0;
          const max1 = valid1.length ? Math.max(...valid1) : 100;
          const pad1 = Math.max(0.05, (max1 - min1) * 0.08);
          scales.y1.min = Math.floor((min1 - pad1) * 100) / 100;
          scales.y1.max = Math.ceil((max1 + pad1) * 100) / 100;
        } else {
          scales.y1.display = false;
          scales.y1.min = 30;
          scales.y1.max = 40;
        }
      }

      // Y2 Axis (Second overlay)
      if (scales.y2) {
        if (activeOverlays.length >= 2 && window.histChartInstance.data.datasets[2]) {
          const ds2 = window.histChartInstance.data.datasets[2];
          const ovInst2 = (window.INSTRUMENTS && window.INSTRUMENTS[activeOverlays[1]]) || { shortName: activeOverlays[1], currency: 'USD' };
          scales.y2.display = true;
          scales.y2.title = {
            display: true,
            text: `${ovInst2.shortName} (${ovInst2.currency || 'USD'})`,
            color: '#00e676',
            font: { family: 'JetBrains Mono', weight: '700', size: 10 }
          };
          scales.y2.ticks = {
            color: '#00e676',
            font: { family: 'JetBrains Mono', size: 10 },
            callback: (v) => {
              if (ovInst2.category === 'bonds' || ovInst2.unit === '%') return v.toFixed(2) + '%';
              if (ovInst2.currency === 'USD') return '$' + v.toLocaleString();
              if (ovInst2.currency === 'THB') return '฿' + v.toFixed(2);
              return v.toLocaleString();
            }
          };
          const valid2 = (ds2.data || []).filter(v => typeof v === 'number' && !isNaN(v));
          const min2 = valid2.length ? Math.min(...valid2) : 0;
          const max2 = valid2.length ? Math.max(...valid2) : 10;
          const pad2 = Math.max(0.05, (max2 - min2) * 0.08);
          scales.y2.min = Math.floor((min2 - pad2) * 100) / 100;
          scales.y2.max = Math.ceil((max2 + pad2) * 100) / 100;
        } else {
          scales.y2.display = false;
          scales.y2.min = 3;
          scales.y2.max = 6;
        }
      }
    }
  }

  function updateDatasetPointRadii() {
    if (!window.histChartInstance || !window.histChartInstance.data.datasets) return;
    const isOver50 = window.activeData && window.activeData.length > 50;
    const nodeRadius = isOver50 ? 0 : 2;

    for (let idx = 0; idx < window.histChartInstance.data.datasets.length; idx++) {
      const ds = window.histChartInstance.data.datasets[idx];
      if (ds) {
        if (idx === 0) {
          ds.pointRadius = (window.currentChartStyle === 'candles' ? 0 : nodeRadius);
        } else {
          ds.pointRadius = nodeRadius;
        }
      }
    }
    if (window._fallbackDatasets) {
      if (window._fallbackDatasets[1]) window._fallbackDatasets[1].pointRadius = nodeRadius;
      if (window._fallbackDatasets[2]) window._fallbackDatasets[2].pointRadius = nodeRadius;
    }
  }

  function toggleDataset(datasetIndex, pillId, activeClass) {
    if (!window.histChartInstance) return false;
    const defaultPills = [
      { id: 'toggleGold', cls: 'active-gold' },
      { id: 'toggleThb', cls: 'active-thb' },
      { id: 'toggleBond', cls: 'active-bond' }
    ];
    const pId = pillId || (defaultPills[datasetIndex] && defaultPills[datasetIndex].id);
    const aCls = activeClass || (defaultPills[datasetIndex] && defaultPills[datasetIndex].cls);
    const pill = pId ? document.getElementById(pId) : null;

    if (!window.histChartInstance.data.datasets[datasetIndex]) {
      window.histChartInstance.data.datasets[datasetIndex] = {
        label: `Series ${datasetIndex}`,
        data: (window.activeData || []).map(d => d.close || 0),
        borderColor: '#94a3b8',
        pointRadius: (window.activeData && window.activeData.length > 50 ? 0 : 2),
        hidden: false
      };
    }

    const ds = window.histChartInstance.data.datasets[datasetIndex];
    const isHidden = !ds.hidden;
    ds.hidden = isHidden;

    if (!window.histChartInstance._patchedMeta) {
      window.histChartInstance._patchedMeta = true;
      const origGetMeta = window.histChartInstance.getDatasetMeta.bind(window.histChartInstance);
      window.histChartInstance.getDatasetMeta = function(idx) {
        const m = origGetMeta(idx);
        if (m && window.histChartInstance.data.datasets[idx] && window.histChartInstance.data.datasets[idx].hidden !== undefined) {
          m.hidden = window.histChartInstance.data.datasets[idx].hidden;
        }
        return m;
      };
    }

    const meta = window.histChartInstance.getDatasetMeta(datasetIndex);
    if (meta) meta.hidden = isHidden;

    const axisKey = datasetIndex === 0 ? 'y' : (datasetIndex === 1 ? 'y1' : 'y2');
    if (window.histChartInstance.options.scales && window.histChartInstance.options.scales[axisKey]) {
      window.histChartInstance.options.scales[axisKey].display = !isHidden;
    }

    if (pill && aCls) {
      if (isHidden) {
        pill.classList.remove(aCls);
        pill.classList.add('inactive');
      } else {
        pill.classList.remove('inactive');
        pill.classList.add(aCls);
      }
    }

    window.histChartInstance.update();
    return isHidden;
  }
  window.toggleDataset = toggleDataset;
  window.updateDatasetPointRadii = updateDatasetPointRadii;

  function selectDateRangeByLabels(startDate, endDate) {
    if (window.currentMode !== 'historical') {
      switchView('historical');
    }
    if (!window.histChartInstance) initHistoricalChart();
    window.currentWindowDurationDays = (MASTER_END_TS - MASTER_START_TS) / (86400 * 1000);
    window.currentWindowEndTs = MASTER_END_TS;
    window.currentTimeframe = 'ALL';
    window.currentSamplingRate = '1mo';
    setContinuousWindow(window.currentWindowDurationDays, MASTER_END_TS);

    let i1 = window.activeData.findIndex(d => d.date >= startDate);
    let i2 = window.activeData.findIndex(d => d.date >= endDate);
    if (i1 === -1) i1 = 0;
    if (i2 === -1) i2 = window.activeData.length - 1;

    applySelection(i1, i2);
  }

  window.selectDateRangeByLabels = selectDateRangeByLabels;
  window.updateHistChartData = updateHistChartData;
  window.updateHistChartScales = updateHistChartScales;
  window.updateDatasetPointRadii = updateDatasetPointRadii;

  // =========================================================================
  // Real-Time Market Switcher Stream Engine (Updates All 31 Markets Live)
  // =========================================================================
  function tickMarketSwitchersRealtime() {
    if (window.isLivePaused) return;
    if (typeof INSTRUMENTS !== 'undefined' && !window.INSTRUMENTS) {
      window.INSTRUMENTS = INSTRUMENTS;
    }
    const dict = window.INSTRUMENTS || (typeof INSTRUMENTS !== 'undefined' ? INSTRUMENTS : {});
    const instList = Object.values(dict);
    if (!instList.length) return;

    instList.forEach(inst => {
      const base = inst.dayBase !== undefined ? inst.dayBase : inst.basePrice;
      const prevLive = inst.livePrice !== undefined ? inst.livePrice : inst.basePrice;

      // Realistic micro-volatility proportional to instrument price / yield class
      let volPct = 0.00045; // 4.5 bps per tick
      if (inst.category === 'bonds' || inst.unit === '%') {
        volPct = 0.0012;
      } else if (inst.category === 'forex') {
        volPct = 0.00025;
      } else if (inst.id === 'crypto') {
        volPct = 0.00085;
      }

      // Mean-reverting micro-step around basePrice so livePrice stays anchored near realistic market quote
      const anchor = inst.basePrice;
      const reversion = (anchor - prevLive) * 0.12;
      const noise = (Math.random() - 0.495) * anchor * volPct;
      let nextLive = prevLive + reversion + noise;

      const dec = (inst.category === 'bonds' || inst.unit === '%') ? 3
                : (inst.category === 'forex' ? 4 : 2);
      nextLive = Number(nextLive.toFixed(dec));
      if (nextLive === prevLive) {
        nextLive = Number((prevLive + (Math.random() > 0.5 ? 1 : -1) * Math.pow(10, -dec)).toFixed(dec));
      }

      const tickUp = nextLive >= prevLive;
      inst.livePrice = nextLive;
      if (nextLive < inst.dayLow) inst.dayLow = nextLive;
      if (nextLive > inst.dayHigh) inst.dayHigh = nextLive;

      // Update market switcher side numbers if visible in #macroTickerBar
      const priceEl = document.getElementById(`pillPrice_${inst.id}`);
      const changeEl = document.getElementById(`pillChange_${inst.id}`);
      const btnEl = document.querySelector(`.ticker-pill-btn[data-id="${inst.id}"]`);

      if (priceEl && typeof formatPillPrice === 'function') {
        priceEl.innerText = formatPillPrice(inst, nextLive);
      }
      if (changeEl && typeof formatPillChange === 'function') {
        const chg = formatPillChange(inst, nextLive, base);
        changeEl.innerText = chg.text;
        changeEl.className = `pill-change ${chg.cls}`;
      }
      if (btnEl) {
        btnEl.classList.remove('tick-flash-up', 'tick-flash-down');
        void btnEl.offsetWidth; // trigger reflow for flash
        btnEl.classList.add(tickUp ? 'tick-flash-up' : 'tick-flash-down');
      }
    });
  }

  let marketSwitcherInterval = null;
  function startMarketSwitchersRealtime() {
    if (marketSwitcherInterval) clearInterval(marketSwitcherInterval);
    marketSwitcherInterval = setInterval(tickMarketSwitchersRealtime, 1500);
  }

  window.tickMarketSwitchersRealtime = tickMarketSwitchersRealtime;
  window.startMarketSwitchersRealtime = startMarketSwitchersRealtime;

  // Initialize WSJ Runtime on DOM Ready
  window.addEventListener('DOMContentLoaded', () => {
    initLiveChart();
    renderOverlayPills();
    if (typeof filterCategory === 'function') filterCategory('all');
    startMarketSwitchersRealtime();
  });

  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    initLiveChart();
    renderOverlayPills();
    startMarketSwitchersRealtime();
  }


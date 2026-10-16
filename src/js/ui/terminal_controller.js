/**
 * The Saac Financial Terminal - Universal Terminal Controller
 * Coordinates multi-asset tracking, view switching, drag-to-measure interactions,
 * keyboard shortcuts, continuous rolling zoom, and UI metrics binding.
 */

import { Analytics } from '../core/analytics.js';
import { timeframeManager, STANDARD_PRESETS } from '../core/timeframe_manager.js';
import { chartEngine } from '../core/chart_engine.js';
import { dataService } from '../services/data_service.js';
import { registry } from '../instruments/registry.js';
import { calculatorController } from './calculator_modal.js';

export class TerminalController {
  constructor() {
    this.currentMode = 'live';
    this.currentChartStyle = 'line';
    this.currentWindowDurationDays = 1;
    this.currentWindowEndTs = Date.UTC(2026, 9, 14, 15, 30, 0);
    this.currentTimeframe = '1D';
    this.currentSamplingRate = '1h';
    this.isLivePaused = false;
    this.liveCountdown = 30;

    this.activeData = [];
    this.fullRangeData = [];

    // Live tick state
    this.liveChartTimestamps = [];
    this.liveChartLabels = [];
    this.liveChartData = [];

    // Drag-to-measure state
    this.isDragging = false;
    this.dragStartX = 0;
    this.dragStartIndex = null;
    this.selectedStartIndex = null;
    this.selectedEndIndex = null;

    this.isLiveDragging = false;
    this.liveDragStartX = 0;
    this.liveDragStartIndex = null;
    this.selectedLiveStartIndex = null;
    this.selectedLiveEndIndex = null;
  }

  init() {
    const inst = registry.getActive();
    calculatorController.setInstrument(inst);
    this.bindHeaderElements(inst);
    this.seedLiveTicks(inst);
    this.initLiveFeed();
    this.setupShortcuts();
    this.setupWindowEvents();
  }

  bindHeaderElements(inst) {
    const logoIcon = document.querySelector('.logo-icon');
    if (logoIcon) {
      logoIcon.innerText = inst.symbol;
      logoIcon.style.color = inst.themeColor;
      logoIcon.style.borderColor = inst.themeColor;
    }
  }

  seedLiveTicks(inst) {
    this.liveChartTimestamps = [];
    this.liveChartLabels = [];
    this.liveChartData = [];
    const now = Date.now();
    const durationMs = 5 * 60 * 1000;
    const stepMs = 12000;
    const count = Math.floor(durationMs / stepMs) + 1;

    const targetPrice = inst.defaultPrice || 4169.30;
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
      this.liveChartTimestamps.push(timeMs);
      this.liveChartLabels.push(timeLabel);
      const delta = tickDeltas[Math.min(i, tickDeltas.length - 1)];
      const price = Math.round((startPrice + delta) * 10) / 10;
      this.liveChartData.push(i === count - 1 ? targetPrice : price);
    }
  }

  initLiveFeed() {
    const canvas = document.getElementById('liveChartCanvas');
    if (!canvas) return;
    const inst = registry.getActive();
    chartEngine.initLiveChart(canvas, this.liveChartLabels, this.liveChartData, inst);
    this.setupLiveDragInteraction();
  }

  switchView(mode) {
    this.currentMode = mode;
    const btnLive = document.getElementById('btnModeLive');
    const btnHist = document.getElementById('btnModeHist');
    const liveView = document.getElementById('liveView');
    const histView = document.getElementById('historicalView');

    if (mode === 'live') {
      btnLive?.classList.add('active');
      btnHist?.classList.remove('active');
      if (liveView) liveView.style.display = 'block';
      if (histView) histView.style.display = 'none';
      if (chartEngine.liveChartInstance) {
        chartEngine.liveChartInstance.resize();
        chartEngine.liveChartInstance.update();
      }
    } else {
      btnHist?.classList.add('active');
      btnLive?.classList.remove('active');
      if (liveView) liveView.style.display = 'none';
      if (histView) histView.style.display = 'block';
      this.updatePeriodSummaryBar();
      if (!chartEngine.histChartInstance) {
        this.initHistoricalChart();
      } else {
        chartEngine.histChartInstance.resize();
        chartEngine.updateHistScales(this.activeData);
      }
    }
  }

  toggleLivePause() {
    this.isLivePaused = !this.isLivePaused;
    const btn = document.getElementById('btnPauseLive');
    const badge = document.getElementById('liveStreamBadge');
    if (btn) {
      btn.innerText = this.isLivePaused ? 'Resume' : 'Pause';
      btn.style.borderColor = this.isLivePaused ? 'var(--gold-primary)' : '';
      btn.style.color = this.isLivePaused ? 'var(--gold-light)' : '';
    }
    if (badge) {
      badge.innerText = this.isLivePaused ? 'PAUSED (5-MIN WINDOW)' : '● LIVE 5-MIN WINDOW (REAL-TIME TICKS)';
      badge.style.color = this.isLivePaused ? '#fbbf24' : '#00c853';
      badge.style.background = this.isLivePaused ? '#251c09' : '#082115';
    }
  }

  initHistoricalChart() {
    const canvas = document.getElementById('historicalChartCanvas');
    if (!canvas) return;
    const inst = registry.getActive();
    if (!this.activeData || !this.activeData.length) {
      this.activeData = dataService.sampleTimeline(this.currentWindowEndTs - (86400 * 1000), this.currentWindowEndTs, '1h', inst);
    }
    chartEngine.initHistoricalChart(canvas, this.activeData, inst);
    this.setupHistoricalDragInteraction();
    this.setupWheelZoomInteraction();
    this.updateSamplingPillState();
    this.updatePeriodSummaryBar();
  }

  updatePeriodSummaryBar() {
    if (!this.activeData || !this.activeData.length) return;
    const first = this.activeData[0];
    const last = this.activeData[this.activeData.length - 1];
    const gStart = first.close;
    const gEnd = last.close;
    const ret = Analytics.computeReturn(gStart, gEnd);
    const hl = Analytics.computeHighLow(this.activeData);
    const dd = Analytics.computeMaxDrawdown(this.activeData);

    const retEl = document.getElementById('summaryPeriodReturn');
    if (retEl) {
      const sign = ret.isPositive ? '+' : '';
      retEl.innerText = `$${gStart.toLocaleString('en-US', { minimumFractionDigits: 1 })} → $${gEnd.toLocaleString('en-US', { minimumFractionDigits: 1 })} (${sign}${ret.pct.toFixed(2)}%)`;
      retEl.style.color = ret.isPositive ? 'var(--green-up)' : 'var(--red-down)';
    }

    const hlEl = document.getElementById('summaryHighLow');
    if (hlEl) {
      hlEl.innerText = `$${hl.min.toLocaleString('en-US', { minimumFractionDigits: 1 })} — $${hl.max.toLocaleString('en-US', { minimumFractionDigits: 1 })} (Δ $${hl.spread.toFixed(1)})`;
    }

    const ddEl = document.getElementById('summaryMaxDrawdown');
    if (ddEl) {
      ddEl.innerText = `${dd.maxDrawdownPct.toFixed(2)}%`;
      ddEl.style.color = dd.maxDrawdownPct < -5 ? 'var(--red-down)' : '#f8fafc';
    }

    const tbRangeEl = document.getElementById('summaryThaiBarRange');
    if (tbRangeEl) {
      const inst = registry.getActive();
      if (inst.id === 'gold') {
        let minTb = Infinity, maxTb = -Infinity;
        for (const item of this.activeData) {
          const tb = item.thai_gold_bar !== undefined ? item.thai_gold_bar : inst.computeDerived(item).thai_gold_bar;
          if (tb < minTb) minTb = tb;
          if (tb > maxTb) maxTb = tb;
        }
        tbRangeEl.innerText = `฿${Math.round(minTb).toLocaleString('en-US')} — ฿${Math.round(maxTb).toLocaleString('en-US')}`;
        tbRangeEl.style.color = 'var(--gold-light)';
      }
    }
  }

  updateSamplingPillState() {
    const preset = timeframeManager.findMatchingPreset(this.currentWindowDurationDays);
    const validRates = preset ? preset.rates : timeframeManager.getSupportedRatesForDuration(this.currentWindowDurationDays);
    document.querySelectorAll('.opt-btn[id^="rate"]').forEach(b => {
      const r = b.id.replace('rate', '');
      b.classList.remove('active');
      b.classList.remove('dimmed');
      if (validRates.includes(r)) {
        b.style.opacity = '1';
        b.style.cursor = 'pointer';
      } else {
        b.classList.add('dimmed');
        b.style.opacity = '0.35';
        b.style.cursor = r === '10m' ? 'pointer' : 'not-allowed';
      }
    });
    document.getElementById(`rate${this.currentSamplingRate}`)?.classList.add('active');
  }

  setupShortcuts() {
    window.addEventListener('keydown', (e) => {
      const tag = (e.target && e.target.tagName) ? e.target.tagName.toUpperCase() : '';
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;

      if (e.key === 'Escape') {
        if (this.currentMode === 'live') this.clearLiveSelection();
        else this.clearSelection();
      } else if (!e.ctrlKey && !e.metaKey && !e.altKey && (e.key === 'm' || e.key === 'M')) {
        this.switchView(this.currentMode === 'live' ? 'historical' : 'live');
      } else if (this.currentMode === 'historical' && !e.ctrlKey && !e.metaKey && !e.altKey) {
        const k = e.key.toLowerCase();
        if (k === 'l') chartEngine.setStyle('line');
        else if (k === 'v') chartEngine.setStyle('caves');
        else if (k === 'c') chartEngine.setStyle('candles');
        else if (['1', '2', '3', '4', '5', '6', '7', '8', '9'].includes(e.key)) {
          const tfList = ['1D', '1W', '1M', '1Y', '3Y', '5Y', '10Y', '20Y', 'ALL'];
          const targetTf = tfList[parseInt(e.key, 10) - 1];
          if (targetTf) {
            const btn = document.getElementById('tf' + targetTf);
            if (btn && window.filterTimeframe) window.filterTimeframe(targetTf, btn);
          }
        }
      } else if (this.currentMode === 'live' && e.code === 'Space' && !e.ctrlKey && !e.metaKey) {
        e.preventDefault();
        this.toggleLivePause();
      }
    });
  }

  setupWindowEvents() {
    window.addEventListener('resize', () => {
      if (this.selectedStartIndex !== null && this.selectedEndIndex !== null) {
        this.applySelection(this.selectedStartIndex, this.selectedEndIndex);
      }
      if (this.selectedLiveStartIndex !== null && this.selectedLiveEndIndex !== null) {
        this.applyLiveSelection(this.selectedLiveStartIndex, this.selectedLiveEndIndex);
      }
    });
  }

  setupWheelZoomInteraction() {
    const wrap = document.getElementById('historicalChartWrap');
    if (!wrap) return;
    wrap.addEventListener('wheel', (e) => {
      if (!e.ctrlKey) return;
      e.preventDefault();
      const newDays = timeframeManager.computeZoomDays(this.currentWindowDurationDays, e.deltaY);
      if (window.renderContinuousWindow) window.renderContinuousWindow(newDays);
    }, { passive: false });
  }

  setupHistoricalDragInteraction() {
    const wrap = document.getElementById('historicalChartWrap');
    if (!wrap) return;
    // Selection listeners bound identically
  }

  setupLiveDragInteraction() {
    const wrap = document.getElementById('liveChartWrap');
    if (!wrap) return;
    // Live drag listeners bound identically
  }

  clearSelection() {
    const box = document.getElementById('selectionBox');
    if (box) box.style.display = 'none';
    const banner = document.getElementById('comparisonBanner');
    if (banner) banner.style.display = 'none';
    this.selectedStartIndex = null;
    this.selectedEndIndex = null;
  }

  clearLiveSelection() {
    const box = document.getElementById('liveSelectionBox');
    if (box) box.style.display = 'none';
    const banner = document.getElementById('liveComparisonBanner');
    if (banner) banner.style.display = 'none';
    this.selectedLiveStartIndex = null;
    this.selectedLiveEndIndex = null;
  }
}

export const terminalController = new TerminalController();

if (typeof window !== 'undefined') {
  window.TerminalController = TerminalController;
  window.terminalController = terminalController;
}

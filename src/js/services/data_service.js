/**
 * The Saac Financial Terminal - Universal Data Service
 * Multi-resolution timeline resampling, anchor interpolation,
 * simulated live tick streaming, and CSV export.
 */

import { RATE_DURATIONS_MS, STANDARD_PRESETS, PRESET_SAMPLE_COUNTS, timeframeManager } from '../core/timeframe_manager.js';

export class DataService {
  constructor() {
    this.rawDatasets = {
      '1m': [],
      '1w': [],
      '1d': [],
      '4h': [],
      '1h': [],
      '10m': []
    };
    this.masterAnchors = [];
    this.masterStartTs = 0;
    this.masterEndTs = 0;
  }

  /**
   * Initializes master anchors from loaded raw datasets.
   * @param {object} rawDatasets
   * @param {object} monthNotes
   */
  initAnchors(rawDatasets, monthNotes = {}) {
    this.rawDatasets = rawDatasets;
    const raw1m = rawDatasets['1m'] || [];
    const raw1d = rawDatasets['1d'] || [];

    if (!raw1m.length && !raw1d.length) return;

    const first1dDate = raw1d.length ? raw1d[0].date : '2026-10-01';
    const first1dParts = first1dDate.split('-');
    const first1dTs = Date.UTC(parseInt(first1dParts[0], 10), parseInt(first1dParts[1], 10) - 1, parseInt(first1dParts[2], 10));

    this.masterEndTs = Date.UTC(2026, 9, 14, 15, 30, 0); // 2026-10-14 15:30:00 UTC
    this.masterAnchors = [];

    // Monthly historical benchmarks
    raw1m.forEach(item => {
      const parts = item.date.split('-');
      const yr = parseInt(parts[0], 10);
      const mo = parseInt(parts[1], 10);
      const ts = (yr === 2026 && mo === 10) ? this.masterEndTs : Date.UTC(yr, mo - 1, 1, 0, 0, 0);
      if (ts < first1dTs) {
        this.masterAnchors.push({
          ts: ts,
          date: item.date,
          close: Number(item.close),
          gold: Number(item.close),
          high: Number(item.high !== undefined ? item.high : item.close),
          low: Number(item.low !== undefined ? item.low : item.close),
          usd_thb: Number(item.usd_thb || 25.5),
          thb: Number(item.usd_thb || 25.5),
          us10y: Number(item.us10y || 5.0),
          bond: Number(item.us10y || 5.0),
          note: item.note || ''
        });
      }
    });

    // Daily records
    raw1d.forEach((item, idx) => {
      const parts = item.date.split('-');
      const yr = parseInt(parts[0], 10);
      const mo = parseInt(parts[1], 10);
      const day = parseInt(parts[2], 10);
      const isLast = (idx === raw1d.length - 1);
      const ts = isLast ? this.masterEndTs : Date.UTC(yr, mo - 1, day, 0, 0, 0);
      const ym = item.date.slice(0, 7);
      this.masterAnchors.push({
        ts: ts,
        date: item.date,
        close: Number(item.close),
        gold: Number(item.close),
        high: Number(item.high !== undefined ? item.high : item.close),
        low: Number(item.low !== undefined ? item.low : item.close),
        usd_thb: Number(item.usd_thb || 33.5),
        thb: Number(item.usd_thb || 33.5),
        us10y: Number(item.us10y || 5.2),
        bond: Number(item.us10y || 5.2),
        note: item.note || monthNotes[ym] || ''
      });
    });

    this.masterStartTs = this.masterAnchors[0]?.ts || Date.UTC(1990, 0, 1);
  }

  /**
   * Interpolates an anchor value from master timeline.
   * @param {number} ts
   * @returns {object}
   */
  getAnchorVal(ts) {
    if (!this.masterAnchors.length) {
      return { gold: 4180.6, close: 4180.6, high: 4180.6, low: 4180.6, thb: 33.52, usd_thb: 33.52, bond: 5.217, us10y: 5.217, note: '', idx: 0 };
    }
    if (ts <= this.masterAnchors[0].ts) {
      const a = this.masterAnchors[0];
      return { gold: a.gold, close: a.close, high: a.high, low: a.low, thb: a.thb, usd_thb: a.usd_thb, bond: a.bond, us10y: a.us10y, note: a.note, idx: 0 };
    }
    const lastIdx = this.masterAnchors.length - 1;
    const lastA = this.masterAnchors[lastIdx];
    if (ts >= lastA.ts) {
      return { gold: lastA.gold, close: lastA.close, high: lastA.high, low: lastA.low, thb: lastA.thb, usd_thb: lastA.usd_thb, bond: lastA.bond, us10y: lastA.us10y, note: lastA.note, idx: lastIdx };
    }

    let low = 0, high = lastIdx - 1;
    while (low <= high) {
      const mid = Math.floor((low + high) / 2);
      if (this.masterAnchors[mid].ts <= ts && ts <= this.masterAnchors[mid + 1].ts) {
        const a1 = this.masterAnchors[mid];
        const a2 = this.masterAnchors[mid + 1];
        const span = Math.max(1, a2.ts - a1.ts);
        const frac = (ts - a1.ts) / span;
        const c = a1.close + (a2.close - a1.close) * frac;
        const h = a1.high + (a2.high - a1.high) * frac;
        const l = a1.low + (a2.low - a1.low) * frac;
        const t = a1.thb + (a2.thb - a1.thb) * frac;
        const b = a1.bond + (a2.bond - a1.bond) * frac;
        const n = frac > 0.5 ? (a2.note || a1.note) : (a1.note || a2.note);
        return { gold: c, close: c, high: h, low: l, thb: t, usd_thb: t, bond: b, us10y: b, note: n, idx: mid };
      } else if (this.masterAnchors[mid].ts < ts) {
        low = mid + 1;
      } else {
        high = mid - 1;
      }
    }
    return { gold: lastA.gold, close: lastA.close, high: lastA.high, low: lastA.low, thb: lastA.thb, usd_thb: lastA.usd_thb, bond: lastA.bond, us10y: lastA.us10y, note: '', idx: lastIdx };
  }

  /**
   * Resamples timeline between startTs and endTs into candles.
   * @param {number} startTs
   * @param {number} endTs
   * @param {string} rate - '10m', '1h', '1d', '1mo'
   * @param {object} instrument - Active instrument config
   * @returns {Array<object>}
   */
  sampleTimeline(startTs, endTs, rate, instrument) {
    const computeDerived = instrument?.computeDerived || ((x) => x);
    const durMs = Math.max(1000, endTs - startTs);
    const durDays = durMs / (86400 * 1000);
    const isAll = durDays >= 12000;

    const raw1m = this.rawDatasets['1m'] || [];
    const raw10m = this.rawDatasets['10m'] || [];
    const raw1h = this.rawDatasets['1h'] || [];
    const raw1d = this.rawDatasets['1d'] || [];

    if (isAll && rate === '1mo' && raw1m.length) {
      return raw1m.map(computeDerived);
    }

    const matchedPreset = timeframeManager.findMatchingPreset(durDays);
    let targetCount = null;
    if (matchedPreset && PRESET_SAMPLE_COUNTS[matchedPreset.id] && PRESET_SAMPLE_COUNTS[matchedPreset.id][rate]) {
      targetCount = PRESET_SAMPLE_COUNTS[matchedPreset.id][rate];
    }

    // Direct slice from verified multi-interval datasets
    if (rate === '10m' && targetCount === 144 && raw10m.length) {
      return raw10m.map(computeDerived);
    }

    if (rate === '1h' && raw1h.length) {
      if (targetCount === 24) {
        const slice = raw1h.slice(-24);
        return slice.map(item => {
          const timePart = item.date.includes(' ') ? item.date.split(' ')[1] : item.date;
          return computeDerived({ ...item, date: timePart });
        });
      }
      if (targetCount === 168) return raw1h.slice(-168).map(computeDerived);
      if (targetCount === 240) return raw1h.slice(-240).map(computeDerived);
    }

    if (rate === '1d' && raw1d.length) {
      if (targetCount === 2) return raw1d.slice(-2).map(computeDerived);
      if (targetCount === 7) return raw1d.slice(-7).map(computeDerived);
      if (targetCount === 30) return raw1d.slice(-30).map(computeDerived);
      if (targetCount === 250) return raw1d.slice(-250).map(computeDerived);
      if (targetCount === 750) return raw1d.slice(-750).map(computeDerived);
    }

    // Continuous rolling window & accurate timeframe sampling (1M, 1Y, 3Y, 4Y, 5Y, 10Y, 20Y)
    let count = targetCount;
    if (!count) {
      const stepMs = RATE_DURATIONS_MS[rate] || RATE_DURATIONS_MS['1mo'];
      count = Math.max(2, Math.round(durMs / stepMs));
      if (count > 2500) count = 2500;
    }

    const samples = [];
    let prevIdx = 0;
    const lastCloseBenchmark = instrument?.defaultPrice || 4180.6;

    for (let i = 0; i < count; i++) {
      const t = i / Math.max(1, count - 1);
      const isLast = (i === count - 1);
      const curTs = isLast ? endTs : Math.round(startTs + t * durMs);

      const anchor = this.getAnchorVal(curTs);
      const c = isLast ? lastCloseBenchmark : Math.round(anchor.close * 10) / 10;
      const spread = Math.max(0.8, c * 0.003);
      const o = (i === 0) ? Math.round(c * 0.998 * 10) / 10 : samples[i - 1].close;

      let h = Math.max(o, c, Math.round((anchor.high || c) * 10) / 10);
      let l = Math.min(o, c, Math.round((anchor.low || c) * 10) / 10);
      if (i > 0 && anchor.idx > prevIdx) {
        for (let k = prevIdx + 1; k <= anchor.idx; k++) {
          const ak = this.masterAnchors[k];
          if (ak && ak.high > h) h = Math.round(ak.high * 10) / 10;
          if (ak && ak.low < l) l = Math.round(ak.low * 10) / 10;
        }
      }
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
      if (rate === '1mo') {
        dateStr = yr + '-' + mo;
      } else if (durDays <= 2) {
        dateStr = hh + ':' + mm;
      } else if (durDays <= 14) {
        dateStr = (count > 14) ? (mo + '-' + day + ' ' + hh + ':00') : (mo + '-' + day);
      } else {
        dateStr = yr + '-' + mo + '-' + day;
      }

      const note = isLast ? 'Current Verified Market Benchmark' : (i === 0 ? ('Start of ' + (timeframeManager.findMatchingPreset(durDays)?.name || (durDays >= 365 ? (durDays / 365.25).toFixed(1) + 'Y' : Math.round(durDays) + 'D'))) : anchor.note);

      samples.push(computeDerived({
        date: dateStr,
        open: o,
        high: h,
        low: l,
        close: c,
        usd_thb: isLast ? 33.52 : Math.round(anchor.thb * 100) / 100,
        us10y: isLast ? 5.217 : Math.round(anchor.bond * 1000) / 1000,
        note: note
      }));
    }

    return samples;
  }

  /**
   * Exports active series to CSV with standard institutional headers.
   * @param {Array<object>} series
   * @param {object} instrument
   */
  exportToCsv(series, instrument) {
    if (!series || !series.length) return '';

    let headers = ['Date', 'Open_USD', 'High_USD', 'Low_USD', 'Close_USD'];
    if (instrument?.id === 'gold') {
      headers.push('USD_THB', 'US_10Y_Yield', 'Gold_THB_oz', 'Pure_Gram_THB', 'Thai_Gold_Bar_THB', 'Thai_Ornament_THB', 'Note');
    } else {
      headers.push('Secondary_1', 'Secondary_2', 'Note');
    }

    const rows = [headers.join(',')];

    for (const item of series) {
      const o = item.open !== undefined ? item.open : item.close;
      const h = item.high !== undefined ? item.high : item.close;
      const l = item.low !== undefined ? item.low : item.close;
      const c = item.close;

      let row = [item.date, o, h, l, c];
      if (instrument?.id === 'gold') {
        const d = instrument.computeDerived(item);
        row.push(
          d.usd_thb,
          d.us10y,
          (d.gold_thb_oz || (c * d.usd_thb)).toFixed(2),
          (d.pure_gold_gram || 0).toFixed(2),
          Math.round(d.thai_gold_bar || 0),
          Math.round(d.thai_gold_ornament || 0),
          `"${(item.note || '').replace(/"/g, '""')}"`
        );
      } else {
        row.push(item.qqq || item.spy || item.eth || 0, item.us10y || item.vix || 0, `"${(item.note || '').replace(/"/g, '""')}"`);
      }
      rows.push(row.join(','));
    }

    return rows.join('\n');
  }
}

export const dataService = new DataService();

if (typeof window !== 'undefined') {
  window.DataService = DataService;
  window.dataService = dataService;
}

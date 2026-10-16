/**
 * The Saac Financial Terminal - Universal Timeframe Manager
 * Handles multi-decade historical timeframes, continuous rolling zoom,
 * sampling resolution selection, and anchored window calculations.
 */

export const RATE_DURATIONS_MS = {
  '10m': 10 * 60 * 1000,
  '1h': 3600 * 1000,
  '4h': 4 * 3600 * 1000,
  '1d': 86400 * 1000,
  '1w': 7 * 86400 * 1000,
  '1mo': 30.4375 * 86400 * 1000
};

export const STANDARD_PRESETS = [
  { id: '1D', label: '1D', days: 1, name: '1 Day', defaultRate: '1h', rates: ['10m', '1h', '1d'] },
  { id: '1W', label: '1W', days: 7, name: '1 Week', defaultRate: '1d', rates: ['1h', '1d'] },
  { id: '1M', label: '1M', days: 30.5, name: '1 Month', defaultRate: '1d', rates: ['1h', '1d', '1mo'] },
  { id: '1Y', label: '1Y', days: 365.25, name: '1 Year', defaultRate: '1d', rates: ['1d', '1mo'] },
  { id: '3Y', label: '3Y', days: 3 * 365.25, name: '3 Years', defaultRate: '1mo', rates: ['1d', '1mo'] },
  { id: '5Y', label: '5Y', days: 5 * 365.25, name: '5 Years', defaultRate: '1mo', rates: ['1mo'] },
  { id: '10Y', label: '10Y', days: 10 * 365.25, name: '10 Years', defaultRate: '1mo', rates: ['1mo'] },
  { id: '20Y', label: '20Y', days: 20 * 365.25, name: '20 Years', defaultRate: '1mo', rates: ['1mo'] },
  { id: 'ALL', label: 'ALL', days: 36.8 * 365.25, name: 'All History', defaultRate: '1mo', rates: ['1mo'] }
];

export const PRESET_SAMPLE_COUNTS = {
  '1D': { '10m': 144, '1h': 24, '1d': 2 },
  '1W': { '1h': 168, '1d': 7 },
  '1M': { '1h': 240, '1d': 30, '1mo': 2 },
  '1Y': { '1d': 250, '1mo': 12 },
  '3Y': { '1d': 750, '1mo': 36 },
  '5Y': { '1mo': 60 },
  '10Y': { '1mo': 120 },
  '20Y': { '1mo': 240 }
};

export class TimeframeManager {
  constructor(presets = STANDARD_PRESETS, sampleCounts = PRESET_SAMPLE_COUNTS) {
    this.presets = presets;
    this.sampleCounts = sampleCounts;
  }

  /**
   * Matches duration in days to a predefined preset within a standard margin.
   * @param {number} days
   * @returns {object|null}
   */
  findMatchingPreset(days) {
    for (const p of this.presets) {
      const ratio = days / p.days;
      if (ratio >= 0.88 && ratio <= 1.14) {
        return p;
      }
    }
    return null;
  }

  /**
   * Returns list of supported candle sampling rates for a given duration.
   * @param {number} days
   * @returns {string[]}
   */
  getSupportedRatesForDuration(days) {
    if (days <= 2) return ['10m', '1h', '1d'];
    if (days <= 14) return ['1h', '1d'];
    if (days <= 90) return ['1h', '1d', '1mo'];
    if (days <= 1500) return ['1d', '1mo'];
    return ['1mo'];
  }

  /**
   * Returns default recommended sampling rate for a given duration.
   * @param {number} days
   * @returns {string}
   */
  getDefaultRateForDuration(days) {
    if (days <= 2) return '1h';
    if (days <= 90) return '1d';
    if (days <= 730) return '1d';
    return '1mo';
  }

  /**
   * Checks whether 10m candles are allowed for the given duration/preset.
   * 10m is exclusive to 1D (duration <= 2 days).
   * @param {number} days
   * @returns {boolean}
   */
  is10mAllowed(days) {
    return days <= 2;
  }

  /**
   * Computes continuous rolling zoom duration from wheel or pinch events.
   * @param {number} currentDays
   * @param {number} deltaY - Negative for zoom in, positive for zoom out
   * @param {number} minDays
   * @param {number} maxDays
   * @returns {number}
   */
  computeZoomDays(currentDays, deltaY, minDays = 0.5, maxDays = 13500) {
    const factor = deltaY < 0 ? 0.85 : 1.18;
    const target = currentDays * factor;
    return Math.max(minDays, Math.min(maxDays, target));
  }

  /**
   * Formats duration display tag string.
   * @param {number} days
   * @returns {string}
   */
  formatDurationLabel(days) {
    if (days < 1) return `${Math.round(days * 24)} Hours`;
    if (days <= 2) return `${days.toFixed(1)} Days`;
    if (days <= 14) return `${Math.round(days)} Days`;
    if (days <= 60) return `${(days / 30.5).toFixed(1)} Months`;
    if (days <= 365) return `${Math.round(days / 30.5)} Months`;
    return `${(days / 365.25).toFixed(1)} Years`;
  }
}

// Global instance
export const timeframeManager = new TimeframeManager();

if (typeof window !== 'undefined') {
  window.TimeframeManager = TimeframeManager;
  window.timeframeManager = timeframeManager;
  window.RATE_DURATIONS_MS = RATE_DURATIONS_MS;
  window.STANDARD_PRESETS = STANDARD_PRESETS;
}

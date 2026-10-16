/**
 * The Saac Financial Terminal - Universal Analytics Engine
 * Agnostic financial mathematics and calculations for any instrument or time-series.
 */

export const Analytics = {
  /**
   * Computes percentage return and absolute delta between two values.
   * @param {number} startVal - Base starting price/value
   * @param {number} endVal - Ending price/value
   * @returns {{ pct: number, abs: number, isPositive: boolean }}
   */
  computeReturn(startVal, endVal) {
    if (startVal === undefined || startVal === null || isNaN(startVal) || startVal === 0) {
      return { pct: 0, abs: 0, isPositive: true };
    }
    const abs = endVal - startVal;
    const pct = (abs / startVal) * 100;
    return {
      pct,
      abs,
      isPositive: abs >= 0
    };
  },

  /**
   * Computes minimum, maximum, and high-low spread across a series.
   * @param {Array<object>} series - Candle or point items
   * @param {string} [highKey='high']
   * @param {string} [lowKey='low']
   * @param {string} [closeKey='close']
   * @returns {{ min: number, max: number, spread: number }}
   */
  computeHighLow(series, highKey = 'high', lowKey = 'low', closeKey = 'close') {
    if (!series || !series.length) return { min: 0, max: 0, spread: 0 };
    let min = Infinity;
    let max = -Infinity;

    for (const item of series) {
      const h = item[highKey] !== undefined ? item[highKey] : item[closeKey];
      const l = item[lowKey] !== undefined ? item[lowKey] : item[closeKey];
      if (h !== undefined && !isNaN(h) && h > max) max = Number(h);
      if (l !== undefined && !isNaN(l) && l < min) min = Number(l);
    }

    if (min === Infinity) min = 0;
    if (max === -Infinity) max = 0;
    return { min, max, spread: max - min };
  },

  /**
   * Computes Maximum Drawdown (Peak to Trough drop percentage) across a series.
   * @param {Array<object>} series
   * @param {string} [valKey='close']
   * @returns {{ maxDrawdownPct: number, peak: number, trough: number }}
   */
  computeMaxDrawdown(series, valKey = 'close') {
    if (!series || !series.length) return { maxDrawdownPct: 0, peak: 0, trough: 0 };
    let peak = -Infinity;
    let maxDrawdown = 0;
    let bestPeak = 0;
    let bestTrough = 0;

    for (const item of series) {
      const val = Number(item[valKey] !== undefined ? item[valKey] : item.primary);
      if (isNaN(val)) continue;

      if (val > peak) {
        peak = val;
      }
      const dd = ((val - peak) / peak) * 100;
      if (dd < maxDrawdown) {
        maxDrawdown = dd;
        bestPeak = peak;
        bestTrough = val;
      }
    }

    return {
      maxDrawdownPct: maxDrawdown,
      peak: bestPeak,
      trough: bestTrough
    };
  },

  /**
   * Formats a number with sign and percentage.
   * @param {number} pct
   * @param {number} [decimals=2]
   * @returns {string}
   */
  formatPct(pct, decimals = 2) {
    if (pct === undefined || pct === null || isNaN(pct)) return '+0.00%';
    const sign = pct > 0 ? '+' : '';
    return `${sign}${pct.toFixed(decimals)}%`;
  },

  /**
   * Formats a monetary or numeric price.
   * @param {number} val
   * @param {string} [prefix='$']
   * @param {number} [decimals=2]
   * @returns {string}
   */
  formatPrice(val, prefix = '$', decimals = 2) {
    if (val === undefined || val === null || isNaN(val)) return `${prefix}0.00`;
    return `${prefix}${val.toLocaleString(undefined, {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    })}`;
  },

  /**
   * Renders percentage into an HTML element with institutional .pct-up or .pct-down class.
   * @param {string|HTMLElement} el
   * @param {number} pct
   */
  renderPctElement(el, pct) {
    const target = typeof el === 'string' ? document.getElementById(el) : el;
    if (!target) return;
    const sign = pct > 0 ? '+' : '';
    target.innerText = `${sign}${pct.toFixed(2)}%`;
    target.classList.remove('pct-up', 'pct-down');
    target.classList.add(pct >= 0 ? 'pct-up' : 'pct-down');
  }
};

// Global fallback for script-tag environments
if (typeof window !== 'undefined') {
  window.Analytics = Analytics;
}

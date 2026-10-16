/**
 * The Saac Financial Terminal - Universal Position & Unit Calculator
 * Supports dynamic unit conversions and negative guards for any active asset.
 */

export class CalculatorController {
  constructor() {
    this.lastSource = 'USD';
    this.activeInstrument = null;
  }

  setInstrument(instrument) {
    this.activeInstrument = instrument;
  }

  /**
   * Sets quick convert preset amount into the appropriate input field.
   * @param {string} source
   * @param {number} amount
   */
  setQuickConvert(source, amount) {
    const map = {
      'USD': 'inputUsd',
      'THB': 'inputThb',
      'OZ': 'inputOz',
      'THAI_BAHT': 'inputThaiBaht',
      'GRAMS': 'inputGrams'
    };
    const elId = map[source];
    const el = elId ? document.getElementById(elId) : null;
    if (el) {
      el.value = amount;
      this.convertFrom(source);
    }
  }

  /**
   * Executes multi-unit conversion while guarding against negatives and NaN.
   * @param {string} source
   */
  convertFrom(source) {
    this.lastSource = source;
    const currentPrice = window.currentGoldUsd || 4169.30;
    const currentFx = window.currentUsdThb || 33.56;
    const TROY_OZ_G = 31.1034768;
    const PURITY_965 = 0.965;
    const THAI_BAR_G = 15.244;

    const goldThbOz = currentPrice * currentFx;
    const pureGramThb = goldThbOz / TROY_OZ_G;
    const pureGramUsd = currentPrice / TROY_OZ_G;
    const thaiBarThb = pureGramThb * PURITY_965 * THAI_BAR_G;

    const usdEl = document.getElementById('inputUsd');
    const thbEl = document.getElementById('inputThb');
    const ozEl = document.getElementById('inputOz');
    const tbEl = document.getElementById('inputThaiBaht');
    const gEl = document.getElementById('inputGrams');

    if (source === 'USD' && usdEl) {
      const rawVal = parseFloat(usdEl.value);
      if (isNaN(rawVal) || rawVal < 0) {
        if (thbEl) thbEl.value = '';
        if (ozEl) ozEl.value = '';
        if (tbEl) tbEl.value = '';
        if (gEl) gEl.value = '';
        return;
      }
      const usd = Math.max(0, rawVal);
      if (thbEl) thbEl.value = usd ? (usd * currentFx).toFixed(2) : '';
      if (ozEl) ozEl.value = usd ? (usd / currentPrice).toFixed(4) : '';
      if (tbEl) tbEl.value = usd ? ((usd * currentFx) / thaiBarThb).toFixed(3) : '';
      if (gEl) gEl.value = usd ? (usd / pureGramUsd).toFixed(3) : '';
    } else if (source === 'THB' && thbEl) {
      const rawVal = parseFloat(thbEl.value);
      if (isNaN(rawVal) || rawVal < 0) {
        if (usdEl) usdEl.value = '';
        if (ozEl) ozEl.value = '';
        if (tbEl) tbEl.value = '';
        if (gEl) gEl.value = '';
        return;
      }
      const thb = Math.max(0, rawVal);
      if (usdEl) usdEl.value = thb ? (thb / currentFx).toFixed(2) : '';
      if (ozEl) ozEl.value = thb ? (thb / goldThbOz).toFixed(4) : '';
      if (tbEl) tbEl.value = thb ? (thb / thaiBarThb).toFixed(3) : '';
      if (gEl) gEl.value = thb ? (thb / pureGramThb).toFixed(3) : '';
    } else if (source === 'OZ' && ozEl) {
      const rawVal = parseFloat(ozEl.value);
      if (isNaN(rawVal) || rawVal < 0) {
        if (usdEl) usdEl.value = '';
        if (thbEl) thbEl.value = '';
        if (tbEl) tbEl.value = '';
        if (gEl) gEl.value = '';
        return;
      }
      const oz = Math.max(0, rawVal);
      if (usdEl) usdEl.value = oz ? (oz * currentPrice).toFixed(2) : '';
      if (thbEl) thbEl.value = oz ? (oz * goldThbOz).toFixed(2) : '';
      if (tbEl) tbEl.value = oz ? ((oz * goldThbOz) / thaiBarThb).toFixed(3) : '';
      if (gEl) gEl.value = oz ? (oz * TROY_OZ_G).toFixed(3) : '';
    } else if (source === 'THAI_BAHT' && tbEl) {
      const rawVal = parseFloat(tbEl.value);
      if (isNaN(rawVal) || rawVal < 0) {
        if (usdEl) usdEl.value = '';
        if (thbEl) thbEl.value = '';
        if (ozEl) ozEl.value = '';
        if (gEl) gEl.value = '';
        return;
      }
      const tb = Math.max(0, rawVal);
      const thbVal = tb * thaiBarThb;
      if (thbEl) thbEl.value = tb ? thbVal.toFixed(2) : '';
      if (usdEl) usdEl.value = tb ? (thbVal / currentFx).toFixed(2) : '';
      if (ozEl) ozEl.value = tb ? (thbVal / goldThbOz).toFixed(4) : '';
      if (gEl) gEl.value = tb ? (tb * THAI_BAR_G * PURITY_965).toFixed(3) : '';
    } else if (source === 'GRAMS' && gEl) {
      const rawVal = parseFloat(gEl.value);
      if (isNaN(rawVal) || rawVal < 0) {
        if (usdEl) usdEl.value = '';
        if (thbEl) thbEl.value = '';
        if (ozEl) ozEl.value = '';
        if (tbEl) tbEl.value = '';
        return;
      }
      const g = Math.max(0, rawVal);
      const ozVal = g / TROY_OZ_G;
      if (ozEl) ozEl.value = g ? ozVal.toFixed(4) : '';
      if (usdEl) usdEl.value = g ? (ozVal * currentPrice).toFixed(2) : '';
      if (thbEl) thbEl.value = g ? (g * pureGramThb).toFixed(2) : '';
      if (tbEl) tbEl.value = g ? ((g * pureGramThb) / thaiBarThb).toFixed(3) : '';
    }
  }
}

export const calculatorController = new CalculatorController();

if (typeof window !== 'undefined') {
  window.CalculatorController = CalculatorController;
  window.calculatorController = calculatorController;
  window.setQuickConvert = (s, a) => calculatorController.setQuickConvert(s, a);
  window.convertFrom = (s) => calculatorController.convertFrom(s);
}

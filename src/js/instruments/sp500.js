/**
 * The Saac Financial Terminal - S&P 500 Macro Benchmark
 */

export function computeDerivedSPX(raw) {
  const c = Number(raw.close !== undefined ? raw.close : 5850.2);
  const o = Number(raw.open !== undefined ? raw.open : c);
  const h = Number(raw.high !== undefined ? raw.high : Math.max(o, c));
  const l = Number(raw.low !== undefined ? raw.low : Math.min(o, c));
  const spy = c / 10.0;
  const vix = Number(raw.vix !== undefined ? raw.vix : 15.4);

  return {
    ...raw,
    date: raw.date,
    open: Math.round(o * 10) / 10,
    high: Math.round(h * 10) / 10,
    low: Math.round(l * 10) / 10,
    close: Math.round(c * 10) / 10,
    primary: Math.round(c * 10) / 10,
    spy: Math.round(spy * 100) / 100,
    vix: Math.round(vix * 100) / 100,
    note: raw.note || ''
  };
}

export const sp500Instrument = {
  id: 'sp500',
  symbol: 'SPX',
  name: 'S&P 500 Macro & Equities Terminal',
  shortName: 'S&P 500',
  exchange: 'S&P Dow Jones Indices (^GSPC) • SPDR S&P 500 ETF (SPY) • CBOE Volatility (^VIX)',
  primaryTicker: '^GSPC',
  unit: 'pts',
  unitPlural: 'points',
  currency: 'USD',
  themeColor: '#38bdf8',
  defaultPrice: 5850.20,
  dayRange: {
    low: 5820.00,
    high: 5875.00,
    base: 5835.00
  },
  cards: [
    {
      id: 'primary',
      domId: 'goldUsdDisplay',
      labelLeft: 'S&P 500 Index',
      labelRight: 'INDEX: ^GSPC',
      accentClass: 'card-primary',
      format: (val) => `${val.toLocaleString(undefined, { minimumFractionDigits: 1, maximumFractionDigits: 1 })} pts`,
      subtextTemplate: () => `
        <span class="badge-change up" id="goldChangeBadge">+0.32%</span>
        <span id="goldRange">Day Range: 5,820.0 - 5,875.0</span>
      `
    },
    {
      id: 'secondary1',
      domId: 'usdThbDisplay',
      labelLeft: 'SPDR S&P 500 ETF',
      labelRight: 'ETF: SPY',
      accentClass: 'card-secondary-1',
      format: (val) => `$${(val / 10.0).toFixed(2)}`,
      subtextTemplate: () => `<span>1/10th S&P Index Value</span>`
    },
    {
      id: 'secondary2',
      domId: 'bondYieldDisplay',
      labelLeft: 'CBOE Volatility Index',
      labelRight: 'VOLATILITY: ^VIX',
      accentClass: 'card-secondary-2',
      style: 'color: #38bdf8;',
      format: () => `15.42`,
      subtextTemplate: () => `
        <span class="badge-change down" id="bondChangeBadge">-2.10%</span>
        <span>Market Fear Gauge</span>
      `
    },
    {
      id: 'derived',
      domId: 'goldThaiBahtDisplay',
      labelLeft: 'Micro E-Mini S&P Notional',
      labelRight: 'CME: MES ($5/PT)',
      accentClass: 'card-derived',
      format: (val) => `$${Math.round(val * 5.0).toLocaleString()}`,
      subtextTemplate: (val) => `<span>E-Mini (ES): $${Math.round(val * 50.0).toLocaleString()}</span>`
    }
  ],
  secondarySeries: [
    {
      id: 'spy',
      label: 'SPDR SPY',
      ticker: 'SPY',
      unit: '$',
      color: '#38bdf8',
      yAxisID: 'y1',
      activeClass: 'active-thb',
      getValue: (item) => item.spy !== undefined ? item.spy : (item.close / 10.0),
      formatValue: (v) => `$${Number(v).toFixed(2)}`
    },
    {
      id: 'vix',
      label: 'CBOE VIX',
      ticker: '^VIX',
      unit: 'pts',
      color: '#a855f7',
      yAxisID: 'y2',
      activeClass: 'active-bond',
      getValue: (item) => item.vix !== undefined ? item.vix : 15.4,
      formatValue: (v) => `${Number(v).toFixed(2)}`
    }
  ],
  conversions: [
    { id: 'pts', name: 'Index Points (pts)', factor: 1.0, isBase: true },
    { id: 'mes', name: 'Micro E-Mini MES ($5)', factor: 5.0 },
    { id: 'es', name: 'Standard E-Mini ES ($50)', factor: 50.0 }
  ],
  eras: [
    { id: '2008', label: '2008 Financial Meltdown', start: '2008-09', end: '2009-03', title: 'Great Recession Low' },
    { id: '2020', label: '2020 COVID Flash Crash', start: '2020-02', end: '2020-04', title: 'Fastest 30% Bear Market' },
    { id: '2024', label: '2024-2026 Expansion', start: '2023-10', end: '2026-10', title: 'Macro Bull Market' }
  ],
  computeDerived: computeDerivedSPX
};

if (typeof window !== 'undefined') {
  window.sp500Instrument = sp500Instrument;
}

/**
 * The Saac Financial Terminal - Nasdaq Composite & Tech Tracker
 * Implements the universal Instrument schema for tech equity indices.
 */

export function computeDerivedNasdaq(raw) {
  const c = Number(raw.close !== undefined ? raw.close : (raw.nasdaq || raw.primary || 20340.5));
  const o = Number(raw.open !== undefined ? raw.open : c);
  const h = Number(raw.high !== undefined ? raw.high : Math.max(o, c));
  const l = Number(raw.low !== undefined ? raw.low : Math.min(o, c));
  const qqq = Number(raw.qqq !== undefined ? raw.qqq : (c / 41.0));
  const bond = Number(raw.us10y !== undefined ? raw.us10y : (raw.bond || 5.217));

  // Micro E-mini contract value ($2 per point), Standard E-mini ($20 per point)
  const mnq_notional = c * 2.0;
  const nq_notional = c * 20.0;
  const tech_pe = c / 680.0;

  return {
    ...raw,
    date: raw.date,
    open: Math.round(o * 10) / 10,
    high: Math.round(h * 10) / 10,
    low: Math.round(l * 10) / 10,
    close: Math.round(c * 10) / 10,
    primary: Math.round(c * 10) / 10,
    qqq: Math.round(qqq * 100) / 100,
    us10y: Math.round(bond * 1000) / 1000,
    bond: Math.round(bond * 1000) / 1000,
    mnq_notional: Math.round(mnq_notional),
    nq_notional: Math.round(nq_notional),
    tech_pe: Math.round(tech_pe * 10) / 10,
    note: raw.note || ''
  };
}

export const nasdaqInstrument = {
  id: 'nasdaq',
  symbol: 'IXIC',
  name: 'Nasdaq Composite & Tech Equity Terminal',
  shortName: 'Nasdaq',
  exchange: 'NASDAQ Global Select (^IXIC) • Invesco QQQ (QQQ) • CBOE US10Y (^TNX)',
  primaryTicker: '^IXIC',
  unit: 'pts',
  unitPlural: 'points',
  currency: 'USD',
  themeColor: '#00c853',
  defaultPrice: 20340.50,
  dayRange: {
    low: 20210.00,
    high: 20450.00,
    base: 20280.00
  },
  cards: [
    {
      id: 'primary',
      domId: 'goldUsdDisplay',
      labelLeft: 'Nasdaq Composite',
      labelRight: 'INDEX: ^IXIC',
      accentClass: 'card-primary',
      format: (val) => `${val.toLocaleString(undefined, { minimumFractionDigits: 1, maximumFractionDigits: 1 })} pts`,
      subtextTemplate: () => `
        <span class="badge-change up" id="goldChangeBadge">+0.48%</span>
        <span id="goldRange">Day Range: 20,210.0 - 20,450.0</span>
      `
    },
    {
      id: 'secondary1',
      domId: 'usdThbDisplay',
      labelLeft: 'Invesco QQQ Trust',
      labelRight: 'ETF: QQQ',
      accentClass: 'card-secondary-1',
      format: (val) => `$${(val / 41.0).toFixed(2)}`,
      subtextTemplate: (val) => `<span>Tech Benchmark Proxy</span>`
    },
    {
      id: 'secondary2',
      domId: 'bondYieldDisplay',
      labelLeft: 'US 10-Year Treasury Yield',
      labelRight: 'RATES: CBOE ^TNX',
      accentClass: 'card-secondary-2',
      style: 'color: #c084fc;',
      format: (val) => `${val.toFixed(3)}%`,
      subtextTemplate: () => `
        <span class="badge-change down" id="bondChangeBadge">-0.44%</span>
        <span>Cost of Capital Anchor</span>
      `
    },
    {
      id: 'derived',
      domId: 'goldThaiBahtDisplay',
      labelLeft: 'Micro E-Mini Notional',
      labelRight: 'CME: MNQ ($2/PT)',
      accentClass: 'card-derived',
      format: (val) => `$${Math.round(val * 2.0).toLocaleString()}`,
      subtextTemplate: (val) => `<span>E-Mini (NQ): $${Math.round(val * 20.0).toLocaleString()}</span>`
    }
  ],
  secondarySeries: [
    {
      id: 'qqq',
      label: 'Invesco QQQ',
      ticker: 'QQQ',
      unit: '$',
      color: '#38bdf8',
      yAxisID: 'y1',
      activeClass: 'active-thb',
      getValue: (item) => item.qqq !== undefined ? item.qqq : (item.close / 41.0),
      formatValue: (v) => `$${Number(v).toFixed(2)}`
    },
    {
      id: 'us10y',
      label: 'US 10Y Yield',
      ticker: '^TNX',
      unit: '%',
      color: '#a855f7',
      yAxisID: 'y2',
      activeClass: 'active-bond',
      getValue: (item) => item.us10y !== undefined ? item.us10y : item.bond,
      formatValue: (v) => `${Number(v).toFixed(3)}%`
    }
  ],
  conversions: [
    { id: 'pts', name: 'Index Points (pts)', factor: 1.0, isBase: true },
    { id: 'mnq', name: 'Micro Futures MNQ ($2)', factor: 2.0 },
    { id: 'nq', name: 'E-Mini Futures NQ ($20)', factor: 20.0 },
    { id: 'pe', name: 'Estimated P/E Multiple', factor: 1 / 680.0 }
  ],
  eras: [
    { id: '2000', label: '2000 Dot-Com Crash', start: '2000-03', end: '2002-10', title: 'Tech Bubble Unwind' },
    { id: '2008', label: '2008 GFC Liquidity Shock', start: '2008-09', end: '2009-03', title: 'Subprime Recession' },
    { id: '2020', label: '2020 COVID Tech Boom', start: '2020-03', end: '2021-11', title: 'Cloud & Remote Growth' },
    { id: '2022', label: '2022 Rate Shock Drawdown', start: '2022-01', end: '2022-10', title: 'Inflationary Tech Compression' },
    { id: '2024', label: '2023-2026 AI Supercycle', start: '2023-01', end: '2026-10', title: 'Generative AI Secular Wave' }
  ],
  computeDerived: computeDerivedNasdaq
};

if (typeof window !== 'undefined') {
  window.nasdaqInstrument = nasdaqInstrument;
  window.computeDerivedNasdaq = computeDerivedNasdaq;
}

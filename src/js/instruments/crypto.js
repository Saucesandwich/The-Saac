/**
 * The Saac Financial Terminal - Bitcoin / Crypto Instrument
 */

export function computeDerivedBTC(raw) {
  const c = Number(raw.close !== undefined ? raw.close : 68450.0);
  const o = Number(raw.open !== undefined ? raw.open : c);
  const h = Number(raw.high !== undefined ? raw.high : Math.max(o, c));
  const l = Number(raw.low !== undefined ? raw.low : Math.min(o, c));
  const eth = Number(raw.eth !== undefined ? raw.eth : (c * 0.038));
  const sats_per_dollar = Math.round(100000000 / c);

  return {
    ...raw,
    date: raw.date,
    open: Math.round(o),
    high: Math.round(h),
    low: Math.round(l),
    close: Math.round(c),
    primary: Math.round(c),
    eth: Math.round(eth * 10) / 10,
    sats_per_dollar,
    note: raw.note || ''
  };
}

export const cryptoInstrument = {
  id: 'crypto',
  symbol: 'BTC',
  name: 'Bitcoin Digital Asset Terminal',
  shortName: 'Bitcoin',
  exchange: 'CME Group / Binance (BTC-USD) • Ethereum (ETH-USD)',
  primaryTicker: 'BTC-USD',
  unit: 'BTC',
  unitPlural: 'coins',
  currency: 'USD',
  themeColor: '#f59e0b',
  defaultPrice: 68450.00,
  dayRange: {
    low: 67800.00,
    high: 69200.00,
    base: 68100.00
  },
  cards: [
    {
      id: 'primary',
      domId: 'goldUsdDisplay',
      labelLeft: 'Bitcoin Spot',
      labelRight: 'CRYPTO: BTC-USD',
      accentClass: 'card-primary',
      format: (val) => `$${val.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`,
      subtextTemplate: () => `
        <span class="badge-change up" id="goldChangeBadge">+0.51%</span>
        <span id="goldRange">Day Range: $67,800 - $69,200</span>
      `
    },
    {
      id: 'secondary1',
      domId: 'usdThbDisplay',
      labelLeft: 'Ethereum / USD',
      labelRight: 'CRYPTO: ETH-USD',
      accentClass: 'card-secondary-1',
      format: (val) => `$${(val * 0.038).toFixed(1)}`,
      subtextTemplate: () => `<span>ETH/BTC Ratio: 0.038</span>`
    },
    {
      id: 'secondary2',
      domId: 'bondYieldDisplay',
      labelLeft: 'US Dollar Index',
      labelRight: 'CURRENCY: DXY',
      accentClass: 'card-secondary-2',
      style: 'color: #38bdf8;',
      format: () => `103.45`,
      subtextTemplate: () => `
        <span class="badge-change down" id="bondChangeBadge">-0.15%</span>
        <span>Global Reserve Currency</span>
      `
    },
    {
      id: 'derived',
      domId: 'goldThaiBahtDisplay',
      labelLeft: 'Satoshis Per Dollar',
      labelRight: 'UNIT: 100M SATS/BTC',
      accentClass: 'card-derived',
      format: (val) => `${Math.round(100000000 / val).toLocaleString()} sats`,
      subtextTemplate: (val) => `<span>1 Sat = $${(val / 100000000).toFixed(6)} USD</span>`
    }
  ],
  secondarySeries: [
    {
      id: 'eth',
      label: 'ETH / USD',
      ticker: 'ETH-USD',
      unit: '$',
      color: '#38bdf8',
      yAxisID: 'y1',
      activeClass: 'active-thb',
      getValue: (item) => item.eth !== undefined ? item.eth : (item.close * 0.038),
      formatValue: (v) => `$${Number(v).toFixed(1)}`
    }
  ],
  conversions: [
    { id: 'btc', name: 'Bitcoin (BTC)', factor: 1.0, isBase: true },
    { id: 'sat', name: 'Satoshis (sats)', factor: 100000000.0 }
  ],
  eras: [
    { id: '2017', label: '2017 Mania Peak', start: '2017-01', end: '2017-12', title: '$20,000 Milestone' },
    { id: '2020', label: '2020 Halving Expansion', start: '2020-03', end: '2021-11', title: '$69,000 High' },
    { id: '2024', label: '2024 ETF Inflow Era', start: '2024-01', end: '2026-10', title: 'Institutional Adoption' }
  ],
  computeDerived: computeDerivedBTC
};

if (typeof window !== 'undefined') {
  window.cryptoInstrument = cryptoInstrument;
}

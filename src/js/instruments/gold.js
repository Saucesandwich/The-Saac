/**
 * The Saac Financial Terminal - Gold Instrument Configuration
 * Verified CME COMEX GC=F, Bank of Thailand THB=X, CBOE ^TNX, and Thai Gold Traders standards.
 */

export const TROY_OZ_TO_GRAMS = 31.1034768;
export const THAI_BAHT_BAR_GRAMS = 15.244;
export const THAI_BAHT_ORNAMENT_GRAMS = 15.16;
export const THAI_GOLD_PURITY_965 = 0.965;

export function computeDerivedGold(raw) {
  const c = Number(raw.close !== undefined ? raw.close : (raw.gold || 0));
  const o = Number(raw.open !== undefined ? raw.open : c);
  const h = Number(raw.high !== undefined ? raw.high : Math.max(o, c));
  const l = Number(raw.low !== undefined ? raw.low : Math.min(o, c));
  const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : (raw.thb || 33.52));
  const bond = Number(raw.us10y !== undefined ? raw.us10y : (raw.bond || 5.217));

  const gold_thb_oz = c * thb;
  const pure_gold_gram = gold_thb_oz / TROY_OZ_TO_GRAMS;
  const thai_gold_bar = pure_gold_gram * THAI_BAHT_BAR_GRAMS * THAI_GOLD_PURITY_965;
  const thai_gold_ornament = pure_gold_gram * THAI_BAHT_ORNAMENT_GRAMS * THAI_GOLD_PURITY_965;

  return {
    ...raw,
    date: raw.date,
    open: Math.round(o * 10) / 10,
    high: Math.round(h * 10) / 10,
    low: Math.round(l * 10) / 10,
    close: Math.round(c * 10) / 10,
    gold: Math.round(c * 10) / 10,
    usd_thb: Math.round(thb * 100) / 100,
    thb: Math.round(thb * 100) / 100,
    us10y: Math.round(bond * 1000) / 1000,
    bond: Math.round(bond * 1000) / 1000,
    gold_thb_oz: Math.round(gold_thb_oz * 100) / 100,
    pure_gold_gram: Math.round(pure_gold_gram * 100) / 100,
    thai_gold_bar: Math.round(thai_gold_bar),
    thai_gold_ornament: Math.round(thai_gold_ornament),
    note: raw.note || ''
  };
}

export const goldInstrument = {
  id: 'gold',
  symbol: 'XAU',
  name: 'Gold, Baht & US Bond Market Terminal',
  shortName: 'Gold',
  exchange: 'CME COMEX Gold Futures (GC=F) • Bank of Thailand (THB=X) • CBOE US10Y (^TNX)',
  primaryTicker: 'GC=F',
  unit: 'oz',
  unitPlural: 'ounces',
  currency: 'USD',
  themeColor: '#ff9800',
  defaultPrice: 4169.30,
  dayRange: {
    low: 4165.50,
    high: 4193.50,
    base: 4159.00
  },
  cards: [
    {
      id: 'primary',
      domId: 'goldUsdDisplay',
      labelLeft: 'Gold Futures (US Market)',
      labelRight: 'COMEX: GC=F',
      accentClass: 'card-gold',
      format: (val) => `$${val.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      subtextTemplate: (val, inst) => `
        <span class="badge-change up" id="goldChangeBadge">+0.25%</span>
        <span id="goldRange">Day Range: $4,165.50 - $4,193.50</span>
      `
    },
    {
      id: 'secondary1',
      domId: 'usdThbDisplay',
      labelLeft: 'Forex Exchange Rate',
      labelRight: 'FX: USD / THB',
      accentClass: 'card-forex',
      format: (val) => `฿${val.toFixed(4)}`,
      subtextTemplate: (val) => `<span id="inverseRate">1 THB ≈ $${(1 / val).toFixed(4)} USD</span>`
    },
    {
      id: 'secondary2',
      domId: 'bondYieldDisplay',
      labelLeft: 'US 10-Year Treasury Yield',
      labelRight: 'RATES: CBOE ^TNX',
      accentClass: 'card-bond',
      style: 'color: #c084fc;',
      format: (val) => `${val.toFixed(3)}%`,
      subtextTemplate: () => `
        <span class="badge-change down" id="bondChangeBadge">-0.44%</span>
        <span>Benchmark Risk-Free Rate</span>
      `
    },
    {
      id: 'derived',
      domId: 'goldThaiBahtDisplay',
      labelLeft: 'Thai Gold Bar (1 บาททอง)',
      labelRight: 'THAI GOLD: 96.5% BAR',
      accentClass: 'card-thai',
      format: (val) => `฿${Math.round(val).toLocaleString()}`,
      subtextTemplate: (val, inst, d) => `<span id="pureGoldGramDisplay">Pure Gold: ฿${Math.round(d?.pure_gold_gram || 4499).toLocaleString()}/g</span>`
    }
  ],
  secondarySeries: [
    {
      id: 'usd_thb',
      label: 'USD / THB',
      ticker: 'THB=X',
      unit: '฿',
      color: '#38bdf8',
      yAxisID: 'y1',
      activeClass: 'active-thb',
      getValue: (item) => item.usd_thb !== undefined ? item.usd_thb : item.thb,
      formatValue: (v) => `฿${Number(v).toFixed(2)}`
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
    { id: 'oz', name: 'Troy Ounces (oz)', factor: 1.0, isBase: true },
    { id: 'grams', name: 'Grams (g)', factor: 1 / TROY_OZ_TO_GRAMS },
    { id: 'thai_bar', name: 'Thai Baht Bar (บาททอง)', factor: (THAI_BAHT_BAR_GRAMS * THAI_GOLD_PURITY_965) / TROY_OZ_TO_GRAMS },
    { id: 'thai_ornament', name: 'Thai Ornament (บาทรูปพรรณ)', factor: (THAI_BAHT_ORNAMENT_GRAMS * THAI_GOLD_PURITY_965) / TROY_OZ_TO_GRAMS }
  ],
  eras: [
    { id: '1997', label: '1997 Asian Crisis', start: '1997-07', end: '1998-01', title: 'Tom Yum Kung Baht Float' },
    { id: '2008', label: '2008 Lehman GFC', start: '2008-03', end: '2008-10', title: 'Subprime & Financial Meltdown' },
    { id: '2020', label: '2020 COVID Shock', start: '2020-03', end: '2020-08', title: 'Global Stimulus & Rate Cuts' },
    { id: '2022', label: '2022 Rate Hikes', start: '2022-03', end: '2022-10', title: 'Fed Tightening Cycle' },
    { id: '2026', label: '2024-2026 ATH Run', start: '2024-03', end: '2026-01', title: 'Secular Milestone Rally' }
  ],
  computeDerived: computeDerivedGold
};

if (typeof window !== 'undefined') {
  window.goldInstrument = goldInstrument;
  window.computeDerivedGold = computeDerivedGold;
}

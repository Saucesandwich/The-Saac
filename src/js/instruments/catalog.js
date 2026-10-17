/**
 * The Saac Financial Terminal - Macro Instrument Catalog
 * Comprehensive coverage of Major Indices, ETFs, Commodities, Sovereign Country Bonds, and Forex.
 * Strict exclusion of individual stocks as requested.
 */

export const INSTRUMENT_CATEGORIES = [
  { id: 'all', label: 'ALL MARKETS', count: 28 },
  { id: 'commodities', label: 'COMMODITIES', count: 5 },
  { id: 'indices', label: 'MAJOR INDICES', count: 8 },
  { id: 'etfs', label: 'BENCHMARK ETFS', count: 8 },
  { id: 'bonds', label: 'SOVEREIGN BONDS', count: 5 },
  { id: 'forex', label: 'FOREX & MACRO', count: 4 }
];

export const MACRO_CATALOG = [
  // ==========================================
  // 1. COMMODITIES
  // ==========================================
  {
    id: 'gold',
    category: 'commodities',
    symbol: 'XAU',
    name: 'Gold Futures & Thai Precious Metals',
    shortName: 'Gold',
    ticker: 'GC=F',
    exchange: 'CME COMEX Gold Futures (GC=F) • Bank of Thailand (THB=X) • CBOE US10Y (^TNX)',
    unit: 'oz',
    currency: 'USD',
    themeColor: '#ff9100',
    defaultPrice: 4169.30,
    dayRange: { low: 4165.50, high: 4193.50, base: 4159.00 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'Gold Futures (US Market)', labelRight: 'COMEX: GC=F', format: (v) => `$${v.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Forex Exchange Rate', labelRight: 'FX: USD / THB', format: (v) => `฿${v.toFixed(4)}` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'US 10-Year Treasury Yield', labelRight: 'RATES: CBOE ^TNX', style: 'color: #ffd600;', format: (v) => `${v.toFixed(3)}%` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Thai Gold Bar (1 บาททอง)', labelRight: 'THAI GOLD: 96.5% BAR', format: (v) => `฿${Math.round(v).toLocaleString()}` }
    ],
    secondarySeries: [
      { id: 'thb', label: 'USD / THB', ticker: 'THB=X', unit: '฿', color: '#00e5ff', yAxisID: 'y1', getValue: (d) => d.usd_thb || d.thb || 33.56, formatValue: (v) => `฿${Number(v).toFixed(2)}` },
      { id: 'us10y', label: 'US 10Y Yield', ticker: '^TNX', unit: '%', color: '#00e676', yAxisID: 'y2', getValue: (d) => d.us10y || d.bond || 5.217, formatValue: (v) => `${Number(v).toFixed(3)}%` }
    ],
    eras: [
      { id: '1997', label: '1997 Asian Crisis', start: '1997-07', end: '1998-01', title: 'Tom Yum Kung Baht Float' },
      { id: '2008', label: '2008 Lehman GFC', start: '2008-03', end: '2008-10', title: 'Subprime & Financial Meltdown' },
      { id: '2020', label: '2020 COVID Shock', start: '2020-03', end: '2020-08', title: 'Global Stimulus & Rate Cuts' },
      { id: '2022', label: '2022 Rate Hikes', start: '2022-03', end: '2022-10', title: 'Fed Tightening Cycle' },
      { id: '2026', label: '2024-2026 ATH Run', start: '2024-03', end: '2026-01', title: 'Secular Milestone Rally' }
    ],
    computeDerived: (raw) => {
      const c = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
      const thb = Number(raw.usd_thb || raw.thb || 33.56);
      const bond = Number(raw.us10y || raw.bond || 5.217);
      const gold_thb_oz = c * thb;
      const pure_gram_thb = gold_thb_oz / 31.1034768;
      return {
        ...raw,
        gold: c,
        close: c,
        usd_thb: thb,
        thb: thb,
        us10y: bond,
        bond: bond,
        gold_thb_oz,
        pure_gram_thb,
        thai_gold_bar: Math.round(pure_gram_thb * 0.965 * 15.244),
        thai_gold_ornament: Math.round(pure_gram_thb * 0.965 * 15.16)
      };
    }
  },
  {
    id: 'silver',
    category: 'commodities',
    symbol: 'XAG',
    name: 'Silver Futures & Gold-Silver Ratio',
    shortName: 'Silver',
    ticker: 'SI=F',
    exchange: 'CME COMEX Silver Futures (SI=F)',
    unit: 'oz',
    currency: 'USD',
    themeColor: '#ffffff',
    defaultPrice: 5.098,
    dayRange: { low: 5.067, high: 5.133, base: 5.089 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'Silver Spot / Futures', labelRight: 'COMEX: SI=F', format: (v) => `$${v.toFixed(2)}/oz` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Gold / Silver Ratio', labelRight: 'SPREAD: XAU/XAG', format: (v) => `${(4169.3 / (v || 32.4)).toFixed(1)}x` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'Industrial Demand Index', labelRight: 'SECTOR: SOLAR & TECH', format: () => `+14.2% YoY` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Silver 1kg Bar Value', labelRight: 'STANDARD 1KG 999', format: (v) => `$${Math.round((v / 31.1035) * 1000).toLocaleString()}` }
    ],
    secondarySeries: [
      { id: 'ratio', label: 'Gold/Silver Ratio', unit: 'x', color: '#ff9100', getValue: (d) => Number((4169.3 / (d.close || 32.4)).toFixed(1)), formatValue: (v) => `${v}x` }
    ]
  },
  {
    id: 'crude_oil',
    category: 'commodities',
    symbol: 'CL',
    name: 'WTI & Brent Crude Oil Benchmark',
    shortName: 'Crude Oil',
    ticker: 'CL=F',
    exchange: 'NYMEX Light Sweet Crude (CL=F) • ICE Brent (BZ=F)',
    unit: 'bbl',
    currency: 'USD',
    themeColor: '#ff1744',
    defaultPrice: 99.04,
    dayRange: { low: 96.85, high: 101.9, base: 97.97 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'WTI Crude Oil', labelRight: 'NYMEX: CL=F', format: (v) => `$${v.toFixed(2)} / bbl` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Brent Crude Premium', labelRight: 'ICE: BZ=F', format: (v) => `$${(v + 3.85).toFixed(2)}` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'US Strategic Petroleum Reserve', labelRight: 'ENERGY INVENTORY', format: () => `385M bbl` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Per Barrel Gallon Price', labelRight: 'UNIT: 42 GALLONS', format: (v) => `$${(v / 42.0).toFixed(2)}/gal` }
    ],
    secondarySeries: [
      { id: 'brent', label: 'Brent Crude', color: '#00e5ff', getValue: (d) => Number((d.close + 3.85).toFixed(2)), formatValue: (v) => `$${v}` }
    ]
  },
  {
    id: 'natural_gas',
    category: 'commodities',
    symbol: 'NG',
    name: 'Natural Gas Henry Hub Spot',
    shortName: 'Natural Gas',
    ticker: 'NG=F',
    exchange: 'NYMEX Henry Hub Natural Gas (NG=F)',
    unit: 'MMBtu',
    currency: 'USD',
    themeColor: '#00e5ff',
    defaultPrice: 3.117,
    dayRange: { low: 3.062, high: 3.229, base: 3.236 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'Henry Hub Natural Gas', labelRight: 'NYMEX: NG=F', format: (v) => `$${v.toFixed(3)} / MMBtu` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'US Working Gas Storage', labelRight: 'EIA REPORT', format: () => `3,650 Bcf` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'LNG Export Capacity', labelRight: 'FEEDGAS DEMAND', format: () => `14.8 Bcf/d` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Contract Notional Value', labelRight: '10,000 MMBTU LOT', format: (v) => `$${Math.round(v * 10000).toLocaleString()}` }
    ]
  },
  {
    id: 'copper',
    category: 'commodities',
    symbol: 'HG',
    name: 'Copper Futures (Doctor Copper)',
    shortName: 'Copper',
    ticker: 'HG=F',
    exchange: 'CME COMEX High Grade Copper (HG=F)',
    unit: 'lb',
    currency: 'USD',
    themeColor: '#ff9100',
    defaultPrice: 6.562,
    dayRange: { low: 6.531, high: 6.607, base: 6.511 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'High Grade Copper', labelRight: 'COMEX: HG=F', format: (v) => `$${v.toFixed(3)} / lb` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Metric Ton Equivalent', labelRight: 'LME SPOT CONVERSION', format: (v) => `$${Math.round(v * 2204.62).toLocaleString()}/t` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'Global PMI Correlation', labelRight: 'MACRO BELLWETHER', format: () => `+0.78 Corr` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Contract Size Notional', labelRight: '25,000 LBS LOT', format: (v) => `$${Math.round(v * 25000).toLocaleString()}` }
    ]
  },

  // ==========================================
  // 2. MAJOR EQUITY INDICES
  // ==========================================
  {
    id: 'sp500',
    category: 'indices',
    symbol: 'SPX',
    name: 'S&P 500 Large-Cap US Index',
    shortName: 'S&P 500',
    ticker: '^GSPC',
    exchange: 'S&P Dow Jones Indices (^GSPC)',
    unit: 'pts',
    currency: 'USD',
    themeColor: '#00b0ff',
    defaultPrice: 7659.4,
    dayRange: { low: 7631.8, high: 7756.8, base: 7744.1 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'S&P 500 Index', labelRight: 'INDEX: ^GSPC', format: (v) => `${v.toLocaleString(undefined, { minimumFractionDigits: 1 })} pts` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'SPDR S&P 500 ETF', labelRight: 'ETF: SPY', format: (v) => `$${(v / 10.0).toFixed(2)}` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'CBOE Volatility Index', labelRight: 'VOLATILITY: ^VIX', format: () => `15.42 pts` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Micro E-Mini S&P Notional', labelRight: 'CME: MES ($5/PT)', format: (v) => `$${Math.round(v * 5.0).toLocaleString()}` }
    ]
  },
  {
    id: 'nasdaq',
    category: 'indices',
    symbol: 'IXIC',
    name: 'Nasdaq Composite Tech Index',
    shortName: 'Nasdaq',
    ticker: '^IXIC',
    exchange: 'NASDAQ Global Select (^IXIC) • Invesco QQQ',
    unit: 'pts',
    currency: 'USD',
    themeColor: '#00e676',
    defaultPrice: 26140.0,
    dayRange: { low: 26023.1, high: 26674.7, base: 26713.0 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'Nasdaq Composite', labelRight: 'NASDAQ: ^IXIC', format: (v) => `${v.toLocaleString(undefined, { minimumFractionDigits: 1 })} pts` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Invesco QQQ Trust', labelRight: 'ETF: QQQ', format: (v) => `$${(v / 41.0).toFixed(2)}` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'US 10-Year Treasury', labelRight: 'DISCOUNT RATE', format: () => `5.217%` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Micro E-Mini NQ Value', labelRight: 'CME: MNQ ($2/PT)', format: (v) => `$${Math.round(v * 2.0).toLocaleString()}` }
    ]
  },
  {
    id: 'dowjones',
    category: 'indices',
    symbol: 'DJI',
    name: 'Dow Jones Industrial Average',
    shortName: 'Dow Jones',
    ticker: '^DJI',
    exchange: 'S&P Dow Jones Indices (^DJI)',
    unit: 'pts',
    currency: 'USD',
    themeColor: '#00b0ff',
    defaultPrice: 52002.4,
    dayRange: { low: 51847.9, high: 52582.3, base: 52177.7 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'Dow Jones Industrial Avg', labelRight: 'INDEX: ^DJI', format: (v) => `${v.toLocaleString(undefined, { minimumFractionDigits: 0 })} pts` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'SPDR Dow ETF', labelRight: 'ETF: DIA', format: (v) => `$${(v / 100.0).toFixed(2)}` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'Dividend Yield Proxy', labelRight: 'ESTIMATED YIELD', format: () => `1.95%` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'E-mini Dow Contract', labelRight: 'CME: YM ($5/PT)', format: (v) => `$${Math.round(v * 5.0).toLocaleString()}` }
    ]
  },
  {
    id: 'russell2000',
    category: 'indices',
    symbol: 'RUT',
    name: 'Russell 2000 US Small-Cap Index',
    shortName: 'Russell 2000',
    ticker: '^RUT',
    exchange: 'FTSE Russell Indices (^RUT)',
    unit: 'pts',
    currency: 'USD',
    themeColor: '#ffd600',
    defaultPrice: 2721.4,
    dayRange: { low: 2716.2, high: 2771.7, base: 2767.3 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'Russell 2000 Small-Cap', labelRight: 'INDEX: ^RUT', format: (v) => `${v.toFixed(1)} pts` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'iShares Russell 2000', labelRight: 'ETF: IWM', format: (v) => `$${(v / 10.0).toFixed(2)}` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'Debt Refinancing Risk', labelRight: 'FLOATING RATE DEBT', format: () => `High Beta` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Micro Russell Contract', labelRight: 'CME: M2K ($5/PT)', format: (v) => `$${Math.round(v * 5.0).toLocaleString()}` }
    ]
  },
  {
    id: 'nikkei225',
    category: 'indices',
    symbol: 'N225',
    name: 'Nikkei 225 Japan Benchmark',
    shortName: 'Nikkei 225',
    ticker: '^N225',
    exchange: 'Tokyo Stock Exchange (^N225)',
    unit: 'pts',
    currency: 'JPY',
    themeColor: '#ff1744',
    defaultPrice: 65324.3,
    dayRange: { low: 64800.9, high: 65712.3, base: 64425.9 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'Nikkei 225 (Japan)', labelRight: 'TSE: ^N225', format: (v) => `¥${Math.round(v).toLocaleString()} JPY` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'USD / JPY Forex Rate', labelRight: 'FX: USD/JPY', format: () => `¥149.50` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'Japan 10Y JGB Yield', labelRight: 'BOJ POLICY RATE', format: () => `0.965%` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'USD Hedged Value', labelRight: 'FX NORMALIZED', format: (v) => `$${(v / 149.5).toFixed(1)} USD` }
    ]
  },
  {
    id: 'dax40',
    category: 'indices',
    symbol: 'DAX',
    name: 'DAX 40 Germany Blue-Chip Index',
    shortName: 'DAX 40',
    ticker: '^GDAXI',
    exchange: 'Deutsche Börse XETRA (^GDAXI)',
    unit: 'pts',
    currency: 'EUR',
    themeColor: '#ffd600',
    defaultPrice: 25622.6,
    dayRange: { low: 25466.1, high: 25693.9, base: 25382.6 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'DAX 40 (Germany)', labelRight: 'XETRA: ^GDAXI', format: (v) => `€${Math.round(v).toLocaleString()} EUR` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'EUR / USD Forex Rate', labelRight: 'FX: EUR/USD', format: () => `$1.0850` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'German 10Y Bund Yield', labelRight: 'ECB BENCHMARK', format: () => `2.215%` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'USD Normalized Value', labelRight: 'FX CONVERTED', format: (v) => `$${Math.round(v * 1.085).toLocaleString()} USD` }
    ]
  },
  {
    id: 'ftse100',
    category: 'indices',
    symbol: 'FTSE',
    name: 'FTSE 100 London UK Index',
    shortName: 'FTSE 100',
    ticker: '^FTSE',
    exchange: 'London Stock Exchange (^FTSE)',
    unit: 'pts',
    currency: 'GBP',
    themeColor: '#00e676',
    defaultPrice: 10881.9,
    dayRange: { low: 10796.7, high: 10892.4, base: 10840.4 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'FTSE 100 (UK)', labelRight: 'LSE: ^FTSE', format: (v) => `£${Math.round(v).toLocaleString()} GBP` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'GBP / USD Cable Rate', labelRight: 'FX: GBP/USD', format: () => `$1.3050` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'UK 10-Year Gilt Yield', labelRight: 'BOE BENCHMARK', format: () => `4.185%` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Commodity Weighting', labelRight: 'ENERGY & MINING', format: () => `22.4% Index` }
    ]
  },
  {
    id: 'hangseng',
    category: 'indices',
    symbol: 'HSI',
    name: 'Hang Seng Index (Hong Kong & China)',
    shortName: 'Hang Seng',
    ticker: '^HSI',
    exchange: 'Hong Kong Exchanges & Clearing (^HSI)',
    unit: 'pts',
    currency: 'HKD',
    themeColor: '#ff1744',
    defaultPrice: 24186.8,
    dayRange: { low: 24087.2, high: 24392.3, base: 24062.7 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'Hang Seng Index', labelRight: 'HKEX: ^HSI', format: (v) => `${Math.round(v).toLocaleString()} HKD` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'USD / HKD Peg Band', labelRight: 'HKMA PEG (7.75-7.85)', format: () => `HK$7.7720` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'PBOC Liquidity Stance', labelRight: 'STIMULUS CYCLE', format: () => `Accommodative` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'USD Converted Index', labelRight: 'FX: USD/HKD', format: (v) => `$${Math.round(v / 7.772).toLocaleString()}` }
    ]
  },

  // ==========================================
  // 3. BENCHMARK ETFS
  // ==========================================
  {
    id: 'spy',
    category: 'etfs',
    symbol: 'SPY',
    name: 'SPDR S&P 500 ETF Trust',
    shortName: 'SPY ETF',
    ticker: 'SPY',
    exchange: 'NYSE Arca (SPY)',
    unit: 'share',
    currency: 'USD',
    themeColor: '#00b0ff',
    defaultPrice: 763.25,
    dayRange: { low: 760.64, high: 773.25, base: 771.79 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'SPDR S&P 500 ETF', labelRight: 'NYSE: SPY', format: (v) => `$${v.toFixed(2)}` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Total Assets (AUM)', labelRight: 'STATE STREET GL', format: () => `$590B+ AUM` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'Expense Ratio', labelRight: 'ANNUAL FEE', format: () => `0.0945%` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Index Tracking Error', labelRight: 'S&P 500 PROXY', format: () => `< 0.02%` }
    ]
  },
  {
    id: 'qqq',
    category: 'etfs',
    symbol: 'QQQ',
    name: 'Invesco QQQ Trust (Nasdaq 100)',
    shortName: 'QQQ ETF',
    ticker: 'QQQ',
    exchange: 'NASDAQ (QQQ)',
    unit: 'share',
    currency: 'USD',
    themeColor: '#00e676',
    defaultPrice: 709.8,
    dayRange: { low: 707.23, high: 725.96, base: 728.0 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'Invesco QQQ Trust', labelRight: 'NASDAQ: QQQ', format: (v) => `$${v.toFixed(2)}` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Total Assets (AUM)', labelRight: 'INVESCO', format: () => `$295B+ AUM` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'Top 10 Tech Concentration', labelRight: 'MEGA-CAP WEIGHT', format: () => `~51.2%` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Expense Ratio', labelRight: 'ANNUAL FEE', format: () => `0.20%` }
    ]
  },
  {
    id: 'iwm',
    category: 'etfs',
    symbol: 'IWM',
    name: 'iShares Russell 2000 ETF',
    shortName: 'IWM ETF',
    ticker: 'IWM',
    exchange: 'NYSE Arca (IWM)',
    unit: 'share',
    currency: 'USD',
    themeColor: '#ffd600',
    defaultPrice: 270.44,
    dayRange: { low: 269.88, high: 275.91, base: 275.08 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'iShares Russell 2000', labelRight: 'NYSE: IWM', format: (v) => `$${v.toFixed(2)}` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Total Assets (AUM)', labelRight: 'BLACKROCK', format: () => `$72B AUM` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'Small-Cap Breadth', labelRight: '2000 HOLDINGS', format: () => `High Breadth` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Expense Ratio', labelRight: 'ANNUAL FEE', format: () => `0.19%` }
    ]
  },
  {
    id: 'vti',
    category: 'etfs',
    symbol: 'VTI',
    name: 'Vanguard Total Stock Market ETF',
    shortName: 'VTI ETF',
    ticker: 'VTI',
    exchange: 'NYSE Arca (VTI)',
    unit: 'share',
    currency: 'USD',
    themeColor: '#00b0ff',
    defaultPrice: 374.07,
    dayRange: { low: 372.74, high: 379.42, base: 378.42 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'Vanguard Total Market', labelRight: 'NYSE: VTI', format: (v) => `$${v.toFixed(2)}` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Total Fund Assets', labelRight: 'VANGUARD', format: () => `$1.6T Total` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'Number of Stocks', labelRight: 'TOTAL US MARKET', format: () => `3,650+ Equities` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Ultra-Low Fee', labelRight: 'EXPENSE RATIO', format: () => `0.03%` }
    ]
  },
  {
    id: 'agg',
    category: 'etfs',
    symbol: 'AGG',
    name: 'iShares Core US Aggregate Bond ETF',
    shortName: 'AGG Bond ETF',
    ticker: 'AGG',
    exchange: 'NYSE Arca (AGG)',
    unit: 'share',
    currency: 'USD',
    themeColor: '#ffd600',
    defaultPrice: 95.38,
    dayRange: { low: 95.22, high: 95.58, base: 95.41 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'US Aggregate Bond ETF', labelRight: 'NYSE: AGG', format: (v) => `$${v.toFixed(2)}` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Average Duration', labelRight: 'INTERMEDIATE BOND', format: () => `6.2 Years` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: '30-Day SEC Yield', labelRight: 'FIXED INCOME RETURN', format: () => `4.72%` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Total Assets (AUM)', labelRight: 'BLACKROCK', format: () => `$115B AUM` }
    ]
  },
  {
    id: 'gld',
    category: 'etfs',
    symbol: 'GLD',
    name: 'SPDR Gold Shares Physical Bullion ETF',
    shortName: 'GLD ETF',
    ticker: 'GLD',
    exchange: 'NYSE Arca (GLD)',
    unit: 'share',
    currency: 'USD',
    themeColor: '#ff9100',
    defaultPrice: 382.01,
    dayRange: { low: 380.89, high: 384.88, base: 382.71 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'SPDR Gold Shares', labelRight: 'NYSE: GLD', format: (v) => `$${v.toFixed(2)}` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Allocated Physical Bullion', labelRight: 'HSBC VAULT LONDON', format: () => `~880 Metric Tons` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'Ounce Fraction per Share', labelRight: 'PHYSICAL BACKING', format: () => `~0.0934 oz/sh` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Total Assets (AUM)', labelRight: 'WORLD GOLD COUNCIL', format: () => `$75B+ AUM` }
    ]
  },
  {
    id: 'uso',
    category: 'etfs',
    symbol: 'USO',
    name: 'United States Oil Fund LP',
    shortName: 'USO Oil ETF',
    ticker: 'USO',
    exchange: 'NYSE Arca (USO)',
    unit: 'share',
    currency: 'USD',
    themeColor: '#ff1744',
    defaultPrice: 161.76,
    dayRange: { low: 155.8, high: 162.38, base: 157.31 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'United States Oil Fund', labelRight: 'NYSE: USO', format: (v) => `$${v.toFixed(2)}` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Futures Roll Exposure', labelRight: 'NYMEX WTI CRUDE', format: () => `Front-Month` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'Contango / Backwardation', labelRight: 'CURVE SPREAD', format: () => `Backwardation` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Total Assets (AUM)', labelRight: 'USCF COMMODITY', format: () => `$1.4B AUM` }
    ]
  },
  {
    id: 'eem',
    category: 'etfs',
    symbol: 'EEM',
    name: 'iShares MSCI Emerging Markets ETF',
    shortName: 'EEM ETF',
    ticker: 'EEM',
    exchange: 'NYSE Arca (EEM)',
    unit: 'share',
    currency: 'USD',
    themeColor: '#00e676',
    defaultPrice: 62.85,
    dayRange: { low: 62.68, high: 63.67, base: 63.96 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'iShares Emerging Markets', labelRight: 'NYSE: EEM', format: (v) => `$${v.toFixed(2)}` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Country Weights', labelRight: 'TAIWAN/CHINA/INDIA', format: () => `Top 3: 58%` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'USD Sensitivity', labelRight: 'DXY CORRELATION', format: () => `Inverse (-0.68)` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Total Assets (AUM)', labelRight: 'BLACKROCK', format: () => `$18B AUM` }
    ]
  },

  // ==========================================
  // 4. SOVEREIGN COUNTRY BONDS & YIELDS
  // ==========================================
  {
    id: 'us10y',
    category: 'bonds',
    symbol: 'US10Y',
    name: 'United States 10-Year Treasury Yield',
    shortName: 'US 10Y Yield',
    ticker: '^TNX',
    exchange: 'CBOE 10-Year Treasury Note Yield (^TNX)',
    unit: '%',
    currency: 'Yield',
    themeColor: '#ffd600',
    defaultPrice: 5.217,
    dayRange: { low: 5.180, high: 5.245, base: 5.200 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'US 10-Year Treasury Yield', labelRight: 'CBOE: ^TNX', style: 'color: #ffd600;', format: (v) => `${v.toFixed(3)}%` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Global Risk-Free Anchor', labelRight: 'DISCOUNT RATE', format: () => `Capital Hurdle` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'Bond Price Direction', labelRight: 'YIELD INVERSE', format: (v) => `${v > 5.0 ? 'Pressure' : 'Stable'}` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Basis Point Change', labelRight: 'DAY SPREAD', format: (v) => `${((v - 5.200) * 100).toFixed(1)} bps` }
    ]
  },
  {
    id: 'us02y',
    category: 'bonds',
    symbol: 'US02Y',
    name: 'United States 2-Year Treasury Yield',
    shortName: 'US 2Y Yield',
    ticker: '^IRX',
    exchange: 'CBOE Short-Term Treasury Yield (Policy Sensitive)',
    unit: '%',
    currency: 'Yield',
    themeColor: '#00e5ff',
    defaultPrice: 4.736,
    dayRange: { low: 4.71, high: 4.783, base: 4.751 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'US 2-Year Treasury Yield', labelRight: 'POLICY: US02Y', format: (v) => `${v.toFixed(3)}%` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: '2Y / 10Y Yield Curve Spread', labelRight: 'RECESSION METRIC', format: () => `+0.332% (Uninverted)` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'Fed Funds Correlation', labelRight: 'RATE EXPECTATIONS', format: () => `98% Corr` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Fed Funds Target Range', labelRight: 'FOMC RATE', format: () => `4.75% - 5.00%` }
    ]
  },
  {
    id: 'bund10y',
    category: 'bonds',
    symbol: 'BUND10Y',
    name: 'German 10-Year Government Bund Yield',
    shortName: 'Germany 10Y Bund',
    ticker: 'DE10Y.F',
    exchange: 'Eurozone Sovereign Risk-Free Benchmark (Bund)',
    unit: '%',
    currency: 'Yield',
    themeColor: '#ffd600',
    defaultPrice: 3.409,
    dayRange: { low: 3.398, high: 3.444, base: 3.407 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'German 10Y Bund Yield', labelRight: 'GERMANY: 10Y BUND', format: (v) => `${v.toFixed(3)}%` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'US - German 10Y Spread', labelRight: 'TRANSATLANTIC GAP', format: () => `+3.002% (US Premium)` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'ECB Deposit Facility Rate', labelRight: 'EUROZONE POLICY', format: () => `3.25%` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'BTP - Bund Spread (Italy)', labelRight: 'PERIPHERAL RISK', format: () => `122 bps` }
    ]
  },
  {
    id: 'gilt10y',
    category: 'bonds',
    symbol: 'GILT10Y',
    name: 'United Kingdom 10-Year Gilt Yield',
    shortName: 'UK 10Y Gilt',
    ticker: 'GB10Y.L',
    exchange: 'Bank of England Benchmark Sovereign Debt (Gilt)',
    unit: '%',
    currency: 'Yield',
    themeColor: '#00e676',
    defaultPrice: 5.377,
    dayRange: { low: 5.347, high: 5.41, base: 5.363 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'UK 10-Year Gilt Yield', labelRight: 'UK DMO: 10Y GILT', format: (v) => `${v.toFixed(3)}%` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Bank of England Base Rate', labelRight: 'BOE MPC POLICY', format: () => `5.00%` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'UK Inflation Trajectory', labelRight: 'CPI BASKET', format: () => `Sticky Services` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'US - UK Yield Spread', labelRight: 'CROSS-CURRENCY', format: () => `+1.032% (US Higher)` }
    ]
  },
  {
    id: 'jgb10y',
    category: 'bonds',
    symbol: 'JGB10Y',
    name: 'Japan 10-Year Government Bond (JGB) Yield',
    shortName: 'Japan 10Y JGB',
    ticker: 'JP10Y.T',
    exchange: 'Ministry of Finance Japan & Bank of Japan Benchmark',
    unit: '%',
    currency: 'Yield',
    themeColor: '#ff1744',
    defaultPrice: 2.941,
    dayRange: { low: 2.86, high: 2.946, base: 2.931 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'Japan 10-Year JGB Yield', labelRight: 'BOJ: 10Y JGB', format: (v) => `${v.toFixed(3)}%` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'BOJ Policy Normalization', labelRight: 'YCC EXIT PHASE', format: () => `0.25% Policy Rate` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'Yen Carry Trade Spread', labelRight: 'US-JP 10Y SPREAD', format: () => `4.252% Wide Gap` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Historical Regime Shift', labelRight: 'EXIT FROM NEGATIVE', format: () => `Multi-Year High` }
    ]
  },

  // ==========================================
  // 5. FOREX & GLOBAL MACRO
  // ==========================================
  {
    id: 'dxy',
    category: 'forex',
    symbol: 'DXY',
    name: 'US Dollar Index (Trade-Weighted DXY)',
    shortName: 'US Dollar Index',
    ticker: 'DX-Y.NYB',
    exchange: 'ICE US Dollar Index Futures (DX-Y.NYB)',
    unit: 'pts',
    currency: 'USD',
    themeColor: '#00e676',
    defaultPrice: 101.78,
    dayRange: { low: 101.58, high: 102.09, base: 102.0 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'US Dollar Index (DXY)', labelRight: 'ICE: DX-Y.NYB', format: (v) => `${v.toFixed(2)} pts` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Euro Weight in Basket', labelRight: '57.6% EUR SHARE', format: () => `Dominant Weight` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'Global Liquidity Bellwether', labelRight: 'CROSS-BORDER FLOW', format: () => `Strong USD Bias` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Emerging Market Pressure', labelRight: 'FX SPREAD', format: () => `Capital Headwind` }
    ]
  },
  {
    id: 'eurusd',
    category: 'forex',
    symbol: 'EURUSD',
    name: 'Euro / US Dollar Currency Pair',
    shortName: 'EUR / USD',
    ticker: 'EURUSD=X',
    exchange: 'Interbank Forex Market (EUR/USD)',
    unit: 'USD',
    currency: 'USD',
    themeColor: '#00b0ff',
    defaultPrice: 1.124,
    dayRange: { low: 1.121, high: 1.127, base: 1.121 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'Euro / US Dollar', labelRight: 'FX: EUR/USD', format: (v) => `$${v.toFixed(4)}` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'ECB - Fed Rate Gap', labelRight: 'POLICY DIFFERENTIAL', format: () => `~150 bps US Lead` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'Purchasing Power Parity', labelRight: 'PPP FAIR VALUE', format: () => `~1.20 Fair Value` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Inverse Dollar Value', labelRight: '1 USD IN EUR', format: (v) => `€${(1 / v).toFixed(4)}` }
    ]
  },
  {
    id: 'usdjpy',
    category: 'forex',
    symbol: 'USDJPY',
    name: 'US Dollar / Japanese Yen Currency Pair',
    shortName: 'USD / JPY',
    ticker: 'USDJPY=X',
    exchange: 'Interbank Forex Market (USD/JPY)',
    unit: 'JPY',
    currency: 'JPY',
    themeColor: '#ff1744',
    defaultPrice: 157.99,
    dayRange: { low: 157.69, high: 158.34, base: 158.14 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'US Dollar / Japanese Yen', labelRight: 'FX: USD/JPY', format: (v) => `¥${v.toFixed(2)}` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Ministry of Finance Watch', labelRight: 'INTERVENTION ZONE', format: () => `152 - 160 Zone` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'Real Interest Rate Spread', labelRight: 'US VS JAPAN', format: () => `+4.25% Spread` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Inverse Yen Value', labelRight: '1000 JPY IN USD', format: (v) => `$${((1000 / v)).toFixed(2)} USD` }
    ]
  },
  {
    id: 'usdthb',
    category: 'forex',
    symbol: 'USDTHB',
    name: 'US Dollar / Thai Baht Forex Exchange',
    shortName: 'USD / THB',
    ticker: 'THB=X',
    exchange: 'Bank of Thailand (THB=X)',
    unit: 'THB',
    currency: 'THB',
    themeColor: '#00e5ff',
    defaultPrice: 33.42,
    dayRange: { low: 33.34, high: 33.54, base: 33.47 },
    cards: [
      { id: 'primary', domId: 'goldUsdDisplay', labelLeft: 'USD / THB Exchange Rate', labelRight: 'BOT: THB=X', format: (v) => `฿${v.toFixed(4)}` },
      { id: 'secondary1', domId: 'usdThbDisplay', labelLeft: 'Inverse Baht Valuation', labelRight: '1 THB IN USD', format: () => `$${(1 / v).toFixed(4)}` },
      { id: 'secondary2', domId: 'bondYieldDisplay', labelLeft: 'BOT Policy Interest Rate', labelRight: 'BANK OF THAILAND', format: () => `2.25% Policy Rate` },
      { id: 'derived', domId: 'goldThaiBahtDisplay', labelLeft: 'Gold Price Converter Multiplier', labelRight: '1 TROY OZ IN THB', format: (v) => `฿${Math.round(4169.3 * v).toLocaleString()}` }
    ]
  }
];

if (typeof window !== "undefined") {
  window.INSTRUMENT_CATEGORIES = INSTRUMENT_CATEGORIES;
  window.MACRO_CATALOG = MACRO_CATALOG;
}

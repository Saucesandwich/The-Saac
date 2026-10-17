  const INSTRUMENTS = {
    gold: {
      id: 'gold',
      category: 'commodities',
      symbol: 'XAU',
      title: 'Gold, Baht & US Bond Market Terminal',
      subtitle: 'CME COMEX Gold Futures (GC=F) • Bank of Thailand (THB=X) • CBOE US10Y (^TNX)',
      shortName: 'Gold',
      currency: 'USD',
      unit: 'oz',
      ticker: 'GC=F',
      themeColor: '#ff9100',
      basePrice: 4169.3,
      dayBase: 4159.0,
      dayLow: 4165.50,
      dayHigh: 4193.50,
      card1: { title: 'Gold Futures (US Market)', sub: 'COMEX: GC=F' },
      card2: { title: 'Forex Exchange Rate', sub: 'FX: USD / THB' },
      card3: { title: 'US 10-Year Treasury Yield', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Thai Gold Bar (1 บาททอง)', sub: 'THAI GOLD: 96.5% BAR' },
      overlay0: 'Gold (USD/oz)',
      overlay1: 'USD / THB (฿)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: computeDerived
    },
    silver: {
      id: 'silver',
      category: 'commodities',
      symbol: 'XAG',
      title: 'Silver Futures & Gold-Silver Ratio',
      subtitle: 'CME COMEX Silver Futures (SI=F)',
      shortName: 'Silver',
      currency: 'USD',
      unit: 'oz',
      ticker: 'SI=F',
      themeColor: '#ffffff',
      basePrice: 32.4,
      dayBase: 32.34,
      dayLow: 32.21,
      dayHigh: 32.59,
      card1: { title: 'Silver Spot / Futures', sub: 'MARKET: SI=F' },
      card2: { title: 'USD / THB Forex', sub: 'FX: USD / THB' },
      card3: { title: 'US 10Y Yield', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Contract Notional (oz)', sub: 'LOT SIZE BENCHMARK' },
      overlay0: 'Silver (XAG)',
      overlay1: 'USD / THB (฿)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (32.4 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    crude_oil: {
      id: 'crude_oil',
      category: 'commodities',
      symbol: 'CL',
      title: 'WTI & Brent Crude Oil Benchmark',
      subtitle: 'NYMEX Light Sweet Crude (CL=F) • ICE Brent (BZ=F)',
      shortName: 'Crude Oil',
      currency: 'USD',
      unit: 'bbl',
      ticker: 'CL=F',
      themeColor: '#ff1744',
      basePrice: 78.4,
      dayBase: 78.24,
      dayLow: 77.93,
      dayHigh: 78.87,
      card1: { title: 'Crude Oil Spot / Futures', sub: 'MARKET: CL=F' },
      card2: { title: 'USD / THB Forex', sub: 'FX: USD / THB' },
      card3: { title: 'US 10Y Yield', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Contract Notional (bbl)', sub: 'LOT SIZE BENCHMARK' },
      overlay0: 'Crude Oil (CL)',
      overlay1: 'USD / THB (฿)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (78.4 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    natural_gas: {
      id: 'natural_gas',
      category: 'commodities',
      symbol: 'NG',
      title: 'Natural Gas Henry Hub Spot',
      subtitle: 'NYMEX Henry Hub Natural Gas (NG=F)',
      shortName: 'Natural Gas',
      currency: 'USD',
      unit: 'MMBtu',
      ticker: 'NG=F',
      themeColor: '#00e5ff',
      basePrice: 2.85,
      dayBase: 2.84,
      dayLow: 2.83,
      dayHigh: 2.87,
      card1: { title: 'Natural Gas Spot / Futures', sub: 'MARKET: NG=F' },
      card2: { title: 'USD / THB Forex', sub: 'FX: USD / THB' },
      card3: { title: 'US 10Y Yield', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Contract Notional (MMBtu)', sub: 'LOT SIZE BENCHMARK' },
      overlay0: 'Natural Gas (NG)',
      overlay1: 'USD / THB (฿)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (2.85 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    copper: {
      id: 'copper',
      category: 'commodities',
      symbol: 'HG',
      title: 'Copper Futures (Doctor Copper)',
      subtitle: 'CME COMEX High Grade Copper (HG=F)',
      shortName: 'Copper',
      currency: 'USD',
      unit: 'lb',
      ticker: 'HG=F',
      themeColor: '#ff9100',
      basePrice: 4.45,
      dayBase: 4.44,
      dayLow: 4.42,
      dayHigh: 4.48,
      card1: { title: 'Copper Spot / Futures', sub: 'MARKET: HG=F' },
      card2: { title: 'USD / THB Forex', sub: 'FX: USD / THB' },
      card3: { title: 'US 10Y Yield', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Contract Notional (lb)', sub: 'LOT SIZE BENCHMARK' },
      overlay0: 'Copper (HG)',
      overlay1: 'USD / THB (฿)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (4.45 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    sp500: {
      id: 'sp500',
      category: 'indices',
      symbol: 'SPX',
      title: 'S&P 500 Macro Benchmark Terminal',
      subtitle: 'S&P Dow Jones Indices (^GSPC) • SPDR S&P 500 ETF (SPY) • CBOE VIX (^VIX)',
      shortName: 'S&P 500',
      currency: 'USD',
      unit: 'pts',
      ticker: '^GSPC',
      themeColor: '#00b0ff',
      basePrice: 5850.2,
      dayBase: 5835.0,
      dayLow: 5820.0,
      dayHigh: 5875.0,
      card1: { title: 'S&P 500 Large-Cap', sub: 'INDEX: ^GSPC' },
      card2: { title: 'SPDR S&P 500 ETF', sub: 'ETF: SPY' },
      card3: { title: 'CBOE Volatility Index', sub: 'VOLATILITY: ^VIX' },
      card4: { title: 'Micro E-Mini S&P Notional', sub: 'CME: MES ($5/PT)' },
      overlay0: 'S&P 500 (^GSPC)',
      overlay1: 'SPDR SPY ($)',
      overlay2: 'CBOE VIX (pts)',
      computeDerived: (raw) => {
        const c = Number(raw.close !== undefined ? raw.close : 5850.2);
        const o = Number(raw.open !== undefined ? raw.open : c);
        const h = Number(raw.high !== undefined ? raw.high : Math.max(o, c));
        const l = Number(raw.low !== undefined ? raw.low : Math.min(o, c));
        const spy = c / 10.0;
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: spy, thb: spy,
          us10y: 15.42, bond: 15.42,
          gold_thb_oz: spy,
          pure_gram_thb: spy / 31.1034768,
          thai_gold_bar: c * 5.0,
          thai_gold_ornament: c * 50.0,
          note: raw.note || ''
        };
      }
    },
    nasdaq: {
      id: 'nasdaq',
      category: 'indices',
      symbol: 'IXIC',
      title: 'Nasdaq Composite Tech Equity Terminal',
      subtitle: 'NASDAQ Global Select (^IXIC) • Invesco QQQ (QQQ) • CBOE US10Y (^TNX)',
      shortName: 'Nasdaq',
      currency: 'USD',
      unit: 'pts',
      ticker: '^IXIC',
      themeColor: '#00e676',
      basePrice: 20340.5,
      dayBase: 20280.0,
      dayLow: 20210.0,
      dayHigh: 20450.0,
      card1: { title: 'Nasdaq Composite Index', sub: 'NASDAQ: ^IXIC' },
      card2: { title: 'Invesco QQQ Trust', sub: 'ETF: QQQ' },
      card3: { title: 'US 10-Year Treasury Yield', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Micro E-Mini Notional', sub: 'CME: MNQ ($2/PT)' },
      overlay0: 'Nasdaq (^IXIC)',
      overlay1: 'Invesco QQQ ($)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const c = Number(raw.close !== undefined ? raw.close : (raw.nasdaq || 20340.5));
        const o = Number(raw.open !== undefined ? raw.open : c);
        const h = Number(raw.high !== undefined ? raw.high : Math.max(o, c));
        const l = Number(raw.low !== undefined ? raw.low : Math.min(o, c));
        const qqq = c / 41.0;
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: qqq, thb: qqq,
          us10y: bond, bond: bond,
          gold_thb_oz: qqq,
          pure_gram_thb: qqq / 31.1034768,
          thai_gold_bar: c * 2.0,
          thai_gold_ornament: c * 20.0,
          note: raw.note || ''
        };
      }
    },
    dowjones: {
      id: 'dowjones',
      category: 'indices',
      symbol: 'DJI',
      title: 'Dow Jones Industrial Average',
      subtitle: 'S&P Dow Jones Indices (^DJI)',
      shortName: 'Dow Jones',
      currency: 'USD',
      unit: 'pts',
      ticker: '^DJI',
      themeColor: '#00b0ff',
      basePrice: 42950.0,
      dayBase: 42864.1,
      dayLow: 42692.3,
      dayHigh: 43207.7,
      card1: { title: 'Dow Jones Benchmark', sub: 'INDEX: ^DJI' },
      card2: { title: 'Tracking ETF Proxy', sub: 'ETF BENCHMARK' },
      card3: { title: 'US 10Y Discount Rate', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Futures Notional', sub: 'EQUITY DERIVATIVES' },
      overlay0: 'Dow Jones (DJI)',
      overlay1: 'ETF Proxy ($)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (42950.0 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    russell2000: {
      id: 'russell2000',
      category: 'indices',
      symbol: 'RUT',
      title: 'Russell 2000 US Small-Cap Index',
      subtitle: 'FTSE Russell Indices (^RUT)',
      shortName: 'Russell 2000',
      currency: 'USD',
      unit: 'pts',
      ticker: '^RUT',
      themeColor: '#ffd600',
      basePrice: 2240.8,
      dayBase: 2236.32,
      dayLow: 2227.36,
      dayHigh: 2254.24,
      card1: { title: 'Russell 2000 Benchmark', sub: 'INDEX: ^RUT' },
      card2: { title: 'Tracking ETF Proxy', sub: 'ETF BENCHMARK' },
      card3: { title: 'US 10Y Discount Rate', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Futures Notional', sub: 'EQUITY DERIVATIVES' },
      overlay0: 'Russell 2000 (RUT)',
      overlay1: 'ETF Proxy ($)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (2240.8 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    nikkei225: {
      id: 'nikkei225',
      category: 'indices',
      symbol: 'N225',
      title: 'Nikkei 225 Japan Benchmark',
      subtitle: 'Tokyo Stock Exchange (^N225)',
      shortName: 'Nikkei 225',
      currency: 'JPY',
      unit: 'pts',
      ticker: '^N225',
      themeColor: '#ff1744',
      basePrice: 38950.0,
      dayBase: 38872.1,
      dayLow: 38716.3,
      dayHigh: 39183.7,
      card1: { title: 'Nikkei 225 Benchmark', sub: 'INDEX: ^N225' },
      card2: { title: 'Tracking ETF Proxy', sub: 'ETF BENCHMARK' },
      card3: { title: 'US 10Y Discount Rate', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Futures Notional', sub: 'EQUITY DERIVATIVES' },
      overlay0: 'Nikkei 225 (N225)',
      overlay1: 'ETF Proxy ($)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (38950.0 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    dax40: {
      id: 'dax40',
      category: 'indices',
      symbol: 'DAX',
      title: 'DAX 40 Germany Blue-Chip Index',
      subtitle: 'Deutsche Börse XETRA (^GDAXI)',
      shortName: 'DAX 40',
      currency: 'EUR',
      unit: 'pts',
      ticker: '^GDAXI',
      themeColor: '#ffd600',
      basePrice: 19480.0,
      dayBase: 19441.04,
      dayLow: 19363.12,
      dayHigh: 19596.88,
      card1: { title: 'DAX 40 Benchmark', sub: 'INDEX: ^GDAXI' },
      card2: { title: 'Tracking ETF Proxy', sub: 'ETF BENCHMARK' },
      card3: { title: 'US 10Y Discount Rate', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Futures Notional', sub: 'EQUITY DERIVATIVES' },
      overlay0: 'DAX 40 (DAX)',
      overlay1: 'ETF Proxy ($)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (19480.0 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    ftse100: {
      id: 'ftse100',
      category: 'indices',
      symbol: 'FTSE',
      title: 'FTSE 100 London UK Index',
      subtitle: 'London Stock Exchange (^FTSE)',
      shortName: 'FTSE 100',
      currency: 'GBP',
      unit: 'pts',
      ticker: '^FTSE',
      themeColor: '#00e676',
      basePrice: 8250.0,
      dayBase: 8233.5,
      dayLow: 8200.5,
      dayHigh: 8299.5,
      card1: { title: 'FTSE 100 Benchmark', sub: 'INDEX: ^FTSE' },
      card2: { title: 'Tracking ETF Proxy', sub: 'ETF BENCHMARK' },
      card3: { title: 'US 10Y Discount Rate', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Futures Notional', sub: 'EQUITY DERIVATIVES' },
      overlay0: 'FTSE 100 (FTSE)',
      overlay1: 'ETF Proxy ($)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (8250.0 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    hangseng: {
      id: 'hangseng',
      category: 'indices',
      symbol: 'HSI',
      title: 'Hang Seng Index (Hong Kong & China)',
      subtitle: 'Hong Kong Exchanges & Clearing (^HSI)',
      shortName: 'Hang Seng',
      currency: 'HKD',
      unit: 'pts',
      ticker: '^HSI',
      themeColor: '#ff1744',
      basePrice: 20600.0,
      dayBase: 20558.8,
      dayLow: 20476.4,
      dayHigh: 20723.6,
      card1: { title: 'Hang Seng Benchmark', sub: 'INDEX: ^HSI' },
      card2: { title: 'Tracking ETF Proxy', sub: 'ETF BENCHMARK' },
      card3: { title: 'US 10Y Discount Rate', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Futures Notional', sub: 'EQUITY DERIVATIVES' },
      overlay0: 'Hang Seng (HSI)',
      overlay1: 'ETF Proxy ($)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (20600.0 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    spy: {
      id: 'spy',
      category: 'etfs',
      symbol: 'SPY',
      title: 'SPDR S&P 500 ETF Trust',
      subtitle: 'NYSE Arca (SPY)',
      shortName: 'SPY ETF',
      currency: 'USD',
      unit: 'share',
      ticker: 'SPY',
      themeColor: '#00b0ff',
      basePrice: 584.5,
      dayBase: 583.33,
      dayLow: 580.99,
      dayHigh: 588.01,
      card1: { title: 'SPY ETF ETF Net Asset Value', sub: 'ETF: SPY' },
      card2: { title: 'AUM & Liquidity Depth', sub: 'INSTITUTIONAL FLOW' },
      card3: { title: 'Benchmark Index Tracking', sub: 'UNDERLYING INDEX' },
      card4: { title: 'Daily Turnover Volume', sub: 'MARKET LIQUIDITY' },
      overlay0: 'SPY ETF (SPY)',
      overlay1: 'Tracking Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (584.5 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    qqq: {
      id: 'qqq',
      category: 'etfs',
      symbol: 'QQQ',
      title: 'Invesco QQQ Trust (Nasdaq 100)',
      subtitle: 'NASDAQ (QQQ)',
      shortName: 'QQQ ETF',
      currency: 'USD',
      unit: 'share',
      ticker: 'QQQ',
      themeColor: '#00e676',
      basePrice: 495.2,
      dayBase: 494.21,
      dayLow: 492.23,
      dayHigh: 498.17,
      card1: { title: 'QQQ ETF ETF Net Asset Value', sub: 'ETF: QQQ' },
      card2: { title: 'AUM & Liquidity Depth', sub: 'INSTITUTIONAL FLOW' },
      card3: { title: 'Benchmark Index Tracking', sub: 'UNDERLYING INDEX' },
      card4: { title: 'Daily Turnover Volume', sub: 'MARKET LIQUIDITY' },
      overlay0: 'QQQ ETF (QQQ)',
      overlay1: 'Tracking Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (495.2 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    iwm: {
      id: 'iwm',
      category: 'etfs',
      symbol: 'IWM',
      title: 'iShares Russell 2000 ETF',
      subtitle: 'NYSE Arca (IWM)',
      shortName: 'IWM ETF',
      currency: 'USD',
      unit: 'share',
      ticker: 'IWM',
      themeColor: '#ffd600',
      basePrice: 222.8,
      dayBase: 222.35,
      dayLow: 221.46,
      dayHigh: 224.14,
      card1: { title: 'IWM ETF ETF Net Asset Value', sub: 'ETF: IWM' },
      card2: { title: 'AUM & Liquidity Depth', sub: 'INSTITUTIONAL FLOW' },
      card3: { title: 'Benchmark Index Tracking', sub: 'UNDERLYING INDEX' },
      card4: { title: 'Daily Turnover Volume', sub: 'MARKET LIQUIDITY' },
      overlay0: 'IWM ETF (IWM)',
      overlay1: 'Tracking Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (222.8 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    vti: {
      id: 'vti',
      category: 'etfs',
      symbol: 'VTI',
      title: 'Vanguard Total Stock Market ETF',
      subtitle: 'NYSE Arca (VTI)',
      shortName: 'VTI ETF',
      currency: 'USD',
      unit: 'share',
      ticker: 'VTI',
      themeColor: '#00b0ff',
      basePrice: 282.4,
      dayBase: 281.84,
      dayLow: 280.71,
      dayHigh: 284.09,
      card1: { title: 'VTI ETF ETF Net Asset Value', sub: 'ETF: VTI' },
      card2: { title: 'AUM & Liquidity Depth', sub: 'INSTITUTIONAL FLOW' },
      card3: { title: 'Benchmark Index Tracking', sub: 'UNDERLYING INDEX' },
      card4: { title: 'Daily Turnover Volume', sub: 'MARKET LIQUIDITY' },
      overlay0: 'VTI ETF (VTI)',
      overlay1: 'Tracking Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (282.4 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    agg: {
      id: 'agg',
      category: 'etfs',
      symbol: 'AGG',
      title: 'iShares Core US Aggregate Bond ETF',
      subtitle: 'NYSE Arca (AGG)',
      shortName: 'AGG Bond ETF',
      currency: 'USD',
      unit: 'share',
      ticker: 'AGG',
      themeColor: '#ffd600',
      basePrice: 97.8,
      dayBase: 97.6,
      dayLow: 97.21,
      dayHigh: 98.39,
      card1: { title: 'AGG Bond ETF ETF Net Asset Value', sub: 'ETF: AGG' },
      card2: { title: 'AUM & Liquidity Depth', sub: 'INSTITUTIONAL FLOW' },
      card3: { title: 'Benchmark Index Tracking', sub: 'UNDERLYING INDEX' },
      card4: { title: 'Daily Turnover Volume', sub: 'MARKET LIQUIDITY' },
      overlay0: 'AGG Bond ETF (AGG)',
      overlay1: 'Tracking Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (97.8 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    gld: {
      id: 'gld',
      category: 'etfs',
      symbol: 'GLD',
      title: 'SPDR Gold Shares Physical Bullion ETF',
      subtitle: 'NYSE Arca (GLD)',
      shortName: 'GLD ETF',
      currency: 'USD',
      unit: 'share',
      ticker: 'GLD',
      themeColor: '#ff9100',
      basePrice: 252.6,
      dayBase: 252.09,
      dayLow: 251.08,
      dayHigh: 254.12,
      card1: { title: 'GLD ETF ETF Net Asset Value', sub: 'ETF: GLD' },
      card2: { title: 'AUM & Liquidity Depth', sub: 'INSTITUTIONAL FLOW' },
      card3: { title: 'Benchmark Index Tracking', sub: 'UNDERLYING INDEX' },
      card4: { title: 'Daily Turnover Volume', sub: 'MARKET LIQUIDITY' },
      overlay0: 'GLD ETF (GLD)',
      overlay1: 'Tracking Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (252.6 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    uso: {
      id: 'uso',
      category: 'etfs',
      symbol: 'USO',
      title: 'United States Oil Fund LP',
      subtitle: 'NYSE Arca (USO)',
      shortName: 'USO Oil ETF',
      currency: 'USD',
      unit: 'share',
      ticker: 'USO',
      themeColor: '#ff1744',
      basePrice: 74.2,
      dayBase: 74.05,
      dayLow: 73.75,
      dayHigh: 74.65,
      card1: { title: 'USO Oil ETF ETF Net Asset Value', sub: 'ETF: USO' },
      card2: { title: 'AUM & Liquidity Depth', sub: 'INSTITUTIONAL FLOW' },
      card3: { title: 'Benchmark Index Tracking', sub: 'UNDERLYING INDEX' },
      card4: { title: 'Daily Turnover Volume', sub: 'MARKET LIQUIDITY' },
      overlay0: 'USO Oil ETF (USO)',
      overlay1: 'Tracking Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (74.2 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    eem: {
      id: 'eem',
      category: 'etfs',
      symbol: 'EEM',
      title: 'iShares MSCI Emerging Markets ETF',
      subtitle: 'NYSE Arca (EEM)',
      shortName: 'EEM ETF',
      currency: 'USD',
      unit: 'share',
      ticker: 'EEM',
      themeColor: '#00e676',
      basePrice: 44.8,
      dayBase: 44.71,
      dayLow: 44.53,
      dayHigh: 45.07,
      card1: { title: 'EEM ETF ETF Net Asset Value', sub: 'ETF: EEM' },
      card2: { title: 'AUM & Liquidity Depth', sub: 'INSTITUTIONAL FLOW' },
      card3: { title: 'Benchmark Index Tracking', sub: 'UNDERLYING INDEX' },
      card4: { title: 'Daily Turnover Volume', sub: 'MARKET LIQUIDITY' },
      overlay0: 'EEM ETF (EEM)',
      overlay1: 'Tracking Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (44.8 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    us10y: {
      id: 'us10y',
      category: 'bonds',
      symbol: 'US10Y',
      title: 'United States 10-Year Treasury Yield',
      subtitle: 'CBOE 10-Year Treasury Note Yield (^TNX)',
      shortName: 'US 10Y Yield',
      currency: 'Yield',
      unit: '%',
      ticker: '^TNX',
      themeColor: '#ffd600',
      basePrice: 5.217,
      dayBase: 5.21,
      dayLow: 5.19,
      dayHigh: 5.25,
      card1: { title: 'US 10Y Yield Yield', sub: 'BENCHMARK: ^TNX' },
      card2: { title: 'Yield Curve Slope', sub: 'TERM PREMIUM' },
      card3: { title: 'Real Yield / Breakeven', sub: 'INFLATION EXPECTATIONS' },
      card4: { title: 'Bond Equivalent Price', sub: 'PAR: 100.00' },
      overlay0: 'US 10Y Yield (US10Y %)',
      overlay1: 'Curve Slope (bps)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (5.217 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    us02y: {
      id: 'us02y',
      category: 'bonds',
      symbol: 'US02Y',
      title: 'United States 2-Year Treasury Yield',
      subtitle: 'CBOE Short-Term Treasury Yield (Policy Sensitive)',
      shortName: 'US 2Y Yield',
      currency: 'Yield',
      unit: '%',
      ticker: '^IRX',
      themeColor: '#00e5ff',
      basePrice: 4.885,
      dayBase: 4.88,
      dayLow: 4.86,
      dayHigh: 4.91,
      card1: { title: 'US 2Y Yield Yield', sub: 'BENCHMARK: ^IRX' },
      card2: { title: 'Yield Curve Slope', sub: 'TERM PREMIUM' },
      card3: { title: 'Real Yield / Breakeven', sub: 'INFLATION EXPECTATIONS' },
      card4: { title: 'Bond Equivalent Price', sub: 'PAR: 100.00' },
      overlay0: 'US 2Y Yield (US02Y %)',
      overlay1: 'Curve Slope (bps)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (4.885 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    bund10y: {
      id: 'bund10y',
      category: 'bonds',
      symbol: 'BUND10Y',
      title: 'German 10-Year Government Bund Yield',
      subtitle: 'Eurozone Sovereign Risk-Free Benchmark (Bund)',
      shortName: 'Germany 10Y Bund',
      currency: 'Yield',
      unit: '%',
      ticker: 'DE10Y.F',
      themeColor: '#ffd600',
      basePrice: 2.215,
      dayBase: 2.21,
      dayLow: 2.2,
      dayHigh: 2.23,
      card1: { title: 'Germany 10Y Bund Yield', sub: 'BENCHMARK: DE10Y.F' },
      card2: { title: 'Yield Curve Slope', sub: 'TERM PREMIUM' },
      card3: { title: 'Real Yield / Breakeven', sub: 'INFLATION EXPECTATIONS' },
      card4: { title: 'Bond Equivalent Price', sub: 'PAR: 100.00' },
      overlay0: 'Germany 10Y Bund (BUND10Y %)',
      overlay1: 'Curve Slope (bps)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (2.215 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    gilt10y: {
      id: 'gilt10y',
      category: 'bonds',
      symbol: 'GILT10Y',
      title: 'United Kingdom 10-Year Gilt Yield',
      subtitle: 'Bank of England Benchmark Sovereign Debt (Gilt)',
      shortName: 'UK 10Y Gilt',
      currency: 'Yield',
      unit: '%',
      ticker: 'GB10Y.L',
      themeColor: '#00e676',
      basePrice: 4.185,
      dayBase: 4.18,
      dayLow: 4.16,
      dayHigh: 4.21,
      card1: { title: 'UK 10Y Gilt Yield', sub: 'BENCHMARK: GB10Y.L' },
      card2: { title: 'Yield Curve Slope', sub: 'TERM PREMIUM' },
      card3: { title: 'Real Yield / Breakeven', sub: 'INFLATION EXPECTATIONS' },
      card4: { title: 'Bond Equivalent Price', sub: 'PAR: 100.00' },
      overlay0: 'UK 10Y Gilt (GILT10Y %)',
      overlay1: 'Curve Slope (bps)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (4.185 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    jgb10y: {
      id: 'jgb10y',
      category: 'bonds',
      symbol: 'JGB10Y',
      title: 'Japan 10-Year Government Bond (JGB) Yield',
      subtitle: 'Ministry of Finance Japan & Bank of Japan Benchmark',
      shortName: 'Japan 10Y JGB',
      currency: 'Yield',
      unit: '%',
      ticker: 'JP10Y.T',
      themeColor: '#ff1744',
      basePrice: 0.965,
      dayBase: 0.96,
      dayLow: 0.96,
      dayHigh: 0.97,
      card1: { title: 'Japan 10Y JGB Yield', sub: 'BENCHMARK: JP10Y.T' },
      card2: { title: 'Yield Curve Slope', sub: 'TERM PREMIUM' },
      card3: { title: 'Real Yield / Breakeven', sub: 'INFLATION EXPECTATIONS' },
      card4: { title: 'Bond Equivalent Price', sub: 'PAR: 100.00' },
      overlay0: 'Japan 10Y JGB (JGB10Y %)',
      overlay1: 'Curve Slope (bps)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (0.965 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    dxy: {
      id: 'dxy',
      category: 'forex',
      symbol: 'DXY',
      title: 'US Dollar Index (Trade-Weighted DXY)',
      subtitle: 'ICE US Dollar Index Futures (DX-Y.NYB)',
      shortName: 'US Dollar Index',
      currency: 'USD',
      unit: 'pts',
      ticker: 'DX-Y.NYB',
      themeColor: '#00e676',
      basePrice: 103.45,
      dayBase: 103.24,
      dayLow: 102.83,
      dayHigh: 104.07,
      card1: { title: 'US Dollar Index Exchange Rate', sub: 'FX: DX-Y.NYB' },
      card2: { title: 'US Dollar Index DXY', sub: 'MACRO DOLLAR' },
      card3: { title: 'Interest Rate Differential', sub: 'POLICY SPREAD' },
      card4: { title: 'Purchasing Power Parity', sub: 'PPP FAIR VALUE' },
      overlay0: 'US Dollar Index (DXY)',
      overlay1: 'US Dollar Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (103.45 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    eurusd: {
      id: 'eurusd',
      category: 'forex',
      symbol: 'EURUSD',
      title: 'Euro / US Dollar Currency Pair',
      subtitle: 'Interbank Forex Market (EUR/USD)',
      shortName: 'EUR / USD',
      currency: 'USD',
      unit: 'USD',
      ticker: 'EURUSD=X',
      themeColor: '#00b0ff',
      basePrice: 1.085,
      dayBase: 1.08,
      dayLow: 1.08,
      dayHigh: 1.09,
      card1: { title: 'EUR / USD Exchange Rate', sub: 'FX: EURUSD=X' },
      card2: { title: 'US Dollar Index DXY', sub: 'MACRO DOLLAR' },
      card3: { title: 'Interest Rate Differential', sub: 'POLICY SPREAD' },
      card4: { title: 'Purchasing Power Parity', sub: 'PPP FAIR VALUE' },
      overlay0: 'EUR / USD (EURUSD)',
      overlay1: 'US Dollar Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (1.085 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    usdjpy: {
      id: 'usdjpy',
      category: 'forex',
      symbol: 'USDJPY',
      title: 'US Dollar / Japanese Yen Currency Pair',
      subtitle: 'Interbank Forex Market (USD/JPY)',
      shortName: 'USD / JPY',
      currency: 'JPY',
      unit: 'JPY',
      ticker: 'USDJPY=X',
      themeColor: '#ff1744',
      basePrice: 149.5,
      dayBase: 149.2,
      dayLow: 148.6,
      dayHigh: 150.4,
      card1: { title: 'USD / JPY Exchange Rate', sub: 'FX: USDJPY=X' },
      card2: { title: 'US Dollar Index DXY', sub: 'MACRO DOLLAR' },
      card3: { title: 'Interest Rate Differential', sub: 'POLICY SPREAD' },
      card4: { title: 'Purchasing Power Parity', sub: 'PPP FAIR VALUE' },
      overlay0: 'USD / JPY (USDJPY)',
      overlay1: 'US Dollar Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (149.5 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    usdthb: {
      id: 'usdthb',
      category: 'forex',
      symbol: 'USDTHB',
      title: 'US Dollar / Thai Baht Forex Exchange',
      subtitle: 'Bank of Thailand (THB=X)',
      shortName: 'USD / THB',
      currency: 'THB',
      unit: 'THB',
      ticker: 'THB=X',
      themeColor: '#00e5ff',
      basePrice: 33.56,
      dayBase: 33.49,
      dayLow: 33.36,
      dayHigh: 33.76,
      card1: { title: 'USD / THB Exchange Rate', sub: 'FX: THB=X' },
      card2: { title: 'US Dollar Index DXY', sub: 'MACRO DOLLAR' },
      card3: { title: 'Interest Rate Differential', sub: 'POLICY SPREAD' },
      card4: { title: 'Purchasing Power Parity', sub: 'PPP FAIR VALUE' },
      overlay0: 'USD / THB (USDTHB)',
      overlay1: 'US Dollar Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (33.56 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.217);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.56);
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        };
      }
    },
    crypto: {
      id: 'crypto',
      category: 'forex',
      symbol: 'BTC',
      title: 'Bitcoin Digital Asset Terminal',
      subtitle: 'CME Group / Binance (BTC-USD) • Ethereum (ETH-USD) • US Dollar Index (DXY)',
      shortName: 'Bitcoin',
      currency: 'USD',
      unit: 'BTC',
      ticker: 'BTC-USD',
      themeColor: '#ffd600',
      basePrice: 68450.0,
      dayBase: 68100.0,
      dayLow: 67800.0,
      dayHigh: 69200.0,
      card1: { title: 'Bitcoin Spot', sub: 'CRYPTO: BTC-USD' },
      card2: { title: 'Ethereum / USD', sub: 'CRYPTO: ETH-USD' },
      card3: { title: 'US Dollar Index', sub: 'CURRENCY: DXY' },
      card4: { title: 'Satoshis Per Dollar', sub: 'UNIT: 100M SATS/BTC' },
      overlay0: 'Bitcoin (BTC)',
      overlay1: 'Ethereum (ETH)',
      overlay2: 'US Dollar Index',
      computeDerived: (raw) => {
        const c = Number(raw.close !== undefined ? raw.close : 68450.0);
        const o = Number(raw.open !== undefined ? raw.open : c);
        const h = Number(raw.high !== undefined ? raw.high : Math.max(o, c));
        const l = Number(raw.low !== undefined ? raw.low : Math.min(o, c));
        const eth = c * 0.038;
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: eth, thb: eth,
          us10y: 103.45, bond: 103.45,
          gold_thb_oz: eth,
          pure_gram_thb: eth / 31.1034768,
          thai_gold_bar: Math.round(100000000 / c),
          thai_gold_ornament: Math.round(100000000 / c),
          note: raw.note || ''
        };
      }
    }
  };
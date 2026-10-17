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
      livePrice: 4169.3,
      dayBase: 4159.0,
      dayOpen: 4159.0,
      dayLow: 4165.50,
      dayHigh: 4193.50,
      low52w: 3901.30,
      high52w: 5586.20,
      ytdPct: 54.2,
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
      basePrice: 57.13,
      livePrice: 57.13,
      dayBase: 56.84,
      dayOpen: 56.99,
      dayLow: 56.99,
      dayHigh: 57.13,
      low52w: 45.85,
      high52w: 121.3,
      ytdPct: -19.96,
      card1: { title: 'Silver Spot / Futures', sub: 'MARKET: SI=F' },
      card2: { title: 'USD / THB Forex', sub: 'FX: USD / THB' },
      card3: { title: 'US 10Y Yield', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Contract Notional (oz)', sub: 'LOT SIZE BENCHMARK' },
      overlay0: 'Silver (XAG)',
      overlay1: 'USD / THB (฿)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (57.13 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 99.04,
      livePrice: 99.04,
      dayBase: 97.97,
      dayOpen: 97.55,
      dayLow: 96.85,
      dayHigh: 101.9,
      low52w: 54.98,
      high52w: 119.48,
      ytdPct: 72.51,
      card1: { title: 'Crude Oil Spot / Futures', sub: 'MARKET: CL=F' },
      card2: { title: 'USD / THB Forex', sub: 'FX: USD / THB' },
      card3: { title: 'US 10Y Yield', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Contract Notional (bbl)', sub: 'LOT SIZE BENCHMARK' },
      overlay0: 'Crude Oil (CL)',
      overlay1: 'USD / THB (฿)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (99.04 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 3.117,
      livePrice: 3.117,
      dayBase: 3.236,
      dayOpen: 3.212,
      dayLow: 3.062,
      dayHigh: 3.229,
      low52w: 2.483,
      high52w: 7.827,
      ytdPct: -15.28,
      card1: { title: 'Natural Gas Spot / Futures', sub: 'MARKET: NG=F' },
      card2: { title: 'USD / THB Forex', sub: 'FX: USD / THB' },
      card3: { title: 'US 10Y Yield', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Contract Notional (MMBtu)', sub: 'LOT SIZE BENCHMARK' },
      overlay0: 'Natural Gas (NG)',
      overlay1: 'USD / THB (฿)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (3.117 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 6.562,
      livePrice: 6.562,
      dayBase: 6.511,
      dayOpen: 6.574,
      dayLow: 6.531,
      dayHigh: 6.607,
      low52w: 4.905,
      high52w: 6.83,
      ytdPct: 16.08,
      card1: { title: 'Copper Spot / Futures', sub: 'MARKET: HG=F' },
      card2: { title: 'USD / THB Forex', sub: 'FX: USD / THB' },
      card3: { title: 'US 10Y Yield', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Contract Notional (lb)', sub: 'LOT SIZE BENCHMARK' },
      overlay0: 'Copper (HG)',
      overlay1: 'USD / THB (฿)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (6.562 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 7659.4,
      livePrice: 7659.4,
      dayBase: 7744.1,
      dayOpen: 7745.3,
      dayLow: 7631.8,
      dayHigh: 7756.8,
      low52w: 6316.9,
      high52w: 7844.5,
      ytdPct: 11.36,
      card1: { title: 'S&P 500 Large-Cap', sub: 'INDEX: ^GSPC' },
      card2: { title: 'SPDR S&P 500 ETF', sub: 'ETF: SPY' },
      card3: { title: 'CBOE Volatility Index', sub: 'VOLATILITY: ^VIX' },
      card4: { title: 'Micro E-Mini S&P Notional', sub: 'CME: MES ($5/PT)' },
      overlay0: 'S&P 500 (^GSPC)',
      overlay1: 'SPDR SPY ($)',
      overlay2: 'CBOE VIX (pts)',
      computeDerived: (raw) => {
        const c = Number(raw.close !== undefined ? raw.close : 7659.4);
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
      basePrice: 26140.0,
      livePrice: 26140.0,
      dayBase: 26713.0,
      dayOpen: 26653.0,
      dayLow: 26023.1,
      dayHigh: 26674.7,
      low52w: 20690.2,
      high52w: 27722.8,
      ytdPct: 11.32,
      card1: { title: 'Nasdaq Composite Index', sub: 'NASDAQ: ^IXIC' },
      card2: { title: 'Invesco QQQ Trust', sub: 'ETF: QQQ' },
      card3: { title: 'US 10-Year Treasury Yield', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Micro E-Mini Notional', sub: 'CME: MNQ ($2/PT)' },
      overlay0: 'Nasdaq (^IXIC)',
      overlay1: 'Invesco QQQ ($)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const c = Number(raw.close !== undefined ? raw.close : (raw.nasdaq || 26140.0));
        const o = Number(raw.open !== undefined ? raw.open : c);
        const h = Number(raw.high !== undefined ? raw.high : Math.max(o, c));
        const l = Number(raw.low !== undefined ? raw.low : Math.min(o, c));
        const qqq = c / 36.8;
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
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
      basePrice: 52002.4,
      livePrice: 52002.4,
      dayBase: 52177.7,
      dayOpen: 52308.3,
      dayLow: 51847.9,
      dayHigh: 52582.3,
      low52w: 45057.3,
      high52w: 54744.3,
      ytdPct: 8.1,
      card1: { title: 'Dow Jones Benchmark', sub: 'INDEX: ^DJI' },
      card2: { title: 'Tracking ETF Proxy', sub: 'ETF BENCHMARK' },
      card3: { title: 'US 10Y Discount Rate', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Futures Notional', sub: 'EQUITY DERIVATIVES' },
      overlay0: 'Dow Jones (DJI)',
      overlay1: 'ETF Proxy ($)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (52002.4 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 2721.4,
      livePrice: 2721.4,
      dayBase: 2767.3,
      dayOpen: 2768.9,
      dayLow: 2716.2,
      dayHigh: 2771.7,
      low52w: 2303.5,
      high52w: 3069.7,
      ytdPct: 9.21,
      card1: { title: 'Russell 2000 Benchmark', sub: 'INDEX: ^RUT' },
      card2: { title: 'Tracking ETF Proxy', sub: 'ETF BENCHMARK' },
      card3: { title: 'US 10Y Discount Rate', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Futures Notional', sub: 'EQUITY DERIVATIVES' },
      overlay0: 'Russell 2000 (RUT)',
      overlay1: 'ETF Proxy ($)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (2721.4 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 65324.3,
      livePrice: 65324.3,
      dayBase: 64425.9,
      dayOpen: 64925.3,
      dayLow: 64800.9,
      dayHigh: 65712.3,
      low52w: 44659.2,
      high52w: 72831.7,
      ytdPct: 28.06,
      card1: { title: 'Nikkei 225 Benchmark', sub: 'INDEX: ^N225' },
      card2: { title: 'Tracking ETF Proxy', sub: 'ETF BENCHMARK' },
      card3: { title: 'US 10Y Discount Rate', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Futures Notional', sub: 'EQUITY DERIVATIVES' },
      overlay0: 'Nikkei 225 (N225)',
      overlay1: 'ETF Proxy ($)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (65324.3 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 25622.6,
      livePrice: 25622.6,
      dayBase: 25382.6,
      dayOpen: 25495.3,
      dayLow: 25466.1,
      dayHigh: 25693.9,
      low52w: 21863.8,
      high52w: 26618.7,
      ytdPct: 4.58,
      card1: { title: 'DAX 40 Benchmark', sub: 'INDEX: ^GDAXI' },
      card2: { title: 'Tracking ETF Proxy', sub: 'ETF BENCHMARK' },
      card3: { title: 'US 10Y Discount Rate', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Futures Notional', sub: 'EQUITY DERIVATIVES' },
      overlay0: 'DAX 40 (DAX)',
      overlay1: 'ETF Proxy ($)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (25622.6 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 10881.9,
      livePrice: 10881.9,
      dayBase: 10840.4,
      dayOpen: 10839.2,
      dayLow: 10796.7,
      dayHigh: 10892.4,
      low52w: 9354.5,
      high52w: 10989.5,
      ytdPct: 9.57,
      card1: { title: 'FTSE 100 Benchmark', sub: 'INDEX: ^FTSE' },
      card2: { title: 'Tracking ETF Proxy', sub: 'ETF BENCHMARK' },
      card3: { title: 'US 10Y Discount Rate', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Futures Notional', sub: 'EQUITY DERIVATIVES' },
      overlay0: 'FTSE 100 (FTSE)',
      overlay1: 'ETF Proxy ($)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (10881.9 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 24186.8,
      livePrice: 24186.8,
      dayBase: 24062.7,
      dayOpen: 24321.4,
      dayLow: 24087.2,
      dayHigh: 24392.3,
      low52w: 22518.0,
      high52w: 28056.1,
      ytdPct: -5.95,
      card1: { title: 'Hang Seng Benchmark', sub: 'INDEX: ^HSI' },
      card2: { title: 'Tracking ETF Proxy', sub: 'ETF BENCHMARK' },
      card3: { title: 'US 10Y Discount Rate', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Futures Notional', sub: 'EQUITY DERIVATIVES' },
      overlay0: 'Hang Seng (HSI)',
      overlay1: 'ETF Proxy ($)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (24186.8 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 763.25,
      livePrice: 763.25,
      dayBase: 771.79,
      dayOpen: 773.24,
      dayLow: 760.64,
      dayHigh: 773.25,
      low52w: 629.28,
      high52w: 781.62,
      ytdPct: 11.31,
      card1: { title: 'SPY ETF ETF Net Asset Value', sub: 'ETF: SPY' },
      card2: { title: 'AUM & Liquidity Depth', sub: 'INSTITUTIONAL FLOW' },
      card3: { title: 'Benchmark Index Tracking', sub: 'UNDERLYING INDEX' },
      card4: { title: 'Daily Turnover Volume', sub: 'MARKET LIQUIDITY' },
      overlay0: 'SPY ETF (SPY)',
      overlay1: 'Tracking Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (763.25 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 709.8,
      livePrice: 709.8,
      dayBase: 728.0,
      dayOpen: 725.52,
      dayLow: 707.23,
      dayHigh: 725.96,
      low52w: 555.6,
      high52w: 762.86,
      ytdPct: 14.47,
      card1: { title: 'QQQ ETF ETF Net Asset Value', sub: 'ETF: QQQ' },
      card2: { title: 'AUM & Liquidity Depth', sub: 'INSTITUTIONAL FLOW' },
      card3: { title: 'Benchmark Index Tracking', sub: 'UNDERLYING INDEX' },
      card4: { title: 'Daily Turnover Volume', sub: 'MARKET LIQUIDITY' },
      overlay0: 'QQQ ETF (QQQ)',
      overlay1: 'Tracking Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (709.8 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 270.44,
      livePrice: 270.44,
      dayBase: 275.08,
      dayOpen: 275.52,
      dayLow: 269.88,
      dayHigh: 275.91,
      low52w: 228.9,
      high52w: 305.18,
      ytdPct: 9.21,
      card1: { title: 'IWM ETF ETF Net Asset Value', sub: 'ETF: IWM' },
      card2: { title: 'AUM & Liquidity Depth', sub: 'INSTITUTIONAL FLOW' },
      card3: { title: 'Benchmark Index Tracking', sub: 'UNDERLYING INDEX' },
      card4: { title: 'Daily Turnover Volume', sub: 'MARKET LIQUIDITY' },
      overlay0: 'IWM ETF (IWM)',
      overlay1: 'Tracking Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (270.44 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 374.07,
      livePrice: 374.07,
      dayBase: 378.42,
      dayOpen: 379.2,
      dayLow: 372.74,
      dayHigh: 379.42,
      low52w: 310.4,
      high52w: 385.12,
      ytdPct: 10.95,
      card1: { title: 'VTI ETF ETF Net Asset Value', sub: 'ETF: VTI' },
      card2: { title: 'AUM & Liquidity Depth', sub: 'INSTITUTIONAL FLOW' },
      card3: { title: 'Benchmark Index Tracking', sub: 'UNDERLYING INDEX' },
      card4: { title: 'Daily Turnover Volume', sub: 'MARKET LIQUIDITY' },
      overlay0: 'VTI ETF (VTI)',
      overlay1: 'Tracking Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (374.07 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 95.38,
      livePrice: 95.38,
      dayBase: 95.41,
      dayOpen: 95.29,
      dayLow: 95.22,
      dayHigh: 95.58,
      low52w: 93.84,
      high52w: 101.46,
      ytdPct: -4.62,
      card1: { title: 'AGG Bond ETF ETF Net Asset Value', sub: 'ETF: AGG' },
      card2: { title: 'AUM & Liquidity Depth', sub: 'INSTITUTIONAL FLOW' },
      card3: { title: 'Benchmark Index Tracking', sub: 'UNDERLYING INDEX' },
      card4: { title: 'Daily Turnover Volume', sub: 'MARKET LIQUIDITY' },
      overlay0: 'AGG Bond ETF (AGG)',
      overlay1: 'Tracking Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (95.38 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 382.01,
      livePrice: 382.01,
      dayBase: 382.71,
      dayOpen: 381.34,
      dayLow: 380.89,
      dayHigh: 384.88,
      low52w: 360.12,
      high52w: 509.7,
      ytdPct: -4.88,
      card1: { title: 'GLD ETF ETF Net Asset Value', sub: 'ETF: GLD' },
      card2: { title: 'AUM & Liquidity Depth', sub: 'INSTITUTIONAL FLOW' },
      card3: { title: 'Benchmark Index Tracking', sub: 'UNDERLYING INDEX' },
      card4: { title: 'Daily Turnover Volume', sub: 'MARKET LIQUIDITY' },
      overlay0: 'GLD ETF (GLD)',
      overlay1: 'Tracking Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (382.01 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 161.76,
      livePrice: 161.76,
      dayBase: 157.31,
      dayOpen: 156.97,
      dayLow: 155.8,
      dayHigh: 162.38,
      low52w: 65.99,
      high52w: 163.35,
      ytdPct: 136.39,
      card1: { title: 'USO Oil ETF ETF Net Asset Value', sub: 'ETF: USO' },
      card2: { title: 'AUM & Liquidity Depth', sub: 'INSTITUTIONAL FLOW' },
      card3: { title: 'Benchmark Index Tracking', sub: 'UNDERLYING INDEX' },
      card4: { title: 'Daily Turnover Volume', sub: 'MARKET LIQUIDITY' },
      overlay0: 'USO Oil ETF (USO)',
      overlay1: 'Tracking Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (161.76 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 62.85,
      livePrice: 62.85,
      dayBase: 63.96,
      dayOpen: 63.64,
      dayLow: 62.68,
      dayHigh: 63.67,
      low52w: 52.38,
      high52w: 71.57,
      ytdPct: 12.45,
      card1: { title: 'EEM ETF ETF Net Asset Value', sub: 'ETF: EEM' },
      card2: { title: 'AUM & Liquidity Depth', sub: 'INSTITUTIONAL FLOW' },
      card3: { title: 'Benchmark Index Tracking', sub: 'UNDERLYING INDEX' },
      card4: { title: 'Daily Turnover Volume', sub: 'MARKET LIQUIDITY' },
      overlay0: 'EEM ETF (EEM)',
      overlay1: 'Tracking Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (62.85 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 5.098,
      livePrice: 5.098,
      dayBase: 5.089,
      dayOpen: 5.114,
      dayLow: 5.067,
      dayHigh: 5.133,
      low52w: 3.947,
      high52w: 5.364,
      ytdPct: 22.52,
      card1: { title: 'US 10Y Yield Yield', sub: 'BENCHMARK: ^TNX' },
      card2: { title: 'Yield Curve Slope', sub: 'TERM PREMIUM' },
      card3: { title: 'Real Yield / Breakeven', sub: 'INFLATION EXPECTATIONS' },
      card4: { title: 'Bond Equivalent Price', sub: 'PAR: 100.00' },
      overlay0: 'US 10Y Yield (US10Y %)',
      overlay1: 'Curve Slope (bps)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (5.098 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 4.736,
      livePrice: 4.736,
      dayBase: 4.751,
      dayOpen: 4.749,
      dayLow: 4.71,
      dayHigh: 4.783,
      low52w: 3.365,
      high52w: 4.96,
      ytdPct: 36.29,
      card1: { title: 'US 2Y Yield Yield', sub: 'BENCHMARK: ^IRX' },
      card2: { title: 'Yield Curve Slope', sub: 'TERM PREMIUM' },
      card3: { title: 'Real Yield / Breakeven', sub: 'INFLATION EXPECTATIONS' },
      card4: { title: 'Bond Equivalent Price', sub: 'PAR: 100.00' },
      overlay0: 'US 2Y Yield (US02Y %)',
      overlay1: 'Curve Slope (bps)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (4.736 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 3.409,
      livePrice: 3.409,
      dayBase: 3.407,
      dayOpen: 3.407,
      dayLow: 3.398,
      dayHigh: 3.444,
      low52w: 2.636,
      high52w: 3.653,
      ytdPct: 19.11,
      card1: { title: 'Germany 10Y Bund Yield', sub: 'BENCHMARK: DE10Y.F' },
      card2: { title: 'Yield Curve Slope', sub: 'TERM PREMIUM' },
      card3: { title: 'Real Yield / Breakeven', sub: 'INFLATION EXPECTATIONS' },
      card4: { title: 'Bond Equivalent Price', sub: 'PAR: 100.00' },
      overlay0: 'Germany 10Y Bund (BUND10Y %)',
      overlay1: 'Curve Slope (bps)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (3.409 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 5.377,
      livePrice: 5.377,
      dayBase: 5.363,
      dayOpen: 5.361,
      dayLow: 5.347,
      dayHigh: 5.41,
      low52w: 4.234,
      high52w: 5.527,
      ytdPct: 20.18,
      card1: { title: 'UK 10Y Gilt Yield', sub: 'BENCHMARK: GB10Y.L' },
      card2: { title: 'Yield Curve Slope', sub: 'TERM PREMIUM' },
      card3: { title: 'Real Yield / Breakeven', sub: 'INFLATION EXPECTATIONS' },
      card4: { title: 'Bond Equivalent Price', sub: 'PAR: 100.00' },
      overlay0: 'UK 10Y Gilt (GILT10Y %)',
      overlay1: 'Curve Slope (bps)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (5.377 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 2.941,
      livePrice: 2.941,
      dayBase: 2.931,
      dayOpen: 2.932,
      dayLow: 2.86,
      dayHigh: 2.946,
      low52w: 1.914,
      high52w: 3.137,
      ytdPct: 42.42,
      card1: { title: 'Japan 10Y JGB Yield', sub: 'BENCHMARK: JP10Y.T' },
      card2: { title: 'Yield Curve Slope', sub: 'TERM PREMIUM' },
      card3: { title: 'Real Yield / Breakeven', sub: 'INFLATION EXPECTATIONS' },
      card4: { title: 'Bond Equivalent Price', sub: 'PAR: 100.00' },
      overlay0: 'Japan 10Y JGB (JGB10Y %)',
      overlay1: 'Curve Slope (bps)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (2.941 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 101.78,
      livePrice: 101.78,
      dayBase: 102.0,
      dayOpen: 102.04,
      dayLow: 101.58,
      dayHigh: 102.09,
      low52w: 95.55,
      high52w: 102.95,
      ytdPct: 3.6,
      card1: { title: 'US Dollar Index Exchange Rate', sub: 'FX: DX-Y.NYB' },
      card2: { title: 'US Dollar Index DXY', sub: 'MACRO DOLLAR' },
      card3: { title: 'Interest Rate Differential', sub: 'POLICY SPREAD' },
      card4: { title: 'Purchasing Power Parity', sub: 'PPP FAIR VALUE' },
      overlay0: 'US Dollar Index (DXY)',
      overlay1: 'US Dollar Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (101.78 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 1.124,
      livePrice: 1.124,
      dayBase: 1.121,
      dayOpen: 1.122,
      dayLow: 1.121,
      dayHigh: 1.127,
      low52w: 1.111,
      high52w: 1.202,
      ytdPct: -4.34,
      card1: { title: 'EUR / USD Exchange Rate', sub: 'FX: EURUSD=X' },
      card2: { title: 'US Dollar Index DXY', sub: 'MACRO DOLLAR' },
      card3: { title: 'Interest Rate Differential', sub: 'POLICY SPREAD' },
      card4: { title: 'Purchasing Power Parity', sub: 'PPP FAIR VALUE' },
      overlay0: 'EUR / USD (EURUSD)',
      overlay1: 'US Dollar Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (1.124 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 157.99,
      livePrice: 157.99,
      dayBase: 158.14,
      dayOpen: 157.97,
      dayLow: 157.69,
      dayHigh: 158.34,
      low52w: 151.55,
      high52w: 163.98,
      ytdPct: 0.8,
      card1: { title: 'USD / JPY Exchange Rate', sub: 'FX: USDJPY=X' },
      card2: { title: 'US Dollar Index DXY', sub: 'MACRO DOLLAR' },
      card3: { title: 'Interest Rate Differential', sub: 'POLICY SPREAD' },
      card4: { title: 'Purchasing Power Parity', sub: 'PPP FAIR VALUE' },
      overlay0: 'USD / JPY (USDJPY)',
      overlay1: 'US Dollar Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (157.99 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 33.42,
      livePrice: 33.42,
      dayBase: 33.47,
      dayOpen: 33.49,
      dayLow: 33.34,
      dayHigh: 33.54,
      low52w: 30.82,
      high52w: 33.86,
      ytdPct: 6.1,
      card1: { title: 'USD / THB Exchange Rate', sub: 'FX: THB=X' },
      card2: { title: 'US Dollar Index DXY', sub: 'MACRO DOLLAR' },
      card3: { title: 'Interest Rate Differential', sub: 'POLICY SPREAD' },
      card4: { title: 'Purchasing Power Parity', sub: 'PPP FAIR VALUE' },
      overlay0: 'USD / THB (USDTHB)',
      overlay1: 'US Dollar Index',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {
        const ratio = (33.42 / 4169.3);
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
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
      basePrice: 81427.3,
      livePrice: 81427.3,
      dayBase: 82141.5,
      dayOpen: 81501.6,
      dayLow: 81302.6,
      dayHigh: 81546.9,
      low52w: 57747.8,
      high52w: 87363.8,
      ytdPct: -6.95,
      card1: { title: 'Bitcoin Spot', sub: 'CRYPTO: BTC-USD' },
      card2: { title: 'Ethereum / USD', sub: 'CRYPTO: ETH-USD' },
      card3: { title: 'US Dollar Index', sub: 'CURRENCY: DXY' },
      card4: { title: 'Satoshis Per Dollar', sub: 'UNIT: 100M SATS/BTC' },
      overlay0: 'Bitcoin (BTC)',
      overlay1: 'Ethereum (ETH)',
      overlay2: 'US Dollar Index',
      computeDerived: (raw) => {
        const c = Number(raw.close !== undefined ? raw.close : 81427.3);
        const o = Number(raw.open !== undefined ? raw.open : c);
        const h = Number(raw.high !== undefined ? raw.high : Math.max(o, c));
        const l = Number(raw.low !== undefined ? raw.low : Math.min(o, c));
        const eth = c * 0.038;
        return {
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: eth, thb: eth,
          us10y: 101.78, bond: 101.78,
          gold_thb_oz: eth,
          pure_gram_thb: eth / 31.1034768,
          thai_gold_bar: Math.round(100000000 / c),
          thai_gold_ornament: Math.round(100000000 / c),
          note: raw.note || ''
        };
      }
    }
  };
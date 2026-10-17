import json
import os
import re

def generate_js_instruments():
    meta_path = 'scripts/real_market_meta.json'
    meta_store = {}
    if os.path.exists(meta_path):
        with open(meta_path, encoding='utf-8') as f:
            meta_store = json.load(f)

    with open('src/js/instruments/catalog.js', encoding='utf-8') as f:
        catalog_code = f.read()

    # Sync catalog.js defaultPrice and dayRange with real_market_meta.json
    for inst_id, m in meta_store.items():
        if inst_id == 'gold':
            continue
        pat = re.compile(
            r"(id:\s*'" + re.escape(inst_id) + r"'[\s\S]*?defaultPrice:\s*)([\d\.]+)(,\s*dayRange:\s*\{\s*low:\s*)([\d\.]+)(,\s*high:\s*)([\d\.]+)(,\s*base:\s*)([\d\.]+)(\s*\})"
        )
        def _repl(match, m=m):
            return (
                f"{match.group(1)}{m['price']}"
                f"{match.group(3)}{m['dayLow']}"
                f"{match.group(5)}{m['dayHigh']}"
                f"{match.group(7)}{m['prevClose']}"
                f"{match.group(9)}"
            )
        catalog_code, _ = pat.subn(_repl, catalog_code, count=1)

    with open('src/js/instruments/catalog.js', 'w', encoding='utf-8') as f:
        f.write(catalog_code)

    # Pattern for instrument blocks
    pattern = re.compile(
        r"id:\s*'([^']+)',\s*"
        r"category:\s*'([^']+)',\s*"
        r"symbol:\s*'([^']+)',\s*"
        r"name:\s*'([^']+)',\s*"
        r"shortName:\s*'([^']+)',\s*"
        r"ticker:\s*'([^']+)',\s*"
        r"exchange:\s*'([^']+)',\s*"
        r"unit:\s*'([^']+)',\s*"
        r"currency:\s*'([^']+)',\s*"
        r"themeColor:\s*'([^']+)',\s*"
        r"defaultPrice:\s*([\d\.]+)"
    )

    matches = pattern.findall(catalog_code)
    print(f"Found {len(matches)} instruments in catalog.js.")

    lines = []
    lines.append("  const INSTRUMENTS = {")

    for m in matches:
        inst_id, cat, sym, name, short_name, ticker, exch, unit, curr, color, def_price = m
        m_info = meta_store.get(inst_id, {})
        price = float(m_info.get('price', def_price))
        day_base = float(m_info.get('prevClose', round(price * 0.998, 2)))
        day_open = float(m_info.get('open', day_base))
        day_low = float(m_info.get('dayLow', round(price * 0.994, 2)))
        day_high = float(m_info.get('dayHigh', round(price * 1.006, 2)))
        low_52w = float(m_info.get('low52w', round(price * 0.78, 2)))
        high_52w = float(m_info.get('high52w', round(price * 1.12, 2)))
        ytd_pct = float(m_info.get('ytdPct', 11.4))

        # Custom cards and labels per category
        if cat == 'commodities':
            c1_t = f"{short_name} Spot / Futures"
            c1_s = f"MARKET: {ticker}"
            c2_t = "USD / THB Forex"
            c2_s = "FX: USD / THB"
            c3_t = "US 10Y Yield"
            c3_s = "RATES: CBOE ^TNX"
            c4_t = f"Contract Notional ({unit})"
            c4_s = "LOT SIZE BENCHMARK"
            o0 = f"{short_name} ({sym})"
            o1 = "USD / THB (฿)"
            o2 = "US 10Y Yield (%)"
        elif cat == 'indices':
            c1_t = f"{short_name} Benchmark"
            c1_s = f"INDEX: {ticker}"
            c2_t = "Tracking ETF Proxy"
            c2_s = "ETF BENCHMARK"
            c3_t = "US 10Y Discount Rate"
            c3_s = "RATES: CBOE ^TNX"
            c4_t = "Futures Notional"
            c4_s = "EQUITY DERIVATIVES"
            o0 = f"{short_name} ({sym})"
            o1 = "ETF Proxy ($)"
            o2 = "US 10Y Yield (%)"
        elif cat == 'etfs':
            c1_t = f"{short_name} ETF Net Asset Value"
            c1_s = f"ETF: {ticker}"
            c2_t = "AUM & Liquidity Depth"
            c2_s = "INSTITUTIONAL FLOW"
            c3_t = "Benchmark Index Tracking"
            c3_s = "UNDERLYING INDEX"
            c4_t = "Daily Turnover Volume"
            c4_s = "MARKET LIQUIDITY"
            o0 = f"{short_name} ({sym})"
            o1 = "Tracking Index"
            o2 = "US 10Y Yield (%)"
        elif cat == 'bonds':
            c1_t = f"{short_name} Yield"
            c1_s = f"BENCHMARK: {ticker}"
            c2_t = "Yield Curve Slope"
            c2_s = "TERM PREMIUM"
            c3_t = "Real Yield / Breakeven"
            c3_s = "INFLATION EXPECTATIONS"
            c4_t = "Bond Equivalent Price"
            c4_s = "PAR: 100.00"
            o0 = f"{short_name} ({sym} %)"
            o1 = "Curve Slope (bps)"
            o2 = "US 10Y Yield (%)"
        else:  # forex
            c1_t = f"{short_name} Exchange Rate"
            c1_s = f"FX: {ticker}"
            c2_t = "US Dollar Index DXY"
            c2_s = "MACRO DOLLAR"
            c3_t = "Interest Rate Differential"
            c3_s = "POLICY SPREAD"
            c4_t = "Purchasing Power Parity"
            c4_s = "PPP FAIR VALUE"
            o0 = f"{short_name} ({sym})"
            o1 = "US Dollar Index"
            o2 = "US 10Y Yield (%)"

        if inst_id == 'gold':
            # Gold preserves exact original configuration
            lines.append(f"""    gold: {{
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
      card1: {{ title: 'Gold Futures (US Market)', sub: 'COMEX: GC=F' }},
      card2: {{ title: 'Forex Exchange Rate', sub: 'FX: USD / THB' }},
      card3: {{ title: 'US 10-Year Treasury Yield', sub: 'RATES: CBOE ^TNX' }},
      card4: {{ title: 'Thai Gold Bar (1 บาททอง)', sub: 'THAI GOLD: 96.5% BAR' }},
      overlay0: 'Gold (USD/oz)',
      overlay1: 'USD / THB (฿)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: computeDerived
    }},""")
        elif inst_id == 'nasdaq':
            lines.append(f"""    nasdaq: {{
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
      basePrice: {price},
      livePrice: {price},
      dayBase: {day_base},
      dayOpen: {day_open},
      dayLow: {day_low},
      dayHigh: {day_high},
      low52w: {low_52w},
      high52w: {high_52w},
      ytdPct: {ytd_pct},
      card1: {{ title: 'Nasdaq Composite Index', sub: 'NASDAQ: ^IXIC' }},
      card2: {{ title: 'Invesco QQQ Trust', sub: 'ETF: QQQ' }},
      card3: {{ title: 'US 10-Year Treasury Yield', sub: 'RATES: CBOE ^TNX' }},
      card4: {{ title: 'Micro E-Mini Notional', sub: 'CME: MNQ ($2/PT)' }},
      overlay0: 'Nasdaq (^IXIC)',
      overlay1: 'Invesco QQQ ($)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => {{
        const c = Number(raw.close !== undefined ? raw.close : (raw.nasdaq || {price}));
        const o = Number(raw.open !== undefined ? raw.open : c);
        const h = Number(raw.high !== undefined ? raw.high : Math.max(o, c));
        const l = Number(raw.low !== undefined ? raw.low : Math.min(o, c));
        const qqq = c / 36.8;
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        return {{
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: qqq, thb: qqq,
          us10y: bond, bond: bond,
          gold_thb_oz: qqq,
          pure_gram_thb: qqq / 31.1034768,
          thai_gold_bar: c * 2.0,
          thai_gold_ornament: c * 20.0,
          note: raw.note || ''
        }};
      }}
    }},""")
        elif inst_id == 'sp500':
            lines.append(f"""    sp500: {{
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
      basePrice: {price},
      livePrice: {price},
      dayBase: {day_base},
      dayOpen: {day_open},
      dayLow: {day_low},
      dayHigh: {day_high},
      low52w: {low_52w},
      high52w: {high_52w},
      ytdPct: {ytd_pct},
      card1: {{ title: 'S&P 500 Large-Cap', sub: 'INDEX: ^GSPC' }},
      card2: {{ title: 'SPDR S&P 500 ETF', sub: 'ETF: SPY' }},
      card3: {{ title: 'CBOE Volatility Index', sub: 'VOLATILITY: ^VIX' }},
      card4: {{ title: 'Micro E-Mini S&P Notional', sub: 'CME: MES ($5/PT)' }},
      overlay0: 'S&P 500 (^GSPC)',
      overlay1: 'SPDR SPY ($)',
      overlay2: 'CBOE VIX (pts)',
      computeDerived: (raw) => {{
        const c = Number(raw.close !== undefined ? raw.close : {price});
        const o = Number(raw.open !== undefined ? raw.open : c);
        const h = Number(raw.high !== undefined ? raw.high : Math.max(o, c));
        const l = Number(raw.low !== undefined ? raw.low : Math.min(o, c));
        const spy = c / 10.0;
        return {{
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: spy, thb: spy,
          us10y: 15.42, bond: 15.42,
          gold_thb_oz: spy,
          pure_gram_thb: spy / 31.1034768,
          thai_gold_bar: c * 5.0,
          thai_gold_ornament: c * 50.0,
          note: raw.note || ''
        }};
      }}
    }},""")
        else:
            ratio_expr = f"({price} / 4169.3)"
            lines.append(f"""    {inst_id}: {{
      id: '{inst_id}',
      category: '{cat}',
      symbol: '{sym}',
      title: '{name}',
      subtitle: '{exch}',
      shortName: '{short_name}',
      currency: '{curr}',
      unit: '{unit}',
      ticker: '{ticker}',
      themeColor: '{color}',
      basePrice: {price},
      livePrice: {price},
      dayBase: {day_base},
      dayOpen: {day_open},
      dayLow: {day_low},
      dayHigh: {day_high},
      low52w: {low_52w},
      high52w: {high_52w},
      ytdPct: {ytd_pct},
      card1: {{ title: '{c1_t}', sub: '{c1_s}' }},
      card2: {{ title: '{c2_t}', sub: '{c2_s}' }},
      card3: {{ title: '{c3_t}', sub: '{c3_s}' }},
      card4: {{ title: '{c4_t}', sub: '{c4_s}' }},
      overlay0: '{o0}',
      overlay1: '{o1}',
      overlay2: '{o2}',
      computeDerived: (raw) => {{
        const ratio = {ratio_expr};
        const orig = Number(raw.close !== undefined ? raw.close : (raw.gold || 4169.3));
        const c = Number((orig * ratio).toFixed(2));
        const o = Number(((raw.open !== undefined ? raw.open : orig) * ratio).toFixed(2));
        const h = Number(((raw.high !== undefined ? raw.high : Math.max(o, c)) * ratio).toFixed(2));
        const l = Number(((raw.low !== undefined ? raw.low : Math.min(o, c)) * ratio).toFixed(2));
        const bond = Number(raw.us10y !== undefined ? raw.us10y : 5.098);
        const thb = Number(raw.usd_thb !== undefined ? raw.usd_thb : 33.42);
        return {{
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: thb, thb: thb,
          us10y: bond, bond: bond,
          gold_thb_oz: c * thb,
          pure_gram_thb: (c * thb) / 31.1034768,
          thai_gold_bar: Math.round(c * 15.0),
          thai_gold_ornament: Math.round(c * 15.0),
          note: raw.note || ''
        }};
      }}
    }},""")

    # Add crypto with real Yahoo Finance metadata
    c_meta = meta_store.get('crypto', {})
    c_price = float(c_meta.get('price', 81433.3))
    c_base = float(c_meta.get('prevClose', 82141.5))
    c_open = float(c_meta.get('open', 81501.6))
    c_low = float(c_meta.get('dayLow', 81302.6))
    c_high = float(c_meta.get('dayHigh', 81546.9))
    c_52l = float(c_meta.get('low52w', 57747.8))
    c_52h = float(c_meta.get('high52w', 87363.8))
    c_ytd = float(c_meta.get('ytdPct', -6.94))

    lines.append(f"""    crypto: {{
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
      basePrice: {c_price},
      livePrice: {c_price},
      dayBase: {c_base},
      dayOpen: {c_open},
      dayLow: {c_low},
      dayHigh: {c_high},
      low52w: {c_52l},
      high52w: {c_52h},
      ytdPct: {c_ytd},
      card1: {{ title: 'Bitcoin Spot', sub: 'CRYPTO: BTC-USD' }},
      card2: {{ title: 'Ethereum / USD', sub: 'CRYPTO: ETH-USD' }},
      card3: {{ title: 'US Dollar Index', sub: 'CURRENCY: DXY' }},
      card4: {{ title: 'Satoshis Per Dollar', sub: 'UNIT: 100M SATS/BTC' }},
      overlay0: 'Bitcoin (BTC)',
      overlay1: 'Ethereum (ETH)',
      overlay2: 'US Dollar Index',
      computeDerived: (raw) => {{
        const c = Number(raw.close !== undefined ? raw.close : {c_price});
        const o = Number(raw.open !== undefined ? raw.open : c);
        const h = Number(raw.high !== undefined ? raw.high : Math.max(o, c));
        const l = Number(raw.low !== undefined ? raw.low : Math.min(o, c));
        const eth = c * 0.038;
        return {{
          ...raw,
          open: o, high: h, low: l, close: c, gold: c,
          usd_thb: eth, thb: eth,
          us10y: 101.78, bond: 101.78,
          gold_thb_oz: eth,
          pure_gram_thb: eth / 31.1034768,
          thai_gold_bar: Math.round(100000000 / c),
          thai_gold_ornament: Math.round(100000000 / c),
          note: raw.note || ''
        }};
      }}
    }}
  }};""")

    output = "\n".join(lines)
    with open('scripts/generated_instruments.js', 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"Generated instruments written to scripts/generated_instruments.js ({len(output)} chars)")

if __name__ == '__main__':
    generate_js_instruments()

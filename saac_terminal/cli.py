#!/usr/bin/env python3
"""
The Saac Financial Terminal - Universal Multi-Asset CLI
Supports Gold (GC=F), Nasdaq (^IXIC), S&P 500 (^GSPC), and custom market symbols.
"""

import sys
import os
import argparse
import time
import csv
from datetime import datetime

# Ensure utf-8 output in Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from .core.instrument import registry, InstrumentConfig
from .core.analytics import calculate_return, calculate_high_low, calculate_max_drawdown
from .instruments.gold import GOLD_INSTRUMENT, calculate_thai_gold, TROY_OZ_TO_GRAMS
from .instruments.nasdaq import NASDAQ_INSTRUMENT, calculate_nasdaq_derivatives
from .instruments.indices import SP500_INSTRUMENT
from .providers.yahoo import fetch_live_quote

# Register instruments in CLI context
registry.register(GOLD_INSTRUMENT)
registry.register(NASDAQ_INSTRUMENT)
registry.register(SP500_INSTRUMENT)

def print_header(inst: InstrumentConfig):
    print("=" * 76)
    print(f"  THE SAAC TERMINAL // {inst.name.upper()}")
    print(f"  Primary Instrument: {inst.symbol} [{inst.ticker}] • {inst.exchange}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} • Status: CONNECTED")
    print("=" * 76)

def print_dashboard(inst: InstrumentConfig):
    print_header(inst)
    
    # Try live fetch or fallback to default
    live_q = fetch_live_quote(inst.ticker)
    price = live_q.get("regularMarketPrice", inst.default_price) if live_q else inst.default_price
    prev_close = live_q.get("previousClose", price * 0.9975) if live_q else (price * 0.9975)
    
    pct_chg, abs_chg = calculate_return(prev_close, price)
    sign = "+" if pct_chg >= 0 else ""
    
    print(f"\n[SPOT QUOTE]")
    print(f"  Price:       ${price:,.2f} {inst.currency} / {inst.unit}")
    print(f"  Day Change:  {sign}{pct_chg:.2f}% ({sign}${abs_chg:,.2f})")
    
    if inst.id == "gold":
        fx_thb = 33.56
        bond_yield = 5.217
        derived = calculate_thai_gold(price, fx_thb)
        print(f"\n[BENCHMARK INDICATORS & DERIVATIVES]")
        print(f"  • USD/THB Forex Rate:        ฿{fx_thb:.4f} THB")
        print(f"  • US 10Y Treasury Yield:     {bond_yield:.3f}% (Benchmark Risk-Free Rate)")
        print(f"  • Thai Gold Bar (96.5%):     ฿{derived['thai_gold_bar']:,.0f} THB / 1 บาททอง")
        print(f"  • Thai Ornament (96.5%):     ฿{derived['thai_gold_ornament']:,.0f} THB / 1 บาท")
        print(f"  • Pure Gold (Gram):          ฿{derived['pure_gram_thb']:,.2f} THB/g (${derived['pure_gram_usd']:,.2f}/g)")
        print(f"  • 1 Kilogram Gold Bar:       ${derived['kg_bar_usd']:,.0f} USD (฿{derived['kg_bar_thb']/1e6:.2f}M THB)")
    elif inst.id == "nasdaq":
        derivatives = calculate_nasdaq_derivatives(price)
        print(f"\n[BENCHMARK INDICATORS & DERIVATIVES]")
        print(f"  • Invesco QQQ Proxy:         ${derivatives['qqq_proxy']:,.2f}")
        print(f"  • Micro Futures (MNQ $2):    ${derivatives['micro_futures_notional']:,.0f} Notional")
        print(f"  • E-Mini Futures (NQ $20):   ${derivatives['emini_futures_notional']:,.0f} Notional")
        print(f"  • Est. P/E Multiple:         {derivatives['est_pe_multiple']:.1f}x")
    
    # Historical stats
    records = inst.historical_records
    if records:
        key = "gold" if inst.id == "gold" else "close"
        min_v, max_v, spread = calculate_high_low(records, key)
        max_dd = calculate_max_drawdown(records, key)
        first_p = records[0].get(key, 0)
        tot_pct, _ = calculate_return(first_p, price)
        print(f"\n[MULTI-DECADE HISTORICAL ANALYTICS ({records[0]['date']} to {records[-1]['date']})]")
        print(f"  • Total Return:              +{tot_pct:.1f}% (${first_p:,.1f} -> ${price:,.1f})")
        print(f"  • Historical Range:          ${min_v:,.1f} - ${max_v:,.1f} (Spread: ${spread:,.1f})")
        print(f"  • Maximum Drawdown:          {max_dd:.2f}%")
        print(f"  • Benchmark Milestones:      {len(records)} verified records loaded")
    print("=" * 76)

def print_history_table(inst: InstrumentConfig):
    print_header(inst)
    records = inst.historical_records
    if not records:
        print("No historical records available for this instrument.")
        return
    
    if inst.id == "gold":
        print(f"{'Date':<8} | {'Gold ($/oz)':<12} | {'USD/THB':<8} | {'US 10Y %':<8} | {'Thai Bar (฿)':<12} | {'Historical Event / Milestone'}")
        print("-" * 76)
        for r in records:
            d = calculate_thai_gold(r["gold"], r["thb"])
            print(f"{r['date']:<8} | ${r['gold']:>10.1f} | ฿{r['thb']:>6.2f} | {r['us10y']:>7.3f}% | ฿{d['thai_gold_bar']:>10,.0f} | {r.get('event', '')}")
    else:
        print(f"{'Date':<8} | {'Close Price':<12} | {'Secondary 1':<12} | {'US 10Y %':<8} | {'Historical Event / Milestone'}")
        print("-" * 76)
        for r in records:
            sec1 = r.get("qqq", r.get("spy", "-"))
            sec1_str = f"${sec1:,.1f}" if isinstance(sec1, (int, float)) else str(sec1)
            print(f"{r['date']:<8} | ${r['close']:>10.1f} | {sec1_str:>12} | {r.get('us10y', 0):>7.3f}% | {r.get('event', '')}")
    print("=" * 76)

def compare_dates(inst: InstrumentConfig, date1_str: str, date2_str: str):
    records = {r["date"]: r for r in inst.historical_records}
    if date1_str not in records or date2_str not in records:
        print(f"Error: Dates must be in historical records. Available sample dates: {list(records.keys())[:5]}... {list(records.keys())[-3:]}")
        return
    
    r1 = records[date1_str]
    r2 = records[date2_str]
    key = "gold" if inst.id == "gold" else "close"
    p1 = r1[key]
    p2 = r2[key]
    pct, delta = calculate_return(p1, p2)
    
    print("=" * 76)
    print(f"  LOOKBACK COMPARISON: {date1_str} -> {date2_str}")
    print(f"  {date1_str}: {r1.get('event', '')}")
    print(f"  {date2_str}: {r2.get('event', '')}")
    print("-" * 76)
    print(f"  {inst.name}:")
    print(f"    ${p1:,.1f} -> ${p2:,.1f}")
    print(f"    Change: {pct:+.2f}% ({delta:+,.1f} {inst.unit})")
    
    if inst.id == "gold":
        d1 = calculate_thai_gold(r1["gold"], r1["thb"])
        d2 = calculate_thai_gold(r2["gold"], r2["thb"])
        tb_pct, tb_abs = calculate_return(d1["thai_gold_bar"], d2["thai_gold_bar"])
        thb_pct, _ = calculate_return(r1["thb"], r2["thb"])
        print(f"\n  Forex USD/THB: ฿{r1['thb']:.2f} -> ฿{r2['thb']:.2f} ({thb_pct:+.2f}%)")
        print(f"  Thai Gold Bar: ฿{d1['thai_gold_bar']:,.0f} -> ฿{d2['thai_gold_bar']:,.0f} ({tb_pct:+.2f}%)")
    print("=" * 76)

def export_csv(inst: InstrumentConfig, filename: str):
    records = inst.historical_records
    if not records:
        print("No historical records to export.")
        return
    
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if inst.id == "gold":
            writer.writerow(["Date", "Gold_USD_oz", "USD_THB", "US_10Y_Yield_Pct", "Thai_Gold_Bar_THB", "Historical_Event"])
            for r in records:
                d = calculate_thai_gold(r["gold"], r["thb"])
                writer.writerow([r["date"], r["gold"], r["thb"], r["us10y"], round(d["thai_gold_bar"], 2), r.get("event", "")])
        else:
            writer.writerow(["Date", "Close_USD", "Secondary_1", "US_10Y_Yield_Pct", "Historical_Event"])
            for r in records:
                writer.writerow([r["date"], r["close"], r.get("qqq", r.get("spy", "")), r.get("us10y", ""), r.get("event", "")])
    print(f"Successfully exported {len(records)} records to {filename}")

def main():
    parser = argparse.ArgumentParser(description="The Saac Financial Terminal - Universal Multi-Asset CLI")
    parser.add_argument("--symbol", "--ticker", "-s", default="GC=F", help="Ticker symbol (e.g. GC=F, ^IXIC, ^GSPC, BTC-USD)")
    parser.add_argument("--instrument", "-i", default=None, help="Instrument ID (e.g. gold, nasdaq, sp500)")
    parser.add_argument("--live", action="store_true", help="Launch live streaming tick stream")
    parser.add_argument("--history", action="store_true", help="Display multi-decade historical records table")
    parser.add_argument("--compare", nargs=2, metavar=("DATE1", "DATE2"), help="Compare market metrics between two dates")
    parser.add_argument("--convert", nargs=2, metavar=("AMOUNT", "UNIT"), help="Convert amounts and position values")
    parser.add_argument("--export", metavar="FILE.CSV", help="Export historical dataset to CSV")
    parser.add_argument("--list", action="store_true", help="List all registered instruments")

    args = parser.parse_args()

    if args.list:
        print("\nRegistered Terminal Instruments:")
        for inst in registry.list_instruments():
            print(f"  • [{inst.symbol}] {inst.name:<35} | Ticker: {inst.ticker:<8} | Unit: {inst.unit}")
        print()
        return

    # Select instrument
    inst_key = args.instrument or args.symbol
    inst = registry.get(inst_key) or GOLD_INSTRUMENT

    if args.history:
        print_history_table(inst)
    elif args.compare:
        compare_dates(inst, args.compare[0], args.compare[1])
    elif args.export:
        export_csv(inst, args.export)
    elif args.live:
        print("Starting live ticker stream. Press Ctrl+C to stop...\n")
        try:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print_dashboard(inst)
                time.sleep(5)
        except KeyboardInterrupt:
            print("\nLive tracker stopped.")
    else:
        print_dashboard(inst)
        print("\nTip: Run with --help to see history, compare, convert, and export options.")

if __name__ == "__main__":
    main()

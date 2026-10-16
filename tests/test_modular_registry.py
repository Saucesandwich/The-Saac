#!/usr/bin/env python3
"""
Test Suite: Universal Multi-Asset Registry & Dynamic Instrument Switching
Verifies that any tracker (Gold, Nasdaq, S&P 500, Crypto, Custom) can be registered
and switched dynamically with zero duplicate code.
"""

import subprocess
import time
import json
import urllib.request
import os
import sys
import websocket

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile_registry')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9244',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--window-size=1400,1000',
    'file:///c:/Users/user/Downloads/gold tracker test/gold_tracker.html'
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    targets = json.loads(urllib.request.urlopen('http://localhost:9244/json').read().decode('utf-8'))
    page_target = [t for t in targets if t.get('type') == 'page'][0]
    ws = websocket.create_connection(page_target['webSocketDebuggerUrl'], timeout=10)

    msg_id = 1
    def send(method, params=None):
        global msg_id
        payload = {"id": msg_id, "method": method, "params": params or {}}
        msg_id += 1
        ws.send(json.dumps(payload))
        return msg_id - 1

    send("Runtime.enable")
    send("Log.enable")
    send("Page.enable")

    def eval_js(expression):
        req_id = send("Runtime.evaluate", {"expression": expression, "returnByValue": True, "awaitPromise": True})
        while True:
            resp = json.loads(ws.recv())
            if resp.get('id') == req_id:
                res = resp.get('result', {})
                if 'exceptionDetails' in res:
                    print(f"EXCEPTION in eval: {expression} =>", res['exceptionDetails'])
                    return None
                return res.get('result', {}).get('value')

    print("=== Testing Universal Multi-Asset Registry & Dynamic Trackers ===")

    # 1. Verify Registry Exists
    reg_defined = eval_js("typeof window.INSTRUMENTS !== 'undefined'")
    print(f"1. INSTRUMENTS Registry Defined: {reg_defined}")
    assert reg_defined is True, "Registry should be defined on window"

    inst_keys = eval_js("Object.keys(window.INSTRUMENTS)")
    print(f"   Registered instruments: {inst_keys}")
    assert "gold" in inst_keys and "nasdaq" in inst_keys and "sp500" in inst_keys and "crypto" in inst_keys

    # 2. Test Switch to Nasdaq (^IXIC)
    print("\n--- 2. Switching to NASDAQ Tracker ---")
    eval_js("switchInstrument('nasdaq')")
    current_sym = eval_js("document.querySelector('.logo-icon').innerText")
    current_title = eval_js("document.querySelector('.logo-text h1').innerText")
    card1_sub = eval_js("document.querySelector('.card-gold .card-label span:last-child').innerText")
    live_label = eval_js("liveChartInstance.data.datasets[0].label")
    live_axis = eval_js("liveChartInstance.options.scales.y.title.text")
    
    print(f"   Logo Symbol: {current_sym} (expected IXIC)")
    print(f"   Header Title: {current_title}")
    print(f"   Card 1 Subtitle: {card1_sub}")
    print(f"   Live Dataset: {live_label}")
    print(f"   Live Y-Axis: {live_axis}")

    assert current_sym == "IXIC"
    assert "NASDAQ" in card1_sub
    assert "Nasdaq Intraday" in live_label
    assert "USD / pts" in live_axis

    # 3. Test Switch to S&P 500
    print("\n--- 3. Switching to S&P 500 Tracker ---")
    eval_js("switchInstrument('sp500')")
    spx_sym = eval_js("document.querySelector('.logo-icon').innerText")
    spx_sub = eval_js("document.querySelector('.card-gold .card-label span:last-child').innerText")
    print(f"   Logo Symbol: {spx_sym} (expected SPX)")
    print(f"   Card 1 Subtitle: {spx_sub}")
    assert spx_sym == "SPX"
    assert "GSPC" in spx_sub

    # 4. Test Dynamic Registration of New Custom Tracker (Crude Oil)
    print("\n--- 4. Dynamically Registering New Custom Tracker (Crude Oil CL=F) ---")
    register_script = """
    registerInstrument({
      id: 'oil',
      symbol: 'CL',
      title: 'WTI Crude Oil Energy Terminal',
      subtitle: 'NYMEX Light Sweet Crude (CL=F) • Energy Benchmark',
      shortName: 'Crude Oil',
      currency: 'USD',
      unit: 'bbl',
      ticker: 'CL=F',
      themeColor: '#ef4444',
      basePrice: 78.50,
      dayBase: 77.80,
      dayLow: 77.20,
      dayHigh: 79.10,
      card1: { title: 'WTI Crude Oil', sub: 'NYMEX: CL=F' },
      card2: { title: 'Brent Spread', sub: 'ICE: BZ=F' },
      card3: { title: 'US 10-Year Treasury', sub: 'RATES: CBOE ^TNX' },
      card4: { title: 'Per Barrel Value', sub: 'BARREL (42 GAL)' },
      overlay0: 'Crude Oil (USD/bbl)',
      overlay1: 'Brent Crude ($)',
      overlay2: 'US 10Y Yield (%)',
      computeDerived: (raw) => ({
        ...raw,
        open: raw.open || 78.5, high: raw.high || 79.1, low: raw.low || 77.2, close: raw.close || 78.5,
        gold: raw.close || 78.5, usd_thb: 82.3, thb: 82.3, us10y: 5.217, bond: 5.217,
        thai_gold_bar: Math.round((raw.close || 78.5) * 42),
        note: raw.note || ''
      })
    });
    switchInstrument('oil');
    """
    eval_js(register_script)
    oil_sym = eval_js("document.querySelector('.logo-icon').innerText")
    oil_title = eval_js("document.querySelector('.logo-text h1').innerText")
    oil_card = eval_js("document.querySelector('.card-gold .card-label span:last-child').innerText")
    oil_axis = eval_js("liveChartInstance.options.scales.y.title.text")

    print(f"   Registered and switched to: {oil_title}")
    print(f"   Logo: {oil_sym} (expected CL)")
    print(f"   Card: {oil_card} (expected NYMEX: CL=F)")
    print(f"   Y-Axis: {oil_axis} (expected USD / bbl)")

    assert oil_sym == "CL"
    assert "CL=F" in oil_card
    assert "USD / bbl" in oil_axis

    # 5. Switch back to Gold
    print("\n--- 5. Switching back to Gold Tracker ---")
    eval_js("switchInstrument('gold')")
    gold_sym = eval_js("document.querySelector('.logo-icon').innerText")
    gold_c1 = eval_js("document.querySelector('.card-gold .card-label span:last-child').innerText")
    gold_c4 = eval_js("document.querySelector('.card-thai .card-label span:last-child').innerText")
    print(f"   Restored Logo: {gold_sym} (expected XAU)")
    print(f"   Restored Card 1: {gold_c1}")
    print(f"   Restored Card 4: {gold_c4}")

    assert gold_sym == "XAU"
    assert "GC=F" in gold_c1
    assert "THAI GOLD: 96.5% BAR" in gold_c4

    print("\nALL MULTI-ASSET REGISTRY AND EXTENSION TESTS PASSED WITH 100% SUCCESS!")

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

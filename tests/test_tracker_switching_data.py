#!/usr/bin/env python3
"""
Test Suite: Authentic Multi-Asset Historical Data & Tracker Switching
Verifies that switching instruments updates the chart with that asset's genuine historical data,
not hardcoded gold series.
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
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile_switching')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9250',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--window-size=1400,1000',
    'file:///c:/Users/user/Downloads/Saac terminal/gold_tracker.html'
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    targets = json.loads(urllib.request.urlopen('http://localhost:9250/json').read().decode('utf-8'))
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

    print("=== Testing Tracker Switching & Genuine Chart Data ===")

    # 1. Initial State: Gold
    cur_inst = eval_js("primaryInstrumentId")
    gold_last_price = eval_js("histChartInstance.data.datasets[0].data.slice(-1)[0]")
    gold_label = eval_js("histChartInstance.data.datasets[0].label")
    print(f"1. Initial instrument: {cur_inst}, dataset label='{gold_label}', last_val={gold_last_price}")
    assert cur_inst == 'gold', f"Expected gold, got {cur_inst}"
    assert "Gold" in gold_label, f"Dataset 0 label should contain Gold, got {gold_label}"
    assert abs(gold_last_price - 4180.6) < 20.0 or abs(gold_last_price - 4169.3) < 20.0, f"Gold price should be ~4169-4180, got {gold_last_price}"

    # 2. Switch to S&P 500 (sp500)
    print("\n--- 2. Switching to S&P 500 (sp500) ---")
    eval_js("switchInstrument('sp500')")
    sp_inst = eval_js("primaryInstrumentId")
    sp_label = eval_js("histChartInstance.data.datasets[0].label")
    sp_data = eval_js("histChartInstance.data.datasets[0].data")
    sp_last = sp_data[-1]
    sp_hero_price = eval_js("document.getElementById('goldUsdDisplay').innerText")
    print(f"   Switched to: {sp_inst}, label='{sp_label}', last_val={sp_last}, hero_price='{sp_hero_price}'")
    assert sp_inst == 'sp500'
    assert "S&P" in sp_label, f"Expected S&P in label, got {sp_label}"
    assert abs(sp_last - 5850.2) < 30.0, f"S&P 500 price should be ~5,850, got {sp_last}"
    assert "5,850" in sp_hero_price or "5850" in sp_hero_price, f"Hero price must show 5850, got {sp_hero_price}"

    # Test ALL timeframe on S&P 500
    eval_js("filterTimeframe('ALL')")
    sp_all_data = eval_js("histChartInstance.data.datasets[0].data")
    sp_1990 = sp_all_data[0]
    print(f"   S&P 500 ALL history: 1990={sp_1990}, 2026={sp_all_data[-1]}, samples={len(sp_all_data)}")
    assert abs(sp_1990 - 330.0) < 20.0, f"S&P 500 in 1990 was ~330, got {sp_1990}"
    assert abs(sp_all_data[-1] - 5850.2) < 20.0, f"S&P 500 in 2026 should be ~5,850, got {sp_all_data[-1]}"

    # 3. Switch to WTI Crude Oil (crude_oil)
    print("\n--- 3. Switching to WTI Crude Oil (crude_oil) ---")
    eval_js("switchInstrument('crude_oil')")
    oil_inst = eval_js("primaryInstrumentId")
    oil_label = eval_js("histChartInstance.data.datasets[0].label")
    oil_data = eval_js("histChartInstance.data.datasets[0].data")
    oil_last = oil_data[-1]
    oil_hero_price = eval_js("document.getElementById('goldUsdDisplay').innerText")
    print(f"   Switched to: {oil_inst}, label='{oil_label}', last_val={oil_last}, hero_price='{oil_hero_price}'")
    assert oil_inst == 'crude_oil'
    assert "Crude Oil" in oil_label
    assert abs(oil_last - 78.4) < 5.0, f"Crude Oil price should be ~$78.4, got {oil_last}"
    assert "78" in oil_hero_price

    # 4. Switch to US 10Y Yield (us10y)
    print("\n--- 4. Switching to US 10-Year Bond Yield (us10y) ---")
    eval_js("switchInstrument('us10y')")
    bond_inst = eval_js("primaryInstrumentId")
    bond_label = eval_js("histChartInstance.data.datasets[0].label")
    bond_data = eval_js("histChartInstance.data.datasets[0].data")
    bond_last = bond_data[-1]
    bond_hero_price = eval_js("document.getElementById('goldUsdDisplay').innerText")
    print(f"   Switched to: {bond_inst}, label='{bond_label}', last_val={bond_last}, hero_price='{bond_hero_price}'")
    assert bond_inst == 'us10y'
    assert "10Y" in bond_label or "Yield" in bond_label
    assert abs(bond_last - 5.217) < 0.1, f"US 10Y Yield should be ~5.217%, got {bond_last}"
    assert "5.2" in bond_hero_price

    # 5. Switch to Silver (silver)
    print("\n--- 5. Switching to Silver (silver) ---")
    eval_js("switchInstrument('silver')")
    silver_inst = eval_js("primaryInstrumentId")
    silver_label = eval_js("histChartInstance.data.datasets[0].label")
    silver_data = eval_js("histChartInstance.data.datasets[0].data")
    silver_last = silver_data[-1]
    print(f"   Switched to: {silver_inst}, label='{silver_label}', last_val={silver_last}")
    assert silver_inst == 'silver'
    assert "Silver" in silver_label
    assert abs(silver_last - 32.4) < 2.0, f"Silver price should be ~$32.4, got {silver_last}"

    print("\n>>> ALL MULTI-ASSET SWITCHING & DATA INTEGRITY TESTS PASSED! <<<")

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

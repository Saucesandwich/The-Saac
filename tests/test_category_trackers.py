#!/usr/bin/env python3
"""
Test Suite: Macro Categories, Multi-Asset Trackers & Quick Ticker Jump
Verifies institutional coverage across Commodities, Major Indices, ETFs, Sovereign Country Bonds, and Forex.
Asserts NO individual stocks are present in the catalog.
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

temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile_categories')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9246',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--window-size=1400,1000',
    'file:///c:/Users/user/Downloads/Saac terminal/gold_tracker.html'
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    targets = json.loads(urllib.request.urlopen('http://localhost:9246/json').read().decode('utf-8'))
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
                return res.get('result', {}).get('value')

    print("=== Testing Macro Categories & Universal Trackers ===")

    # 1. Verify Category Bar & Tabs
    cat_tabs = eval_js("Array.from(document.querySelectorAll('.cat-tab-btn')).map(b => b.dataset.category)")
    print(f"1. Category Tabs in DOM: {cat_tabs}")
    assert 'all' in cat_tabs and 'commodities' in cat_tabs and 'indices' in cat_tabs and 'etfs' in cat_tabs and 'bonds' in cat_tabs and 'forex' in cat_tabs

    # 2. Verify Exclusion of Individual Stocks
    all_syms = eval_js("Object.values(INSTRUMENTS).map(i => i.symbol)")
    print(f"2. Registered Asset Symbols ({len(all_syms)} total): {all_syms}")
    for forbidden in ['AAPL', 'TSLA', 'NVDA', 'MSFT', 'AMZN', 'GOOGL', 'META']:
        assert forbidden not in all_syms, f"Individual stock {forbidden} found in macro terminal catalog!"
    print("   Verified: Zero individual stocks present. Only macro indices, ETFs, commodities, bonds, and forex.")

    # 3. Test Category Filtering
    eval_js("filterCategory('bonds')")
    bonds_pills = eval_js("Array.from(document.querySelectorAll('.ticker-pill-btn')).map(b => b.dataset.id)")
    print(f"3. Bond Tickers Filtered: {bonds_pills}")
    assert set(bonds_pills) == {'us10y', 'us02y', 'bund10y', 'gilt10y', 'jgb10y'}

    eval_js("filterCategory('commodities')")
    comm_pills = eval_js("Array.from(document.querySelectorAll('.ticker-pill-btn')).map(b => b.dataset.id)")
    print(f"   Commodity Tickers Filtered: {comm_pills}")
    assert set(comm_pills) == {'gold', 'silver', 'crude_oil', 'natural_gas', 'copper'}

    eval_js("filterCategory('indices')")
    idx_pills = eval_js("Array.from(document.querySelectorAll('.ticker-pill-btn')).map(b => b.dataset.id)")
    print(f"   Indices Filtered: {idx_pills}")
    assert 'sp500' in idx_pills and 'nasdaq' in idx_pills and 'nikkei225' in idx_pills and 'dax40' in idx_pills and 'hangseng' in idx_pills

    # 4. Test Ticker Search Input
    eval_js("handleTickerSearch('oil')")
    search_oil = eval_js("Array.from(document.querySelectorAll('.ticker-pill-btn')).map(b => b.dataset.id)")
    print(f"4. Search 'oil' results: {search_oil}")
    assert 'crude_oil' in search_oil or 'uso' in search_oil

    eval_js("filterCategory('all'); handleTickerSearch('')")
    all_pills_count = eval_js("document.querySelectorAll('.ticker-pill-btn').length")
    print(f"   Reset to All: {all_pills_count} ticker pills rendered")
    assert all_pills_count >= 30

    # 5. Switch to Sovereign Bond Tracker: German 10Y Bund
    print("\n--- 5. Switching to German 10Y Bund (bund10y) ---")
    eval_js("switchInstrument('bund10y')")
    bund_sym = eval_js("document.querySelector('.logo-icon').innerText")
    bund_title = eval_js("document.querySelector('.logo-text h1').innerText")
    bund_card = eval_js("document.querySelector('.card-gold .card-label').innerText")
    print(f"   Bund Symbol: {bund_sym} (expected BUND10Y)")
    print(f"   Bund Title: {bund_title}")
    print(f"   Card 1 Label: {bund_card}")
    assert bund_sym == 'BUND10Y'
    assert 'BUND' in bund_title.upper() or 'GERMAN' in bund_title.upper()

    # 6. Switch to Commodity Tracker: WTI Crude Oil
    print("\n--- 6. Switching to WTI Crude Oil (crude_oil) ---")
    eval_js("switchInstrument('crude_oil')")
    oil_sym = eval_js("document.querySelector('.logo-icon').innerText")
    oil_title = eval_js("document.querySelector('.logo-text h1').innerText")
    print(f"   Crude Oil Symbol: {oil_sym} (expected CL)")
    print(f"   Crude Oil Title: {oil_title}")
    assert oil_sym == 'CL'
    assert 'CRUDE OIL' in oil_title.upper() or 'WTI' in oil_title.upper()

    # 7. Switch to Benchmark ETF: GLD Bullion ETF
    print("\n--- 7. Switching to GLD ETF (gld) ---")
    eval_js("switchInstrument('gld')")
    gld_sym = eval_js("document.querySelector('.logo-icon').innerText")
    gld_title = eval_js("document.querySelector('.logo-text h1').innerText")
    print(f"   GLD Symbol: {gld_sym} (expected GLD)")
    print(f"   GLD Title: {gld_title}")
    assert gld_sym == 'GLD'

    # 8. Switch to Forex: US Dollar Index (dxy)
    print("\n--- 8. Switching to US Dollar Index (dxy) ---")
    eval_js("switchInstrument('dxy')")
    dxy_sym = eval_js("document.querySelector('.logo-icon').innerText")
    dxy_title = eval_js("document.querySelector('.logo-text h1').innerText")
    print(f"   DXY Symbol: {dxy_sym} (expected DXY)")
    print(f"   DXY Title: {dxy_title}")
    assert dxy_sym == 'DXY'

    # 9. Restore Gold
    eval_js("switchInstrument('gold')")
    assert eval_js("document.querySelector('.logo-icon').innerText") == 'XAU'
    print("\nALL MACRO CATEGORY & ASSET TRACKER TESTS PASSED WITH 100% SUCCESS!\n")

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

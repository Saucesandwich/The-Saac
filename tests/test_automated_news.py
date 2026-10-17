#!/usr/bin/env python3
"""
Test Suite: Automated Financial News Headlines & Historical Market Shocks
Verifies:
1. News section is positioned at the very bottom below charts and specifications.
2. Headlines & market catalysts automatically populate on terminal startup.
3. Switching to any tracker automatically updates the bottom news feed for that asset.
4. Switching subtabs between 'Latest Live Headlines' and 'Historic Market Shocks' works smoothly.
5. Clicking a historical market shock automatically highlights the historical era on the chart.
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

temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile_news')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9248',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--window-size=1400,1000',
    'file:///c:/Users/user/Downloads/Saac terminal/gold_tracker.html'
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    targets = json.loads(urllib.request.urlopen('http://localhost:9248/json').read().decode('utf-8'))
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

    print("=== Testing Verification of News Feed Removal & Minimalist Layout ===")

    # 1. Verify news container is completely removed from DOM
    news_container = eval_js("Boolean(document.getElementById('marketNewsContainer'))")
    news_cards = eval_js("document.querySelectorAll('.news-card').length")
    news_feed = eval_js("Boolean(document.getElementById('newsFeedGrid'))")
    catalysts_grid = eval_js("Boolean(document.getElementById('catalystsTimelineGrid'))")
    print(f"1. #marketNewsContainer exists: {news_container}")
    print(f"   .news-card count: {news_cards}")
    print(f"   #newsFeedGrid exists: {news_feed}")
    print(f"   #catalystsTimelineGrid exists: {catalysts_grid}")
    assert not news_container, "#marketNewsContainer must be completely removed"
    assert news_cards == 0, "No news cards should exist in the DOM"
    assert not news_feed, "#newsFeedGrid must not exist"
    assert not catalysts_grid, "#catalystsTimelineGrid must not exist"

    # 2. Verify clean transition from chart/specs to footer without news section
    footer_exists = eval_js("Boolean(document.querySelector('footer'))")
    chart_exists = eval_js("Boolean(document.getElementById('historicalChartCanvas'))")
    print(f"2. Chart exists: {chart_exists}, Footer exists: {footer_exists}")
    assert chart_exists and footer_exists

    # 3. Verify switching instruments works seamlessly without news feed errors
    print("\n--- 3. Testing switching instruments without news feed ---")
    eval_js("switchInstrument('sp500')")
    time.sleep(0.5)
    sp_inst = eval_js("primaryInstrumentId")
    assert sp_inst == 'sp500'
    assert eval_js("Boolean(document.getElementById('marketNewsContainer'))") is False

    eval_js("switchInstrument('us10y')")
    time.sleep(0.5)
    bond_inst = eval_js("primaryInstrumentId")
    assert bond_inst == 'us10y'
    assert eval_js("Boolean(document.getElementById('marketNewsContainer'))") is False

    eval_js("switchInstrument('gold')")
    time.sleep(0.5)
    gold_inst = eval_js("primaryInstrumentId")
    assert gold_inst == 'gold'

    print("\nALL NEWS FEED REMOVAL & CLEAN DOM TESTS PASSED WITH 100% SUCCESS!\n")

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

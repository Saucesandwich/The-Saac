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
    'file:///c:/Users/user/Downloads/gold tracker test/gold_tracker.html'
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

    print("=== Testing Automated News Headlines & Market Catalysts ===")

    # 1. Verify container existence and placement
    news_container = eval_js("Boolean(document.getElementById('marketNewsContainer'))")
    print(f"1. #marketNewsContainer exists: {news_container}")
    assert news_container

    # Verify positioned before footer and after info-table
    is_before_footer = eval_js("""
      const c = document.getElementById('marketNewsContainer');
      const f = document.querySelector('footer');
      c.compareDocumentPosition(f) & Node.DOCUMENT_POSITION_FOLLOWING
    """)
    print(f"   Positioned immediately before footer: {bool(is_before_footer)}")
    assert bool(is_before_footer)

    # 2. Wait briefly for news feed population and verify articles
    time.sleep(1)
    title_text = eval_js("document.querySelector('.news-title')?.innerText || ''")
    badge_text = eval_js("document.querySelector('.news-badge-live')?.innerText || ''")
    print(f"2. Initial News Title: {title_text}")
    print(f"   Live Badge: {badge_text}")
    assert 'XAU' in title_text or 'GOLD' in title_text
    assert 'LIVE FEED' in badge_text

    card_count = eval_js("document.querySelectorAll('#newsFeedGrid .news-card').length")
    print(f"   News Cards Loaded in Feed Grid: {card_count}")
    assert card_count > 0

    first_headline = eval_js("document.querySelector('#newsFeedGrid .news-card .news-headline')?.innerText || ''")
    first_source = eval_js("document.querySelector('#newsFeedGrid .news-card .news-source-tag')?.innerText || ''")
    print(f"   First Headline: '{first_headline}' | Source: {first_source}")
    assert len(first_headline) > 5

    # 3. Test Subtab Switching: Switch to Historic Market Shocks
    print("\n--- 3. Testing Subtab Switching to Historic Market Shocks ---")
    eval_js("document.getElementById('tabHistoricCatalysts').click()")
    feed_display = eval_js("document.getElementById('newsFeedGrid').style.display")
    shocks_display = eval_js("document.getElementById('catalystsTimelineGrid').style.display")
    shock_cards = eval_js("document.querySelectorAll('#catalystsTimelineGrid .shock-card').length")
    print(f"   Headlines Grid Display: {feed_display} (expected 'none')")
    print(f"   Historic Shocks Grid Display: {shocks_display} (expected 'grid')")
    print(f"   Historical Shock Timeline Cards: {shock_cards}")
    assert feed_display == 'none'
    assert shocks_display == 'grid'
    assert shock_cards >= 3

    # Switch back to Headlines
    eval_js("document.getElementById('tabLatestHeadlines').click()")
    assert eval_js("document.getElementById('newsFeedGrid').style.display") == 'grid'

    # 4. Test Automated News Update on Switching Trackers
    print("\n--- 4. Testing Auto-Update on Switching Trackers ---")
    eval_js("switchInstrument('sp500')")
    time.sleep(1)
    spx_title = eval_js("document.querySelector('.news-title')?.innerText || ''")
    spx_cards = eval_js("document.querySelectorAll('#newsFeedGrid .news-card').length")
    print(f"   S&P 500 News Title: {spx_title}")
    print(f"   S&P 500 News Cards: {spx_cards}")
    assert 'SPX' in spx_title or 'S&P 500' in spx_title
    assert spx_cards > 0

    eval_js("switchInstrument('us10y')")
    time.sleep(1)
    bond_title = eval_js("document.querySelector('.news-title')?.innerText || ''")
    bond_cards = eval_js("document.querySelectorAll('#newsFeedGrid .news-card').length")
    print(f"   US10Y Bond News Title: {bond_title}")
    print(f"   US10Y Bond News Cards: {bond_cards}")
    assert 'US10Y' in bond_title or 'TREASURY' in bond_title or 'YIELD' in bond_title
    assert bond_cards > 0

    # 5. Test Click on Historical Market Shock Highlights Chart
    print("\n--- 5. Testing Historical Shock Click Chart Integration ---")
    eval_js("switchInstrument('gold')")
    eval_js("switchView('historical')")
    eval_js("document.getElementById('tabHistoricCatalysts').click()")
    time.sleep(0.5)

    # Click on the first shock card (e.g. 1997 Asian Crisis)
    eval_js("document.querySelector('#catalystsTimelineGrid .shock-card').click()")
    banner_display = eval_js("document.getElementById('comparisonBanner').style.display")
    flow_text = eval_js("document.getElementById('compGoldFlow')?.innerText || ''")
    print(f"   Comparison Banner Display: {banner_display} (expected 'block')")
    print(f"   Comparison Flow: {flow_text}")
    assert banner_display == 'block'
    assert len(flow_text) > 3

    print("\nALL AUTOMATED NEWS & MARKET CATALYST TESTS PASSED WITH 100% SUCCESS!\n")

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

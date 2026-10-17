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

    # Check Header Title
    top_title = eval_js("document.getElementById('terminalTopTitle')?.textContent.trim()")
    print(f"   Top Header Title: '{top_title}'")
    assert top_title == "The Saac Terminal" or top_title == "THE SAAC TERMINAL", f"Expected 'The Saac Terminal', got '{top_title}'"

    # 2. Switch to S&P 500 (sp500)
    print("\n--- 2. Switching to S&P 500 (sp500) ---")
    eval_js("switchInstrument('sp500')")
    sp_inst = eval_js("primaryInstrumentId")
    sp_label = eval_js("histChartInstance.data.datasets[0].label")
    sp_data = eval_js("histChartInstance.data.datasets[0].data")
    sp_last = sp_data[-1]
    sp_hero_price = eval_js("document.getElementById('goldUsdDisplay').innerText")
    top_title_after_switch = eval_js("document.getElementById('terminalTopTitle')?.textContent.trim()")
    print(f"   Switched to: {sp_inst}, label='{sp_label}', last_val={sp_last}, hero_price='{sp_hero_price}'")
    print(f"   Top Title after switch: '{top_title_after_switch}'")
    assert sp_inst == 'sp500'
    assert top_title_after_switch == "The Saac Terminal" or top_title_after_switch == "THE SAAC TERMINAL", "Top title must remain 'The Saac Terminal'!"
    assert "S&P" in sp_label, f"Expected S&P in label, got {sp_label}"
    assert abs(sp_last - 7659.4) < 30.0, f"S&P 500 price should be ~7,659.4, got {sp_last}"
    assert "7,659" in sp_hero_price or "7659" in sp_hero_price, f"Hero price must show 7,659, got {sp_hero_price}"

    # Test ALL timeframe on S&P 500
    eval_js("filterTimeframe('ALL')")
    sp_all_data = eval_js("histChartInstance.data.datasets[0].data")
    sp_1990 = sp_all_data[0]
    print(f"   S&P 500 ALL history: 1990={sp_1990}, 2026={sp_all_data[-1]}, samples={len(sp_all_data)}")
    assert abs(sp_1990 - 329.08) < 20.0, f"S&P 500 in 1990 was ~329.08, got {sp_1990}"
    assert abs(sp_all_data[-1] - 7659.4) < 20.0, f"S&P 500 in 2026 should be ~7,659.4, got {sp_all_data[-1]}"
    assert len(sp_all_data) == 442, f"Expected 442 monthly candles from 1990-01 to 2026-10, got {len(sp_all_data)}"

    # Test Sample Rates on S&P 500
    print("\n--- Testing Sample Rate Selector on S&P 500 ---")
    rate_wrap_disp = eval_js("window.getComputedStyle(document.getElementById('samplingRateWrap')).display")
    print(f"   #samplingRateWrap display: {rate_wrap_disp}")
    assert rate_wrap_disp != 'none', "Sampling rate wrap must be visible"

    eval_js("filterTimeframe('1D')")
    eval_js("setSamplingRate('10m')")
    pts_10m = eval_js("histChartInstance.data.datasets[0].data.length")
    print(f"   1D @ 10m points: {pts_10m}")
    assert pts_10m == 144, f"Expected 144 points for 1D @ 10m, got {pts_10m}"

    eval_js("setSamplingRate('1h')")
    pts_1h = eval_js("histChartInstance.data.datasets[0].data.length")
    print(f"   1D @ 1h points: {pts_1h}")
    assert pts_1h == 24, f"Expected 24 points for 1D @ 1h, got {pts_1h}"

    eval_js("setSamplingRate('1d')")
    pts_1d = eval_js("histChartInstance.data.datasets[0].data.length")
    print(f"   1D @ 1d points: {pts_1d}")
    assert pts_1d == 2, f"Expected 2 points for 1D @ 1d, got {pts_1d}"

    eval_js("filterTimeframe('1Y')")
    eval_js("setSamplingRate('1mo')")
    pts_1mo = eval_js("histChartInstance.data.datasets[0].data.length")
    sp_1y_vals = eval_js("histChartInstance.data.datasets[0].data")
    print(f"   1Y @ 1mo points: {pts_1mo}, values={sp_1y_vals[:3]}...{sp_1y_vals[-3:]}")
    assert pts_1mo == 12, f"Expected 12 points for 1Y @ 1mo, got {pts_1mo}"
    assert len(set(sp_1y_vals)) >= 10, f"1Y monthly series must NOT be a flat line! Got {sp_1y_vals}"

    # 3. Switch to WTI Crude Oil (crude_oil)
    print("\n--- 3. Switching to WTI Crude Oil (crude_oil) ---")
    eval_js("switchInstrument('crude_oil')")
    oil_inst = eval_js("primaryInstrumentId")
    oil_label = eval_js("histChartInstance.data.datasets[0].label")
    oil_data = eval_js("histChartInstance.data.datasets[0].data")
    oil_last = oil_data[-1]
    oil_hero_price = eval_js("document.getElementById('goldUsdDisplay').innerText")
    assert eval_js("document.getElementById('terminalTopTitle')?.textContent.trim()").lower() == "the saac terminal"
    print(f"   Switched to: {oil_inst}, label='{oil_label}', last_val={oil_last}, hero_price='{oil_hero_price}'")
    assert oil_inst == 'crude_oil'
    assert "Crude Oil" in oil_label
    assert abs(oil_last - 99.04) < 5.0, f"Crude Oil price should be ~$99.04, got {oil_last}"
    assert "99" in oil_hero_price

    # 4. Switch to US 10Y Yield (us10y)
    print("\n--- 4. Switching to US 10-Year Bond Yield (us10y) ---")
    eval_js("switchInstrument('us10y')")
    bond_inst = eval_js("primaryInstrumentId")
    bond_label = eval_js("histChartInstance.data.datasets[0].label")
    bond_data = eval_js("histChartInstance.data.datasets[0].data")
    bond_last = bond_data[-1]
    bond_hero_price = eval_js("document.getElementById('goldUsdDisplay').innerText")
    assert eval_js("document.getElementById('terminalTopTitle')?.textContent.trim()").lower() == "the saac terminal"
    print(f"   Switched to: {bond_inst}, label='{bond_label}', last_val={bond_last}, hero_price='{bond_hero_price}'")
    assert bond_inst == 'us10y'
    assert "10Y" in bond_label or "Yield" in bond_label
    assert abs(bond_last - 5.098) < 0.15, f"US 10Y Yield should be ~5.098%, got {bond_last}"
    assert "5.0" in bond_hero_price or "5.1" in bond_hero_price

    # 5. Switch to Silver (silver)
    print("\n--- 5. Switching to Silver (silver) ---")
    eval_js("switchInstrument('silver')")
    silver_inst = eval_js("primaryInstrumentId")
    silver_label = eval_js("histChartInstance.data.datasets[0].label")
    silver_data = eval_js("histChartInstance.data.datasets[0].data")
    silver_last = silver_data[-1]
    assert eval_js("document.getElementById('terminalTopTitle')?.textContent.trim()").lower() == "the saac terminal"
    print(f"   Switched to: {silver_inst}, label='{silver_label}', last_val={silver_last}")
    assert silver_inst == 'silver'
    assert "Silver" in silver_label
    assert abs(silver_last - 57.13) < 2.0, f"Silver price should be ~$57.13, got {silver_last}"

    # 6. Verify All 31 Markets Have Non-Flat 1Y & 1M Data and Authentic Date Labels
    print("\n--- 6. Verifying All 31 Markets Have Non-Flat 1Y & 1M Series & Authentic Dates ---")
    all_ids = eval_js("Object.keys(window.INSTRUMENTS)")
    assert len(all_ids) == 31, f"Expected 31 instruments, got {len(all_ids)}"
    for inst_id in all_ids:
        s_1y = eval_js(f"getSeriesForInstrument('{inst_id}', '1Y', '1mo').map(d => d.close)")
        s_1m = eval_js(f"getSeriesForInstrument('{inst_id}', '1M', '1d')")
        assert len(set(s_1y)) >= 6, f"Instrument {inst_id} 1Y monthly series is flat: {s_1y}"
        assert len(s_1m) == 30, f"Instrument {inst_id} 1M daily series should have 30 points, got {len(s_1m)}"
        assert not s_1m[0]['date'].startswith('D'), f"Instrument {inst_id} 1M date label must be real YYYY-MM-DD, got {s_1m[0]['date']}"
    print(f"   Verified all {len(all_ids)} instruments have authentic non-flat 1Y & 1M curves and real calendar dates!")

    # 7. Verify Real-Time Data on Market Switcher Side Numbers (#pillPrice_<id> & #pillChange_<id>)
    print("\n--- 7. Verifying Real-Time Market Switcher Side Numbers & Live Ticks ---")
    eval_js("filterCategory('all')")
    pill_side_count = eval_js("document.querySelectorAll('#macroTickerBar .pill-side').length")
    pill_price_before = eval_js("document.getElementById('pillPrice_sp500')?.innerText")
    pill_chg_before = eval_js("document.getElementById('pillChange_sp500')?.innerText")
    print(f"   Market switcher pills count: {pill_side_count}, sp500 before tick: price='{pill_price_before}', chg='{pill_chg_before}'")
    assert pill_side_count == 31, f"Expected 31 market switcher side blocks in #macroTickerBar, got {pill_side_count}"
    assert pill_price_before and len(pill_price_before) > 0
    assert pill_chg_before and ('%' in pill_chg_before)

    # Trigger a real-time market switcher tick and verify live prices update
    eval_js("window.isLivePaused = false; tickMarketSwitchersRealtime();")
    changed_count = eval_js("""
      Object.values(window.INSTRUMENTS).filter(i => i.livePrice !== i.basePrice).length
    """)
    pill_price_after = eval_js("document.getElementById('pillPrice_sp500')?.innerText")
    pill_chg_after = eval_js("document.getElementById('pillChange_sp500')?.innerText")
    print(f"   After tickMarketSwitchersRealtime(): {changed_count}/31 live prices ticked; sp500 now price='{pill_price_after}', chg='{pill_chg_after}'")
    assert changed_count >= 25, f"Expected most instruments to tick in real time, got {changed_count}"

    # 8. Verify Minimalist Neutral Black Palette & No Purple
    print("\n--- 8. Verifying Minimalist Neutral Black Dark Mode & No Purple ---")
    body_bg = eval_js("window.getComputedStyle(document.body).backgroundColor")
    print(f"   body background color: {body_bg}")
    for inst in ['gold', 'sp500', 'crude_oil', 'us10y', 'silver', 'crypto', 'eurusd']:
        eval_js(f"switchInstrument('{inst}')")
        bcolor = eval_js("histChartInstance.data.datasets[0].borderColor")
        assert not any(p in bcolor.lower() for p in ['purple', '#8a2be2', '#9932cc', '#b388ff', '#7c4dff', '#d500f9']), f"Instrument {inst} has purple color: {bcolor}"
    print("   All sampled instruments have vibrant/authentic non-purple colors!")

    print("\n>>> ALL MULTI-ASSET SWITCHING, REAL-TIME TICKER & DATA INTEGRITY TESTS PASSED! <<<")

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

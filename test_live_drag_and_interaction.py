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

temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile_live_drag')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9240',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--window-size=1450,1100',
    'file:///c:/Users/user/Downloads/gold tracker test/gold_tracker.html'
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    targets = json.loads(urllib.request.urlopen('http://localhost:9240/json').read().decode('utf-8'))
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

    print("=== Testing Real-Time Tracker Drag-to-Measure Feature ===")

    # 1. Confirm initial state on Live View
    live_visible = eval_js("document.getElementById('liveView').style.display !== 'none'")
    assert live_visible, "Live view should be visible on initial entry"
    data_len = eval_js("liveChartData.length")
    print(f"1. Live chart initialized with {data_len} data points")
    assert data_len >= 20, "Live chart should be pre-seeded"

    # 2. Test applyLiveSelection programmatic invocation
    print("\n--- 2. Testing applyLiveSelection ---")
    eval_js("applyLiveSelection(5, 20)")
    banner_disp = eval_js("document.getElementById('liveComparisonBanner').style.display")
    box_disp = eval_js("document.getElementById('liveSelectionBox').style.display")
    start_time = eval_js("document.getElementById('liveCompStartTime').innerText")
    end_time = eval_js("document.getElementById('liveCompEndTime').innerText")
    duration = eval_js("document.getElementById('liveCompDuration').innerText")
    gold_flow = eval_js("document.getElementById('liveCompGoldFlow').innerText")
    gold_pct = eval_js("document.getElementById('liveCompGoldPct').innerText")
    thai_bar_flow = eval_js("document.getElementById('liveCompThaiBarFlow').innerText")

    print(f"   Live Banner Display: {banner_disp}, Selection Box: {box_disp}")
    print(f"   Period: {start_time} -> {end_time} {duration}")
    print(f"   Gold Flow: {gold_flow}, Pct: {gold_pct}")
    print(f"   Thai Bar Flow: {thai_bar_flow}")

    assert banner_disp == 'block', "liveComparisonBanner should be displayed!"
    assert box_disp == 'block', "liveSelectionBox should be displayed!"
    assert len(start_time) > 0 and len(end_time) > 0, "Start/End timestamps must be populated!"
    assert "ticks" in duration, "Duration should show ticks count"
    assert "$" in gold_flow, "Gold flow should show prices"
    assert "%" in gold_pct, "Gold percentage must be computed"

    # 3. Test clearLiveSelection
    print("\n--- 3. Testing clearLiveSelection ---")
    eval_js("clearLiveSelection()")
    banner_after = eval_js("document.getElementById('liveComparisonBanner').style.display")
    box_after = eval_js("document.getElementById('liveSelectionBox').style.display")
    print(f"   After Clear: Banner={banner_after}, Box={box_after}")
    assert banner_after == 'none'
    assert box_after == 'none'

    # 4. Test DOM Drag Events on Live Canvas (mousedown -> mousemove -> mouseup)
    print("\n--- 4. Testing DOM Mouse Drag & Measure on Live Canvas ---")
    eval_js("""
        (() => {
            const c = document.getElementById('liveChartCanvas');
            const r = c.getBoundingClientRect();
            const sX = r.left + r.width * 0.25;
            const eX = r.left + r.width * 0.75;
            const y = r.top + r.height * 0.5;

            c.dispatchEvent(new MouseEvent('mousedown', { clientX: sX, clientY: y, bubbles: true }));
            window.dispatchEvent(new MouseEvent('mousemove', { clientX: eX, clientY: y, bubbles: true }));
            window.dispatchEvent(new MouseEvent('mouseup', { clientX: eX, clientY: y, bubbles: true }));
        })();
    """)
    dom_banner_disp = eval_js("document.getElementById('liveComparisonBanner').style.display")
    dom_gold_pct = eval_js("document.getElementById('liveCompGoldPct').innerText")
    dom_duration = eval_js("document.getElementById('liveCompDuration').innerText")
    print(f"   After DOM Drag: banner={dom_banner_disp}, Gold %={dom_gold_pct}, duration={dom_duration}")
    assert dom_banner_disp == 'block', "Dragging across canvas must show liveComparisonBanner!"
    assert "%" in dom_gold_pct, "Percentage must be displayed after drag!"

    # 5. Test Click on Live Canvas to Clear
    print("\n--- 5. Testing Click on Live Canvas to Clear ---")
    eval_js("""
        (() => {
            const c = document.getElementById('liveChartCanvas');
            const r = c.getBoundingClientRect();
            const cX = r.left + r.width * 0.5;
            const cY = r.top + r.height * 0.5;

            c.dispatchEvent(new MouseEvent('mousedown', { clientX: cX, clientY: cY, bubbles: true }));
            window.dispatchEvent(new MouseEvent('mouseup', { clientX: cX, clientY: cY, bubbles: true }));
        })();
    """)
    click_banner_disp = eval_js("document.getElementById('liveComparisonBanner').style.display")
    print(f"   After Single Click: banner={click_banner_disp}")
    assert click_banner_disp == 'none', "Single click must clear live selection!"

    # 6. Verify Interoperability: Switch to Historical, Drag Measure there, Switch back
    print("\n--- 6. Testing Full Cross-Mode Interoperability ---")
    eval_js("switchView('historical')")
    hist_visible = eval_js("document.getElementById('historicalView').style.display === 'block'")
    assert hist_visible

    # Historical drag
    eval_js("applySelection(10, 30)")
    hist_banner = eval_js("document.getElementById('comparisonBanner').style.display")
    hist_flow = eval_js("document.getElementById('compGoldFlow').innerText")
    hist_pct = eval_js("document.getElementById('compGoldPct').innerText")
    print(f"   Historical Drag Measure: banner={hist_banner}, Flow={hist_flow}, %={hist_pct}")
    assert hist_banner == 'block'
    assert len(hist_pct) > 0

    # Switch back to live
    eval_js("switchView('live')")
    live_visible_again = eval_js("document.getElementById('liveView').style.display !== 'none'")
    assert live_visible_again

    # Live drag measure again
    eval_js("applyLiveSelection(2, 15)")
    live_banner_again = eval_js("document.getElementById('liveComparisonBanner').style.display")
    live_pct_again = eval_js("document.getElementById('liveCompGoldPct').innerText")
    print(f"   Live Drag Measure (after returning): banner={live_banner_again}, %={live_pct_again}")
    assert live_banner_again == 'block'
    assert len(live_pct_again) > 0

    print("\nALL REAL-TIME TRACKER DRAG-TO-MEASURE TESTS PASSED PERFECTLY!")

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

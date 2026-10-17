#!/usr/bin/env python3
"""
Test Suite: Chart Overlays (1 to 3 Charts) & Scale Modes
Verifies overlaying charts down to 1 and up to 3 charts, removing overlays,
and toggling between Actual Price (multi-axis) and % Return (normalized relative comparison).
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

temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile_overlays')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9252',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--window-size=1400,1000',
    'file:///c:/Users/user/Downloads/Saac terminal/gold_tracker.html'
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    targets = json.loads(urllib.request.urlopen('http://localhost:9252/json').read().decode('utf-8'))
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

    print("=== Testing Chart Overlays (1 to 3 Charts) ===")

    # 1. Default State: Exactly 1 chart (Gold)
    cnt_default = eval_js("histChartInstance.data.datasets.length")
    ds0_label = eval_js("histChartInstance.data.datasets[0].label")
    p_pill_text = eval_js("document.getElementById('primaryPillLabel').innerText")
    ov_cnt = eval_js("activeOverlays.length")
    print(f"1. Default state: total_charts={cnt_default}, primary_label='{ds0_label}', pill='{p_pill_text}', overlays_cnt={ov_cnt}")
    assert cnt_default == 1, f"Default should be exactly 1 chart, got {cnt_default}"
    assert ov_cnt == 0, f"Default overlays count should be 0, got {ov_cnt}"
    assert "Gold" in ds0_label

    # 2. Add First Overlay (S&P 500) -> 2 Charts Total
    print("\n--- 2. Adding First Overlay: S&P 500 (sp500) ---")
    eval_js("addOverlay('sp500')")
    cnt_after_1 = eval_js("histChartInstance.data.datasets.length")
    ds1_label = eval_js("histChartInstance.data.datasets[1].label")
    ds1_last_val = eval_js("histChartInstance.data.datasets[1].data.slice(-1)[0]")
    pill_elements = eval_js("[...document.querySelectorAll('#activeOverlaysList .wsj-overlay-pill')].map(p => p.innerText.trim())")
    print(f"   Total charts: {cnt_after_1}, Overlay 1: '{ds1_label}' (last_val={ds1_last_val})")
    print(f"   Overlay pills in DOM: {pill_elements}")
    assert cnt_after_1 == 2, f"Expected 2 charts, got {cnt_after_1}"
    assert "S&P" in ds1_label
    assert abs(ds1_last_val - 5850.2) < 30.0, f"Overlay S&P 500 price should be ~5,850, got {ds1_last_val}"
    assert len(pill_elements) == 1
    assert "S&P" in pill_elements[0]

    # 3. Add Second Overlay (US 10Y Yield) -> 3 Charts Total (Maximum)
    print("\n--- 3. Adding Second Overlay: US 10Y Yield (us10y) ---")
    eval_js("addOverlay('us10y')")
    cnt_after_2 = eval_js("histChartInstance.data.datasets.length")
    ds2_label = eval_js("histChartInstance.data.datasets[2].label")
    ds2_last_val = eval_js("histChartInstance.data.datasets[2].data.slice(-1)[0]")
    btn_add_disabled = eval_js("document.getElementById('btnAddOverlay').disabled")
    btn_add_text = eval_js("document.getElementById('btnAddOverlay').innerText")
    print(f"   Total charts: {cnt_after_2}, Overlay 2: '{ds2_label}' (last_val={ds2_last_val})")
    print(f"   Add Button state: disabled={btn_add_disabled}, text='{btn_add_text}'")
    assert cnt_after_2 == 3, f"Expected 3 charts, got {cnt_after_2}"
    assert "10Y" in ds2_label or "Yield" in ds2_label
    assert abs(ds2_last_val - 5.217) < 0.1, f"Overlay US 10Y price should be ~5.217%, got {ds2_last_val}"
    assert btn_add_disabled is True, "Add overlay button must be disabled when max 3 charts reached!"

    # 4. Attempt to Add 3rd Overlay (Crude Oil) -> Must be blocked
    print("\n--- 4. Verifying Maximum Limit (Cannot exceed 3 charts) ---")
    eval_js("addOverlay('crude_oil')")
    cnt_blocked = eval_js("histChartInstance.data.datasets.length")
    print(f"   Total charts after attempting 4th chart: {cnt_blocked}")
    assert cnt_blocked == 3, f"Chart count must NOT exceed 3, got {cnt_blocked}"

    # 5. Remove First Overlay (sp500) -> 2 Charts Remaining
    print("\n--- 5. Removing Overlay 1 (sp500) ---")
    eval_js("removeOverlay('sp500')")
    cnt_after_rem1 = eval_js("histChartInstance.data.datasets.length")
    active_ovs = eval_js("activeOverlays")
    ds_remaining = eval_js("histChartInstance.data.datasets.map(d => d.label)")
    print(f"   Total charts: {cnt_after_rem1}, activeOverlays={active_ovs}, datasets={ds_remaining}")
    assert cnt_after_rem1 == 2, f"Expected 2 charts after removal, got {cnt_after_rem1}"
    assert active_ovs == ['us10y']

    # 6. Remove Second Overlay (us10y) -> Down to 1 Chart
    print("\n--- 6. Removing Overlay 2 (us10y) -> Down to 1 Chart ---")
    eval_js("removeOverlay('us10y')")
    cnt_after_rem2 = eval_js("histChartInstance.data.datasets.length")
    active_ovs2 = eval_js("activeOverlays")
    ds_final = eval_js("histChartInstance.data.datasets.map(d => d.label)")
    print(f"   Total charts: {cnt_after_rem2}, activeOverlays={active_ovs2}, datasets={ds_final}")
    assert cnt_after_rem2 == 1, f"Expected 1 chart remaining, got {cnt_after_rem2}"
    assert len(active_ovs2) == 0

    # 7. Test Normalized % Return Scale Mode
    print("\n--- 7. Testing Normalized % Return Scale Mode ---")
    eval_js("addOverlay('sp500')")
    eval_js("setChartScaleMode('percent')")
    scale_mode = eval_js("chartScaleMode")
    d0_first = eval_js("histChartInstance.data.datasets[0].data[0]")
    d1_first = eval_js("histChartInstance.data.datasets[1].data[0]")
    y_axis_title = eval_js("histChartInstance.options.scales.y.title.text")
    print(f"   Scale mode: {scale_mode}, Dataset 0 start={d0_first}%, Dataset 1 start={d1_first}%")
    print(f"   Y-Axis title: '{y_axis_title}'")
    assert scale_mode == 'percent'
    assert d0_first == 0.0, f"Primary normalized series must start at 0.0%, got {d0_first}"
    assert d1_first == 0.0, f"Overlay normalized series must start at 0.0%, got {d1_first}"
    assert "%" in y_axis_title

    # 8. Test Switching Back to Actual Price Mode
    print("\n--- 8. Switching Back to Actual Price Mode ---")
    eval_js("setChartScaleMode('actual')")
    scale_mode_act = eval_js("chartScaleMode")
    d0_last_act = eval_js("histChartInstance.data.datasets[0].data.slice(-1)[0]")
    d1_last_act = eval_js("histChartInstance.data.datasets[1].data.slice(-1)[0]")
    y1_display = eval_js("histChartInstance.options.scales.y1.display")
    print(f"   Scale mode: {scale_mode_act}, D0 last={d0_last_act}, D1 last={d1_last_act}, Y1 display={y1_display}")
    assert scale_mode_act == 'actual'
    assert abs(d0_last_act - 4180.6) < 30.0 or abs(d0_last_act - 4169.3) < 30.0
    assert abs(d1_last_act - 5850.2) < 30.0
    assert y1_display is True

    print("\n>>> ALL CHART OVERLAY & SCALE MODE TESTS PASSED WITH 100% SUCCESS! <<<")

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

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
    ds1_len = eval_js("histChartInstance.data.datasets[1].data.length")
    labels_len = eval_js("histChartInstance.data.labels.length")
    y1_min = eval_js("histChartInstance.options.scales.y1.min")
    y1_max = eval_js("histChartInstance.options.scales.y1.max")
    meta1_hidden = eval_js("histChartInstance.getDatasetMeta(1).hidden")
    meta1_data_len = eval_js("histChartInstance.getDatasetMeta(1).data.length")
    pill_elements = eval_js("[...document.querySelectorAll('#activeOverlaysList .wsj-overlay-pill')].map(p => p.innerText.trim())")
    btn_remove_primary_disp = eval_js("document.getElementById('btnRemovePrimary').style.display")

    print(f"   Total charts: {cnt_after_1}, Overlay 1: '{ds1_label}' (last_val={ds1_last_val})")
    print(f"   Dataset 1 length={ds1_len}, Labels length={labels_len}")
    print(f"   Y1 scale bounds: [{y1_min}, {y1_max}], meta1_hidden={meta1_hidden}, meta1_points={meta1_data_len}")
    print(f"   btnRemovePrimary display: '{btn_remove_primary_disp}'")
    print(f"   Overlay pills in DOM: {pill_elements}")
    assert cnt_after_1 == 2, f"Expected 2 charts, got {cnt_after_1}"
    assert "S&P" in ds1_label
    assert abs(ds1_last_val - 7659.4) < 30.0, f"Overlay S&P 500 price should be ~7,659.4, got {ds1_last_val}"
    assert ds1_len == labels_len, f"Overlay series must span 100% of labels, got {ds1_len} vs {labels_len}"
    assert y1_min < 7659.4 < y1_max, f"Y1 scale [{y1_min}, {y1_max}] must encompass 7,659.4!"
    assert not meta1_hidden, f"Dataset 1 meta must not be hidden, got {meta1_hidden}"
    assert meta1_data_len == labels_len, f"Dataset 1 must have rendered canvas points for all labels ({meta1_data_len} vs {labels_len})"
    assert btn_remove_primary_disp != 'none', "btnRemovePrimary must be visible when multiple charts active"
    assert len(pill_elements) == 1
    assert "S&P" in pill_elements[0]

    # 3. Add Second Overlay (US 10Y Yield) -> 3 Charts Total (Maximum)
    print("\n--- 3. Adding Second Overlay: US 10Y Yield (us10y) ---")
    eval_js("addOverlay('us10y')")
    cnt_after_2 = eval_js("histChartInstance.data.datasets.length")
    ds2_label = eval_js("histChartInstance.data.datasets[2].label")
    ds2_last_val = eval_js("histChartInstance.data.datasets[2].data.slice(-1)[0]")
    ds2_len = eval_js("histChartInstance.data.datasets[2].data.length")
    y2_min = eval_js("histChartInstance.options.scales.y2.min")
    y2_max = eval_js("histChartInstance.options.scales.y2.max")
    meta2_hidden = eval_js("histChartInstance.getDatasetMeta(2).hidden")
    meta2_data_len = eval_js("histChartInstance.getDatasetMeta(2).data.length")
    btn_add_disabled = eval_js("document.getElementById('btnAddOverlay').disabled")
    btn_add_text = eval_js("document.getElementById('btnAddOverlay').innerText")

    print(f"   Total charts: {cnt_after_2}, Overlay 2: '{ds2_label}' (last_val={ds2_last_val})")
    print(f"   Dataset 2 length={ds2_len}, Labels length={labels_len}")
    print(f"   Y2 scale bounds: [{y2_min}, {y2_max}], meta2_hidden={meta2_hidden}, meta2_points={meta2_data_len}")
    print(f"   Add Button state: disabled={btn_add_disabled}, text='{btn_add_text}'")
    assert cnt_after_2 == 3, f"Expected 3 charts, got {cnt_after_2}"
    assert "10Y" in ds2_label or "Yield" in ds2_label
    assert abs(ds2_last_val - 5.098) < 0.15, f"Overlay US 10Y price should be ~5.098%, got {ds2_last_val}"
    assert ds2_len == labels_len, f"Overlay 2 series must span 100% of labels, got {ds2_len} vs {labels_len}"
    assert y2_min < 5.098 < y2_max, f"Y2 scale [{y2_min}, {y2_max}] must encompass 5.098!"
    assert not meta2_hidden, f"Dataset 2 meta must not be hidden, got {meta2_hidden}"
    assert meta2_data_len == labels_len, f"Dataset 2 must have rendered canvas points for all labels ({meta2_data_len} vs {labels_len})"
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
    btn_rem_prim = eval_js("document.getElementById('btnRemovePrimary').style.display")
    ds_final = eval_js("histChartInstance.data.datasets.map(d => d.label)")
    print(f"   Total charts: {cnt_after_rem2}, activeOverlays={active_ovs2}, btnRemovePrimary={btn_rem_prim}")
    assert cnt_after_rem2 == 1, f"Expected 1 chart remaining, got {cnt_after_rem2}"
    assert len(active_ovs2) == 0
    assert btn_rem_prim == 'none', "btnRemovePrimary must be hidden when only 1 chart is active"

    # 7. Test Removing the 1st (Primary) Chart when 2 and 3 charts are active
    print("\n--- 7. Testing Ability to Remove Primary Chart (Promoting next active series) ---")
    eval_js("addOverlay('sp500')")
    eval_js("addOverlay('us10y')")
    assert eval_js("histChartInstance.data.datasets.length") == 3
    assert eval_js("primaryInstrumentId") == 'gold'
    assert eval_js("document.getElementById('btnRemovePrimary').style.display") != 'none'

    # Remove Gold (the primary chart) -> sp500 becomes new primary, us10y remains overlay
    print("   Calling removePrimaryChart()...")
    eval_js("removePrimaryChart()")
    new_prim = eval_js("primaryInstrumentId")
    new_tot = eval_js("histChartInstance.data.datasets.length")
    new_ovs = eval_js("activeOverlays")
    prim_label = eval_js("document.getElementById('primaryPillLabel').innerText")
    btn_prim_after1 = eval_js("document.getElementById('btnRemovePrimary').style.display")
    print(f"   New Primary: {new_prim}, Total charts: {new_tot}, Overlays: {new_ovs}, Pill text: '{prim_label}'")
    assert new_prim == 'sp500', f"Expected sp500 promoted to primary, got {new_prim}"
    assert new_tot == 2, f"Expected 2 charts remaining, got {new_tot}"
    assert new_ovs == ['us10y'], f"Expected us10y to remain as overlay, got {new_ovs}"
    assert "S&P 500" in prim_label or "SPX" in prim_label
    assert btn_prim_after1 != 'none', "btnRemovePrimary should still be visible because 2 charts are active"

    # Remove sp500 -> us10y becomes new primary, 1 chart remains, btnRemovePrimary hidden
    print("   Calling removePrimaryChart() again down to 1 chart...")
    eval_js("removePrimaryChart()")
    final_prim = eval_js("primaryInstrumentId")
    final_tot = eval_js("histChartInstance.data.datasets.length")
    final_ovs = eval_js("activeOverlays")
    btn_prim_final = eval_js("document.getElementById('btnRemovePrimary').style.display")
    print(f"   Final Primary: {final_prim}, Total: {final_tot}, Overlays: {final_ovs}, btnRemovePrimary={btn_prim_final}")
    assert final_prim == 'us10y', f"Expected us10y promoted to primary, got {final_prim}"
    assert final_tot == 1, f"Expected 1 chart remaining, got {final_tot}"
    assert len(final_ovs) == 0
    assert btn_prim_final == 'none', "btnRemovePrimary must be hidden when only 1 chart remains"

    # 8. Test Normalized % Return Scale Mode
    print("\n--- 8. Testing Normalized % Return Scale Mode ---")
    eval_js("switchInstrument('gold')")
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

    # 9. Test Switching Back to Actual Price Mode
    print("\n--- 9. Switching Back to Actual Price Mode ---")
    eval_js("setChartScaleMode('actual')")
    scale_mode_act = eval_js("chartScaleMode")
    d0_last_act = eval_js("histChartInstance.data.datasets[0].data.slice(-1)[0]")
    d1_last_act = eval_js("histChartInstance.data.datasets[1].data.slice(-1)[0]")
    y1_display = eval_js("histChartInstance.options.scales.y1.display")
    print(f"   Scale mode: {scale_mode_act}, D0 last={d0_last_act}, D1 last={d1_last_act}, Y1 display={y1_display}")
    assert scale_mode_act == 'actual'
    assert abs(d0_last_act - 4180.6) < 30.0 or abs(d0_last_act - 4169.3) < 30.0
    assert abs(d1_last_act - 7659.4) < 30.0
    assert y1_display is True

    # 10. Test Ctrl+Click on Market Switchers (#macroTickerBar .ticker-pill-btn)
    print("\n--- 10. Testing Ctrl+Click on Market Switchers to Add/Remove Comparison ---")
    eval_js("removeOverlay('sp500')")
    assert eval_js("activeOverlays.length") == 0

    # Dispatch synthetic MouseEvent with ctrlKey: true on nasdaq market switcher button
    eval_js("""
      const btnNasdaq = document.querySelector('.ticker-pill-btn[data-id="nasdaq"]');
      btnNasdaq.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, ctrlKey: true }));
    """)
    ovs_ctrl1 = eval_js("activeOverlays")
    nasdaq_cls = eval_js("document.querySelector('.ticker-pill-btn[data-id=\"nasdaq\"]').className")
    print(f"   After Ctrl+Click on nasdaq: activeOverlays={ovs_ctrl1}, btn class='{nasdaq_cls}'")
    assert ovs_ctrl1 == ['nasdaq'], f"Ctrl+Click on nasdaq should add nasdaq to overlays, got {ovs_ctrl1}"
    assert 'overlay-active-1' in nasdaq_cls, f"nasdaq button should have overlay-active-1 class, got '{nasdaq_cls}'"
    assert eval_js("histChartInstance.data.datasets.length") == 2

    # Dispatch synthetic MouseEvent with ctrlKey: true on silver market switcher button
    eval_js("""
      const btnSilver = document.querySelector('.ticker-pill-btn[data-id="silver"]');
      btnSilver.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, ctrlKey: true }));
    """)
    ovs_ctrl2 = eval_js("activeOverlays")
    silver_cls = eval_js("document.querySelector('.ticker-pill-btn[data-id=\"silver\"]').className")
    print(f"   After Ctrl+Click on silver: activeOverlays={ovs_ctrl2}, btn class='{silver_cls}'")
    assert ovs_ctrl2 == ['nasdaq', 'silver'], f"Ctrl+Click on silver should add silver to overlays, got {ovs_ctrl2}"
    assert 'overlay-active-2' in silver_cls, f"silver button should have overlay-active-2 class, got '{silver_cls}'"
    assert eval_js("histChartInstance.data.datasets.length") == 3

    # Dispatch Ctrl+Click again on nasdaq to toggle/remove it from overlays
    eval_js("""
      const btnNasdaq2 = document.querySelector('.ticker-pill-btn[data-id="nasdaq"]');
      btnNasdaq2.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, ctrlKey: true }));
    """)
    ovs_ctrl3 = eval_js("activeOverlays")
    nasdaq_cls_after = eval_js("document.querySelector('.ticker-pill-btn[data-id=\"nasdaq\"]').className")
    print(f"   After second Ctrl+Click on nasdaq (toggle off): activeOverlays={ovs_ctrl3}, class='{nasdaq_cls_after}'")
    assert ovs_ctrl3 == ['silver'], f"Second Ctrl+Click on nasdaq should remove it, got {ovs_ctrl3}"
    assert 'overlay-active' not in nasdaq_cls_after
    assert eval_js("histChartInstance.data.datasets.length") == 2

    # Clean up overlay
    eval_js("removeOverlay('silver')")

    print("\n>>> ALL CHART OVERLAY, CTRL+CLICK COMPARISON & SCALE MODE TESTS PASSED WITH 100% SUCCESS! <<<")

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

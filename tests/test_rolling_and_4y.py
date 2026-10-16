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

temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile_rolling')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9232',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--window-size=1400,1000',
    'file:///c:/Users/user/Downloads/gold tracker test/gold_tracker.html'
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    targets = json.loads(urllib.request.urlopen('http://localhost:9232/json').read().decode('utf-8'))
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

    print("=== Testing Continuous Rolling Timeframe & 4-Year Window ===")

    # Switch to historical
    eval_js("switchView('historical')")
    hist_active = eval_js("document.getElementById('historicalView').style.display === 'block'")
    assert hist_active, "Historical view must be visible!"

    # 1. Test 4-Year Timeframe (Arbitrary non-preset)
    print("\n--- 1. Testing 4-Year Timeframe Display ---")
    eval_js("setContinuousWindow(4 * 365.25)")
    tf_val = eval_js("currentTimeframe")
    days_val = eval_js("currentWindowDurationDays")
    btn_custom_text = eval_js("document.getElementById('tfCustom').innerText")
    btn_custom_disp = eval_js("document.getElementById('tfCustom').style.display")
    btn_custom_active = eval_js("document.getElementById('tfCustom').classList.contains('active')")
    tag_text = eval_js("document.getElementById('currentSamplingTag').innerText")
    rate_val = eval_js("currentSamplingRate")
    cnt_val = eval_js("activeData.length")
    first_candle = eval_js("activeData[0]")
    last_candle = eval_js("activeData[activeData.length - 1]")

    print(f"   Timeframe State: {tf_val}, Duration: {days_val:.1f} days")
    print(f"   Custom Button: text='{btn_custom_text}', display='{btn_custom_disp}', active={btn_custom_active}")
    print(f"   Tag Header: '{tag_text}'")
    print(f"   Sampling Rate: {rate_val}, Samples: {cnt_val}")
    print(f"   First Candle: date={first_candle['date']}, close=${first_candle['close']}")
    print(f"   Last Candle: date={last_candle['date']}, close=${last_candle['close']}")

    assert tf_val == 'CUSTOM', f"Expected currentTimeframe to be 'CUSTOM', got {tf_val}"
    assert btn_custom_text == '4.0Y', f"Expected button text '4.0Y', got {btn_custom_text}"
    assert btn_custom_active is True, "Custom button should have .active class"
    assert "4.0 Years" in tag_text, f"Tag should display 4.0 Years! Got: {tag_text}"
    assert "2022" in first_candle['date'], f"4Y should start in 2022! Got: {first_candle['date']}"
    assert abs(first_candle['close'] - 1633.0) < 50.0, f"Gold close in Oct 2022 was ~$1633! Got: {first_candle['close']}"
    assert abs(last_candle['close'] - 4180.6) < 0.1, f"Gold close in Oct 2026 should be $4,180.6! Got: {last_candle['close']}"

    # 2. Test Sampling Rate inside 4-Year Timeframe (Detail Scaling)
    print("\n--- 2. Testing Detail Scaling within 4-Year Timeframe ---")
    eval_js("setSamplingRate('1d')")
    cnt_1d = eval_js("activeData.length")
    tag_1d = eval_js("document.getElementById('currentSamplingTag').innerText")
    tf_1d = eval_js("currentTimeframe")
    print(f"   4Y with 1d: samples={cnt_1d}, tag='{tag_1d}', tf={tf_1d}")
    assert tf_1d == 'CUSTOM', "Timeframe must stay 4 years when changing to 1d!"
    assert cnt_1d >= 1000, f"Expected ~1461 daily candles for 4Y, got {cnt_1d}"
    assert "4.0 Years" in tag_1d

    eval_js("setSamplingRate('1mo')")
    cnt_1mo = eval_js("activeData.length")
    tag_1mo = eval_js("document.getElementById('currentSamplingTag').innerText")
    tf_after = eval_js("currentTimeframe")
    print(f"   4Y with 1mo: samples={cnt_1mo}, tag='{tag_1mo}', tf={tf_after}")
    assert tf_after == 'CUSTOM', "Timeframe must stay 4 years when changing to 1mo!"
    assert cnt_1mo == 48, f"Expected 48 monthly candles for 4Y, got {cnt_1mo}"
    assert "4.0 Years" in tag_1mo

    # 3. Test Ctrl + Wheel continuous zoom
    print("\n--- 3. Testing Ctrl + Wheel Continuous Zoom Interaction ---")
    # Zoom In from 4Y (factor 1.18)
    initial_days = eval_js("currentWindowDurationDays")
    eval_js("zoomContinuousTimeframe(true, 1.18)")
    zoomed_in_days = eval_js("currentWindowDurationDays")
    print(f"   Zoom In: {initial_days:.1f} days -> {zoomed_in_days:.1f} days")
    assert zoomed_in_days < initial_days, "Zooming in must decrease window duration!"

    # Zoom Out
    eval_js("zoomContinuousTimeframe(false, 1.18)")
    zoomed_out_days = eval_js("currentWindowDurationDays")
    print(f"   Zoom Out: {zoomed_in_days:.1f} days -> {zoomed_out_days:.1f} days")
    assert zoomed_out_days > zoomed_in_days, "Zooming out must increase window duration!"

    # 4. Test Snapping to Preset Buttons
    print("\n--- 4. Testing Snapping to Preset Buttons ---")
    presets = [('1D', 1), ('1W', 7), ('1Y', 365.25), ('3Y', 1095.75), ('5Y', 1826.25), ('ALL', 13436)]
    for pid, expected_days in presets:
        eval_js(f"filterTimeframe('{pid}')")
        curr_days = eval_js("currentWindowDurationDays")
        curr_tf = eval_js("currentTimeframe")
        btn_active = eval_js(f"(document.getElementById('tf{pid}') || document.getElementById('btnTfAll')).classList.contains('active')")
        custom_disp = eval_js("document.getElementById('tfCustom').style.display")
        print(f"   Snap to '{pid}': duration={curr_days:.1f} days, tf={curr_tf}, active={btn_active}, custom_hidden={custom_disp == 'none'}")
        assert curr_tf == pid, f"Expected tf {pid}, got {curr_tf}"
        assert btn_active, f"Preset button {pid} must be active"
        assert custom_disp == 'none', "Custom button should hide when snapped to preset"

    # 5. Test Wheel Event dispatch on #histChartWrap with ctrlKey: true
    print("\n--- 5. Testing DOM Wheel Event Dispatch with ctrlKey=true ---")
    eval_js("filterTimeframe('1Y')")
    before_wheel_days = eval_js("currentWindowDurationDays")
    eval_js("""
        const wrap = document.getElementById('histChartWrap');
        const wheelEvt = new WheelEvent('wheel', {
            deltaY: -100,
            ctrlKey: true,
            bubbles: true,
            cancelable: true
        });
        wrap.dispatchEvent(wheelEvt);
    """)
    after_wheel_days = eval_js("currentWindowDurationDays")
    print(f"   Wheel Scroll UP with Ctrl: {before_wheel_days:.1f} days -> {after_wheel_days:.1f} days")
    assert after_wheel_days < before_wheel_days, "Wheel scroll UP with Ctrl must zoom in (decrease days)!"

    print("\nALL ROLLING TIMEFRAME & 4-YEAR TESTS PASSED SUCCESSFULLY!")

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

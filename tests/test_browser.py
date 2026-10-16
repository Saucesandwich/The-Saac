import subprocess
import time
import json
import urllib.request
import websocket
import os
import sys

# Start Chrome in headless mode with remote debugging
temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9222',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--no-first-run',
    '--no-default-browser-check',
    'file:///c:/Users/user/Downloads/gold tracker test/gold_tracker.html'
]

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(2)

try:
    # Query targets
    targets_data = urllib.request.urlopen('http://localhost:9222/json').read()
    targets = json.loads(targets_data.decode('utf-8'))
    ws_url = None
    for t in targets:
        if t.get('type') == 'page':
            ws_url = t.get('webSocketDebuggerUrl')
            break
    
    if not ws_url:
        print("No page target found!")
        sys.exit(1)

    print(f"Connecting to {ws_url}...")
    ws = websocket.create_connection(ws_url, timeout=10)

    # Enable console and runtime
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

    # Helper to evaluate JS and get result
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
            elif resp.get('method') == 'Runtime.consoleAPICalled':
                print(f"[CONSOLE.{resp['params']['type']}]", resp['params'].get('args'))
            elif resp.get('method') == 'Runtime.exceptionThrown':
                print(f"[PAGE UNCAUGHT EXCEPTION]", resp['params'])

    time.sleep(1)

    print("\n--- 1. Testing Page Load ---")
    title = eval_js("document.title")
    print("Page Title:", title)

    chart_defined = eval_js("typeof Chart !== 'undefined'")
    print("Chart.js defined:", chart_defined)

    live_chart_exists = eval_js("liveChartInstance !== null && liveChartInstance !== undefined")
    print("liveChartInstance exists:", live_chart_exists)

    hist_chart_exists = eval_js("histChartInstance !== null && histChartInstance !== undefined")
    print("histChartInstance exists before switch:", hist_chart_exists)

    print("\n--- 2. Testing switchView('historical') ---")
    eval_js("switchView('historical')")
    hist_chart_exists = eval_js("histChartInstance !== null && histChartInstance !== undefined")
    print("histChartInstance exists after switch:", hist_chart_exists)

    print("\n--- 3. Testing Sampling Rates ---")
    for rate in ['10m', '1h', '1d', '1mo']:
        eval_js(f"setSamplingRate('{rate}')")
        count = eval_js("activeData.length")
        labels_len = eval_js("histChartInstance.data.labels.length")
        print(f"Sampling {rate}: activeData={count}, labels={labels_len}")
        assert count > 0, f"Sampling rate {rate} must have data"

    print("\n--- 3b. Testing Smaller & Standard Timeframes (1D, 1W, 1M, 1Y, etc.) ---")
    for tf in ['1D', '1W', '1M', '1Y', '3Y', '5Y', '10Y', '20Y', 'ALL']:
        eval_js(f"filterTimeframe('{tf}')")
        count = eval_js("activeData.length")
        btn_active = eval_js(f"(document.getElementById('tf{tf}') || document.getElementById('btnTfAll')).classList.contains('active')")
        print(f"Timeframe {tf}: activeData={count}, button active={btn_active}")
        assert count > 0, f"Timeframe {tf} must have active candles"
        assert btn_active, f"Timeframe button for {tf} should have active class"

    print("\n--- 4. Testing Chart Styles ---")
    for style in ['candles', 'caves', 'line']:
        eval_js(f"setChartStyle('{style}')")
        curr_style = eval_js("currentChartStyle")
        print(f"Style set to {style}: confirmed currentChartStyle={curr_style}")

    print("\n--- 5. Testing Overlays Toggle ---")
    for ds_idx in [0, 1, 2]:
        eval_js(f"toggleDataset({ds_idx})")
        hidden = eval_js(f"histChartInstance.getDatasetMeta({ds_idx}).hidden")
        print(f"Toggle dataset {ds_idx}: hidden={hidden}")
        eval_js(f"toggleDataset({ds_idx})")
        hidden = eval_js(f"histChartInstance.getDatasetMeta({ds_idx}).hidden")
        print(f"Toggle back dataset {ds_idx}: hidden={hidden}")

    print("\n--- 6. Testing Drag Selection ---")
    eval_js("applySelection(5, 15)")
    banner_disp = eval_js("document.getElementById('comparisonBanner').style.display")
    gold_pct = eval_js("document.getElementById('compGoldPct').innerText")
    print(f"Apply selection (5, 15): banner display={banner_disp}, Gold %={gold_pct}")

    print("\n--- 7. Testing Era Click ---")
    eval_js("selectDateRangeByLabels('1997-07', '1998-01')")
    thb_pct = eval_js("document.getElementById('compThbPct').innerText")
    print(f"Era 1997-07 to 1998-01: THB %={thb_pct}")

    print("\n--- 8. Testing Switch back to Live ---")
    eval_js("switchView('live')")
    live_disp = eval_js("document.getElementById('liveSection').style.display")
    hist_disp = eval_js("document.getElementById('historicalSection').style.display")
    print(f"Switch back to live: liveSection={live_disp}, histSection={hist_disp}")

    # Check for any queued console errors or exceptions
    print("\nChecking for any unhandled events...")
    ws.settimeout(1)
    try:
        while True:
            resp = json.loads(ws.recv())
            if resp.get('method') == 'Runtime.exceptionThrown':
                print("[EXCEPTION THROWN]", resp['params'])
            elif resp.get('method') == 'Runtime.consoleAPICalled':
                print(f"[CONSOLE.{resp['params']['type']}]", resp['params'].get('args'))
    except websocket.WebSocketTimeoutException:
        print("Done listening.")

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

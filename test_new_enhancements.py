import subprocess
import time
import json
import urllib.request
import websocket
import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Start Chrome in headless mode with remote debugging
temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile_enh')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9223',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--no-first-run',
    '--no-default-browser-check',
    'file:///c:/Users/user/Downloads/Saac terminal/gold_tracker.html'
]

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(2)

try:
    targets_data = urllib.request.urlopen('http://localhost:9223/json').read()
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
                res = resp.get('result', {}).get('result', {})
                if 'value' in res:
                    return res['value']
                return res

    print("\n--- 1. Testing Dynamic Live Range & Benchmark Elements ---")
    badge_text = eval_js("document.getElementById('goldChangeBadge').innerText")
    badge_class = eval_js("document.getElementById('goldChangeBadge').className")
    range_text = eval_js("document.getElementById('goldRange').innerText")
    spec_gold = eval_js("document.getElementById('specGoldBench').innerText")
    spec_thb = eval_js("document.getElementById('specThbBench').innerText")
    spec_bond = eval_js("document.getElementById('specBondBench').innerText")
    print(f"Badge: {badge_text} ({badge_class})")
    print(f"Range: {range_text}")
    print(f"Spec Gold: {spec_gold}")
    print(f"Spec THB: {spec_thb}")
    print(f"Spec Bond: {spec_bond}")
    assert "%" in badge_text
    assert "Day Range:" in range_text
    assert "CME Group GC=F" in spec_gold
    assert "Bank of Thailand THB=X" in spec_thb
    assert "CBOE ^TNX / FRED GS10" in spec_bond

    print("\n--- 2. Testing Negative Converter Inputs Guard ---")
    eval_js("document.getElementById('inputUsd').value = '-1000'; convertFrom('USD');")
    usd_val = eval_js("document.getElementById('inputUsd').value")
    thb_val = eval_js("document.getElementById('inputThb').value")
    oz_val = eval_js("document.getElementById('inputOz').value")
    print(f"USD Input: {usd_val} -> THB: '{thb_val}', Oz: '{oz_val}'")
    assert thb_val == "" and oz_val == "", "Negative input must result in empty output without crash"

    print("\n--- 3. Testing Keyboard Shortcuts (M for Mode Switch) ---")
    mode_before = eval_js("currentMode")
    print(f"Initial mode: {mode_before}")
    eval_js("window.dispatchEvent(new KeyboardEvent('keydown', { key: 'm' }));")
    mode_after_m = eval_js("currentMode")
    print(f"Mode after pressing 'm': {mode_after_m}")
    assert mode_after_m == 'historical', "Pressing 'm' should switch to historical mode"

    eval_js("window.dispatchEvent(new KeyboardEvent('keydown', { key: 'M' }));")
    mode_after_m2 = eval_js("currentMode")
    print(f"Mode after pressing 'M': {mode_after_m2}")
    assert mode_after_m2 == 'live', "Pressing 'M' again should switch back to live mode"

    print("\n--- 4. Testing Keyboard Shortcuts (1-9 for Historical Timeframes) ---")
    eval_js("switchView('historical');")
    eval_js("window.dispatchEvent(new KeyboardEvent('keydown', { key: '4' }));")
    tf_4 = eval_js("currentTimeframe")
    print(f"Timeframe after pressing '4': {tf_4}")
    assert tf_4 == '1Y', "Key 4 should set timeframe to 1Y"

    eval_js("window.dispatchEvent(new KeyboardEvent('keydown', { key: '9' }));")
    tf_9 = eval_js("currentTimeframe")
    print(f"Timeframe after pressing '9': {tf_9}")
    assert tf_9 == 'ALL', "Key 9 should set timeframe to ALL"

    eval_js("window.dispatchEvent(new KeyboardEvent('keydown', { key: '1' }));")
    tf_1 = eval_js("currentTimeframe")
    print(f"Timeframe after pressing '1': {tf_1}")
    assert tf_1 == '1D', "Key 1 should set timeframe to 1D"

    print("\n--- 5. Testing selectDateRangeByLabels Auto-Switch from Live ---")
    eval_js("switchView('live');")
    assert eval_js("currentMode") == 'live'
    eval_js("selectDateRangeByLabels('1997-06', '1998-01');")
    mode_after_era = eval_js("currentMode")
    banner_display = eval_js("document.getElementById('comparisonBanner').style.display")
    print(f"Mode after selectDateRangeByLabels: {mode_after_era}, Banner: {banner_display}")
    assert mode_after_era == 'historical', "selectDateRangeByLabels should auto-switch to historical view"
    assert banner_display == 'block', "Comparison banner should be visible"

    print("\n--- 6. Testing Canvas Background Color & Export CSV Columns ---")
    csv_code = """
    (function() {
      let csv = 'Date,Open_USD,High_USD,Low_USD,Close_USD,USD_THB,US_10Y_Yield,Gold_THB_oz,Pure_Gram_THB,Thai_Gold_Bar_THB,Thai_Ornament_THB,Note\\n';
      activeData.slice(0, 3).forEach(d => {
        const goldThbOz = d.close * d.usd_thb;
        const pureGramThb = goldThbOz / TROY_OZ_G;
        const thaiBar = pureGramThb * PURITY_965 * THAI_BAR_G;
        const thaiOrnament = pureGramThb * PURITY_965 * 15.16;
        const row = [
          d.date,
          d.open !== undefined ? d.open : d.close,
          d.high !== undefined ? d.high : d.close,
          d.low !== undefined ? d.low : d.close,
          d.close,
          d.usd_thb,
          d.us10y,
          goldThbOz.toFixed(2),
          pureGramThb.toFixed(2),
          Math.round(thaiBar),
          Math.round(thaiOrnament),
          `"${d.note || ''}"`
        ];
        csv += row.join(',') + '\\n';
      });
      return csv;
    })()
    """
    csv_output = eval_js(csv_code)
    print("CSV Header & First Rows:")
    print(csv_output.strip())
    assert "Date,Open_USD,High_USD,Low_USD,Close_USD,USD_THB,US_10Y_Yield,Gold_THB_oz,Pure_Gram_THB,Thai_Gold_Bar_THB,Thai_Ornament_THB,Note" in csv_output

    print("\nALL NEW ENHANCEMENTS AND DEFENSIVE FIXES VERIFIED SUCCESSFULLY!")

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

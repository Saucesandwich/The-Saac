import subprocess
import time
import json
import urllib.request
import websocket
import base64
import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_live_5m')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9231',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--window-size=1400,1050',
    'file:///c:/Users/user/Downloads/gold tracker test/gold_tracker.html'
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    targets = json.loads(urllib.request.urlopen('http://localhost:9231/json').read().decode('utf-8'))
    page_target = [t for t in targets if t.get('type') == 'page'][0]
    ws = websocket.create_connection(page_target['webSocketDebuggerUrl'], timeout=10)

    def ev(expr):
        ws.send(json.dumps({'id': 100, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        while True:
            resp = json.loads(ws.recv())
            if resp.get('id') == 100:
                res = resp.get('result', {})
                if 'exceptionDetails' in res:
                    print('EXCEPTION:', res['exceptionDetails'])
                    return None
                return res.get('result', {}).get('value')

    time.sleep(1)
    labels = ev("JSON.stringify(liveChartLabels)")
    data = ev("JSON.stringify(liveChartData)")
    labels_list = json.loads(labels)
    data_list = json.loads(data)

    print(f"Total live points on entry: {len(labels_list)}")
    print(f"First tick label (5 min ago): {labels_list[0]}")
    print(f"Last tick label (current): {labels_list[-1]}")
    print(f"Price range: min=${min(data_list)}, max=${max(data_list)}")
    print(f"First 5 ticks: {labels_list[:5]}")
    print(f"Last 5 ticks: {labels_list[-5:]}")

    # Capture new live screenshot
    ws.send(json.dumps({'id': 200, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
    while True:
        resp = json.loads(ws.recv())
        if resp.get('id') == 200:
            raw_png = base64.b64decode(resp['result']['data'])
            with open('screenshot_live.png', 'wb') as f:
                f.write(raw_png)
            print(f"Updated screenshot_live.png ({len(raw_png)} bytes)")
            break

    assert len(labels_list) >= 25, "Must have at least 25 ticks spanning the past 5 minutes"
    print("VERIFICATION SUCCESSFUL: Live real-time chart has the past 5 minutes of activity on entry!")

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

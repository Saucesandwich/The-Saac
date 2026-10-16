import subprocess
import time
import json
import urllib.request
import os
import sys
import base64
import websocket

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile_tf_bar')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9238',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--window-size=1450,1350',
    'file:///c:/Users/user/Downloads/gold tracker test/gold_tracker.html'
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    targets = json.loads(urllib.request.urlopen('http://localhost:9238/json').read().decode('utf-8'))
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
                    print(f"EXCEPTION: {expression} =>", res['exceptionDetails'])
                    return None
                return res.get('result', {}).get('value')

    def capture_screen(filename):
        time.sleep(0.5)
        req_id = send("Page.captureScreenshot", {"format": "png"})
        while True:
            resp = json.loads(ws.recv())
            if resp.get('id') == req_id:
                data = base64.b64decode(resp['result']['data'])
                with open(filename, 'wb') as f:
                    f.write(data)
                print(f"Captured: {filename} ({len(data)} bytes)")
                break

    eval_js("switchView('historical')")
    eval_js("setContinuousWindow(4 * 365.25)")
    eval_js("setSamplingRate('1w')")
    capture_screen("screenshot_4Y_with_timeframe_bar.png")

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

import subprocess
import time
import json
import urllib.request
import websocket
import base64
import os

temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_screenshot_verify_2')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9252',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--window-size=1400,1050',
    'file:///c:/Users/user/Downloads/gold tracker test/gold_tracker.html'
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
        payload = {'id': msg_id, 'method': method, 'params': params or {}}
        msg_id += 1
        ws.send(json.dumps(payload))
        return msg_id - 1

    send('Runtime.enable')
    send('Page.enable')

    def eval_js(expr):
        req_id = send('Runtime.evaluate', {'expression': expr, 'returnByValue': True, 'awaitPromise': True})
        while True:
            resp = json.loads(ws.recv())
            if resp.get('id') == req_id:
                return resp.get('result', {}).get('result', {}).get('value')

    def capture_screenshot(filename):
        req_id = send('Page.captureScreenshot', {'format': 'png'})
        while True:
            resp = json.loads(ws.recv())
            if resp.get('id') == req_id:
                data = resp['result']['data']
                with open(filename, 'wb') as f:
                    f.write(base64.b64decode(data))
                print(f'Saved {filename}')
                break

    time.sleep(1)

    # 1. Switch to Historical (verify default: 1 day in the past with 1 hour sample rate)
    eval_js("switchView('historical')")
    time.sleep(0.5)
    capture_screenshot("screenshot_default_1D_1h.png")

    # 2. Historical view on 1D with 10m candles
    eval_js("setSamplingRate('10m')")
    time.sleep(0.5)
    capture_screenshot("screenshot_1D_10m.png")

    # 3. Historical view on 1W
    eval_js("filterTimeframe('1W')")
    time.sleep(0.5)
    capture_screenshot("screenshot_1W_view.png")

    # 4. Auto-adjust test: Go to 1Y (1d/1mo), then minimize to 1D
    eval_js("filterTimeframe('1Y')")
    eval_js("setSamplingRate('1mo')")
    time.sleep(0.3)
    eval_js("filterTimeframe('1D')")
    time.sleep(0.5)
    capture_screenshot("screenshot_auto_adjust_1D.png")

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

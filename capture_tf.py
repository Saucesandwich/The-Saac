import subprocess
import time
import json
import urllib.request
import os
import websocket
import base64

temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile_tf')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9235',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--window-size=1400,1250',
    'file:///c:/Users/user/Downloads/Saac terminal/gold_tracker.html'
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    targets = json.loads(urllib.request.urlopen('http://localhost:9235/json').read().decode('utf-8'))
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

    def eval_js(expression):
        req_id = send('Runtime.evaluate', {'expression': expression, 'returnByValue': True, 'awaitPromise': True})
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
    eval_js("switchView('historical')")

    # 1. Capture 1D at 1h (24 candles)
    eval_js("filterTimeframe('1D'); setSamplingRate('1h');")
    time.sleep(0.5)
    capture_screenshot('screenshot_1D_1h_detail.png')

    # 2. Capture 1D at 5m (288 candles)
    eval_js("setSamplingRate('5m')")
    time.sleep(0.5)
    capture_screenshot('screenshot_1D_5m_detail.png')

    # 3. Capture 1W at 1d (7 candles)
    eval_js("filterTimeframe('1W'); setSamplingRate('1d');")
    time.sleep(0.5)
    capture_screenshot('screenshot_1W_1d_detail.png')

    # 4. Capture 1W at 1h (168 candles)
    eval_js("setSamplingRate('1h')")
    time.sleep(0.5)
    capture_screenshot('screenshot_1W_1h_detail.png')

    print('Detail scaling screenshots captured successfully!')

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

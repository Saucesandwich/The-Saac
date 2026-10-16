import subprocess
import os
import time
import urllib.request
import json
import websocket
import base64

temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile_both')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9229',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--window-size=1400,1200',
    'file:///c:/Users/user/Downloads/Saac terminal/gold_tracker.html'
]
proc = subprocess.Popen(cmd)
time.sleep(2)
try:
    targets = json.loads(urllib.request.urlopen('http://localhost:9229/json').read().decode())
    page_target = [t for t in targets if t.get('type') == 'page'][0]
    ws = websocket.create_connection(page_target['webSocketDebuggerUrl'], timeout=10)

    def capture(filename):
        ws.send(json.dumps({'id': 10, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
        while True:
            resp = json.loads(ws.recv())
            if resp.get('id') == 10:
                data = base64.b64decode(resp['result']['data'])
                with open(filename, 'wb') as f:
                    f.write(data)
                print(f"Captured {filename}, size: {len(data)}")
                break

    time.sleep(1)
    capture('screenshot_live.png')

    ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': "switchView('historical')"} }))
    time.sleep(1)
    capture('screenshot_historical.png')

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

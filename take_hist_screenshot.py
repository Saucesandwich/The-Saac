import subprocess
import os
import time
import urllib.request
import json
import websocket
import base64

temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile_hist')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9224',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--window-size=1400,1400',
    'file:///c:/Users/user/Downloads/gold tracker test/gold_tracker.html'
]
proc = subprocess.Popen(cmd)
time.sleep(2)
try:
    targets = json.loads(urllib.request.urlopen('http://localhost:9224/json').read().decode())
    page_target = [t for t in targets if t.get('type') == 'page'][0]
    ws_url = page_target['webSocketDebuggerUrl']
    ws = websocket.create_connection(ws_url, timeout=10)
    
    # Send switch view to historical
    ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': "switchView('historical')"} }))
    time.sleep(1.5)
    
    out_path = os.path.abspath('screenshot_historical.png')
    ws.send(json.dumps({'id': 2, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'} }))
    while True:
        resp = json.loads(ws.recv())
        if resp.get('id') == 2:
            data = base64.b64decode(resp['result']['data'])
            with open(out_path, 'wb') as f:
                f.write(data)
            print('Saved screenshot_historical.png, size:', len(data))
            break
except Exception as e:
    print('Error:', e)
finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

import subprocess
import os
import time
import urllib.request
import json
import websocket
import base64

temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile_rates')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9225',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--window-size=1400,1200',
    'file:///c:/Users/user/Downloads/gold tracker test/gold_tracker.html'
]
proc = subprocess.Popen(cmd)
time.sleep(2)
try:
    targets = json.loads(urllib.request.urlopen('http://localhost:9225/json').read().decode())
    page_target = [t for t in targets if t.get('type') == 'page'][0]
    ws = websocket.create_connection(page_target['webSocketDebuggerUrl'], timeout=10)
    
    # Switch to historical
    ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': "switchView('historical')"} }))
    time.sleep(1)
    
    msg_id = 10
    for rate in ['5m', '30m', '1h', '4h', '1d', '1mo']:
        msg_id += 1
        ws.send(json.dumps({'id': msg_id, 'method': 'Runtime.evaluate', 'params': {'expression': f"setSamplingRate('{rate}')"} }))
        time.sleep(0.5)
        
        msg_id += 1
        out_path = os.path.abspath(f'screenshot_rate_{rate}.png')
        ws.send(json.dumps({'id': msg_id, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'} }))
        while True:
            resp = json.loads(ws.recv())
            if resp.get('id') == msg_id:
                data = base64.b64decode(resp['result']['data'])
                with open(out_path, 'wb') as f:
                    f.write(data)
                print(f'Saved screenshot_rate_{rate}.png, size:', len(data))
                break
except Exception as e:
    print('Error:', e)
finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

import subprocess
import time
import json
import urllib.request
import websocket
import os

temp_dir = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile_chk')
proc = subprocess.Popen([
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9228',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_dir}',
    '--window-size=1400,1000',
    'file:///c:/Users/user/Downloads/Saac terminal/gold_tracker.html'
])
time.sleep(2)
try:
    targets = json.loads(urllib.request.urlopen('http://localhost:9228/json').read().decode())
    p = [t for t in targets if t.get('type') == 'page'][0]
    ws = websocket.create_connection(p['webSocketDebuggerUrl'], timeout=10)

    def ev(expr):
        ws.send(json.dumps({'id': 100, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        while True:
            r = json.loads(ws.recv())
            if r.get('id') == 100:
                res = r.get('result', {})
                if 'exceptionDetails' in res:
                    print('EXCEPTION:', res['exceptionDetails'])
                    return None
                return res.get('result', {}).get('value')

    print("Title:", ev("document.title"))
    print("Chart type:", ev("typeof Chart"))
    ev("switchView('historical')")
    time.sleep(0.5)
    s_y1 = ev("JSON.stringify({left: histChartInstance.scales.y1.left, right: histChartInstance.scales.y1.right, width: histChartInstance.scales.y1.width})")
    s_y2 = ev("JSON.stringify({left: histChartInstance.scales.y2.left, right: histChartInstance.scales.y2.right, width: histChartInstance.scales.y2.width})")
    print("Scale y1:", s_y1)
    print("Scale y2:", s_y2)
    chart_area = ev("JSON.stringify(histChartInstance.chartArea)")
    print("Chart area:", chart_area)
    canvas_w = ev("document.getElementById('historicalChartCanvas').offsetWidth")
    print("Canvas offsetWidth:", canvas_w)
finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

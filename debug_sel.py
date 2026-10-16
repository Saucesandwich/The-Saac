import subprocess, os, time, urllib.request, json, websocket

temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_debug_sel')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9226',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--window-size=1400,1200',
    'file:///c:/Users/user/Downloads/gold tracker test/gold_tracker.html'
]
proc = subprocess.Popen(cmd)
time.sleep(2)
try:
    targets = json.loads(urllib.request.urlopen('http://localhost:9226/json').read().decode())
    page_target = [t for t in targets if t.get('type') == 'page'][0]
    ws = websocket.create_connection(page_target['webSocketDebuggerUrl'], timeout=10)
    
    def eval_js(expr):
        ws.send(json.dumps({'id': 100, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        while True:
            resp = json.loads(ws.recv())
            if resp.get('id') == 100:
                return resp.get('result', {}).get('result', {}).get('value')

    print("Initial (live view):")
    print("histChartInstance:", eval_js("typeof histChartInstance"))
    
    print("\nCalling switchView('historical'):")
    eval_js("switchView('historical')")
    time.sleep(0.5)
    
    sel_info = eval_js("""
    (() => {
        const box = document.getElementById('selectionBox');
        const canvas = document.getElementById('historicalChartCanvas');
        const ca = histChartInstance.chartArea;
        return {
            boxLeft: box.style.left,
            boxWidth: box.style.width,
            boxDisplay: box.style.display,
            chartArea: ca,
            canvasWidth: canvas.width,
            canvasOffsetWidth: canvas.offsetWidth,
            canvasRect: canvas.getBoundingClientRect()
        };
    })()
    """)
    print("Selection info:", json.dumps(sel_info, indent=2))
finally:
    try: ws.close()
    except: pass
    proc.terminate()

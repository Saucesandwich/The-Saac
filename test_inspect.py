import urllib.request, json, websocket

targets = json.loads(urllib.request.urlopen('http://localhost:9222/json').read().decode())
page_target = [t for t in targets if t.get('type') == 'page'][0]
ws = websocket.create_connection(page_target['webSocketDebuggerUrl'])

def eval_js(expr):
    ws.send(json.dumps({'id': 99, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
    while True:
        resp = json.loads(ws.recv())
        if resp.get('id') == 99:
            return resp.get('result', {}).get('result', {}).get('value')

print('Chart Area:', eval_js('JSON.stringify(histChartInstance.chartArea)'))
print('Selection Box:', eval_js('document.getElementById("selectionBox").style.cssText'))
print('Canvas dims:', eval_js('[document.getElementById("historicalChartCanvas").offsetWidth, document.getElementById("historicalChartCanvas").offsetHeight]'))

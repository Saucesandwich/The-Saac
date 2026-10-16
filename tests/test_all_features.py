import subprocess
import time
import json
import urllib.request
import os
import sys
import websocket
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

temp_user_data = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'chrome_test_profile_features')
cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--remote-debugging-port=9230',
    '--remote-allow-origins=*',
    f'--user-data-dir={temp_user_data}',
    '--window-size=1400,1000',
    'file:///c:/Users/user/Downloads/gold tracker test/gold_tracker.html'
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    targets = json.loads(urllib.request.urlopen('http://localhost:9230/json').read().decode('utf-8'))
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
                    print(f"EXCEPTION in eval: {expression} =>", res['exceptionDetails'])
                    return None
                return res.get('result', {}).get('value')

    print("=== Comprehensive Terminal Integration Tests ===")

    # 1. Page & Local Chart.js
    chart_defined = eval_js("typeof Chart !== 'undefined'")
    print(f"1. Chart.js Loaded (Local UMD): {chart_defined}")
    assert chart_defined, "Chart.js must be defined!"

    # 2. Live Chart verification
    live_labels_cnt = eval_js("liveChartLabels.length")
    live_data_cnt = eval_js("liveChartData.length")
    print(f"2. Live Chart Pre-seeded: labels={live_labels_cnt}, points={live_data_cnt}")
    assert live_labels_cnt > 10, "Live chart should be seeded with multiple intraday points!"

    # 3. Converter verification
    eval_js("document.getElementById('inputUsd').value = 5000; convertFrom('USD');")
    thb_val = eval_js("document.getElementById('inputThb').value")
    oz_val = eval_js("document.getElementById('inputOz').value")
    tb_val = eval_js("document.getElementById('inputThaiBaht').value")
    print(f"3. Converter $5,000 USD => THB: ฿{thb_val}, Oz: {oz_val} oz, Thai Bar: {tb_val} บาท")
    assert float(thb_val) > 100000, "THB conversion must be realistic!"

    # 4. Switch to Historical (verify default: 1 day in the past with 1 hour sample rate)
    eval_js("switchView('historical')")
    hist_active = eval_js("document.getElementById('historicalView').style.display === 'block'")
    def_tf = eval_js("currentTimeframe")
    def_rate = eval_js("currentSamplingRate")
    def_samples = eval_js("activeData.length")
    def_style = eval_js("currentChartStyle")
    tf1d_active = eval_js("document.getElementById('tf1D').classList.contains('active')")
    rate1h_active = eval_js("document.getElementById('rate1h').classList.contains('active')")
    style_line_active = eval_js("document.getElementById('styleLine').classList.contains('active')")
    style_buttons = eval_js("[...document.querySelectorAll('.control-cluster button[id^=\"style\"]')].map(b => b.id)")
    print(f"4. Switch to Historical View: active={hist_active}, def_tf={def_tf}, def_rate={def_rate}, samples={def_samples}, def_style={def_style}")
    print(f"   Graph Style slot ordering in DOM: {style_buttons}")
    assert hist_active
    assert def_tf == '1D', f"Default timeframe must be 1D, got {def_tf}"
    assert def_rate == '1h', f"Default rate must be 1h, got {def_rate}"
    assert def_samples == 24, f"Default 1D 1h must have 24 candles, got {def_samples}"
    assert def_style == 'line', f"Default chart style must be line, got {def_style}"
    assert tf1d_active, "tf1D button must have active class by default"
    assert rate1h_active, "rate1h button must have active class by default"
    assert style_line_active, "styleLine button must have active class by default"
    assert style_buttons == ['styleLine', 'styleCaves', 'styleCandles'], f"Line must be first and Candles last! Got {style_buttons}"

    # 5. Verify absence of log graph mode
    scale_log_btn = eval_js("document.getElementById('scaleLog')")
    scale_type = eval_js("histChartInstance.options.scales.y.type")
    print(f"5. Absence of Log Graph Mode: scaleLog={scale_log_btn}, scale_type={scale_type}")
    assert scale_log_btn is None, "scaleLog button must not exist in DOM!"
    assert scale_type == 'linear', "Chart scale must be linear!"

    # 6. Test all 3 Supported Chart Styles (dotted and stepped removed)
    for style in ['candles', 'caves', 'line']:
        eval_js(f"setChartStyle('{style}')")
        curr = eval_js("currentChartStyle")
        print(f"6. Chart Style set to '{style}': verified={curr == style}")
        assert curr == style

    # Verify absence of dotted and stepped buttons in DOM
    dotted_btn = eval_js("document.getElementById('styleDotted')")
    stepped_btn = eval_js("document.getElementById('styleStepped')")
    print(f"   Style absence check: styleDotted={dotted_btn}, styleStepped={stepped_btn}")
    assert dotted_btn is None, "styleDotted button must not exist in DOM!"
    assert stepped_btn is None, "styleStepped button must not exist in DOM!"

    # 7. Test all 4 Supported Sampling Rates (4h and 1w removed)
    for rate in ['10m', '1h', '1d', '1mo']:
        eval_js(f"setSamplingRate('{rate}')")
        cnt = eval_js("activeData.length")
        curr_rate = eval_js("currentSamplingRate")
        y1_min = eval_js("histChartInstance.options.scales.y1.min")
        y1_max = eval_js("histChartInstance.options.scales.y1.max")
        y2_min = eval_js("histChartInstance.options.scales.y2.min")
        y2_max = eval_js("histChartInstance.options.scales.y2.max")
        print(f"7. Sampling Rate '{rate}': {cnt} candles, THB Scale=[{y1_min}, {y1_max}], Yield Scale=[{y2_min}, {y2_max}]")
        assert cnt > 1, f"Sampling rate {rate} must have candles!"
        assert y1_max > y1_min, f"THB scale must have valid range for {rate}"
        assert y2_max > y2_min, f"Yield scale must have valid range for {rate}"

    # 8. Test Overlay Toggles (without arguments, with arguments)
    for ds_idx in [0, 1, 2]:
        eval_js(f"toggleDataset({ds_idx})")
        hidden = eval_js(f"histChartInstance.getDatasetMeta({ds_idx}).hidden")
        print(f"8. Toggle Dataset {ds_idx} hidden={hidden}")
        assert hidden is True
        eval_js(f"toggleDataset({ds_idx})")
        hidden = eval_js(f"histChartInstance.getDatasetMeta({ds_idx}).hidden")
        print(f"   Toggle Dataset {ds_idx} back hidden={hidden}")
        assert hidden is False

    # 9. Test Preset Historic Eras
    eras = [
        ('1997-06', '1998-01', 'Tom Yum Kung'),
        ('2007-07', '2011-09', '2008 GFC to 2011 ATH'),
        ('2019-12', '2020-08', 'COVID Shock'),
        ('2022-03', '2024-10', 'Tightening & ATH'),
        ('2025-06', '2026-10', '2026 $4k Milestone')
    ]
    for d1, d2, name in eras:
        eval_js(f"selectDateRangeByLabels('{d1}', '{d2}')")
        flow = eval_js("document.getElementById('compGoldFlow').innerText")
        pct = eval_js("document.getElementById('compGoldPct').innerText")
        thb_pct = eval_js("document.getElementById('compThbPct').innerText")
        print(f"9. Era '{name}' ({d1} to {d2}): Gold Flow={flow}, Gold %={pct}, THB %={thb_pct}")
        assert len(flow) > 0 and len(pct) > 0

    # 10. Test Clear Selection
    eval_js("clearSelection()")
    banner_disp = eval_js("document.getElementById('comparisonBanner').style.display")
    box_disp = eval_js("document.getElementById('selectionBox').style.display")
    print(f"10. Clear Selection: banner={banner_disp}, box={box_disp}")
    assert banner_disp == 'none'
    assert box_disp == 'none'

    # 11. Test Timeframe Filters & Multi-Resolution Detail Scaling
    for tf in ['1D', '1W', '1M', '1Y', '3Y', '5Y', '10Y', '20Y', 'ALL']:
        eval_js(f"filterTimeframe('{tf}')")
        cnt = eval_js("activeData.length")
        btn_active = eval_js(f"(document.getElementById('tf{tf}') || document.getElementById('btnTfAll')).classList.contains('active')")
        print(f"11. Timeframe '{tf}': active candles={cnt}, button active={btn_active}")
        assert cnt > 0, f"Timeframe {tf} must have active candles!"
        assert btn_active, f"Timeframe button for {tf} should have active class!"

    # 11b. Verify user requirement: Sampling rate keeps the same timeframe and increases sample detail!
    print("\n--- 11b. Testing Detail Scaling in 1D Timeframe (including 10m) ---")
    eval_js("filterTimeframe('1D')")
    d_rates = [('1d', 2), ('1h', 24), ('10m', 144)]
    prev_cnt = 0
    for r, expected_cnt in d_rates:
        eval_js(f"setSamplingRate('{r}')")
        tf = eval_js("currentTimeframe")
        curr_r = eval_js("currentSamplingRate")
        cnt = eval_js("activeData.length")
        print(f"   1D at '{r}': timeframe={tf}, samples={cnt} (expected={expected_cnt})")
        assert tf == '1D', f"Timeframe must stay 1D! Got {tf}"
        assert cnt == expected_cnt, f"Expected {expected_cnt} samples for {r} in 1D, got {cnt}"
        assert cnt > prev_cnt, f"Samples must increase as granularity gets finer! {cnt} vs {prev_cnt}"
        prev_cnt = cnt

    print("\n--- 11c. Testing Detail Scaling in 1W Timeframe ---")
    eval_js("filterTimeframe('1W')")
    w_rates = [('1d', 7), ('1h', 168)]
    prev_cnt = 0
    for r, expected_cnt in w_rates:
        eval_js(f"setSamplingRate('{r}')")
        tf = eval_js("currentTimeframe")
        cnt = eval_js("activeData.length")
        print(f"   1W at '{r}': timeframe={tf}, samples={cnt} (expected={expected_cnt})")
        assert tf == '1W', f"Timeframe must stay 1W! Got {tf}"
        assert cnt == expected_cnt, f"Expected {expected_cnt} samples for {r} in 1W, got {cnt}"
        assert cnt > prev_cnt, f"Samples must increase as granularity gets finer! {cnt} vs {prev_cnt}"
        prev_cnt = cnt

    print("\n--- 11d. Testing Detail Scaling in 1Y Timeframe ---")
    eval_js("filterTimeframe('1Y')")
    y_rates = [('1mo', 12), ('1d', 250)]
    prev_cnt = 0
    for r, expected_cnt in y_rates:
        eval_js(f"setSamplingRate('{r}')")
        tf = eval_js("currentTimeframe")
        cnt = eval_js("activeData.length")
        print(f"   1Y at '{r}': timeframe={tf}, samples={cnt} (expected={expected_cnt})")
        assert tf == '1Y', f"Timeframe must stay 1Y! Got {tf}"
        assert cnt == expected_cnt, f"Expected {expected_cnt} samples for {r} in 1Y, got {cnt}"
        assert cnt > prev_cnt, f"Samples must increase as granularity gets finer! {cnt} vs {prev_cnt}"
        prev_cnt = cnt

    print("\n--- 11e. Testing 10m Exclusivity & Auto-Snap to 1D ---")
    eval_js("filterTimeframe('1W')")
    opacity_1w = eval_js("document.getElementById('rate10m').style.opacity")
    title_1w = eval_js("document.getElementById('rate10m').title")
    print(f"   10m button on 1W: opacity={opacity_1w}, title='{title_1w}'")
    assert opacity_1w == '0.35', "10m button must be dimmed (opacity 0.35) when viewing 1W!"
    assert "only available for 1D" in title_1w

    eval_js("filterTimeframe('1Y')")
    opacity_1y = eval_js("document.getElementById('rate10m').style.opacity")
    print(f"   10m button on 1Y: opacity={opacity_1y}")
    assert opacity_1y == '0.35', "10m button must be dimmed on 1Y!"

    # Clicking 10m while on 1Y should snap back to 1D with 144 samples
    eval_js("setSamplingRate('10m')")
    tf_after_10m = eval_js("currentTimeframe")
    cnt_after_10m = eval_js("activeData.length")
    opacity_after_10m = eval_js("document.getElementById('rate10m').style.opacity")
    print(f"   Clicking 10m from 1Y snaps timeframe to: {tf_after_10m}, samples={cnt_after_10m}, opacity={opacity_after_10m}")
    assert tf_after_10m == '1D', "Clicking 10m must snap timeframe to 1D!"
    assert cnt_after_10m == 144, "1D at 10m must have exactly 144 candles!"
    assert opacity_after_10m == '1', "10m button must be fully active on 1D!"

    print("\n--- 11f. Testing Auto-Adjust Sampling Rate When Minimizing Timeframe & Absence of 4h/1w ---")
    rate4h_el = eval_js("document.getElementById('rate4h')")
    rate1w_el = eval_js("document.getElementById('rate1w')")
    print(f"   Absence check: rate4h={rate4h_el}, rate1w={rate1w_el}")
    assert rate4h_el is None, "rate4h button must not exist in DOM!"
    assert rate1w_el is None, "rate1w button must not exist in DOM!"

    # Test auto-adjust when minimizing from 1Y with 1d to 1D
    eval_js("filterTimeframe('1Y')")
    eval_js("setSamplingRate('1d')")
    y_rate = eval_js("currentSamplingRate")
    print(f"   At 1Y: currentSamplingRate={y_rate}")
    # Minimize to 1D
    eval_js("filterTimeframe('1D')")
    minimized_rate = eval_js("currentSamplingRate")
    minimized_cnt = eval_js("activeData.length")
    print(f"   After minimizing to 1D: rate={minimized_rate}, samples={minimized_cnt}")
    assert minimized_rate == '1h', f"Minimizing to 1D must auto-adjust to 1h for best viewability! Got {minimized_rate}"
    assert minimized_cnt == 24, f"Minimizing to 1D must show 24 hourly candles! Got {minimized_cnt}"

    # Test auto-adjust when minimizing from 5Y with 1mo to 1M
    eval_js("filterTimeframe('5Y')")
    eval_js("setSamplingRate('1mo')")
    eval_js("filterTimeframe('1M')")
    m_rate = eval_js("currentSamplingRate")
    m_cnt = eval_js("activeData.length")
    print(f"   After minimizing from 5Y (1mo) to 1M: rate={m_rate}, samples={m_cnt}")
    assert m_rate == '1d', f"Minimizing to 1M must auto-adjust to 1d (30 candles) for best viewability! Got {m_rate}"
    assert m_cnt == 30, f"1M must have 30 daily candles! Got {m_cnt}"

    # Test continuous zoom minimizing to <= 2 days
    eval_js("setContinuousWindow(365)")
    eval_js("setSamplingRate('1d')")
    eval_js("zoomContinuousTimeframe(true, 250)") # Zoom in to ~1.46 days
    zoom_days = eval_js("currentWindowDurationDays")
    zoom_rate = eval_js("currentSamplingRate")
    zoom_cnt = eval_js("activeData.length")
    print(f"   Continuous zoom in to {zoom_days:.2f} days: rate={zoom_rate}, samples={zoom_cnt}")
    assert zoom_days <= 2.2, "Zoom in must reduce duration below 2.2 days"
    assert zoom_rate == '1h', f"Minimizing via continuous zoom below 2.2 days must auto-adjust to 1h! Got {zoom_rate}"
    assert zoom_cnt > 10, "Must have viewable candle count"

    print("\n--- 11g. Testing 50 Sample Nodes Threshold (Smooth Line vs Specific Nodes) ---")
    eval_js("filterTimeframe('1D')")
    eval_js("setSamplingRate('1h')") # 24 samples (<= 50)
    cnt_24 = eval_js("activeData.length")
    eval_js("setChartStyle('line')")
    p0_line_24 = eval_js("histChartInstance.data.datasets[0].pointRadius")
    p1_line_24 = eval_js("histChartInstance.data.datasets[1].pointRadius")
    p2_line_24 = eval_js("histChartInstance.data.datasets[2].pointRadius")
    print(f"   <= 50 nodes (24 samples) in 'line': ds0={p0_line_24}, ds1={p1_line_24}, ds2={p2_line_24}")
    assert cnt_24 == 24, "Should have 24 samples"
    assert p0_line_24 == 2, "ds0 should show specific nodes (radius 2) when <= 50 nodes"
    assert p1_line_24 == 2, "ds1 should show specific nodes (radius 2) when <= 50 nodes"
    assert p2_line_24 == 2, "ds2 should show specific nodes (radius 2) when <= 50 nodes"

    eval_js("setChartStyle('caves')")
    p0_caves_24 = eval_js("histChartInstance.data.datasets[0].pointRadius")
    print(f"   <= 50 nodes (24 samples) in 'caves': ds0={p0_caves_24}")
    assert p0_caves_24 == 2, "ds0 should show specific nodes in caves when <= 50 nodes"

    eval_js("setChartStyle('candles')")
    p0_candles_24 = eval_js("histChartInstance.data.datasets[0].pointRadius")
    p1_candles_24 = eval_js("histChartInstance.data.datasets[1].pointRadius")
    print(f"   <= 50 nodes (24 samples) in 'candles': ds0={p0_candles_24}, ds1={p1_candles_24}")
    assert p0_candles_24 == 0, "ds0 pointRadius should be 0 in candles mode (rendered as candle bars)"
    assert p1_candles_24 == 2, "ds1 overlay should show nodes when <= 50 nodes"

    # Now test with > 50 nodes (144 samples in 10m)
    eval_js("setSamplingRate('10m')")
    cnt_144 = eval_js("activeData.length")
    eval_js("setChartStyle('line')")
    p0_line_144 = eval_js("histChartInstance.data.datasets[0].pointRadius")
    p1_line_144 = eval_js("histChartInstance.data.datasets[1].pointRadius")
    p2_line_144 = eval_js("histChartInstance.data.datasets[2].pointRadius")
    print(f"   > 50 nodes (144 samples) in 'line': ds0={p0_line_144}, ds1={p1_line_144}, ds2={p2_line_144}")
    assert cnt_144 == 144, "Should have 144 samples"
    assert p0_line_144 == 0, "ds0 must NOT show specific nodes (>50 samples) - smooth line only!"
    assert p1_line_144 == 0, "ds1 must NOT show specific nodes (>50 samples) - smooth line only!"
    assert p2_line_144 == 0, "ds2 must NOT show specific nodes (>50 samples) - smooth line only!"

    eval_js("setChartStyle('caves')")
    p0_caves_144 = eval_js("histChartInstance.data.datasets[0].pointRadius")
    p1_caves_144 = eval_js("histChartInstance.data.datasets[1].pointRadius")
    print(f"   > 50 nodes (144 samples) in 'caves': ds0={p0_caves_144}, ds1={p1_caves_144}")
    assert p0_caves_144 == 0, "ds0 must NOT show specific nodes in caves when > 50 samples"
    assert p1_caves_144 == 0, "ds1 must NOT show specific nodes in caves when > 50 samples"

    # Switch back to 1h (24 samples <= 50) and verify nodes restore
    eval_js("setSamplingRate('1h')")
    p0_restored = eval_js("histChartInstance.data.datasets[0].pointRadius")
    print(f"   Switch back to 1h (24 samples <= 50): ds0 pointRadius restored={p0_restored}")
    assert p0_restored == 2, "ds0 pointRadius should restore to 2 when returning to <= 50 samples!"

    # 12. Switch back to live
    eval_js("switchView('live')")
    live_active = eval_js("document.getElementById('liveSection').style.display === 'block'")
    print(f"12. Switch back to Live: liveSection={live_active}")
    assert live_active

    # 13. Test Real-Time Tracker Drag-to-Measure & Click-to-Clear
    print("\n--- 13. Testing Live Drag-to-Measure & Click-to-Clear ---")
    eval_js("applyLiveSelection(3, 18)")
    live_banner_disp = eval_js("document.getElementById('liveComparisonBanner').style.display")
    live_box_disp = eval_js("document.getElementById('liveSelectionBox').style.display")
    live_gold_flow = eval_js("document.getElementById('liveCompGoldFlow').innerText")
    live_gold_pct = eval_js("document.getElementById('liveCompGoldPct').innerText")
    live_thai_bar = eval_js("document.getElementById('liveCompThaiBarFlow').innerText")
    print(f"   Live Drag Measure (3 to 18): banner={live_banner_disp}, Gold Flow={live_gold_flow}, Pct={live_gold_pct}, Thai Bar={live_thai_bar}")
    assert live_banner_disp == 'block', "Live comparison banner must display on drag!"
    assert live_box_disp == 'block', "Live selection box must display on drag!"
    assert "%" in live_gold_pct, "Live percentage must be computed!"
    assert "฿" in live_thai_bar, "Thai gold bar impact must be displayed!"

    # Click to clear live selection
    eval_js("clearLiveSelection()")
    live_banner_after = eval_js("document.getElementById('liveComparisonBanner').style.display")
    live_box_after = eval_js("document.getElementById('liveSelectionBox').style.display")
    print(f"   Live Clear: banner={live_banner_after}, box={live_box_after}")
    assert live_banner_after == 'none', "Live banner must hide on clear!"
    assert live_box_after == 'none', "Live box must hide on clear!"

    # 14. Test Real-Time Tracker Vertical Line Hover Interaction
    print("\n--- 14. Testing Live Vertical Line Hover Interaction ---")
    live_inter_mode = eval_js("liveChartInstance.options.interaction.mode")
    live_inter_intersect = eval_js("liveChartInstance.options.interaction.intersect")
    print(f"   Live Interaction Config: mode={live_inter_mode}, intersect={live_inter_intersect}")
    assert live_inter_mode == 'index', f"Live interaction mode must be 'index', got {live_inter_mode}"
    assert live_inter_intersect == False, f"Live interaction intersect must be False, got {live_inter_intersect}"

    rect_live = eval_js("document.getElementById('liveChartCanvas').getBoundingClientRect().toJSON()")
    send("Input.dispatchMouseEvent", {
        "type": "mouseMoved",
        "x": rect_live['left'] + 350,
        "y": rect_live['top'] + 60
    })
    time.sleep(0.5)

    live_tooltip_active = eval_js("Boolean(liveChartInstance.tooltip && liveChartInstance.tooltip.opacity > 0)")
    live_tooltip_title = eval_js("liveChartInstance.tooltip ? liveChartInstance.tooltip.title[0] : ''")
    live_tooltip_lines = eval_js("liveChartInstance.tooltip ? liveChartInstance.tooltip.body[0].lines : []")
    print(f"   Hovering high above nodes: tooltip active={live_tooltip_active}, title={live_tooltip_title}, lines={live_tooltip_lines}")
    assert live_tooltip_active, "Live tooltip must be active when hovering in vertical line of mouse above nodes!"
    assert any("Gold" in line for line in live_tooltip_lines), "Tooltip must display gold price!"

    # 15. Test New Features & Consistency Fixes (24K Grams, Quick Presets, Converter Refresh Persistence, Pause Toggle, Window Analytics, Daily Anchors)
    print("\n--- 15. Testing New Features & Consistency Fixes ---")
    anchor_cnt = eval_js("MASTER_ANCHORS.length")
    print(f"   Enriched MASTER_ANCHORS count: {anchor_cnt}")
    assert anchor_cnt > 2500, f"Expected > 2500 daily+monthly anchors in MASTER_ANCHORS, got {anchor_cnt}"

    eval_js("setQuickConvert('GRAMS', 100)")
    g_val = float(eval_js("document.getElementById('inputGrams').value"))
    oz_from_g = float(eval_js("document.getElementById('inputOz').value"))
    src_before = eval_js("lastConverterSource")
    eval_js("refreshLiveData()")
    g_val_after = float(eval_js("document.getElementById('inputGrams').value"))
    src_after = eval_js("lastConverterSource")
    print(f"   Quick Convert 100g => {oz_from_g} oz, source preserved across refreshLiveData: {src_before} -> {src_after}, grams={g_val_after}")
    assert g_val == 100.0 and g_val_after == 100.0, "Converter must preserve user-edited GRAMS field across live refresh!"
    assert src_after == 'GRAMS', f"lastConverterSource must remain GRAMS, got {src_after}"
    assert abs(oz_from_g - (100.0 / 31.1034768)) < 0.01

    eval_js("toggleLivePause()")
    paused_state = eval_js("isLivePaused")
    pause_btn_txt = eval_js("document.getElementById('btnPauseLive').innerText")
    print(f"   Live Pause Toggle: isLivePaused={paused_state}, btn='{pause_btn_txt}'")
    assert paused_state is True and "Resume" in pause_btn_txt
    eval_js("toggleLivePause()")
    assert eval_js("isLivePaused") is False

    eval_js("switchView('historical')")
    eval_js("filterTimeframe('5Y')")
    sum_ret = eval_js("document.getElementById('summaryPeriodReturn').innerText")
    sum_hl = eval_js("document.getElementById('summaryHighLow').innerText")
    sum_dd = eval_js("document.getElementById('summaryMaxDrawdown').innerText")
    sum_tb = eval_js("document.getElementById('summaryThaiBarRange').innerText")
    print(f"   5Y Window Summary Analytics: Return='{sum_ret}', High/Low='{sum_hl}', MaxDD='{sum_dd}', ThaiBar='{sum_tb}'")
    assert "%" in sum_ret and "Δ $" in sum_hl and "%" in sum_dd and "฿" in sum_tb

    print("\nALL 15 INTEGRATION TEST SUITES PASSED SUCCESSFULLY!")

finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()

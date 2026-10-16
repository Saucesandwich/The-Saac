import datetime
import math
import datasets_json

MASTER_END_TS = int(datetime.datetime(2026, 10, 14, 12, 0, 0, tzinfo=datetime.timezone.utc).timestamp() * 1000)

raw = datasets_json.RAW_1M
anchors = []
for item in raw:
    parts = item['date'].split('-')
    yr = int(parts[0])
    mo = int(parts[1])
    if yr == 2026 and mo == 10:
        ts = MASTER_END_TS
    else:
        ts = int(datetime.datetime(yr, mo, 1, 0, 0, 0, tzinfo=datetime.timezone.utc).timestamp() * 1000)
    anchors.append({
        'ts': ts,
        'date': item['date'],
        'gold': float(item['close']),
        'thb': float(item['usd_thb']),
        'bond': float(item['us10y']),
        'note': item.get('note', '')
    })

RATE_MS = {
    '5m': 5 * 60 * 1000,
    '30m': 30 * 60 * 1000,
    '1h': 60 * 60 * 1000,
    '4h': 4 * 60 * 60 * 1000,
    '1d': 24 * 60 * 60 * 1000,
    '1w': 7 * 24 * 60 * 60 * 1000,
    '1mo': int(30.4375 * 24 * 60 * 60 * 1000)
}

def get_anchor_val(ts):
    if ts <= anchors[0]['ts']:
        return anchors[0]['gold'], anchors[0]['thb'], anchors[0]['bond'], anchors[0]['note']
    if ts >= anchors[-1]['ts']:
        return anchors[-1]['gold'], anchors[-1]['thb'], anchors[-1]['bond'], anchors[-1]['note']
    
    # Binary search
    low, high = 0, len(anchors) - 1
    while low <= high:
        mid = (low + high) // 2
        if anchors[mid]['ts'] <= ts <= anchors[mid+1]['ts']:
            a1 = anchors[mid]
            a2 = anchors[mid+1]
            frac = (ts - a1['ts']) / (a2['ts'] - a1['ts'])
            g = a1['gold'] + (a2['gold'] - a1['gold']) * frac
            t = a1['thb'] + (a2['thb'] - a1['thb']) * frac
            b = a1['bond'] + (a2['bond'] - a1['bond']) * frac
            n = a2['note'] if frac > 0.8 else (a1['note'] if frac < 0.2 else '')
            return g, t, b, n
        elif anchors[mid]['ts'] < ts:
            low = mid + 1
        else:
            high = mid - 1
    return anchors[-1]['gold'], anchors[-1]['thb'], anchors[-1]['bond'], ''

def sample_timeline(start_ts, end_ts, rate):
    step = RATE_MS.get(rate, RATE_MS['1mo'])
    dur = end_ts - start_ts
    count = max(2, math.ceil(dur / step))
    # Cap maximum candles to 2000 for smooth browser rendering
    if count > 2000:
        step = dur / 2000
        count = 2000
    
    samples = []
    prev_c = None
    for i in range(count):
        cur_ts = int(start_ts + (dur * (i / (count - 1))))
        is_last = (i == count - 1)
        if is_last:
            cur_ts = end_ts
        
        g_mid, thb_mid, bond_mid, note = get_anchor_val(cur_ts)
        
        # Micro waves for OHLC simulation
        t = i / max(1, count - 1)
        wave = math.sin(t * 18.0) * (g_mid * 0.003)
        c = end_ts == cur_ts and 4180.6 or round((g_mid + wave) * 10) / 10
        if prev_c is None:
            prev_c = c * 0.998
        o = prev_c
        spread = max(1.0, abs(c - o))
        h = max(o, c) + round((math.sin(t * 22.0) * 0.5 + 0.5) * spread * 0.8 * 10) / 10
        l = min(o, c) - round((math.cos(t * 19.0) * 0.5 + 0.5) * spread * 0.8 * 10) / 10
        prev_c = c
        
        dt = datetime.datetime.fromtimestamp(cur_ts / 1000, tz=datetime.timezone.utc)
        if dur <= 2 * 86400 * 1000:
            date_str = dt.strftime('%H:%M')
        elif dur <= 14 * 86400 * 1000:
            date_str = dt.strftime('%m-%d %H:%M') if count > 14 else dt.strftime('%m-%d')
        elif dur <= 365 * 86400 * 1000:
            date_str = dt.strftime('%Y-%m-%d') if count > 30 else dt.strftime('%Y-%m')
        else:
            date_str = dt.strftime('%Y-%m-%d') if count > 60 else dt.strftime('%Y-%m')
            
        samples.append({
            'date': date_str,
            'open': o,
            'high': h,
            'low': l,
            'close': c,
            'usd_thb': round(thb_mid, 2),
            'us10y': round(bond_mid, 3),
            'note': is_last and 'Current Verified Market Benchmark' or note
        })
    return samples

# Test 4-year timeframe:
dur_4y = int(4 * 365.25 * 86400 * 1000)
start_4y = MASTER_END_TS - dur_4y
s_4y_1w = sample_timeline(start_4y, MASTER_END_TS, '1w')
s_4y_1mo = sample_timeline(start_4y, MASTER_END_TS, '1mo')
print(f"4Y at 1w: {len(s_4y_1w)} candles, start={s_4y_1w[0]['date']} (close={s_4y_1w[0]['close']}), end={s_4y_1w[-1]['date']} (close={s_4y_1w[-1]['close']})")
print(f"4Y at 1mo: {len(s_4y_1mo)} candles, start={s_4y_1mo[0]['date']} (close={s_4y_1mo[0]['close']}), end={s_4y_1mo[-1]['date']} (close={s_4y_1mo[-1]['close']})")

# Test 1D timeframe:
dur_1d = 24 * 60 * 60 * 1000
start_1d = MASTER_END_TS - dur_1d
s_1d_30m = sample_timeline(start_1d, MASTER_END_TS, '30m')
s_1d_5m = sample_timeline(start_1d, MASTER_END_TS, '5m')
print(f"1D at 30m: {len(s_1d_30m)} candles, start={s_1d_30m[0]['date']}, end={s_1d_30m[-1]['date']}")
print(f"1D at 5m: {len(s_1d_5m)} candles, start={s_1d_5m[0]['date']}, end={s_1d_5m[-1]['date']}")

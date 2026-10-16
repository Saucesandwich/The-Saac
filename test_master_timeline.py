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
        'gold': item['close'],
        'thb': item['usd_thb'],
        'bond': item['us10y'],
        'note': item.get('note', '')
    })

print(f"Total anchors: {len(anchors)}")
print("First anchor:", anchors[0])
print("Last anchor:", anchors[-1])

dur_4y = int(4 * 365.25 * 86400 * 1000)
t_start = MASTER_END_TS - dur_4y
dt_start = datetime.datetime.fromtimestamp(t_start / 1000, tz=datetime.timezone.utc)
dt_end = datetime.datetime.fromtimestamp(MASTER_END_TS / 1000, tz=datetime.timezone.utc)
print(f"4Y Start: {dt_start.strftime('%Y-%m-%d %H:%M')} -> End: {dt_end.strftime('%Y-%m-%d %H:%M')}")

step_1w = 7 * 86400 * 1000
num_samples_1w = math.ceil(dur_4y / step_1w)
print(f"4Y with 1w: {num_samples_1w} candles")

step_1mo = int(30.4375 * 86400 * 1000)
num_samples_1mo = math.ceil(dur_4y / step_1mo)
print(f"4Y with 1mo: {num_samples_1mo} candles")

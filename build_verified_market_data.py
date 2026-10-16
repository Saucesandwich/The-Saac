import urllib.request
import json
import datetime
import math

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch_chart(symbol, rng, interval):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={rng}&interval={interval}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        d = json.loads(r.read().decode('utf-8'))['chart']['result'][0]
        ts = d.get('timestamp', [])
        q = d['indicators']['quote'][0]
        return ts, q

print("Fetching full market history from Yahoo Finance...")

# 1. Monthly data
g_m_ts, g_m_q = fetch_chart('GC=F', 'max', '1mo')
t_m_ts, t_m_q = fetch_chart('THB=X', 'max', '1mo')
b_m_ts, b_m_q = fetch_chart('^TNX', 'max', '1mo')

# 2. 10Y Daily data
g_d_ts, g_d_q = fetch_chart('GC=F', '10y', '1d')
t_d_ts, t_d_q = fetch_chart('THB=X', '10y', '1d')
b_d_ts, b_d_q = fetch_chart('^TNX', '10y', '1d')

# 3. 1mo Hourly data
g_h_ts, g_h_q = fetch_chart('GC=F', '1mo', '1h')
t_h_ts, t_h_q = fetch_chart('THB=X', '1mo', '1h')
b_h_ts, b_h_q = fetch_chart('^TNX', '1mo', '1h')

# 4. 5d 5m Intraday data
g_5m_ts, g_5m_q = fetch_chart('GC=F', '5d', '5m')
t_5m_ts, t_5m_q = fetch_chart('THB=X', '5d', '5m')
b_5m_ts, b_5m_q = fetch_chart('^TNX', '5d', '5m')

print("All data fetched successfully!")

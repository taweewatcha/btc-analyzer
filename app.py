import ccxt
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="BTCUSD Realtime & Backtest Analyzer", layout="wide"
)

st.title("🚀 BTCUSD Real-Time & Analysis Web App")
st.write(
    "เว็บแอปวิเคราะห์กราฟและจำลองระบบเทรดเบื้องต้น ดึงข้อมูลสดจากตลาดคริปโต"
)

# 1. ดึงข้อมูลราคาจาก Binance ผ่าน CCXT
@st.cache_data(ttl=60)  # แคชข้อมูลไว้ 60 วินาทีเพื่อไม่ให้โหลดถี่เกินไป
def load_data():
  exchange = ccxt.binance()
  bars = exchange.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=100)
  df = pd.DataFrame(
      bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
  )
  df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
  return df


df = load_data()

# 2. แสดงกราฟแท่งเทียนด้วย Plotly
fig = go.Figure(
    data=[
        go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='BTCUSD',
        )
    ]
)
fig.update_layout(
    title='BTC/USDT Hourly Chart',
    xaxis_title='Time',
    yaxis_title='Price (USD)',
    template='plotly_dark',
)

st.plotly_chart(fig, use_container_width=True)

# 3. ส่วนจำลองระบบเทรด (Backtest เบื้องต้น)
st.subheader("⚙️ ทดสอบระบบเทรด (Simple Moving Average Strategy)")
short_window = st.slider("Short SMA Period", 5, 20, 10)
long_window = st.slider("Long SMA Period", 21, 50, 30)

df['SMA_Short'] = df['close'].rolling(window=short_window).mean()
df['SMA_Long'] = df['close'].rolling(window=long_window).mean()

# แสดงข้อมูลสรุป
st.write(f"ราคาปัจจุบันล่าสุด: **${df['close'].iloc[-1]:,.2f}**")
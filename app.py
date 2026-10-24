import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="BTCUSD Realtime & Backtest Analyzer", layout="wide"
)

st.title("🚀 BTCUSD Real-Time & Analysis Web App")
st.write(
    "เว็บแอปวิเคราะห์กราฟและจำลองระบบเทรดเบื้องต้น (ดึงข้อมูลจาก Yahoo Finance)"
)


# 1. ดึงข้อมูลราคา BTC-USD ผ่าน yfinance
@st.cache_data(ttl=60)
def load_data():
  # ดึงข้อมูลย้อนหลัง 5 วัน ความถี่รายชั่วโมง
  df = yf.download('BTC-USD', period='5d', interval='1h', progress=False)
  df.reset_index(inplace=True)

  # จัดการโครงสร้างคอลัมน์ของ yfinance เวอร์ชันล่าสุด
  if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

  return df


df = load_data()

# ตรวจสอบว่าดึงข้อมูลสำเร็จหรือไม่
if not df.empty:
  # กำหนดชื่อคอลัมน์เวลา (บางทีเป็น Datetime หรือ Date)
  time_col = 'Datetime' if 'Datetime' in df.columns else 'Date'

  # 2. แสดงกราฟแท่งเทียนด้วย Plotly
  fig = go.Figure(
      data=[
          go.Candlestick(
              x=df[time_col],
              open=df['Open'],
              high=df['High'],
              low=df['Low'],
              close=df['Close'],
              name='BTCUSD',
          )
      ]
  )
  fig.update_layout(
      title='BTC/USD Hourly Chart',
      xaxis_title='Time',
      yaxis_title='Price (USD)',
      template='plotly_dark',
  )

  st.plotly_chart(fig, use_container_width=True)

  # 3. ส่วนจำลองระบบเทรด (Backtest เบื้องต้น)
  st.subheader("⚙️ ทดสอบระบบเทรด (Simple Moving Average Strategy)")
  short_window = st.slider("Short SMA Period", 5, 20, 10)
  long_window = st.slider("Long SMA Period", 21, 50, 30)

  df['SMA_Short'] = df['Close'].rolling(window=short_window).mean()
  df['SMA_Long'] = df['Close'].rolling(window=long_window).mean()

  # แสดงข้อมูลสรุปราคาล่าสุด
  latest_price = float(df['Close'].iloc[-1])
  st.write(f"ราคาปัจจุบันล่าสุด: **${latest_price:,.2f}**")
else:
  st.error(
      "ไม่สามารถดึงข้อมูลราคาได้ในขณะนี้ กรุณารีเฟรชหน้าเว็บใหม่อีกครั้ง"
  )

import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import random
from datetime import datetime, timedelta

# ---------- Page Config ----------
st.set_page_config(page_title="AI Stock Dashboard", layout="wide")

# ---------- Styles ----------
st.markdown("""
    <style>
    body {
        background-color: #0E0E10;
        color: #F9FAFB;
    }
    .block-container {
        padding: 1rem;
    }
    h1, h2, h3 {
        color: #F472B6;
    }
    .stTextInput > div > div > input {
        background-color: #333333;
        color: white;
    }
    .stDataFrame {
        background-color: #333333;
        color: white;
    }
    .css-1cpxqw2 {
        background-color: #18181B !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Sidebar Inputs ----------
st.sidebar.header("Trading Parameters")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., TSLA, AAPL)", "AAPL").upper()

# Set trading strategy parameters
entry_price = st.sidebar.number_input("Entry Price (Pre-Market)", min_value=0.0, value=150.0)
stop_loss = st.sidebar.number_input("Stop Loss", min_value=0.0, value=145.0)
close_price = st.sidebar.number_input("Sell Price (Before Close)", min_value=0.0, value=155.0)
update_button = st.sidebar.button("Update Data")

# ---------- Fetch Stock Data Function ----------
def get_stock_data(ticker, period="1d", interval="5m"):
    stock = yf.Ticker(ticker)
    return stock.history(period=period, interval=interval)

# ---------- Chart: Show Entry, Stop-Loss, Close ----------
def plot_trading_strategy(data, entry_price, stop_loss, close_price):
    fig = go.Figure()

    # Candlestick Chart
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name="Price"
    ))

    # Add entry, stop loss, and sell points
    fig.add_hline(y=entry_price, line_dash="solid", line_color="#F472B6", annotation_text="Entry Price", annotation_position="top left")
    fig.add_hline(y=stop_loss, line_dash="dash", line_color="#EF4444", annotation_text="Stop Loss", annotation_position="bottom left")
    fig.add_hline(y=close_price, line_dash="dashdot", line_color="#22C55E", annotation_text="Close Price", annotation_position="top left")

    # Chart aesthetics
    fig.update_layout(
        title="Trading Strategy Visualization",
        xaxis_rangeslider_visible=False,
        paper_bgcolor="#18181B",
        plot_bgcolor="#18181B",
        font=dict(color="white"),
        xaxis=dict(gridcolor="#333333"),
        yaxis=dict(gridcolor="#333333")
    )
    return fig

# ---------- Main App Content ----------
if update_button or ticker:
    try:
        # Fetch Stock Data
        stock_data = get_stock_data(ticker)
        st.title(f"📈 AI Stock Dashboard for {ticker}")

        # ---------- Chart Section ----------
        st.subheader("Trading Strategy Chart")
        strategy_chart = plot_trading_strategy(stock_data, entry_price, stop_loss, close_price)
        st.plotly_chart(strategy_chart, use_container_width=True)

        # ---------- AI Predictions ----------
        st.subheader("🤖 AI Predictions")
        ai_prediction = {
            "Next-Day Movement": f"{random.uniform(-3, 5):.2f}%",
            "Direction": random.choice(["Bullish", "Bearish"]),
            "Confidence": f"{random.uniform(75, 95):.2f}%"
        }

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Predicted Movement", ai_prediction["Next-Day Movement"], delta=ai_prediction["Direction"])
        with col2:
            st.metric("Confidence Level", ai_prediction["Confidence"])

        # ---------- Wallet Summary ----------
        st.subheader("💼 Wallet Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Buying Power", "$184.52")
        with col2:
            st.metric("Today's Return", "-$5.80", delta="-0.66%")
        with col3:
            st.metric("Total Return", "+$136.68", delta="+18.55%")

        # ---------- Recent News ----------
        st.subheader("📰 News & Social Mentions")
        news_articles = [
            f"{ticker} shows strong pre-market activity!",
            f"{ticker} approaching key resistance near {close_price}."
        ]
        for article in news_articles:
            st.write(f"✅ {article}")

    except Exception as e:
        st.error(f"An error occurred: {e}")

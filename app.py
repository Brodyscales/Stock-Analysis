import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta

# Streamlit app setup
st.set_page_config(page_title="Stock Prediction & Chart", layout="wide")

# Create tabs
tab1, tab2 = st.tabs(["📊 Dashboard", "📈 Chart"])

# --- TAB 1: OLD FUNCTIONALITY ---
with tab1:
    st.title("Stock Prediction Dashboard")
    st.write("Welcome to the stock prediction tool!")
    # Old code or main dashboard functionality goes here
    st.subheader("Main Features")
    st.write("Include all the existing features here.")

    # Example of placeholder old code:
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", value="AAPL")
    if st.button("Fetch Data"):
        data = yf.download(ticker, period="5d", interval="1h")
        st.write("Latest Stock Data:")
        st.dataframe(data)

# --- TAB 2: CHART FUNCTIONALITY ---
with tab2:
    st.title("Stock Entry Point Chart")
    st.write("Visualize your entry, stop loss, and close positions.")

    # Input stock ticker and trade parameters
    stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL)", value="AAPL")
    entry_price = st.number_input("Entry Price", value=150.0, step=0.1)
    stop_loss = st.number_input("Stop Loss Price", value=145.0, step=0.1)
    target_close = st.number_input("Close Target Price", value=155.0, step=0.1)

    if st.button("Generate Chart"):
        # Fetch historical data for the last day
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)
        data = yf.download(stock_symbol, start=start_date, end=end_date, interval="5m")

        if not data.empty:
            # Create a Plotly chart
            fig = go.Figure()

            # Add candlestick chart for stock data
            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name="Market Data"
            ))

            # Add entry point, stop loss, and close levels as horizontal lines
            fig.add_hline(y=entry_price, line_dash="dash", line_color="green", annotation_text="Entry Price")
            fig.add_hline(y=stop_loss, line_dash="dot", line_color="red", annotation_text="Stop Loss")
            fig.add_hline(y=target_close, line_dash="dash", line_color="blue", annotation_text="Close Target")

            # Customize chart layout
            fig.update_layout(
                title=f"{stock_symbol} Entry and Stop Loss Chart",
                xaxis_title="Time",
                yaxis_title="Price",
                template="plotly_dark",
                height=600
            )

            # Show the chart
            st.plotly_chart(fig)
        else:
            st.warning("No data available for the selected stock and time range.")

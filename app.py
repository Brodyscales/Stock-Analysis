import streamlit as st
import yfinance as yf

# Title and header
st.title("📈 Stock Analysis App")
st.header("Analyze Stock Prices in Real Time")

# User input: stock ticker symbol
ticker = st.text_input("Enter a Stock Ticker (e.g., AAPL, TSLA, MSFT):", "AAPL")

# Fetch and display stock data
if ticker:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d", interval="5m")
        
        st.subheader(f"Latest Data for {ticker.upper()}")
        st.line_chart(hist['Close'])  # Display a chart of closing prices
        
        st.subheader("Stock Details")
        st.write(f"**Name:** {stock.info['longName']}")
        st.write(f"**Sector:** {stock.info['sector']}")
        st.write(f"**Market Cap:** {stock.info['marketCap']:,}")
    except Exception as e:
        st.error("Error fetching data. Please check the ticker symbol and try again!")

# Footer
st.caption("Built with ❤️ using Streamlit and Yahoo Finance API")

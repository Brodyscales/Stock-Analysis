import streamlit as st
import pandas as pd
import yfinance as yf
import random
import datetime as dt
import plotly.graph_objects as go

# ---------- Helper Functions ----------
def fetch_articles_and_social_media(stock):
    """
    Simulate trusted sources and articles scanning for stocks.
    """
    trusted_articles = [
        f"Breaking news: {stock} shows strong bullish trend!",
        f"Market analysts recommend {stock} as a solid pick for tomorrow."
    ]
    social_media_posts = [
        f"@TrustedInvestor: {stock} is trending upward. 🚀",
        f"@MarketGuru: {stock} could see gains tomorrow."
    ]
    return trusted_articles, social_media_posts

def calculate_sentiment():
    """
    Simulate social media sentiment analysis for a stock.
    """
    return random.uniform(60, 90)  # Simulated sentiment %

def fetch_live_stock_data(tickers):
    """
    Fetch live stock data for multiple tickers.
    """
    live_data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        try:
            hist = stock.history(period="1d")
            if not hist.empty and 'Close' in hist.columns:
                current_price = hist['Close'].iloc[-1]
                live_data.append({"ticker": ticker, "price": current_price})
            else:
                live_data.append({"ticker": ticker, "price": "N/A"})
        except:
            live_data.append({"ticker": ticker, "price": "Error"})
    return live_data

def simulate_next_day_prediction(tickers):
    """
    Simulate AI predictions for the next trading day.
    """
    predictions = []
    for ticker in tickers:
        # Simulate next-day price prediction
        price_change = random.uniform(-3, 5)  # Price movement % (-3% to +5%)
        direction = "Bullish" if price_change > 0 else "Bearish"
        confidence = random.uniform(70, 95)  # Confidence %
        
        predictions.append({
            "ticker": ticker,
            "predicted_change": f"{price_change:.2f}%",
            "direction": direction,
            "confidence": f"{confidence:.2f}%"
        })
    return predictions

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Next-Day AI Stock Predictions", layout="wide")
st.title("🌟 AI Stock Predictions for Tomorrow")

# Choose stocks to analyze
st.subheader("📊 Select Stocks for Prediction")
default_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
user_tickers = st.text_input("Enter Stock Tickers (comma-separated):", "AAPL, MSFT, TSLA")
tickers = [ticker.strip().upper() for ticker in user_tickers.split(",")]

# Simulated Predictions for the Next Trading Day
if st.button("Generate AI Predictions"):
    st.subheader("📈 AI Predictions for the Day Ahead")
    predictions = simulate_next_day_prediction(tickers)
    
    for pred in predictions:
        st.write(f"**{pred['ticker']}**:")
        st.info(f"Predicted Price Change: {pred['predicted_change']}")
        st.success(f"Direction: {pred['direction']}")
        st.warning(f"Confidence Level: {pred['confidence']}")

    # Sentiment Analysis
    st.subheader("🔍 Trusted Sources & Sentiment Analysis")
    for ticker in tickers:
        articles, social_posts = fetch_articles_and_social_media(ticker)
        sentiment = calculate_sentiment()

        st.write(f"**{ticker}:**")
        st.write("**Trusted Articles:**")
        for article in articles:
            st.info(article)

        st.write("**Social Media Posts:**")
        for post in social_posts:
            st.success(post)

        st.write(f"**Sentiment Score:** {sentiment:.2f}%")

# Display Latest Prices
st.subheader("🔄 Latest Stock Prices")
live_data = fetch_live_stock_data(tickers)
df_live = pd.DataFrame(live_data)
st.dataframe(df_live)

# ---------- Footer ----------
st.caption("Built with Streamlit | Simulated AI Predictions | Data via Yahoo Finance")

import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from datetime import datetime, timedelta

# Function to scrape headlines from a website
def scrape_news(stock_symbol):
    url = f"https://finance.yahoo.com/quote/{stock_symbol}/news"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract news headlines
        headlines = []
        for item in soup.find_all("h3", class_="Mb(5px)"):
            headline = item.text
            if headline:
                headlines.append(headline)
        return headlines
    except Exception as e:
        st.error(f"Failed to fetch news: {e}")
        return []

# Function to calculate sentiment score
def analyze_sentiment(headlines):
    total_score = 0
    for headline in headlines:
        analysis = TextBlob(headline)
        total_score += analysis.sentiment.polarity
    avg_score = total_score / len(headlines) if headlines else 0
    return avg_score

# Function to predict entry, stop loss, and close
def calculate_trade_params(latest_price, sentiment_score):
    try:
        entry = latest_price * (1 + (sentiment_score * 0.01))  # Entry point
        stop_loss = latest_price * 0.98  # Stop loss at 2% lower
        close_target = latest_price * (1 + abs(sentiment_score * 0.02))
        return round(entry, 2), round(stop_loss, 2), round(close_target, 2)
    except ZeroDivisionError:
        return None, None, None

# Streamlit UI setup
st.set_page_config(page_title="AI Stock Analysis", layout="wide")

# Initialize Session State
if 'entry' not in st.session_state:
    st.session_state.entry = None
if 'stop_loss' not in st.session_state:
    st.session_state.stop_loss = None
if 'close_target' not in st.session_state:
    st.session_state.close_target = None

# Tabs for Dashboard and Chart
tab1, tab2 = st.tabs(["📊 AI Analysis", "📈 Chart"])

# --- TAB 1: AI Analysis ---
with tab1:
    st.title("AI Stock Analysis Based on News Sentiment")

    stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", value="AAPL")

    if st.button("Analyze"):
        st.info("Fetching news and analyzing sentiment...")

        # Scrape news headlines
        headlines = scrape_news(stock_symbol)
        sentiment_score = analyze_sentiment(headlines)

        # Fetch the latest stock price
        try:
            ticker = yf.Ticker(stock_symbol)
            latest_price = ticker.history(period="1d")["Close"].iloc[-1]

            # Calculate trade parameters
            entry, stop_loss, close_target = calculate_trade_params(latest_price, sentiment_score)

            if entry is not None and stop_loss is not None and close_target is not None:
                st.session_state.entry = entry
                st.session_state.stop_loss = stop_loss
                st.session_state.close_target = close_target

                # Display results
                st.subheader("Sentiment Analysis Results:")
                st.write(f"**Sentiment Score:** {sentiment_score:.2f}")
                st.write("**Trade Parameters:**")
                st.write(f"- **Entry Point:** ${entry}")
                st.write(f"- **Stop Loss:** ${stop_loss}")
                st.write(f"- **Target Close:** ${close_target}")

                # Show news headlines
                st.subheader("Latest News Headlines:")
                for headline in headlines:
                    st.write(f"- {headline}")

            else:
                st.error("Trade parameters could not be calculated.")

        except Exception as e:
            st.error(f"Failed to fetch stock data: {e}")

# --- TAB 2: Chart Visualization ---
with tab2:
    st.title("Trade Visualization Chart")

    if st.button("Show Chart"):
        if st.session_state.entry and st.session_state.stop_loss and st.session_state.close_target:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=5)

            try:
                # Download stock data
                data = yf.download(stock_symbol, start=start_date, end=end_date, interval="1h")

                if not data.empty:
                    fig = go.Figure()

                    # Plot candlestick chart
                    fig.add_trace(go.Candlestick(
                        x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'],
                        name=f"{stock_symbol} Data"
                    ))

                    # Plot trade levels on chart
                    fig.add_hline(y=st.session_state.entry, line_dash="dash", line_color="green", annotation_text="Entry")
                    fig.add_hline(y=st.session_state.stop_loss, line_dash="dot", line_color="red", annotation_text="Stop Loss")
                    fig.add_hline(y=st.session_state.close_target, line_dash="dash", line_color="blue", annotation_text="Close Target")

                    fig.update_layout(
                        title=f"{stock_symbol} Trade Analysis",
                        xaxis_title="Date",
                        yaxis_title="Price",
                        template="plotly_dark"
                    )

                    st.plotly_chart(fig)
                else:
                    st.warning("No data available for this stock.")

            except Exception as e:
                st.error(f"Failed to plot chart: {e}")

        else:
            st.write("Please run the Analysis tab first to get trade parameters.")


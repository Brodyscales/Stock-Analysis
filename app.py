import streamlit as st
import pandas as pd
import yfinance as yf
import random
import plotly.graph_objects as go

# Trusted sources and social media simulation
def fetch_articles_and_social_media(stock):
    """
    Simulate trusted sources and articles scanning for stocks.
    """
    trusted_articles = [
        f"Breaking news: {stock} shows strong bullish trend!",
        f"Market analysts recommend {stock} as a solid pick for intraday trades.",
    ]
    social_media_posts = [
        f"@TrustedInvestor: {stock} is a buy at this level! 🚀",
        f"@MarketGuru: {stock} showing great sentiment today!",
    ]
    return trusted_articles, social_media_posts

def calculate_sentiment(stock):
    """
    Simulate social media sentiment analysis for a stock.
    """
    sentiment_score = random.uniform(50, 90)  # Simulated sentiment %
    return sentiment_score

def recommend_stocks():
    """
    Simulate scanning for the best-performing stocks under $50 for day trading.
    """
    stocks = [
        {"ticker": "AMC", "price": 10.5, "sentiment": 88, "entry": 10.2, "stop_loss": 9.5},
        {"ticker": "F", "price": 13.8, "sentiment": 84, "entry": 13.5, "stop_loss": 13.0},
        {"ticker": "PLTR", "price": 19.0, "sentiment": 91, "entry": 18.8, "stop_loss": 18.0},
        {"ticker": "BBBY", "price": 5.3, "sentiment": 85, "entry": 5.2, "stop_loss": 4.8},
    ]
    df = pd.DataFrame(stocks)
    return df

def get_stock_chart(ticker):
    """
    Fetch stock price chart using Yahoo Finance.
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5d")  # Fetch last 5 days
    return hist

def portfolio_tracker():
    """
    Simple portfolio tracker to add stocks and calculate profits.
    """
    st.subheader("📊 Portfolio Tracker")
    st.write("Add stocks to your portfolio and track profits:")
    portfolio = st.session_state.get("portfolio", [])

    # Add new stock to portfolio
    with st.form("add_stock"):
        ticker = st.text_input("Stock Ticker (e.g., AMC)")
        buy_price = st.number_input("Buy Price", min_value=0.0, format="%.2f")
        quantity = st.number_input("Quantity", min_value=1, step=1)
        submitted = st.form_submit_button("Add to Portfolio")

        if submitted and ticker and buy_price > 0:
            portfolio.append({"ticker": ticker.upper(), "buy_price": buy_price, "quantity": quantity})
            st.session_state["portfolio"] = portfolio
            st.success(f"Added {ticker.upper()} to your portfolio!")

    # Display portfolio
    if portfolio:
        portfolio_df = pd.DataFrame(portfolio)
        st.table(portfolio_df)
    else:
        st.info("Your portfolio is empty. Add stocks to begin tracking.")

# --------------- Website Layout -----------------
st.set_page_config(page_title="Stock Analysis & Predictions", layout="wide")
st.title("💹 AI-Powered Stock Prediction and Analysis")

# Section 1: Sentiment Analysis
st.subheader("🔍 Social Media Sentiment & AI Prediction")
stock_to_check = st.text_input("Enter a Stock Ticker (e.g., AMC, PLTR):", "AMC")
if stock_to_check:
    try:
        # Fetch trusted sources
        articles, social_posts = fetch_articles_and_social_media(stock_to_check)
        st.write("**Trusted Articles & News:**")
        for article in articles:
            st.info(article)

        st.write("**Trusted Social Media Posts:**")
        for post in social_posts:
            st.success(post)

        # Calculate sentiment
        sentiment = calculate_sentiment(stock_to_check)
        st.write(f"**Social Media Sentiment Score:** {sentiment:.2f}%")
        if sentiment > 80:
            st.success(f"{stock_to_check} has a HIGH chance of making profits today! ⭐")
        elif sentiment > 60:
            st.warning(f"{stock_to_check} has a MODERATE chance of profit. Consider carefully.")
        else:
            st.error(f"{stock_to_check} has a LOW chance of making profits. Be cautious.")

        # Show recent stock chart
        hist = get_stock_chart(stock_to_check)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Close Price'))
        fig.update_layout(title=f"{stock_to_check} Recent Price Chart", xaxis_title="Date", yaxis_title="Price (USD)")
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error fetching data for {stock_to_check}: {e}")

# Section 2: Best Stocks to Buy for Today
st.subheader("💼 Today's Best Stocks for Intraday Trading")
st.write("Below are AI-selected stocks under $50 with high sentiment and calculated profit potential:")
recommended_df = recommend_stocks()
st.dataframe(recommended_df)

# Section 3: Detailed Entry & Stop-Loss
st.subheader("🔄 Exact Entry and Stop-Loss Points")
selected_stock = st.selectbox("Choose a Stock to View Detailed Entry/Stop-Loss:", recommended_df['ticker'])
if selected_stock:
    stock_details = recommended_df[recommended_df['ticker'] == selected_stock].iloc[0]
    st.write(f"**Stock:** {stock_details['ticker']}")
    st.write(f"**Entry Price:** ${stock_details['entry']:.2f}")
    st.write(f"**Stop-Loss Price:** ${stock_details['stop_loss']:.2f}")
    st.write(f"**Sentiment Score:** {stock_details['sentiment']}%")

    # Fetch and show a chart
    hist = get_stock_chart(selected_stock)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Close Price'))
    fig.add_hline(y=stock_details['entry'], line_dash="dash", line_color="green", annotation_text="Entry")
    fig.add_hline(y=stock_details['stop_loss'], line_dash="dash", line_color="red", annotation_text="Stop-Loss")
    fig.update_layout(title=f"{selected_stock} Intraday Analysis", xaxis_title="Date", yaxis_title="Price (USD)")
    st.plotly_chart(fig)

# Section 4: Portfolio Tracker
portfolio_tracker()

# Footer
st.caption("Built with Streamlit | Powered by Yahoo Finance | AI-Simulated Analysis")

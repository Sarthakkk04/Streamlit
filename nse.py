import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

# Function to get stock data


def get_stock_data(ticker, start_date, end_date):
    if ticker.endswith(".NS") or ticker.endswith(".BO"):
        ticker = ticker.replace(".NS", ".NS").replace(".BO", ".BO")
        stock_data = yf.download(ticker, start=start_date, end=end_date)
    else:
        st.error(
            "Currently, only Indian stocks ending with '.NS' or '.BO' are supported.")
        stock_data = None
    return stock_data

# Function to calculate moving averages


def calculate_moving_averages(stock_data, window):
    return stock_data['Close'].rolling(window=window).mean()

# Function to calculate Bollinger Bands


def calculate_bollinger_bands(stock_data, window):
    moving_avg = stock_data['Close'].rolling(window=window).mean()
    rolling_std = stock_data['Close'].rolling(window=window).std()
    upper_band = moving_avg + (rolling_std * 2)
    lower_band = moving_avg - (rolling_std * 2)
    return moving_avg, upper_band, lower_band

# Main Streamlit app


def main():
    st.title("Stock Market Analysis")

    # Sidebar for user input
    st.sidebar.header("Stock Selection")
    ticker = st.sidebar.text_input(
        "Enter stock ticker (e.g., TCS.NS)", "TCS.NS")
    start_date = st.sidebar.date_input(
        "Start date", pd.to_datetime("2024-06-07"))
    end_date = st.sidebar.date_input("End date", pd.to_datetime("today"))
    moving_average_window = st.sidebar.slider(
        "Moving Average Window", 1, 50, 20)
    bollinger_bands_window = st.sidebar.slider(
        "Bollinger Bands Window", 1, 50, 20)

    # Fetching the stock data
    stock_data = get_stock_data(ticker, start_date, end_date)

    if stock_data is not None:
        # Displaying the stock data
        st.subheader(f"{ticker} Stock Data")
        st.write(stock_data)

        # Line chart of closing prices
        st.subheader("Line Chart - Closing Prices")
        st.line_chart(stock_data['Close'])

        # Candlestick chart
        st.subheader("Candlestick Chart")
        fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                             open=stock_data['Open'],
                                             high=stock_data['High'],
                                             low=stock_data['Low'],
                                             close=stock_data['Close'])])
        st.plotly_chart(fig)

        # Moving Averages
        st.subheader("Moving Averages")
        stock_data['Moving_Avg'] = calculate_moving_averages(
            stock_data, moving_average_window)
        st.line_chart(stock_data[['Close', 'Moving_Avg']])

        # Volume Chart
        st.subheader("Volume Chart")
        st.bar_chart(stock_data['Volume'])

        # Bollinger Bands
        st.subheader("Bollinger Bands")
        moving_avg, upper_band, lower_band = calculate_bollinger_bands(
            stock_data, bollinger_bands_window)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_data.index,
                      y=stock_data['Close'], mode='lines', name='Close'))
        fig.add_trace(go.Scatter(x=stock_data.index, y=moving_avg,
                      mode='lines', name='Moving Average'))
        fig.add_trace(go.Scatter(x=stock_data.index, y=upper_band, mode='lines',
                      name='Upper Band', line=dict(color='rgba(255,0,0,0.5)')))
        fig.add_trace(go.Scatter(x=stock_data.index, y=lower_band, mode='lines',
                      name='Lower Band', line=dict(color='rgba(0,0,255,0.5)')))
        st.plotly_chart(fig)

        # Compare different stocks
        st.sidebar.header("Comparison")
        tickers = st.sidebar.text_input(
            "Enter stock tickers for comparison (comma separated)", "TCS.NS, INFY.NS")
        tickers_list = [ticker.strip() for ticker in tickers.split(",")]

        if len(tickers_list) > 1:
            comparison_data = {}
            for t in tickers_list:
                comparison_data[t] = get_stock_data(
                    t, start_date, end_date)['Close']

            comparison_df = pd.DataFrame(comparison_data)
            st.subheader("Comparison of Stocks")
            st.line_chart(comparison_df)


if __name__ == "__main__":
    main()

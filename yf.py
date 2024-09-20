import yfinance as yf

# Get the ticker symbol for the company
ticker = yf.Ticker("TCS.NS")  # Example for Apple Inc.

# Access the financial data
financials = ticker.financials
print(financials)

# Get revenue
revenue = financials.loc['Total Revenue']
print("Revenue:\n", revenue)

# Get net income (profit)
net_income = financials.loc['Net Income']
print("Net Income:\n", net_income)

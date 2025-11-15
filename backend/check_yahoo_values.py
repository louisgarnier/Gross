"""Script to check what values Yahoo Finance actually has for NVDA."""
import yfinance as yf

print("=== NVDA Yahoo Finance Data ===\n")

stock = yf.Ticker('NVDA')
info = stock.info
financials = stock.financials

print("P/E Ratios:")
print(f"  trailingPE: {info.get('trailingPE')}")
print(f"  forwardPE: {info.get('forwardPE')}")
print(f"  priceToEarnings: {info.get('priceToEarnings')}")

print("\nPrice and EPS:")
print(f"  Current Price: {info.get('regularMarketPrice')}")
print(f"  trailingEPS: {info.get('trailingEPS')}")
if info.get('regularMarketPrice') and info.get('trailingEPS'):
    calculated_pe = info.get('regularMarketPrice') / info.get('trailingEPS')
    print(f"  Calculated P/E (Price/EPS): {calculated_pe}")

print("\nFinancials (most recent period):")
if 'EBIT' in financials.index:
    ebit = financials.loc['EBIT'].iloc[0]
    print(f"  EBIT: {ebit:,.0f}")
if 'Interest Expense' in financials.index:
    ie = financials.loc['Interest Expense'].iloc[0]
    print(f"  Interest Expense: {ie:,.0f}")
    if ebit and ie and ie != 0:
        ic = ebit / abs(ie)
        print(f"  Calculated Interest Coverage: {ic:.2f}x")

print("\nPlease check on Yahoo Finance website:")
print("  https://finance.yahoo.com/quote/NVDA")
print("  https://finance.yahoo.com/quote/NVDA/financials")


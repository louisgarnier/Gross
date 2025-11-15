"""Debug script to check Yahoo Finance data structure."""
import yfinance as yf

stock = yf.Ticker('PLTR')
financials = stock.financials

print("=== Financials Index (all rows) ===")
for idx in financials.index:
    print(f"  {idx}")

print("\n=== Sample values ===")
if 'EBIT' in financials.index:
    print(f"EBIT: {financials.loc['EBIT']}")

# Check for interest-related rows
print("\n=== Interest-related rows ===")
for idx in financials.index:
    if 'interest' in idx.lower() or 'Interest' in idx:
        print(f"  {idx}: {financials.loc[idx].iloc[0]}")


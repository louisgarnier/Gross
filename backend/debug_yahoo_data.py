"""
Generic debug script to inspect Yahoo Finance data structure.

Use this to debug issues with yfinance data or to understand the data structure.
Usage: python3 debug_yahoo_data.py TICKER
Example: python3 debug_yahoo_data.py NVDA
"""

import sys
import yfinance as yf

def debug_ticker(ticker: str):
    """Debug Yahoo Finance data for a given ticker."""
    print(f"=== Yahoo Finance Data for {ticker} ===\n")
    
    stock = yf.Ticker(ticker)
    info = stock.info
    financials = stock.financials
    quarterly = stock.quarterly_financials
    
    print("=== Info (P/E, Price, etc.) ===")
    print(f"  trailingPE: {info.get('trailingPE')}")
    print(f"  forwardPE: {info.get('forwardPE')}")
    print(f"  currentPrice: {info.get('currentPrice')}")
    print(f"  regularMarketPrice: {info.get('regularMarketPrice')}")
    
    print("\n=== Annual Financials (all rows) ===")
    if not financials.empty:
        for idx in financials.index:
            value = financials.loc[idx].iloc[0] if len(financials.loc[idx]) > 0 else None
            print(f"  {idx}: {value}")
    
    print("\n=== Quarterly Financials (first 4 quarters) ===")
    if not quarterly.empty:
        print(f"Columns: {list(quarterly.columns[:4])}")
        print("\nKey metrics:")
        for metric in ['EBIT', 'Operating Income', 'Interest Expense', 'Interest Income']:
            if metric in quarterly.index:
                values = quarterly.loc[metric].iloc[:4].tolist()
                print(f"  {metric}: {values}")
    
    print("\n=== Interest-related rows (Annual) ===")
    if not financials.empty:
        for idx in financials.index:
            if 'interest' in str(idx).lower():
                value = financials.loc[idx].iloc[0] if len(financials.loc[idx]) > 0 else None
                print(f"  {idx}: {value}")

if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "NVDA"
    debug_ticker(ticker.upper())


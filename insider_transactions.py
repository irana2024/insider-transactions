# insider_transactions.py
import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import time

class InsiderTransactionsFetcher:
    def __init__(self):
        self.base_url = "https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json"
        self.headers = {
            'User-Agent': 'self systain njhills1@gmail.com'
        }
    
    def get_company_cik(self, ticker):
        """Get CIK number for a ticker symbol"""
        ticker_url = "https://www.sec.gov/files/company_tickers.json"
        response = requests.get(ticker_url, headers=self.headers)
        tickers = response.json()
        
        for company in tickers.values():
            if company['ticker'].upper() == ticker.upper():
                return str(company['cik_str']).zfill(10)
        return None
    
    def fetch_insider_transactions(self, ticker, days_back=90):
        """Fetch insider transactions for a given ticker"""
        cik = self.get_company_cik(ticker)
        if not cik:
            print(f"Could not find CIK for ticker {ticker}")
            return None
        
        # SEC Form 4 filings URL
        filings_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        
        try:
            response = requests.get(filings_url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            # Filter for Form 4 filings (insider transactions)
            filings = data.get('filings', {}).get('recent', {})
            form4_indices = []
            
            for i, form_type in enumerate(filings.get('form', [])):
                if form_type == '4':
                    form4_indices.append(i)
            
            transactions = []
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            for idx in form4_indices[:50]:  # Limit to recent 50 filings
                filing_date = datetime.strptime(filings['filingDate'][idx], '%Y-%m-%d')
                if filing_date < cutoff_date:
                    continue
                
                transaction = {
                    'Filing Date': filings['filingDate'][idx],
                    'Accession Number': filings['accessionNumber'][idx],
                    'Document URL': f"https://www.sec.gov/Archives/edgar/data/{cik}/{filings['accessionNumber'][idx].replace('-', '')}/{filings['primaryDocument'][idx]}",
                    'Company': ticker.upper(),
                    'CIK': cik
                }
                transactions.append(transaction)
                
                # Rate limiting
                time.sleep(0.1)
            
            return pd.DataFrame(transactions)
            
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
    
    def export_to_csv(self, df, filename=None):
        """Export DataFrame to CSV"""
        if filename is None:
            filename = f"insider_transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        df.to_csv(filename, index=False)
        print(f"Data exported to {filename}")
        return filename

# Usage example
if __name__ == "__main__":
    fetcher = InsiderTransactionsFetcher()
    
    # Get user input
    ticker = input("Enter ticker symbol: ").upper()
    days = int(input("Enter number of days to look back (default 90): ") or 90)
    
    print(f"Fetching insider transactions for {ticker}...")
    
    # Fetch data
    df = fetcher.fetch_insider_transactions(ticker, days)
    
    if df is not None and not df.empty:
        print(f"\nFound {len(df)} insider transaction filings")
        print(df.head())
        
        # Export to CSV
        filename = fetcher.export_to_csv(df)
        print(f"\nData saved to {filename}")
    else:
        print("No data found or error occurred")
# Insider Transactions Script

This Python script fetches recent insider transaction filings for a given stock ticker from the SEC EDGAR database and exports the results to a CSV file.

## Features
- Prompts for a ticker symbol and lookback period (in days)
- Fetches insider transaction filings from EDGAR
- Displays a summary in the terminal
- Exports results to a timestamped CSV file

## Requirements
- Python 3.9+
- requests
- pandas

## Installation
Install the required packages:

```bash
pip install requests pandas
```

## Usage
Run the script from the command line:

```bash
python insider_transactions.py
```

You will be prompted to enter:
- The ticker symbol (e.g., AAPL, MSFT, FI)
- The number of days to look back (default is 90)

## Output
- The script prints a summary of the filings found.
- Results are saved to a CSV file named like `insider_transactions_YYYYMMDD_HHMMSS.csv` in the current directory.

## License
This project is licensed under the Apache 2.0 License.

import csv
import os
from datetime import date


def _load_ticker(filename):
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [{
                'date': date.fromisoformat(day['Date']),
                'open': float(day['Open']),
                'close': float(day['Close']),
                'volume': int(day['Volume']),
                'high': float(day['High']),
                'low': float(day['Low'])
            } for day in reader]
            quotes = {day['date']: day for day in data}
            dates = {day['date'] for day in data}
            ticker = os.path.basename(filename).upper()
            ticker = os.path.splitext(ticker)[0]
            return ticker, dates, quotes
            
    except Exception as exc:
        print(exc)
        return None


def load_data(directory):
    files = [f for f in os.listdir(directory)]
    total_data = {}
    trading_days = set()
    for filename in files:
        full_path = os.path.join(directory, filename)
        if os.path.isfile(full_path) and os.path.splitext(full_path)[1].lower() == '.csv':
            ticker, dates, quotes = _load_ticker(os.path.join(directory, filename))
            if ticker:
                print(f'Loaded quotes for {ticker}')
                total_data[ticker] = quotes
                trading_days = trading_days.union(dates)
    trading_days = list(trading_days)
    trading_days.sort()
    return trading_days, total_data
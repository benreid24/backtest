import csv
import os


def _get_file(ticker):
    paths = ['{}.csv', 'data/{}.csv', '../data/{}.csv']
    for path in paths:
        if os.path.isfile(path.format(ticker)):
            return path.format(ticker)
    return ''


def load_ticker(ticker):
    try:
        with open(_get_file(ticker.upper()), 'r') as file:
            reader = csv.DictReader(file)
            return [day for day in reader]
    except Exception:
        return []

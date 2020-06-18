class Market:
    def __init__(self, tickerstore):
        self._date = None
        self._stonks = tickerstore # ticker -> date -> quote

    def set_date(self, date):
        self._date = date

    def get_quote(self, ticker):
        if not self._date:
            return None
        if ticker not in self._stonks.keys():
            return None
        data = self._stonks[ticker]
        if self._date not in data.keys():
            return None
        return data[self._date]

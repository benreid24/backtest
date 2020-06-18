import math

from strategy import Strategy


class BuyAndHold(Strategy):
    def __init__(self, ticker, starting_cash, monthly_cash):
        super().__init__(starting_cash, monthly_cash)
        self._ticker = ticker.upper()

    def name(self):
        return f'BuyAndHold({self._ticker})'

    def do_trades(self, date, market):
        quote = market.get_quote(self._ticker)
        if quote:
            qty = math.floor(self.cash_balance() / quote['open'])
            self.buy(self._ticker, qty, market)
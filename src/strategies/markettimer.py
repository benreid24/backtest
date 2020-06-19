import math

from strategy import Strategy
import market as mkt


class MarketTimer(Strategy):
    def __init__(self, ticker, starting_cash, monthly_cash):
        super().__init__(starting_cash, monthly_cash)
        self._ticker = ticker.upper()

    def name(self):
        return f'MarketTimer({self._ticker})'

    def do_trades(self, date, market):
        qty = self.max_buy(self._ticker, market)
        if qty:
            self.buy(self._ticker, qty, market, mkt.LOW)
            self.sell(self._ticker, qty, market, mkt.HIGH)

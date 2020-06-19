import math

import market as mkt
from strategy import Strategy

VOLUME = 'volume'
PRICE_UP = 'price_up'
PRICE_DOWN = 'price_down'


class WaveRider(Strategy):
    def __init__(self, mode, always_enter, starting_cash, monthly_cash):
        super().__init__(starting_cash, monthly_cash)
        self._mode = mode
        self._always_enter = always_enter
        self._tomorrows_bet = None

    def name(self):
        enter_str = 'AlwaysEnter' if self._always_enter else 'PickyEntry'
        return f'WaveRider({self._mode}:{enter_str})'

    def do_trades(self, date, market):
        if self._tomorrows_bet:
            qty = self.max_buy(self._tomorrows_bet, market)
            if qty:
                self.buy(self._tomorrows_bet, qty, market, mkt.OPEN)
                self.sell(self._tomorrows_bet, qty, market, mkt.CLOSE)
        
        cmp_var = None
        busy_ticker = None
        for ticker in market.tickers():
            quote = market.get_quote(ticker)
            if quote:
                spread = quote[mkt.CLOSE] - quote[mkt.OPEN]

                if self._mode == VOLUME:
                    if not cmp_var or quote['volume'] > cmp_var:
                        cmp_var = quote['volume']
                        busy_ticker = ticker

                elif self._mode == PRICE_UP:
                    if not cmp_var or spread > cmp_var:
                        cmp_var = spread
                        if spread > 0 or self._always_enter:
                            busy_ticker = ticker

                elif self._mode == PRICE_DOWN:
                    if not cmp_var or spread < cmp_var:
                        cmp_var = spread
                        if spread < 0 or self._always_enter:
                            busy_ticker = ticker

        self._tomorrows_bet = busy_ticker

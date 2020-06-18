class Strategy:
    def __init__(self, starting_cash, monthly_cash):
        self._contributions = starting_cash
        self._cash = starting_cash
        self._monthly_cash = monthly_cash
        self._holdings = {}
        self._last_month = None

    def name(self):
        pass

    def new_month(self, trade_date, market):
        pass

    def do_trades(self, trade_date, market):
        pass

    def notify_day(self, trade_date, market):
        if self._last_month is None or trade_date.month != self._last_month:
            self._last_month = trade_date.month
            self._cash += self._monthly_cash
            self._contributions += self._monthly_cash
            self.new_month(trade_date, market)
        self.do_trades(trade_date, market)

    def cash_balance(self):
        return self._cash 

    def total_contributions(self):
        return self._contributions

    def holdings(self):
        return self._holdings

    def total_balance(self, market):
        total = self._cash
        for ticker, holding in self._holdings.items():
            quote = market.get_quote(ticker)
            if quote:
                price = quote['close'] # TODO - configure which price to use
                total += price * holding['qty']
        return total

    def buy(self, ticker, qty, market):
        quote = market.get_quote(ticker)
        if quote:
            price = quote['open'] # TODO - configure which price to use
            cost = qty * price
            self._cash -= cost
            if ticker in self._holdings:
                orig_basis = self._holdings[ticker]['qty'] * self._holdings[ticker]['avgcost']
                self._holdings[ticker]['qty'] += qty
                self._holdings[ticker]['avgcost'] = (orig_basis + cost) / self._holdings[ticker]['qty']
            else:
                self._holdings[ticker] = {
                    'qty': qty,
                    'avgcost': cost
                }
        else:
            print(f'Error getting quote for {ticker}')

    def sell(self, ticker, qty, market):
        quote = market.get_quote()
        if quote:
            price = quote['open'] # TODO - configure which price to use
            cost = qty * price
            self._cash += cost
            if ticker in self._holdings:
                orig_basis = self._holdings[ticker]['qty'] * self._holdings[ticker]['avgcost']
                self._holdings['ticker']['qty'] -= qty
                if self._holdings[ticker]['qty'] != 0:
                    self._holdings['ticker']['avgcost'] = (orig_basis - cost) / self._holdings[ticker]['qty']
                else:
                    self._holdings.pop(ticker, None)
            else:
                self._holdings[ticker] = {
                    'qty': -qty,
                    'avgcost': -cost
                }
        else:
            print(f'Error getting quote for {ticker}')
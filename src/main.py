from datetime import date
import sys

import data
from market import Market
from strategies.buyhold import BuyAndHold
import strategies.waverider as waverider

START_DATE = date(2011, 1, 3)
END_DATE = date(2020, 6, 17)
STARTING_CASH = 10000
MONTHLY_CASH = 1000
STRATEGIES = [
    BuyAndHold('SPY', STARTING_CASH, MONTHLY_CASH),
    BuyAndHold('SPXL', STARTING_CASH, MONTHLY_CASH),
    waverider.WaveRider(waverider.PRICE_DOWN, True, STARTING_CASH, MONTHLY_CASH),
    waverider.WaveRider(waverider.PRICE_UP, True, STARTING_CASH, MONTHLY_CASH),
    waverider.WaveRider(waverider.VOLUME, True, STARTING_CASH, MONTHLY_CASH),
    waverider.WaveRider(waverider.PRICE_DOWN, False, STARTING_CASH, MONTHLY_CASH),
    waverider.WaveRider(waverider.PRICE_UP, False, STARTING_CASH, MONTHLY_CASH),
]


def _find_range(trade_dates):
    start = None
    end = None
    i = 0
    for date in trade_dates:
        if not start and date >= START_DATE:
            start = i
        if not end and date >= END_DATE:
            end = i + 1
            break
        i = i + 1

    if not start:
        start = 0
    if not end:
        end = len(trade_dates)

    return trade_dates[start:end]


def main():
    # Parse Input
    if len(sys.argv) != 2:
        print('Usage: python main.py <path-to-data>')
        return
    data_dir = sys.argv[1]

    # Load Data
    trade_dates, market_data = data.load_data(data_dir)
    market = Market(market_data)
    trade_dates = _find_range(trade_dates)

    # Output Starting Conditions
    print(f'Starting cash: ${STARTING_CASH:,.2f}')
    print(f'Monthly cash: ${MONTHLY_CASH:,.2f}')
    print(f'Trading Start: {trade_dates[0]}')
    print(f'Trading End: {trade_dates[-1]}')
    print('')
    print('Strategies:')
    for strat in STRATEGIES:
        print(f'    {strat.name()}')
    print('')

    # Run Backtest
    for trade_date in trade_dates:
        market.set_date(trade_date)
        for strat in STRATEGIES:
            strat.notify_day(trade_date, market)

    # Output Results
    for strat in STRATEGIES:
        name = strat.name()
        result = strat.total_balance(market)
        contribs = strat.total_contributions()
        print(f'{name} ended with ${result:,.2f} from ${contribs:,.2f} in contributions')


if __name__ == '__main__':
    main()

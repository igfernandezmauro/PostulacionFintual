from datetime import datetime, timedelta
import yfinance as yf


class Portfolio:
    def __init__(self):
        self.stocks = (Stock("AAPL"), Stock("MSFT"), Stock("AMZN"))

    def add_stock(self, ticker):
        self.stocks.__add__(Stock(ticker))

    def profit(self, start_date, end_date):
        portfolio_start = 0
        portfolio_end = 0
        for stock in self.stocks:
            try:
                portfolio_start += stock.price(start_date)
                portfolio_end += stock.price(end_date)
            except:
                return False
        portfolio_profit = portfolio_end - portfolio_start
        return (portfolio_profit / portfolio_start) * 100

    def annualized_return(self, start_date, end_date):
        start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
        days_difference = float((end_date_dt - start_date_dt).days)
        cumulative_return = self.profit(start_date, end_date)/100
        if(cumulative_return):
            return (((1 + cumulative_return) ** (365 / days_difference)) - 1) * 100
        else:
            return False


class Stock:
    def __init__(self, _ticker):
        self.ticker = _ticker

    def price(self, _date):
        date_dt = datetime.strptime(_date, '%Y-%m-%d')
        data = yf.download(self.ticker, start=date_dt, end=(date_dt + timedelta(days=1)), group_by='ticker')
        return data['Close'][_date]


if __name__ == '__main__':
    portfolio = Portfolio()
    print "Portfolio's profit: " + str(portfolio.profit("2019-11-01", "2021-11-01")) + "%"
    print "Annualized return: " + str(portfolio.annualized_return("2019-11-01", "2021-11-01")) + "%"

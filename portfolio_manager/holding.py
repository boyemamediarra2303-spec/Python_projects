class InvalidHoldingError(Exception):
        pass


class Holding:
    def __init__(self, ticker, shares, buy_price):
        if shares <= 0 or buy_price <=0:
            raise InvalidHoldingError("Shares and buy price must be non-negative.") 

        self.ticker = ticker
        self.shares = shares
        self.buy_price = buy_price
    def cost_basis(self):
         return self.shares * self.buy_price
    def current_value(self, current_price):
         return self.shares * current_price
    def gain_loss (self, current_price):
         return self.current_value(current_price) - self.cost_basis()
    def __str__(self):
         return f'Holding: {self.ticker}| Shares: {self.shares}| Buy_price: {self.buy_price} '
    def __eq__(self, other):
        if not isinstance(other, Holding):
            return False
        return self.ticker.lower() == other.ticker.lower()

if __name__ == "__main__":  
    h1 = Holding("AAPL", 10, 150.00)
    print(h1.cost_basis() )          # expected: 1500.0
    print(h1.current_value(175.00) )   # expected: 1750.0
    print(h1.gain_loss(175.00) )       # expected: 250.0
    
    h2 = Holding("aapl", 5, 100.00)
    print(h1 == h2)                   # expected: True
    
    # error cases -- each must raise InvalidHoldingError
    print(Holding("TSLA", -5, 220.00))
    print(Holding("TSLA", 5, 0))
    print(Holding("TSLA", 5, -10))
            
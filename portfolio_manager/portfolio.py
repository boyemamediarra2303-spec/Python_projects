class DuplicateHoldingError (Exception):
    #Raise an error whenever someone tries to enter a ticker that already exists.
    pass
class HoldingNotFoundError(Exception):
    #Raised when someone tries to look up or remove an asset that does not exist
    pass

from holding import Holding

class Portfolio:
    def __init__(self, name: str):
        self.name= name
        self._holdings= {}

    def add_holding(self,  holding: Holding):
        if holding.ticker.upper() in self._holdings:
            raise DuplicateHoldingError(f"Holding with ticker {holding.ticker} already exists in the portfolio.")
        self._holdings[holding.ticker.upper()] = holding
    def remove_holding(self, ticker: str):
        if ticker.upper() not in self._holdings:
            raise HoldingNotFoundError(f"Holding with ticker {ticker} not found in the portfolio.")
        del self._holdings[ticker.upper()]
    def get_holding(self, ticker: str):
        if ticker.upper() not in self._holdings:
            raise HoldingNotFoundError(f"Holding with ticker {ticker} not found in the portfolio.")
        return self._holdings[ticker.upper()]
    def total_value(self, current_prices: dict) -> float:
        """Calculates the combined market value of all assets together."""
        total = 0.0
        # We loop through all the Holding objects stored in our dictionary values
        for holding in self._holdings.values():
            # Look up the current market price for this specific stock ticker. 
            # If it's missing from current_prices, default to its original purchase price.
            price = current_prices.get(holding.ticker, holding.buy_price)
            total += holding.current_value(price)
        return total
    def holding_weight(self, ticker: str, current_prices: dict) -> float:
        """Calculates the percentage weight of a single asset relative to the portfolio total."""
        portfolio_total = self.total_value(current_prices)
        if portfolio_total == 0:
            return 0.0
            
        ticker_upper = ticker.upper()
        if ticker_upper not in self._holdings:
            raise HoldingNotFoundError(f"Asset {ticker_upper} not found.")
            
        # Get the value of this single stock line right now
        holding_obj = self._holdings[ticker_upper]
        price = current_prices.get(ticker_upper, holding_obj.buy_price)
        asset_value = holding_obj.current_value(price)
        
        # Formula: (Asset Value / Total Value) * 100
        return round((asset_value / portfolio_total) * 100, 2)

    def tickers(self) -> set:
        """Returns a unique Python Set of all held ticker strings."""
        return set(self._holdings.keys())

    def __len__(self) -> int:
        """Allows typing len(portfolio) to see the number of distinct assets held."""
        return len(self._holdings)

    def __iter__(self):
        """Allows typing 'for holding in portfolio:' to loop over the asset objects directly."""
        return iter(self._holdings.values())

    def to_dict(self) -> dict:
        """Converts the portfolio object structures into a standard JSON-ready dictionary."""
        serialized_holdings = {}
        for ticker, holding in self._holdings.items():
            # Breakdown the complex object into basic raw types
            serialized_holdings[ticker] = {
                "ticker": holding.ticker,
                "shares": holding.shares,
                "buy_price": holding.buy_price
            }
        return {"portfolio_name": self.name, "holdings": serialized_holdings}

    def load_from_dict(self, data: dict):
        """Rebuilds the internal portfolio map from a plain data dictionary."""
        self.name = data.get("portfolio_name", self.name)
        self._holdings = {} # Reset current container
        
        # Loop through raw entries and re-instantiate true Holding object instances
        for ticker, info in data.get("holdings", {}).items():
            rebuilt_holding = Holding(info["ticker"], info["shares"], info["buy_price"])
            self._holdings[ticker] = rebuilt_holding


if __name__ == "__main__":

    p = Portfolio("My Portfolio")
    print(p.add_holding(Holding("AAPL", 10, 150.00)))
    print(p.add_holding(Holding("TSLA", 5, 220.00)))
    
    print(len(p))                                    # expected: 2
    print(p.tickers())                               # expected: {"AAPL", "TSLA"}
    
    current_prices = {"AAPL": 175.00, "TSLA": 240.00}
    print(p.total_value(current_prices))             # expected: 3950.0
    print(p.holding_weight("AAPL", current_prices))  # expected: ~44.30
    
    for h in p:
        print(h)   # must not error
    
    p.remove_holding("TSLA")
    print(len(p))                                     # expected: 1
    
    # error cases
    print(p.add_holding(Holding("AAPL", 1, 100.00)))  # raises DuplicateHoldingError
    print(p.get_holding("MSFT"))                      # raises HoldingNotFoundError
    print(p.remove_holding("MSFT"))                   # raises HoldingNotFoundError
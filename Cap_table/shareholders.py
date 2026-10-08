from shares import CommonShare, PreferredShare, InvalidShareClassError

class InvalidHoldingError(Exception):
    pass

class Shareholder:
    def __init__(self, name, shares, share_class, investor_id=None):
        self.name= name
        self.share_class= share_class
        self.shares= shares
        self.__investor_id = investor_id
    @property
    def shares(self):
        return self._shares
    @shares.setter
    def shares(self, value):
        if value <= 0:
            raise InvalidHoldingError("Shareholder must hold a positive number of shares.")
        self._shares = value
    @property
    def investor_id(self):
        return self.__investor_id
    def __str__(self):
        return f"{self.name} holds {self.shares} shares of {self.share_class.name} class"
    def __eq__(self,other):
        if isinstance(other, Shareholder):
             return self.name.lower() == other.name.lower()
        return False
    def __lt__(self,other):
        if isinstance(other, Shareholder):
            return self.shares < other.shares 
        return NotImplemented
#Test cases:
if __name__ == "__main__":
    common = CommonShare("Common")
    s = Shareholder("Amina", 100000, common, investor_id="INV001")
    
    # Encapsulation
    print(s.shares)                          # expected: 100000
    s.shares = 150000
    print(s.shares)                          # expected: 150000
    try:
        s.shares = -10                    # raises InvalidHoldingError
    except InvalidHoldingError as e:
        print(f"Error: {e}")

    # Name mangling
    print(s.investor_id)                     # expected: "INV001"   (proper access, via property)
    print(s._Shareholder__investor_id)       # expected: "INV001"   (proves the mangled name exists)
    print(hasattr(s, "__investor_id"))       # expected: False  (that literal name doesn't exist on the instance)
    
    # dunder methods
    s2 = Shareholder("Investor Fund", 50000, common)
    print(str(s))                            # must include "Amina" and share count
    print(s == Shareholder("amina", 1, common))   # expected: True (case-insensitive name match)
    print(s2 < s)                            # expected: True (50000 < 150000)
    print(sorted([s, s2]))                   # must not error, s2 comes first
    try:
        Shareholder("Bad", -5, common)    # raises InvalidHoldingError
        Shareholder("Bad", 0, common)     # raises InvalidHoldingError
    except InvalidHoldingError as e:
        print(f"Error: {e}")
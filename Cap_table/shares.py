from abc import ABC, abstractmethod
class InvalidShareClassError(Exception):
    pass
class Share(ABC):
    def __init__(self, name):
        self.name= name
    @abstractmethod
    def liquidation_multiple(self):
        pass
    @abstractmethod
    def describe(self):
        return f"{self.name} share with liquidation multiple of {self.liquidation_multiple()}"

class CommonShare(Share):
    def __init__(self, name):
        super().__init__(name)

    def liquidation_multiple(self):
        return 0
    def describe(self):
        return f"{self.name} common share, no liquidation preference"
    def to_dict(self):
        return {"type": "Common", "name": self.name}
class PreferredShare(Share):
    def __init__(self,name, liquidation_multiple=1.0):
        super().__init__(name)
        self._liquidation_multiple = liquidation_multiple
        if liquidation_multiple <= 0:
            raise InvalidShareClassError("Liquidation multiple must be greater than 0 for preferred shares.")
    def liquidation_multiple(self):
        return self._liquidation_multiple
    def describe(self):
        return f"{self.name} preferred share: {self._liquidation_multiple} Liquidation preference"
    def to_dict(self):
        return {
            "type": "Preferred", 
            "name": self.name, 
            "liquidation_multiple": self._liquidation_multiple
        }

#test cases:
if __name__ == "__main__":
    c = CommonShare("Common")
    pref = PreferredShare("Series A Preferred", 1.5)
    
    print(c.liquidation_multiple())                    # expected: 0
    print(pref.liquidation_multiple())                 # expected: 1.5
    print(isinstance(pref, Share))                # expected: True

    mixed = [c, pref]
    for share in mixed:
        print(share.describe())     # two DIFFERENT strings, one per class
        print(share.liquidation_multiple())   # 0, then 1.5
    try:
        PreferredShare("Series B", -1)              # raises InvalidShareClassError
        PreferredShare("Series B", 0)               # raises InvalidShareClassError
    except InvalidShareClassError as e:
        print(f"Error: {e}")
# Test cases approved.
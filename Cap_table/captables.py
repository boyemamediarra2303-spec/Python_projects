from shareholders import Shareholder
from shares import CommonShare, PreferredShare

class DuplicateShareholderError(Exception):
    pass
class ShareholderNotFoundError(Exception):
    pass
class CapTable:
    def __init__(self, company_name):
        self.company_name = company_name
        self.shareholders = {}
    def add_shareholder(self, shareholder):
        key= shareholder.name.lower()
        if key in self.shareholders:
            raise DuplicateShareholderError(f"Shareholder {shareholder.name} already exists in the cap table.")
        self.shareholders[key] = shareholder
    def remove_shareholder(self, name):
        key = name.lower()
        if key not in self.shareholders:
            raise ShareholderNotFoundError(f"Shareholder {name} not found in the cap table.")
        del self.shareholders[key]
    def total_shares(self):
        return sum(shareholder.shares for shareholder in self.shareholders.values())
    def ownership_percentage(self, name):
        key= name.lower()
        if key not in self.shareholders:
            raise ShareholderNotFoundError(f"Shareholder {name} not found in the cap table.")
        shareholder = self.shareholders[key]
        percentage = shareholder.shares / self.total_shares() * 100
        return round(percentage, 2)
    def issue_new_round(self, new_shareholder, price_per_share):
        key = new_shareholder.name.lower()
        if key in self.shareholders:
            raise DuplicateShareholderError(f"Shareholder {new_shareholder.name} already exists in the cap table.")
            
        report = {}
        for shareholder in self.shareholders.values():
            report[shareholder.name] = {
                "before": self.ownership_percentage(shareholder.name) # Fix 4: Exact key names
            }
            
        self.shareholders[key] = new_shareholder
        
        for name in report.keys():  # Fix 3: Iterate over report tracking keys
            report[name]["after"] = self.ownership_percentage(name)
            
        return report
    def __len__(self):
        """Returns the total number of shareholders when len(ct) is called."""
        return len(self.shareholders)

    def __iter__(self):
        """Enables looping directly through the cap table objects."""
        return iter(self.shareholders.values())

    def describe_all(self):
        """Returns a list of descriptions from all share classes polymorphically."""
        return [sh.share_class.describe() for sh in self.shareholders.values()]

if __name__ == "__main__":
    #testing the script
    common = CommonShare("Common")
    ct = CapTable("Acme Inc")
    ct.add_shareholder(Shareholder("Founder", 800000, common))
    ct.add_shareholder(Shareholder("Cofounder", 200000, common))
    
    print(len(ct))                                  # expected: 2
    print(ct.total_shares())                        # expected: 1000000
    print(ct.ownership_percentage("Founder"))       # expected: 80.0
    
    pref = PreferredShare("Series A Preferred", 1.0)
    new_investor = Shareholder("VC Fund", 250000, pref)
    report = ct.issue_new_round(new_investor, price_per_share=4.00)
    
    print(ct.total_shares())                        # expected: 1250000
    print(ct.ownership_percentage("Founder"))       # expected: 64.0
    print(report["Founder"]["before"])              # expected: 80.0
    print(report["Founder"]["after"])               # expected: 64.0
    
    descriptions = ct.describe_all()
    print(len(descriptions))                        # expected: 3
    # descriptions should NOT all be identical -- Common vs Preferred differ
    
    for sh in ct:
        print(sh)     # must not error
    
    ct.remove_shareholder("Cofounder")
    print(len(ct))                                  # expected: 2
    
    # error cases
    ct.add_shareholder(Shareholder("Founder", 1, common))   # raises DuplicateShareholderError
    print(ct.ownership_percentage("Nobody"))                       # raises ShareholderNotFoundError
    ct.remove_shareholder("Nobody")                          # raises ShareholderNotFoundError
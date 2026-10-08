import json
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

    def exit_waterfall(self, exit_value):
    
        #Distributes acquisition value across shareholders respecting preferred constraints polymorphically, then distributing the remainder pro-rata.
        payouts = {sh.name: 0.0 for sh in self.shareholders.values()}
        remaining_cash = float(exit_value)
    
        # Collect all preferred claims polymorphically. 
        # Common shares naturally return 0, filtering themselves out without isinstance!
        preferred_claims = {}
        total_preferred_claims = 0.0
        
        for sh in self.shareholders.values():
            multiple = sh.share_class.liquidation_multiple()
            if multiple > 0:
                # Payout ceiling formula based on share volume preference bounds
                claim = sh.shares * multiple
                preferred_claims[sh.name] = claim
                total_preferred_claims += claim

        if total_preferred_claims > 0:
            if remaining_cash <= total_preferred_claims:
                # Scenario A: Crunch time. Cash cannot cover preferred baseline entirely.
                for name, claim in preferred_claims.items():
                    payouts[name] = round((claim / total_preferred_claims) * remaining_cash, 2)
                return payouts  # Game over, all cash completely exhausted
            else:
                # Scenario B: Satisfy preferred holders completely and move to remainder pool
                for name, claim in preferred_claims.items():
                    payouts[name] = round(claim, 2)
                    remaining_cash -= claim

        # Determine the total common share pool baseline remaining
        common_shareholders = [sh for sh in self.shareholders.values() if sh.share_class.liquidation_multiple() == 0]
        total_common_shares = sum(sh.shares for sh in common_shareholders)

        if total_common_shares > 0 and remaining_cash > 0:
            for sh in common_shareholders:
                pro_rata_share = (sh.shares / total_common_shares) * remaining_cash
                payouts[sh.name] = round(pro_rata_share, 2)

        return payouts


    def save_to_json(self, filename="data.json"):
        #Converts all data into standard dictionaries and writes to a file.
        serialized_data = {
            "company_name": self.company_name,
            "shareholders": [sh.to_dict() for sh in self.shareholders.values()]
        }
        with open(filename, "w") as file:
            json.dump(serialized_data, file, indent=4)
        print(f"Cap table data safely written to {filename}")

    def load_from_json(self, filename="data.json"):
        #Reads a file and reconstructs complex Python objects dynamically.
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                
            self.company_name = data["company_name"]
            self.shareholders = {}  # Reset current tracking workspace
            
            for sh_data in data["shareholders"]:
                # 1. Rebuild the polymorphic share class round-trip
                sc_data = sh_data["share_class"]
                if sc_data["type"] == "Preferred":
                    share_class = PreferredShare(sc_data["name"], sc_data["liquidation_multiple"])
                else:
                    share_class = CommonShare(sc_data["name"])
                    
                # 2. Rebuild the Shareholder object
                shareholder = Shareholder(
                    name=sh_data["name"],
                    shares=sh_data["shares"],
                    share_class=share_class,
                    investor_id=sh_data["investor_id"]
                )
                
                # 3. Re-index into the engine's active dictionary storage
                self.add_shareholder(shareholder)
            print(f" Cap table successfully restored from {filename}")
        except FileNotFoundError:
            print(f" No existing data file found at {filename}. Starting fresh.")

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
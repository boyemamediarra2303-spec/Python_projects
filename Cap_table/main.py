from shares import CommonShare, PreferredShare, InvalidShareClassError
from shareholders import Shareholder, InvalidHoldingError
from captables import CapTable, DuplicateShareholderError, ShareholderNotFoundError
#import pandas as pd

def main():
    company_name= input('Enter company name to start: ')
    ct = CapTable(company_name)
    ct.load_from_json()
    last_report= None

    while True:
        print(f'\n ==={ct.company_name} Cap table Manager ===')
        print('1. Add Shareholder (Founding Team)')
        print('2. Issue New Funding Round')
        print('3. View Cap Table (Sorted by Stake)')
        print('4. View Last Dilution Report')
        print('5. Run Exit Waterfall Simulation')
        print('6. Save & Exit')
        choice = input('select an option (1-6): ')

        try:
            if choice == "1":
                name = input("Enter shareholder name: ")
                shares = int(input("Enter number of shares: "))
                share_class = CommonShare("Common") 
                
                new_sh = Shareholder(name, shares, share_class)
                ct.add_shareholder(new_sh)
                print(f"Successfully added {name} to the cap table.")

            elif choice == "2":
                name = input("Enter investor name: ")
                shares = int(input("Enter shares issued: "))
                price = float(input("Enter price per share ($): "))
                type_share = input("Share type (Common/Preferred): ").strip().lower()
                
                if type_share == "preferred":
                    multiple = float(input("Enter liquidation multiple (e.g., 1.0): "))
                    share_class = PreferredShare(f"{name} Preferred", multiple)
                else:
                    share_class = CommonShare("Common")

                new_investor = Shareholder(name, shares, share_class)
                # This returns the dictionary report and saves it globally
                last_report = ct.issue_new_round(new_investor, price)
                print(f"Round closed! {name} injected capital into the company.")

            elif choice == "3":
                print(f"\n--- Current Cap Table Total Shares: {ct.total_shares()} ---")
                # Convert the cap table to a list. Python uses your __lt__ to sort them!
                # Because __lt__ checks if s1 < s2, sorting normally gives smallest first. 
                # Use reverse=True to get the LARGEST stakes printed first!
                sorted_shareholders = sorted(list(ct), reverse=True)
                
                print(f"{'Shareholder':<20} | {'Shares':<12} | {'Ownership %':<10}")
                print("-" * 50)
                for sh in sorted_shareholders:
                    pct = ct.ownership_percentage(sh.name)
                    print(f"{sh.name:<20} | {sh.shares:<12,} | {pct:>9}%")
                    #just learned about format specification

            elif choice == "4":
                if not last_report:
                    print("No funding rounds have been issued yet.")
                else:
                    print("\n--- Last Dilution Report ---")
                    print(f"{'Shareholder':<20} | {'Before %':<10} | {'After %':<10} | {'Change':<10}")
                    print("-" * 60)
                    for name, metrics in last_report.items():
                        before = metrics['before']
                        after = metrics['after']
                        diff = round(after - before, 2)
                        print(f"{name:<20} | {before:>9}% | {after:>8}% | {diff:>9}%")

            elif choice == "5":
                valuation = float(input("Enter the total enterprise acquisition exit value ($): "))
                payout_table = ct.exit_waterfall(valuation)
                print(f"\n--- Acquisition Payout Liquidation Chart ($ {valuation:,}) ---")
                print(f"{'Shareholder':<20} | {'Final Payout Pct/Cash':<20}")
                print("-" * 45)
                for name, cash in payout_table.items():
                    print(f"{name:<20} | ${cash:,.2f}")

            elif choice == "6":
                # Save automatically right before the break state closes memory blocks
                ct.save_to_json()
                print("Exiting Cap Table Simulator safely. Goodbye!")
                break
            else:
                print("Invalid option. Please choose 1-6.")
        except (DuplicateShareholderError, ShareholderNotFoundError, 
                InvalidShareClassError, InvalidHoldingError) as e:
            print(f"\n LOGIC ERROR: {e}")
        except ValueError:
            print("\n INPUT ERROR: Please enter valid numbers for shares and prices.")

if __name__ == "__main__":
    main()

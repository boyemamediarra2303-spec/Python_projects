import json
import os 

from holding import Holding, InvalidHoldingError
from calculator import calculate_npv, calculate_roi, calculate_payback_period, calculate_irr, InvalidFinanceInputError
from portfolio import Portfolio, DuplicateHoldingError, HoldingNotFoundError

def main():
    print("Welcome to the Corporate Capital Budgeting & Portfolio Engine!")
    portfolio_name = input("Enter a name for your portfolio: ")
    my_portfolio = Portfolio(portfolio_name)
    
    # STRETCH GOAL: AUTOMATED DATA RETRIEVAL LINK 
    db_filename = "data.json"
    if os.path.exists(db_filename):
        try:
            with open(db_filename, "r") as file:
                raw_data = json.load(file)
                my_portfolio.load_from_dict(raw_data)
            print(f"Found existing data! Successfully loaded portfolio assets.")
        except Exception as e:
            print(f"Warning: Could not parse data file securely ({e}). Starting fresh.")
    
    market_prices = {"AAPL": 175.00, "TSLA": 240.00, "MSFT": 420.00}


    # Start the continuous runtime loop
    while True:
        print("\n" + "="*40)
        print(f"--- MENU: {my_portfolio.name.upper()} ---")
        print("1. Add Holding")
        print("2. Remove Holding")
        print("3. View Portfolio Summary")
        print("4. Run Hypothetical Capital Budgeting Calculation")
        print("5. Exit")
        print("="*40)
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == "1":
            try:
                ticker = input("Enter asset ticker (e.g., AAPL): ")
                shares = float(input("Enter number of shares: "))
                price = float(input("Enter purchase price per share: "))
                
                # Create a temporary Holding object and pass it to your portfolio
                new_holding = Holding(ticker, shares, price)
                my_portfolio.add_holding(new_holding)
                print(f"✅ Successfully added {shares} shares of {ticker.upper()}!")
                
            except (ValueError, InvalidHoldingError, DuplicateHoldingError) as error_msg:
                print(f"❌ Input Error: {error_msg}")
                
        elif choice == "2":
            try:
                ticker_to_remove = input("Enter the stock ticker you want to remove: ").strip()
                # Run the backend lookup and removal logic you coded in portfolio.py
                my_portfolio.remove_holding(ticker_to_remove)
                print(f"✅ Successfully removed {ticker_to_remove.upper()} from your portfolio.")
                
            except HoldingNotFoundError as error_msg:
                # Captures cases where the stock doesn't exist without crashing the menu
                print(f"❌ Removal Error: {error_msg}")

            
        elif choice == "3":
            print(f"\n--- {my_portfolio.name} Holdings Breakdown ---")
            if len(my_portfolio) == 0:
                print("Your portfolio is currently empty.")
            else:
                # Use the __iter__ dunder hook you built to loop directly over your holdings!
                for holding in my_portfolio:
                    # Get the individual weight using your holding_weight method
                    weight = my_portfolio.holding_weight(holding.ticker, market_prices)
                    print(f"- {holding} | Portfolio Weight: {weight}%")
                print(f"Total Portfolio Valuation: ${my_portfolio.total_value(market_prices):.2f}")
                
        elif choice == "4":
            print("\n--- Hypothetical Investment Calculator ---")
            print("A. Net Present Value (NPV)")
            print("B. Return on Investment (ROI)")
            print("C. Payback Period")
            print("D. Internal Rate of Return (IRR)")
            calc_choice = input("Select calculation type (A-D): ").strip().upper()
            
            try:
                # Scenario A, C, and D all require an Initial Investment and Cash Flows list
                if calc_choice in ["A", "C", "D"]:
                    initial_inv = float(input("Enter initial investment amount: "))
                    num_years = int(input("How many years of cash flows will you input? "))
                    
                    cash_flows = []
                    for i in range(num_years):
                        cf = float(input(f"Enter cash flow for Year {i + 1}: "))
                        cash_flows.append(cf)
                
                # Execute individual formulas based on choice
                if calc_choice == "A":
                    rate = float(input("Enter the discount rate (e.g., 0.10 for 10%): "))
                    npv_res = calculate_npv(initial_inv, cash_flows, rate)
                    print(f"📊 Calculated NPV: ${npv_res:.2f}")
                    
                elif calc_choice == "B":
                    initial_inv = float(input("Enter initial investment amount: "))
                    final_val = float(input("Enter expected final portfolio value: "))
                    roi_res = calculate_roi(initial_inv, final_val)
                    print(f"📊 Calculated ROI: {roi_res}%")
                    
                elif calc_choice == "C":
                    payback_res = calculate_payback_period(initial_inv, cash_flows)
                    if payback_res is not None:
                        print(f"📊 Calculated Payback Period: {payback_res} years")
                    else:
                        print("⚠️ This project never recovers its initial investment.")
                        
                elif calc_choice == "D":
                    irr_res = calculate_irr(initial_inv, cash_flows)
                    print(f"📊 Calculated IRR: {irr_res * 100:.1f}% ({irr_res})")
                    
                else:
                    print("❌ Invalid calculation type selected.")
                    
            except (ValueError, InvalidFinanceInputError) as error_msg:
                print(f"❌ Calculation Error: {error_msg}")

            
        elif choice == "5":
            #STRETCH GOAL: AUTOSAVE BEFORE DISCONNECTING
            try:
                with open(db_filename, "w") as file:
                    json.dump(my_portfolio.to_dict(), file, indent=4)
                print("💾 Application data backed up cleanly to data.json.")
            except Exception as e:
                print(f"⚠️ Error saving application backup state: {e}")
                
            print("Exiting program. Thank you for using the Portfolio Engine!")
            break


if __name__ == "__main__":
    main()

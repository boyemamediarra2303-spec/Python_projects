def calculate_npv(initial_investment, cash_flows, discount_rate):
    npv= - initial_investment
    for year,cf in enumerate(cash_flows, start=1):
        npv += cf/(1+discount_rate)**year
    return round(npv,2)
try:
    initial_investment = int(input("Enter the initial investment: "))
    discount_rate = float(input("Enter the discount rate: "))
    cash_flows = []
    num_years = int(input("Enter the number of years: "))
    for i in range(num_years):
        cash_flow = float(input(f"Enter the cash flow for year {i+1}: "))
        cash_flows.append(cash_flow)
    npv = calculate_npv(initial_investment, cash_flows, discount_rate)
    if npv > 0:
        print(f"""The Net Present Value (NPV) is: {npv}.
        ACCEPT: This project generates positive economic value.""")
    else:
        print(f"""The Net Present Value (NPV) is: {npv}.
        REJECT: This project destroys capital value.""")
    input("\nPress Enter to exit the program...")
except ValueError:
    print("Invalid input. Please enter valid numbers.")

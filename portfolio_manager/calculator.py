class InvalidFinanceInputError(Exception):
    """Custom exception raised for invalid inputs in financial calculations."""
    pass

def calculate_npv(initial_investment, cash_flows, interest_rate):
    if initial_investment <= 0 or interest_rate <= -1:
        raise InvalidFinanceInputError("Initial investment cannot be negative or zero and interest rate cannot be less than or equal to -1.")
    npv= - initial_investment
    for year,cf in enumerate(cash_flows, start=1):
        npv += cf/(1+interest_rate)**year
    return round(npv,2)
def calculate_roi(initial_investment, final_value):
    if initial_investment <= 0:
        raise InvalidFinanceInputError("Initial investment cannot be negative or zero.")
    return round((final_value - initial_investment) / initial_investment * 100, 2)
def calculate_payback_period(initial_investment, cash_flows):
    if initial_investment <= 0 or not cash_flows:
        raise InvalidFinanceInputError("Initial investment cannot be negative or zero and cash flows list cannot be empty.")
    unrecovered_amount = initial_investment
    years_elapsed = 0
    for year, cf in enumerate (cash_flows, start = 1):
        if unrecovered_amount > cf:
           unrecovered_amount -= cf 
           years_elapsed = year
        else:
            payback_perod= years_elapsed + unrecovered_amount / cf
            return round(payback_perod, 1)
    return None 
def calculate_irr(initial_investments, cash_flows, guess_range = (0, 1), precision= 0.0001):
    if initial_investments <= 0 or not cash_flows :
        raise InvalidFinanceInputError("Initial investment cannot be negative or zero and cash flows list cannot be empty.")
    low, high = guess_range
    if high - low < precision:
        return round((low + high)/ 2,3)
    mid_guess = (low + high) / 2
    current_npv = calculate_npv(initial_investments, cash_flows, mid_guess)
    if current_npv > 0:
        return calculate_irr(initial_investments, cash_flows, (mid_guess, high), precision)
    else:
        return calculate_irr(initial_investments, cash_flows, (low, mid_guess), precision)
    
if __name__ == "__main__":
    print(calculate_npv(10000, [3000, 4000, 5000, 2000], 0.10)  )    # expected: 1155.66
    print(calculate_npv(5000, [1000, 1000, 1000], 0.08))             # expected: -2422.90
    print(calculate_roi(10000, 12500))                      # expected: 25.0
    print(calculate_payback_period(10000, [3000, 4000, 5000, 2000])) # expected: 2.6
    print(calculate_irr(10000, [3000, 4000, 5000, 2000]))           # expected: ~0.153 (+/- 0.005)
    
    # error cases -- each must raise InvalidFinanceInputError
    print(calculate_npv(10000, [3000], -1.5))
    print(calculate_npv(-5000, [3000], 0.1))
    print(calculate_npv(10000, [], 0.1))
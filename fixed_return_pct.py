import csv

"""
Main Program
"""

"""
This function will iterate through the list and print out starting
capital, utilization, and expected perfect take profit, and ending
balance.

Assume first trade maxes out utilization percent. Each iteration will
run through a trade trade until the (sum of an additional trade trade)
is less than the capital utilization max.
"""
def prompt(threshold: float, cap_start: float, util_pct_max: float,
           adj_gain: float, contract_cost: float, platform_fee: str
           ) -> None:
    """
    Fixed Return - Percentage CSV calculates sequential balances from
    a given take-profit percentage, and a CSV will be produced in the
    <export/> internal folder.
    
    Args:
        threshold (float)
        cap_start (float)
        util_pct_max (float)
        adj_gain (float)
        contract_cost (float)
        platform_fee (str)

    Returns:
        None
    """

    file_path = 'export/export_scratch.csv'

    meta_list = []
    # init portfolio and trade costs
    portfolio = cap_start
    contract_amt = 1
    # define iteration end
    while portfolio < threshold:
        # track amount of contracts being traded per spread
        # add an additional contract if portfolio utilization allows
        level = contract_cost * (contract_amt + 1)
        capacity = portfolio * util_pct_max
        if level <= capacity:
            while level <= capacity:
                level += contract_cost
                contract_amt += 1

        def mathing(portfolio, contract_amt):
            # define actual_utilization
            actual_cost = contract_cost * contract_amt
            actual_util = actual_cost / portfolio
            # define profits
            profit = actual_cost * adj_gain
            # define ending portfolio
            fees = contract_amt * 2 * platform_fee
            end_port = portfolio + profit - fees
            transaction = [portfolio, contract_amt, actual_cost,
                           actual_util, profit, fees, end_port]
            meta_list.append(transaction)
            return end_port

        portfolio = mathing(portfolio, contract_amt)
    transaction_header = [["Portfolio", "Contract Amount", "Trade Cost",
                          "Portfolio Utilization", "Profit", "Fees",
                          "Ending Balance"]]
    data = transaction_header + meta_list
    
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def main() -> tuple[float, float, float, float, str, float]:
    """
    Begins Fixed Return - Percentage by collecting user input.

    Args:
        None

    Returns:
        threshold (float)
        cap_start (float)
        util_pct_max (float)
        adj_gain (float)
        contract_cost (float)
        platform_fee (str)
    """
    def get_input(question: str, default: any, input_type: str) -> any:
        """
        
        """
        user_input = input(f"{question} (default: {default}): ")
        if not user_input:
            return default
        try:
            return input_type(user_input)
        except ValueError:
            print(f"Invalid input. Using default: {default}")
            return default


    while True:
        while True:
            threshold = get_input("What's the target: ", 1000000, float)
            cap_start = get_input("What's the starting balance: ", 25000, float)
            util_pct_max = get_input("Maximum portfolio utilization percentage (%): ", 55, float) # convert percent to decimal
            adj_gain = get_input("What's the trade's take-profit percentage (%): ", 10, float) # convert percent to decimal
            contract_cost = get_input("What's the typical premium: ", 1.5, float) # convert cost/share to cost/contract
            platform_fee = None

    prompt(threshold, cap_start, util_pct_max, adj_gain,
         contract_cost, platform_fee)


if __name__ == "__main__":
    threshold = 1000000 # monetary goal
    cap_start = 300 # starting portfolio
    util_pct_max = 0.55 # maximum portfolio utilization percent
    adj_gain = 0.1 # profit percentage in decimal
    contract_cost = 150 # typical trade max risk
    platform_fee = 0.65# variable for platform fee (RH = .08, CS = 0.65)
    print("running program")
    prompt(threshold, cap_start, util_pct_max, adj_gain,
         contract_cost, platform_fee)
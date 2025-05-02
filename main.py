"""
Main Program
"""

"""
This function will iterate through the list and print out starting capital, utilization, and expected perfect take profit, and ending balance.

Assume first trade maxes out utilization percent. Each iteration will run through a spread trade until the (sum of an additional spread trade) is less than the capital utilization max.
"""
def main(threshold, cap_start, util_pct_max, adj_gain, spread_cost):
    meta_list = []
    # init portfolio and trade costs
    portfolio = cap_start
    trade_cost = spread_cost
    # define iteration end
    while portfolio < threshold:
        # track amount of contracts being traded per spread
        contract_amt = 1
        # add an additional contract if portfolio utilization allows
        if (trade_cost + spread_cost) <= (portfolio * util_pct_max):
            trade_cost += spread_cost
            contract_amt += 1

        def mathing(portfolio, trade_cost, contract_amt):
            # define actual_utilization
            actual_util = trade_cost / portfolio
            # define profits
            profit = trade_cost * adj_gain
            # define ending portfolio
            end_port = portfolio + profit
            transaction = [portfolio, contract_amt, trade_cost, actual_util, profit, end_port]
            meta_list.append(transaction)
            return end_port

        portfolio = mathing(portfolio, trade_cost, contract_amt)
    for index, item in enumerate(meta_list):
        print(index, item)


if __name__ == "__main__":
    threshold = 25000 # monetary goal
    cap_start = 1345 # starting portfolio
    util_pct_max = 0.55 # maximum portfolio utilization percent
    adj_gain = 0.28 #
    spread_cost = 740 # typical spread max risk
    print("running program")
    main(threshold, cap_start, util_pct_max, adj_gain, spread_cost)
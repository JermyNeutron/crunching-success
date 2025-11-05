import csv
import platform
import subprocess

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


def get_duration(days: int) -> str:
    """
    Converts days into a duration statement, i.e. "2 months, 1 day, (60 days)

    Args:
        days (int)

    Returns:
        duration_print (str)
    """
    
    years = days // 365
    if years:
        days -= years * 365
    calendar_seq = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    months = 0
    i = 0
    while i < len(calendar_seq) and days >= calendar_seq[i]:
        days -= calendar_seq[i]
        months += 1
        i +=1

    rem_days = days
    y_prefix = "years" if years > 1 else "year"
    m_prefix = "months" if months > 1 else "month"
    rd_prefix = "days" if rem_days > 1 else "day"

    duration_print = ""
    if years:
        duration_print += f"{years} {y_prefix}"
        if months:
            duration_print += f", {months} {m_prefix}"
        if rem_days:
            duration_print += f", {rem_days} {rd_prefix}"
    elif months:
        duration_print += f"{months} {m_prefix}"
        if rem_days:
            duration_print += f", {rem_days} {rd_prefix}"
    else:
        duration_print += f"{rem_days} {rd_prefix}"

    return duration_print

print(get_duration(41))


def get_summary(meta_list: list) -> tuple[int, float, float]:
    """
    Args:
        meta_list (list)

    Returns:
        something

    Format:
        0 = starting balance
        1 = contract amount
        2 = trade cost
        3 = portfolio utilization
        4 = trade profit
        5 = fees
        6 = ending balance
    """
    total = len(meta_list)
    duration = get_duration(len(meta_list))
    starting_balance = meta_list[0][0]
    ending_balance = meta_list[-1][6]
    return total, duration, starting_balance, ending_balance


def get_platform_fee(brok_index: int) -> float:
    # 1) Charles Schwab
    # 2) Robinhood
    fees = {0: 0, 1: 0.65, 2: 0.04}
    return fees[brok_index]


def prompt(cap_start: float, threshold: float, util_pct_max: float,
           adj_gain: float, contract_cost: float, brok_index: int,
           os_type: str,) -> None:
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
        platform_fee (float)
        os_type (str)

    Returns:
        None
    """

    # export CSV location
    file_path = 'export/export_scratch.csv'

    # data list for export
    meta_list = []

    # initialization of user input
    util_pct_max = util_pct_max / 100
    adj_gain = adj_gain / 100
    contract_cost = contract_cost * 100

    # init portfolio and trade costs
    portfolio = cap_start
    contract_amt = 1
    platform_fee = get_platform_fee(brok_index)
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
            target = actual_cost * adj_gain
            # define ending portfolio
            fees = contract_amt * 2 * platform_fee
            end_port = portfolio + target - fees
            transaction = [f"{portfolio:.2f}", int(contract_amt),
                           f"{actual_cost:.2f}", f"{actual_util:.2f}",
                           f"{target:.2f}", f"{fees:.2f}", f"{end_port:.2f}"]
            meta_list.append(transaction)
            return end_port

        portfolio = mathing(portfolio, contract_amt)
    transaction_header = [["Starting Balance", "C. Amt", "Cost",
                          "Util%", "Target", "Fees",
                          "Ending Balance"]]
    summary = get_summary(meta_list)
    data = transaction_header + meta_list

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    # For macOS, opens up 'Numbers' app.
    if os_type == 'Darwin':
        subprocess.run(['open', '-a', 'Numbers', file_path])

    return meta_list, summary

    # deletable, testing popping
    #
    # things i want to pull for more important details
    # - how many days converted to years, months, day
    # - starting balance
    # - ending balance


def main(os_type: str) -> tuple[float, float, float, float, float, float]:
    """
    Begins Fixed Return - Percentage by collecting user input.

    Args:
        os_type (str)

    Returns:
        threshold (float)
        cap_start (float)
        util_pct_max (float)
        adj_gain (float)
        contract_cost (float)
        platform_fee (float)
    """


    threshold = get_input("What's the target?", 1000000, float)
    cap_start = get_input("What's the starting balance?", 25000, float)
    util_pct_max = get_input("Maximum portfolio utilization percentage (%)?", 55, float) # convert percent to decimal
    adj_gain = get_input("What's the trade's take-profit percentage (%)?", 10, float) # convert percent to decimal
    contract_cost = get_input("What's the typical premium?", 1.5, float) # convert cost/share to cost/contract
    brok_index = int(get_input("""Select a broker:
    1) Charles Schwab (ThinkOrSwim)
    2) Robinhood
                            
    : """, 1, str))

    prompt(cap_start, threshold, util_pct_max, adj_gain,
         contract_cost, brok_index, os_type)


if __name__ == "__main__":
    print("running program")
    os_type = platform.system()
    main(os_type)
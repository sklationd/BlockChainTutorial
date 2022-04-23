from brownie import FundMe
from scripts.helpful_scripts import get_account


def check_price_feed():
    fund_me = FundMe[-1]
    print(fund_me.getPrice())  # 20,000,000,000,000 * 10**18
    print(fund_me.getConversionRate(1))  # 2000
    print(fund_me.getEntranceFee())


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    print(f"Current entrance fee is {entrance_fee}")

    print(f"Funding {entrance_fee}")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()

    fund_me.withdraw({"from": account})
    print("Withdraw")


def main():
    check_price_feed()
    fund()
    withdraw()

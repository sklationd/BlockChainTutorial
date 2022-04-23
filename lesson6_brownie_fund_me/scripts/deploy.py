from brownie import FundMe, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    active_network = network.show_active()
    print(f"The active network is {active_network}")

    if active_network not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        priceFeed = config["networks"][active_network].get("eth_usd_price_feed")
    else:
        priceFeed = deploy_mocks()

    fund_me = FundMe.deploy(
        priceFeed,
        {"from": account},
        publish_source=config["networks"][active_network].get("verify"),
    )

    # if we are on a persistent network like linkeby
    print(f"Contract deployed to {fund_me.address}")

    return fund_me


def main():
    deploy_fund_me()

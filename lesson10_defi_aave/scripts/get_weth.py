from brownie import config, network, interface
from scripts.helpful_scripts import get_account


def main():
    get_weth()


def get_weth():
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.1 * (10**18)})
    tx.wait(1)
    print("Received 0.1 WETH")
    return tx
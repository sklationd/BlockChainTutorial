from brownie import config, network
from dotenv import get_key
from scripts.get_weth import get_weth
from scripts.helpful_scripts import get_account, FORKED_LOCAL_ENVIRONMENTS


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        get_weth()

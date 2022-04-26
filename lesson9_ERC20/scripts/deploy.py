from scripts.helpful_scripts import get_account
from brownie import APPLToken, config, network


def deploy_apple_token():
    account = get_account()
    applToken = APPLToken.deploy(10000 * (10**18), {"from": account})
    print(f"user 0 owns {applToken.balanceOf(account.address)} Apple Token!")


def send_token():
    account0 = get_account(index=0)
    account1 = get_account(index=1)
    applToken = APPLToken[-1]

    amount = 100 * (10**18)
    print(f"user 0 sends {amount} token to user 1!")
    send_tx = applToken.transfer(account1.address, amount, {"from": account0})
    send_tx.wait
    print(f"user 1 owns {applToken.balanceOf(account1.address)} Apple Token!")


def main():
    deploy_apple_token()
    # send_token()

from os import link
from brownie import accounts, config, network

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account(index=None, id=None):
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        if index:
            return accounts[index]
        return accounts[0]
    else:
        if id:
            return accounts.load(id)
        else:
            return accounts.load("sklationd")
    # return accounts.add(config["wallets"]["from_key"])

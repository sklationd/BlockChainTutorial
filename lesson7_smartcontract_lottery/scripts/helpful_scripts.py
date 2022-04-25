from os import link
from brownie import (
    accounts,
    config,
    network,
    MockV3Aggregator,
    Contract,
    VRFCoordinatorMock,
    LinkToken,
    interface,
)

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


DECIMAL = 8
STARTING_PRICE = 200000000000


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


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )

    return contract


def deploy_mocks():
    account = get_account()

    # MockV3Aggregator
    if len(MockV3Aggregator) <= 0:
        print("Deploying MockV3Aggregator")
        MockV3Aggregator.deploy(DECIMAL, STARTING_PRICE, {"from": account})

    # LinkToken
    if len(LinkToken) <= 0:
        print("Deploying LinkToken")
        LinkToken.deploy({"from": account})
    link_token = LinkToken[-1]

    # VRFCoordinatorMock
    if len(VRFCoordinatorMock) <= 0:
        print("Deploying VRFCoordinatorMock")
        VRFCoordinatorMock.deploy(link_token.address, {"from": account})


def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Fund Contract!")
    return tx

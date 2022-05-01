from brownie import (
    network,
    accounts,
    config,
    MockV3Aggregator,
    MockDAI,
    MockWETH,
    Contract,
    web3,
)
import time

NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
    "mainnet-fork",
    "binance-fork",
    "matic-fork",
]
# Etherscan usually takes a few blocks to register the contract has been deployed
BLOCK_CONFIRMATIONS_FOR_VERIFICATION = 6

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "dai_usd_price_feed": MockV3Aggregator,
    "weth_token": MockWETH,
    "fau_token": MockDAI,
}

DECIMALS = 18
INITIAL_VALUE = web3.toWei(2000, "ether")


def get_account(index=None, id=None):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if index:
            return accounts[index]
        return accounts[0]
    else:
        if id:
            return accounts.load(id)
        else:
            return accounts.load("sklationd")
    # return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        try:
            contract_address = config["networks"][network.show_active()][contract_name]
            contract = Contract.from_abi(
                contract_type._name, contract_address, contract_type.abi
            )
        except KeyError:
            print(
                f"{network.show_active()} address not found, perhaps you should add it to the config or deploy mocks?"
            )
            print(
                f"brownie run scripts/deploy_mocks.py --network {network.show_active()}"
            )
    return contract


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    print(f"The active network is {network.show_active()}")

    print("Deploying Mocks...")
    account = get_account()

    print("Deploying Mock Price Feed...")
    mock_price_feed = MockV3Aggregator.deploy(
        decimals, initial_value, {"from": account}
    )
    print(f"Deployed to {mock_price_feed.address}")

    print("Deploying Mock DAI Token")
    dai_token = MockDAI.deploy({"from": account})
    print(f"Deployed to {dai_token.address}")

    print("Deploying Mock WETH Token")
    weth_token = MockWETH.deploy({"from": account})
    print(f"Deployed to {weth_token.address}")

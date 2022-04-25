from scripts.deploy import deploy_lottery, USD_ENTRY_FEE
from scripts.helpful_scripts import (
    DECIMAL,
    STARTING_PRICE,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
    fund_with_link,
)
from brownie import Lottery, accounts, config, network, exceptions
from web3 import Web3
import pytest
import time


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery.address)

    # Act
    lottery.endLottery({"from": account})

    time.sleep(60)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0

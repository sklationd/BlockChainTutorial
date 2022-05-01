from brownie import config, network, TokenFarm, DAppToken, exceptions
import pytest
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    INITIAL_VALUE,
    DECIMALS,
)
from scripts.deploy import deploy_token_farm_and_dapp_token, KEPT_BALANCE


def test_set_price_feed_contract():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local block chain")
    account = get_account()
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()

    # Act
    newPriceFeedContractAddress = get_contract("eth_usd_price_feed")
    set_tx = token_farm.setTokenPriceFeed(
        dapp_token.address, newPriceFeedContractAddress, {"from": account}
    )
    set_tx.wait(1)

    # Assert
    assert (
        token_farm.tokenToPriceFeed(dapp_token.address) == newPriceFeedContractAddress
    )

    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setTokenPriceFeed(
            dapp_token.address, newPriceFeedContractAddress, {"from": non_owner}
        )


def test_stake_tokens(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local block chain")
    account = get_account()
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()

    # Act
    dapp_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, dapp_token.address, {"from": account})

    # Assert
    assert (
        token_farm.stakingBalance(dapp_token.address, account.address) == amount_staked
    )
    assert token_farm.uniqueTokensStaked(account.address) == 1
    assert token_farm.stakers(0) == account.address

    return token_farm, dapp_token


def test_get_user_total_value(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local block chain")
    account = get_account()
    token_farm, _ = test_stake_tokens(amount_staked)

    # Act/Assert
    assert token_farm.getUserTotalValue(account.address) == INITIAL_VALUE


def test_issue_tokens(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local block chain")
    account = get_account()
    token_farm, dapp_token = test_stake_tokens(amount_staked)
    starting_balance = dapp_token.balanceOf(account.address)

    # Act
    token_farm.issueTokens({"from": account})

    # Assert
    assert dapp_token.balanceOf(
        account.address
    ) == starting_balance + token_farm.getUserTotalValue(account.address)


def test_get_user_total_value_with_different_tokens(amount_staked, random_erc20):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    account = get_account()
    token_farm, dapp_token = test_stake_tokens(amount_staked)
    # Act
    token_farm.addAllowedTokens(random_erc20.address, {"from": account})
    token_farm.setTokenPriceFeed(
        random_erc20.address, get_contract("eth_usd_price_feed"), {"from": account}
    )
    random_erc20_stake_amount = amount_staked * 2
    random_erc20.approve(
        token_farm.address, random_erc20_stake_amount, {"from": account}
    )
    token_farm.stakeTokens(
        random_erc20_stake_amount, random_erc20.address, {"from": account}
    )
    # Assert
    total_value = token_farm.getUserTotalValue(account.address)
    assert total_value == INITIAL_VALUE * 3


def test_get_token_value():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # Act / Assert
    assert token_farm.getTokenValue(dapp_token.address) == (
        INITIAL_VALUE,
        DECIMALS,
    )


def test_unstake_tokens(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    account = get_account()
    token_farm, dapp_token = test_stake_tokens(amount_staked)
    # Act
    token_farm.unstakeTokens(dapp_token.address, {"from": account})
    assert dapp_token.balanceOf(account.address) == KEPT_BALANCE
    assert token_farm.stakingBalance(dapp_token.address, account.address) == 0
    assert token_farm.uniqueTokensStaked(account.address) == 0


def test_add_allowed_tokens():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    account = get_account()
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # Act
    token_farm.addAllowedTokens(dapp_token.address, {"from": account})
    # Assert
    assert token_farm.allowedTokens(0) == dapp_token.address
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.addAllowedTokens(dapp_token.address, {"from": non_owner})


def test_token_is_allowed():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")

    token_farm, dapp_token = deploy_token_farm_and_dapp_token()

    # Assert
    assert token_farm.isAllowedToken(dapp_token.address) == True

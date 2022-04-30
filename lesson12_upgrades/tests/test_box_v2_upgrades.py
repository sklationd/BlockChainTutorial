from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import (
    config,
    network,
    Contract,
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
)
import pytest


def test_upgrade():
    # Arrange
    account = get_account()
    box = Box.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
    )
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account})

    # Act
    boxv2 = BoxV2.deploy({"from": account})

    upgrade_transaction = upgrade(
        account, proxy, boxv2.address, proxy_admin_contract=proxy_admin
    )
    upgrade_transaction.wait(1)

    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)

    # Act/Assert
    assert proxy_box.retrieve() == 1

    inc_tx = proxy_box.increment({"from": account})  # SHOULD ERROR!!!
    inc_tx.wait(1)

    assert proxy_box.retrieve() == 2

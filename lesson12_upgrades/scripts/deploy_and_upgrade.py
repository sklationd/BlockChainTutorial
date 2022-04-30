from brownie import (
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    network,
    Contract,
    config,
)
from scripts.helpful_scripts import get_account, encode_function_data, upgrade


def main():
    account = get_account()
    print(f"Deploying Box into {network.show_active()}")
    box = Box.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    # print(f"Box value is: {box.retrieve()}")

    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    # initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    print(f"Proxy deployed to {proxy}")

    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    print(f"Box(Proxy) value is: {proxy_box.retrieve()}")

    tx = proxy_box.store(100, {"from": account})
    tx.wait(1)
    # proxy_box.increment({"from": account})  # SHOULD ERROR!!!

    # Upgrade
    print(f"Deploying BoxV2 into {network.show_active()}")
    boxv2 = BoxV2.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    # print(f"BoxV2 value is: {boxv2.retrieve()}")

    upgrade_transaction = upgrade(
        account, proxy, boxv2.address, proxy_admin_contract=proxy_admin
    )
    upgrade_transaction.wait(1)

    print("Proxy has been upgraded!")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    inc_tx = proxy_box.increment({"from": account})  # SHOULD ERROR!!!
    inc_tx.wait(1)
    print(f"BoxV2(Proxy) value is: {proxy_box.retrieve()}")

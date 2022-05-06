from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from brownie import network, exceptions, AdvancedCollectible
import pytest
import time


def test_can_create_advanced_collectible_integration():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration tests")

    # Act
    if len(AdvancedCollectible) > 0:
        advanced_collectible = AdvancedCollectible[-1]
    else:
        advanced_collectible, creation_transaction = deploy_and_create()
        time.sleep(60)

    # Assert
    assert advanced_collectible.tokenCounter() > 0

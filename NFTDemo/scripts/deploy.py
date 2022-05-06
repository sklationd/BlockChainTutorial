import json
import os
import random
from pathlib import Path
import requests
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    OPENSEA_URL,
)
from dotenv import load_dotenv
from brownie import SOCollectible, config, network
from scripts.printLog import printLog
from metadata.sample_metadata import metadata_template

load_dotenv()


def main():
    (account, contract) = deploy()
    create_token(account, contract)


def deploy(redeploy=False):
    account = get_account()
    if len(SOCollectible) > 0 and not redeploy:
        printLog(f"Contract is already deployed, skip the deploying process")
        return account, SOCollectible[-1]
    else:
        # DEPLOYING
        printLog("Deploying...")
        so_collectible = SOCollectible.deploy(
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "verify", False
            ),
        )
        printLog(
            f'Deployed NFT Contract Name: {so_collectible.name({"from": account})}'
        )
        printLog(
            f'Deployed NFT Contract Symbol: {so_collectible.symbol({"from": account})}'
        )

        return account, so_collectible


def create_token(account, contract):
    printLog("Minting Token...")
    creating_tx = contract.awardItem(account.address, {"from": account})
    creating_tx.wait(1)

    # tokenId = creating_tx.return_value # INFURA doesn't support debug_traceTransaction
    tokenId = creating_tx.events["tokenMinted"]["tokenId"]
    printLog(f"Token {tokenId} is Minted")

    printLog(f"Set Token URI of token {tokenId}")
    token_uri = getTokenURI(tokenId, random.randint(0, 10**10))
    set_token_uri_tx = contract.setTokenURI(tokenId, token_uri, {"from": account})
    set_token_uri_tx.wait(1)
    printLog(f"Token URI of token {tokenId} is set to {token_uri}")
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        printLog(
            f"NFT is available at: {OPENSEA_URL.format(contract.address, tokenId)}"
        )
    return creating_tx


def getTokenURI(tokenId, props):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return f"SOME_TOKEN_URI_OF_{tokenId}_{props}"

    metadata_file_name = f"./metadata/{network.show_active()}/{tokenId}-{props}.json"
    collectible_metadata = metadata_template

    if Path(metadata_file_name).exists():
        printLog(f"{metadata_file_name} already exists! Delete it to overwrite.")
        return ""
    else:
        printLog(f"Creating metadata file {metadata_file_name}")
        tokenProps = getTokenProps(props)
        collectible_metadata["name"] = tokenProps["name"]
        collectible_metadata["description"] = tokenProps["description"]
        collectible_metadata["image"] = tokenProps["image"]
        collectible_metadata["attributes"] = tokenProps["attributes"]

        # image_path = "~"
        # image_uri = None:
        # image_uri = upload_to_ipfs(image_path)
        # image_uri = image_uri if image_uri else breed_to_image_uri[breed]
        # collectible_metadata["image"] = image_uri

        with open(metadata_file_name, "w") as file:
            json.dump(collectible_metadata, file)
        return upload_to_pinata(metadata_file_name)


def getTokenProps(props):
    return {
        "name": f"NAME-{props}",
        "description": f"DESCRIPTION-{props}",
        "image": f"https://picsum.photos/seed/{props}/300/300",
        "attributes": [
            {"trait_type": "TRAIT 0", "value": props},
            {"trait_type": "TRAIT 1", "value": props},
            {"trait_type": "TRAIT 2", "value": props},
        ],
    }


def upload_to_ipfs(file_path):
    with Path(file_path).open("rb") as fp:
        file_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": file_binary})
        ipfs_hash = response.json()["Hash"]
        file_name = file_path.split("/")[-1]
        file_uri = f"ipfs://{ipfs_hash}?filename={file_name}"
        printLog(f"Uploaded {file_path} to ipfs at {file_uri}")
        return file_uri


def upload_to_pinata(file_path):
    PINATA_BASE_URL = "https://api.pinata.cloud/"
    # pinning/pinFileToIPFS
    endpoint = "pinning/pinFileToIPFS"
    filename = file_path.split("/")[-1:][0]
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
    }

    with Path(file_path).open("rb") as fp:
        file_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, file_binary)},
            headers=headers,
        )
        ipfs_hash = response.json()["IpfsHash"]
        file_uri = f"ipfs://{ipfs_hash}?filename={filename}"
        printLog(f"Uploaded {file_path} to ipfs at {file_uri}")
        return file_uri

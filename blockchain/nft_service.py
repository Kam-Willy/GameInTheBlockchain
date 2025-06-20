import json
from pathlib import Path
import requests
from web3 import Web3
import os

PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")
INFURA_URL = os.getenv("INFURA_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

w3 = Web3(Web3.HTTPProvider(INFURA_URL))


def upload_to_ipfs(file_path):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }

    with open(file_path, 'rb') as file:
        files = {"file": (os.path.basename(file_path), file)}
        response = requests.post(url, files=files, headers=headers)

    if response.status_code == 200:
        ipfs_hash = response.json()["IpfsHash"]
        return f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
    else:
        raise Exception(f"IPFS upload failed: {response.text}")


def upload_metadata(image_url, player_name, score, length):
    metadata = {
        "name": f"Snake Run - {player_name}",
        "description": f"{player_name}'s Snake score of {score} with length {length}",
        "image": image_url,
        "attributes": [
            {"trait_type": "Score", "value": score},
            {"trait_type": "Length", "value": length}
        ]
    }

    temp_path = "temp_metadata.json"
    with open(temp_path, 'w') as f:
        json.dump(metadata, f)

    return upload_to_ipfs(temp_path)


def mint_nft(metadata_uri):
    abi_path = "blockchain/abi/SnakeNFT.json"
    
    with open(Path(abi_path)) as f:
        artifact = json.load(f)
        abi = artifact["abi"]

    contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)
    nonce = w3.eth.get_transaction_count(Web3.to_checksum_address(PUBLIC_ADDRESS))

    gas_price = w3.eth.gas_price
    adjusted_gas_price = int(gas_price * 1.1)  # add 10% bump

    txn = contract.functions.mintNFT(Web3.to_checksum_address(PUBLIC_ADDRESS), metadata_uri).build_transaction({
        "chainId": 11155111,  # Sepolia testnet
        "gas": 300000,
        "gasPrice": adjusted_gas_price,
        "nonce": nonce
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"🎉 Transaction sent! View at: https://sepolia.etherscan.io/tx/{tx_hash.hex()}\n")

    # ✅ Wait for confirmation (optional but recommended)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"✅ NFT Minted! Block: {tx_receipt.blockNumber}, Status: {tx_receipt.status}")

    return tx_hash.hex()

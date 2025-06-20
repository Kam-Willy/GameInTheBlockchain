from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_URL")))
private_key = os.getenv("PRIVATE_KEY")
public_address = Web3.to_checksum_address(os.getenv("PUBLIC_ADDRESS"))
scoreboard_address = Web3.to_checksum_address(os.getenv("SCOREBOARD_ADDRESS"))

with open("blockchain/abi/ScoreBoard.json") as f:
    artifact = json.load(f)
    abi = artifact["abi"]

contract = w3.eth.contract(address=scoreboard_address, abi=abi)

def record_score_on_chain(player_name, player_address, score):
    nonce = w3.eth.get_transaction_count(public_address)
    checksum_address = Web3.to_checksum_address(player_address)
    txn = contract.functions.recordScore(player_name, checksum_address, score).build_transaction({
        "chainId": 11155111,  # Sepolia
        "gas": 200000,
        "gasPrice": int(w3.eth.gas_price * 1.1),  # Increase gas price by 10%
        "nonce": nonce
    })

    signed = w3.eth.account.sign_transaction(txn, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"✅ Score pushed: https://sepolia.etherscan.io/tx/{tx_hash.hex()}\n")

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"✅ Score recorded! Block: {tx_receipt.blockNumber}")
    
    return tx_hash.hex()

def fetch_all_scores():
    try:
        print("🔄 Fetching scores from the blockchain...")
        raw_scores = contract.functions.getAllScores().call()

        scores = []
        for s in raw_scores:
            if len(s) >= 3:  # Make sure the tuple has expected structure
                scores.append({
                    "name": s[0],
                    "player": s[1],
                    "score": s[2]
                })
            else:
                print("⚠️ Unexpected score entry:", s)

        return scores

    except Exception as e:
        print("⚠️ Failed to fetch scores from chain:", e)
        return []

import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")
INFURA_URL = os.getenv("INFURA_URL")
os.getenv("CONTRACT_ADDRESS")

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

if w3.is_connected():
    print("✅ Connected to Blockchain\n")
    print("🔌 Using Infura:", os.getenv("INFURA_URL"))  # Should show full URL with ID
else:
    print("❌ Blockchain connection failed.")

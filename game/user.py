import uuid
from web3 import Web3


class Player:
    def __init__(self, name, wallet_address):
        self.name = name
        self.address = Web3.to_checksum_address(wallet_address)
        self.id = str(uuid.uuid4())

    def __repr__(self):
        return f"Player(name={self.name}, Id={self.id}, Address={self.address})"
